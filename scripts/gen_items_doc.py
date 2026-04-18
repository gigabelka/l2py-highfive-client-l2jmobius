"""Generate docs/ITEMS.md from L2JMobius CT 2.6 HighFive server item XMLs.

Scans `dist/game/data/stats/items/*.xml` and emits a single Markdown catalogue
of every **equippable** item a character can put on the paperdoll plus the two
money items (Adena, Ancient Adena). Etc items other than those two are ignored.

Grouping:
    Adena / money
    Weapons        -> per weapon_type
    Armor          -> per body slot (chest/legs/gloves/feet/head/under/cloak)
                      split by armor_type (HEAVY/LIGHT/MAGIC)
    Off-hand       -> shields and sigils (bodypart=lhand with armor_type)
    Jewelry        -> necklace, earring, ring, bracelet, talisman
    Belt / Hair    -> waist, hair, hair2

Each table is sorted by crystal grade (NONE, D, C, B, A, S, S80, S84) then id.
"""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_SERVER = Path(r"c:\MyProg\l2J-Mobius-CT-2.6-HighFive")
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "docs" / "ITEMS.md"

GRADE_ORDER = {g: i for i, g in enumerate(("NONE", "D", "C", "B", "A", "S", "S80", "S84"))}

MONEY_IDS = {57: "Adena", 5575: "Ancient Adena"}

WEAPON_GROUP_ORDER = (
    "SWORD", "BLUNT", "DAGGER", "DUALDAGGER", "DUAL", "FIST", "DUALFIST",
    "POLE", "BOW", "CROSSBOW", "RAPIER", "ANCIENTSWORD", "FISHINGROD",
    "ETC", "FLAG", "OWNTHING", "NONE",
)

ARMOR_SLOT_ORDER = (
    ("chest",     "Chest"),
    ("legs",      "Legs"),
    ("onepiece",  "Full armor (chest+legs)"),
    ("alldress",  "Formal all-dress"),
    ("gloves",    "Gloves"),
    ("feet",      "Boots"),
    ("head",      "Head"),
    ("underwear", "Underwear / shirt"),
    ("back",      "Cloak"),
)

JEWELRY_SLOT_ORDER = (
    ("neck",            "Necklace"),
    ("rear;lear",       "Earring"),
    ("rfinger;lfinger", "Ring"),
    ("lbracelet",       "Left bracelet"),
    ("rbracelet",       "Right bracelet (talisman carrier)"),
    ("deco1",           "Talisman"),
    ("waist",           "Belt"),
    ("hair",            "Hair accessory"),
    ("hair2",           "Hair accessory (slot 2)"),
    ("hairall",         "Hair accessory (covers both slots)"),
)


@dataclass
class Item:
    id: int
    name: str
    type: str
    bodypart: str = ""
    weapon_type: str = ""
    armor_type: str = ""
    crystal: str = "NONE"
    weight: int = 0
    sets: dict = field(default_factory=dict)
    stats: dict = field(default_factory=dict)

    @property
    def grade_sort(self) -> int:
        return GRADE_ORDER.get(self.crystal, 99)


def _int(s: str | None) -> int:
    if not s:
        return 0
    try:
        return int(float(s))
    except ValueError:
        return 0


def parse_item(el: ET.Element) -> Item:
    it = Item(id=int(el.attrib["id"]), name=el.attrib.get("name", ""), type=el.attrib.get("type", ""))
    for s in el.findall("set"):
        name = s.attrib.get("name", "")
        val = s.attrib.get("val", "")
        it.sets[name] = val
    for s in el.findall("./stats/set"):
        it.stats[s.attrib.get("stat", "")] = s.attrib.get("val", "")
    it.bodypart = it.sets.get("bodypart", "")
    it.weapon_type = it.sets.get("weapon_type", "")
    it.armor_type = it.sets.get("armor_type", "")
    it.crystal = it.sets.get("crystal_type", "NONE")
    it.weight = _int(it.sets.get("weight", "0"))
    return it


def load_items(items_dir: Path) -> list[Item]:
    out: list[Item] = []
    for xml in sorted(items_dir.glob("*.xml")):
        root = ET.parse(xml).getroot()
        for el in root.findall("item"):
            try:
                out.append(parse_item(el))
            except (KeyError, ValueError):
                continue
    return out


def is_placeholder(name: str) -> bool:
    low = name.lower()
    return "not in use" in low or low in ("", "-", "--")


def fmt_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def weapon_rows(items: list[Item]) -> dict[str, list[Item]]:
    buckets: dict[str, list[Item]] = defaultdict(list)
    for it in items:
        if it.type != "Weapon" or is_placeholder(it.name):
            continue
        buckets[it.weapon_type or "NONE"].append(it)
    for k in buckets:
        buckets[k].sort(key=lambda i: (i.grade_sort, i.id))
    return buckets


def armor_rows(items: list[Item]) -> dict[str, dict[str, list[Item]]]:
    """bodypart -> armor_type -> [items]"""
    buckets: dict[str, dict[str, list[Item]]] = defaultdict(lambda: defaultdict(list))
    slots = {s for s, _ in ARMOR_SLOT_ORDER}
    for it in items:
        if it.type != "Armor" or is_placeholder(it.name):
            continue
        if it.bodypart not in slots:
            continue
        at = it.armor_type or "NONE"
        buckets[it.bodypart][at].append(it)
    for slot, by_type in buckets.items():
        for at in by_type:
            by_type[at].sort(key=lambda i: (i.grade_sort, i.id))
    return buckets


def offhand_rows(items: list[Item]) -> dict[str, list[Item]]:
    """Shields and sigils: bodypart=lhand with armor_type SHIELD or SIGIL."""
    buckets: dict[str, list[Item]] = defaultdict(list)
    for it in items:
        if it.type != "Armor" or is_placeholder(it.name):
            continue
        if it.bodypart != "lhand":
            continue
        at = it.armor_type or "NONE"
        buckets[at].append(it)
    for k in buckets:
        buckets[k].sort(key=lambda i: (i.grade_sort, i.id))
    return buckets


def jewelry_rows(items: list[Item]) -> dict[str, list[Item]]:
    slots = {s for s, _ in JEWELRY_SLOT_ORDER}
    buckets: dict[str, list[Item]] = defaultdict(list)
    for it in items:
        if it.type != "Armor" or is_placeholder(it.name):
            continue
        if it.bodypart not in slots:
            continue
        buckets[it.bodypart].append(it)
    for k in buckets:
        buckets[k].sort(key=lambda i: (i.grade_sort, i.id))
    return buckets


def render_weapon_table(items: list[Item]) -> str:
    hdr = fmt_row(["Id", "Name", "Grade", "Body", "Weight", "pAtk", "mAtk", "Atk.Spd"])
    sep = fmt_row(["---:", "---", "---", "---", "---:", "---:", "---:", "---:"])
    rows = [hdr, sep]
    for it in items:
        rows.append(fmt_row([
            str(it.id),
            it.name,
            it.crystal,
            it.bodypart,
            str(it.weight),
            it.stats.get("pAtk", ""),
            it.stats.get("mAtk", ""),
            it.stats.get("pAtkSpd", ""),
        ]))
    return "\n".join(rows)


def render_armor_table(items: list[Item]) -> str:
    hdr = fmt_row(["Id", "Name", "Grade", "Weight", "pDef", "mDef"])
    sep = fmt_row(["---:", "---", "---", "---:", "---:", "---:"])
    rows = [hdr, sep]
    for it in items:
        rows.append(fmt_row([
            str(it.id),
            it.name,
            it.crystal,
            str(it.weight),
            it.stats.get("pDef", ""),
            it.stats.get("mDef", ""),
        ]))
    return "\n".join(rows)


def render_jewelry_table(items: list[Item]) -> str:
    hdr = fmt_row(["Id", "Name", "Grade", "Weight", "mDef", "Notes"])
    sep = fmt_row(["---:", "---", "---", "---:", "---:", "---"])
    rows = [hdr, sep]
    for it in items:
        extra: list[str] = []
        if "HP" in it.stats:
            extra.append(f"+HP {it.stats['HP']}")
        if "MP" in it.stats:
            extra.append(f"+MP {it.stats['MP']}")
        if "CP" in it.stats:
            extra.append(f"+CP {it.stats['CP']}")
        rows.append(fmt_row([
            str(it.id),
            it.name,
            it.crystal,
            str(it.weight),
            it.stats.get("mDef", ""),
            ", ".join(extra),
        ]))
    return "\n".join(rows)


def build_doc(items: list[Item]) -> str:
    out: list[str] = []
    w = out.append

    w("# Character Equipment & Money Catalogue (L2JMobius CT 2.6 HighFive)")
    w("")
    w("## Overview")
    w("")
    w("Every item that a character of any class can place into their personal inventory "
      "and — if applicable — wear on the paperdoll. Scope:")
    w("")
    w("- **Money:** Adena, Ancient Adena.")
    w("- **Weapons:** every `type=\"Weapon\"` template, grouped by `weapon_type`.")
    w("- **Armor:** every `type=\"Armor\"` template that equips onto a body slot "
      "(chest / legs / gloves / feet / head / underwear / cloak) and full-armor / all-dress variants.")
    w("- **Off-hand:** shields and sigils (`bodypart=lhand`).")
    w("- **Jewelry & accessories:** necklace, earring, ring, bracelet, talisman, belt, hair.")
    w("")
    w("Excluded: etc items (potions, shots, scrolls, recipes, materials, arrows/bolts, quest items), pet-only gear, and entries named `(Not In Use)`.")
    w("")
    w("- **Source of truth:** `dist/game/data/stats/items/*.xml` in the L2JMobius CT 2.6 HighFive server tree.")
    w("- **Regenerate with:** `python scripts/gen_items_doc.py`. Output is deterministic.")
    w("- **Related:** paperdoll slot layout, equip rules, on-wire item record — see [INVENTORY.md](INVENTORY.md).")
    w("")
    w("### Column meanings")
    w("")
    w("| Column | Meaning |")
    w("|--------|---------|")
    w("| **Id** | Template id — value written into the `itemId` field of every on-wire item record. |")
    w("| **Name** | Display name as shipped by the server. |")
    w("| **Grade** | Crystal grade (`NONE` / `D` / `C` / `B` / `A` / `S` / `S80` / `S84`). |")
    w("| **Body** | `bodypart` attribute — target paperdoll slot (see [INVENTORY.md](INVENTORY.md)). |")
    w("| **Weight** | Item weight; summed into `Player.currentLoad`. |")
    w("| **pAtk / mAtk / Atk.Spd** | Weapon stats from the item template. |")
    w("| **pDef / mDef** | Armor / jewelry stats from the item template. |")
    w("")

    # Money
    money_items = [it for it in items if it.id in MONEY_IDS]
    w("## Money")
    w("")
    w("| Id | Name | Template type | Notes |")
    w("|---:|------|---------------|-------|")
    for it in sorted(money_items, key=lambda i: i.id):
        note = "Universal currency; capped at `PlayerConfig.MAX_ADENA` (default 99 900 000 000)." if it.id == 57 else "Kamaloka / Seven Signs currency."
        w(f"| {it.id} | {it.name} | `{it.type}` | {note} |")
    w("")

    # Weapons
    buckets = weapon_rows(items)
    total_weapons = sum(len(v) for v in buckets.values())
    w(f"## Weapons ({total_weapons})")
    w("")
    w("Grouped by `weapon_type`. Two-handed weapon types (`bodypart=lrhand`) occupy the RHAND slot and implicitly clear LHAND.")
    w("")
    for wt in WEAPON_GROUP_ORDER:
        lst = buckets.get(wt)
        if not lst:
            continue
        w(f"### {wt} ({len(lst)})")
        w("")
        w(render_weapon_table(lst))
        w("")
    # any leftover weapon types
    for wt, lst in sorted(buckets.items()):
        if wt in WEAPON_GROUP_ORDER:
            continue
        w(f"### {wt} ({len(lst)})")
        w("")
        w(render_weapon_table(lst))
        w("")

    # Armor (body slots)
    armor_buckets = armor_rows(items)
    total_armor = sum(sum(len(v) for v in by_type.values()) for by_type in armor_buckets.values())
    w(f"## Armor ({total_armor})")
    w("")
    w("Grouped by body slot and split by `armor_type`. Kamael cannot equip `HEAVY` or `MAGIC`; non-Kamael cannot equip Kamael-exclusive templates — this is enforced server-side in `UseItem`.")
    w("")
    for slot_key, slot_label in ARMOR_SLOT_ORDER:
        by_type = armor_buckets.get(slot_key)
        if not by_type:
            continue
        total = sum(len(v) for v in by_type.values())
        w(f"### {slot_label} — `bodypart={slot_key}` ({total})")
        w("")
        for at in ("HEAVY", "LIGHT", "MAGIC", "NONE"):
            lst = by_type.get(at)
            if not lst:
                continue
            w(f"#### {at} ({len(lst)})")
            w("")
            w(render_armor_table(lst))
            w("")
        # any leftover types
        for at, lst in sorted(by_type.items()):
            if at in ("HEAVY", "LIGHT", "MAGIC", "NONE"):
                continue
            w(f"#### {at} ({len(lst)})")
            w("")
            w(render_armor_table(lst))
            w("")

    # Off-hand
    oh = offhand_rows(items)
    total_off = sum(len(v) for v in oh.values())
    w(f"## Off-hand — `bodypart=lhand` ({total_off})")
    w("")
    w("Shields (`SHIELD`) block physical damage; sigils (`SIGIL`) are magic off-hands for casters. Cannot coexist with a two-handed weapon.")
    w("")
    for at in ("SHIELD", "SIGIL", "NONE"):
        lst = oh.get(at)
        if not lst:
            continue
        w(f"### {at} ({len(lst)})")
        w("")
        w(render_armor_table(lst))
        w("")
    for at, lst in sorted(oh.items()):
        if at in ("SHIELD", "SIGIL", "NONE"):
            continue
        w(f"### {at} ({len(lst)})")
        w("")
        w(render_armor_table(lst))
        w("")

    # Jewelry
    jew = jewelry_rows(items)
    total_jew = sum(len(v) for v in jew.values())
    w(f"## Jewelry & accessories ({total_jew})")
    w("")
    for slot_key, slot_label in JEWELRY_SLOT_ORDER:
        lst = jew.get(slot_key)
        if not lst:
            continue
        w(f"### {slot_label} — `bodypart={slot_key}` ({len(lst)})")
        w("")
        w(render_jewelry_table(lst))
        w("")

    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", type=Path, default=DEFAULT_SERVER)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    items_dir = args.server / "dist" / "game" / "data" / "stats" / "items"
    if not items_dir.is_dir():
        ap.error(f"items dir not found: {items_dir}")

    items = load_items(items_dir)
    doc = build_doc(items)
    args.out.write_text(doc, encoding="utf-8", newline="\n")
    print(f"Wrote {args.out} ({len(doc):,} bytes, {len(items):,} items scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
