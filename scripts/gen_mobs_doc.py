"""Generate docs/MOBS.md from L2JMobius CT 2.6 HighFive server NPC XMLs.

Scans `dist/game/data/stats/npcs/*.xml` and emits a single Markdown catalogue
of every **combat-relevant** NPC the client can target: regular monsters,
raid/grand bosses, chests, festival/rift invaders, beasts, and siege-style
combat NPCs (guards, defenders, fort commanders, quest guards, decoys,
friendly mobs).

Excluded: merchants, teleporters, trainers, warehouse keepers, doormen,
village masters, clan hall / fort managers, pets / summons, effect points,
static towers, territory wards — none of those ever appear as an attack
target on the wire.

Per-mob drop/spoil detail tables are emitted **only for RaidBoss and
GrandBoss**. Regular monsters get a count column; callers who need a
specific monster's drop chances should read the source XML directly.
"""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_SERVER = Path(r"c:\MyProg\l2J-Mobius-CT-2.6-HighFive")
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "docs" / "MOBS.md"

# Ordered list of types that end up in the doc, with display labels.
# Everything else (Folk/Merchant/Pet/Trainer/VillageMaster…) is skipped.
TYPE_ORDER: tuple[tuple[str, str], ...] = (
    ("GrandBoss",       "Grand Bosses"),
    ("RaidBoss",        "Raid Bosses"),
    ("Monster",         "Monsters"),
    ("L2Monster",       "Monsters (legacy `L2Monster` tag)"),
    ("FestivalMonster", "Festival monsters"),
    ("RiftInvader",     "Rift invaders"),
    ("FeedableBeast",   "Feedable beasts"),
    ("TamedBeast",      "Tamed beasts"),
    ("Chest",           "Chests"),
    ("Guard",           "Guards"),
    ("Defender",        "Defenders"),
    ("FortCommander",   "Fort commanders"),
    ("QuestGuard",      "Quest guards"),
    ("FriendlyMob",     "Friendly mobs"),
    ("Decoy",           "Decoys"),
)
TYPE_INDEX = {t: i for i, (t, _) in enumerate(TYPE_ORDER)}
INCLUDED_TYPES = set(TYPE_INDEX)

BOSS_TYPES = {"RaidBoss", "GrandBoss"}


@dataclass
class DropItem:
    item_id: int
    min_q: int
    max_q: int
    chance: float            # 0..100 from XML
    group_chance: float = 100.0   # 0..100; only meaningful for drops


@dataclass
class Mob:
    id: int
    name: str
    title: str
    type: str
    level: int
    race: str = ""
    hp: int = 0
    p_atk: int = 0
    m_atk: int = 0
    p_def: int = 0
    m_def: int = 0
    atk_range: int = 0
    atk_type: str = ""
    exp: int = 0
    sp: int = 0
    aggro: int = -1          # -1 means "no <ai aggroRange>" (non-aggressive)
    skills: list[tuple[int, int]] = field(default_factory=list)
    drops: list[DropItem] = field(default_factory=list)
    spoil: list[DropItem] = field(default_factory=list)


def _num(s: str | None, default: float = 0) -> float:
    if not s:
        return default
    try:
        return float(s)
    except ValueError:
        return default


def _i(s: str | None, default: int = 0) -> int:
    return int(_num(s, default))


def parse_mob(el: ET.Element) -> Mob | None:
    try:
        mob_id = int(el.attrib["id"])
    except (KeyError, ValueError):
        return None
    mtype = el.attrib.get("type", "")
    if mtype not in INCLUDED_TYPES:
        return None

    m = Mob(
        id=mob_id,
        name=el.attrib.get("name", ""),
        title=el.attrib.get("title", ""),
        type=mtype,
        level=_i(el.attrib.get("level", "0")),
    )

    race_el = el.find("race")
    if race_el is not None and race_el.text:
        m.race = race_el.text.strip()

    acq = el.find("acquire")
    if acq is not None:
        m.exp = _i(acq.attrib.get("exp", "0"))
        m.sp = _i(acq.attrib.get("sp", "0"))

    vit = el.find("./stats/vitals")
    if vit is not None:
        m.hp = _i(vit.attrib.get("hp", "0"))

    atk = el.find("./stats/attack")
    if atk is not None:
        m.p_atk = _i(atk.attrib.get("physical", "0"))
        m.m_atk = _i(atk.attrib.get("magical", "0"))
        m.atk_range = _i(atk.attrib.get("range", "0"))
        m.atk_type = atk.attrib.get("type", "")

    de = el.find("./stats/defence")
    if de is not None:
        m.p_def = _i(de.attrib.get("physical", "0"))
        m.m_def = _i(de.attrib.get("magical", "0"))

    ai = el.find("ai")
    if ai is not None and "aggroRange" in ai.attrib:
        m.aggro = _i(ai.attrib["aggroRange"], -1)

    sl = el.find("skillList")
    if sl is not None:
        for s in sl.findall("skill"):
            try:
                m.skills.append((int(s.attrib["id"]), int(s.attrib.get("level", "1"))))
            except (KeyError, ValueError):
                continue

    dl = el.find("dropLists")
    if dl is not None:
        drop = dl.find("drop")
        if drop is not None:
            for g in drop.findall("group"):
                gc = _num(g.attrib.get("chance", "100"), 100)
                for it in g.findall("item"):
                    try:
                        m.drops.append(DropItem(
                            item_id=int(it.attrib["id"]),
                            min_q=_i(it.attrib.get("min", "1"), 1),
                            max_q=_i(it.attrib.get("max", "1"), 1),
                            chance=_num(it.attrib.get("chance", "100"), 100),
                            group_chance=gc,
                        ))
                    except (KeyError, ValueError):
                        continue
            # bare <item> directly under <drop> (rare but valid)
            for it in drop.findall("item"):
                try:
                    m.drops.append(DropItem(
                        item_id=int(it.attrib["id"]),
                        min_q=_i(it.attrib.get("min", "1"), 1),
                        max_q=_i(it.attrib.get("max", "1"), 1),
                        chance=_num(it.attrib.get("chance", "100"), 100),
                    ))
                except (KeyError, ValueError):
                    continue
        sp_el = dl.find("spoil")
        if sp_el is not None:
            for it in sp_el.findall("item"):
                try:
                    m.spoil.append(DropItem(
                        item_id=int(it.attrib["id"]),
                        min_q=_i(it.attrib.get("min", "1"), 1),
                        max_q=_i(it.attrib.get("max", "1"), 1),
                        chance=_num(it.attrib.get("chance", "100"), 100),
                    ))
                except (KeyError, ValueError):
                    continue

    return m


def load_mobs(npcs_dir: Path) -> list[Mob]:
    out: list[Mob] = []
    for xml in sorted(npcs_dir.glob("*.xml")):
        try:
            root = ET.parse(xml).getroot()
        except ET.ParseError:
            continue
        for el in root.findall("npc"):
            m = parse_mob(el)
            if m is not None:
                out.append(m)
    out.sort(key=lambda m: (TYPE_INDEX.get(m.type, 99), m.level, m.id))
    return out


def load_item_names(items_dir: Path) -> dict[int, str]:
    names: dict[int, str] = {}
    for xml in sorted(items_dir.glob("*.xml")):
        try:
            root = ET.parse(xml).getroot()
        except ET.ParseError:
            continue
        for el in root.findall("item"):
            try:
                iid = int(el.attrib["id"])
            except (KeyError, ValueError):
                continue
            names[iid] = el.attrib.get("name", "")
    return names


def fmt_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def render_mob_table(mobs: list[Mob]) -> str:
    hdr = fmt_row([
        "Id", "Name", "Lv", "Race", "HP", "pAtk", "mAtk", "pDef", "mDef",
        "Rng", "Exp", "SP", "Aggro", "Skills", "Drops",
    ])
    sep = fmt_row([
        "---:", "---", "---:", "---", "---:", "---:", "---:", "---:", "---:",
        "---:", "---:", "---:", "---:", "---:", "---:",
    ])
    rows = [hdr, sep]
    for m in mobs:
        aggro = str(m.aggro) if m.aggro >= 0 else ""
        drops_cell = str(len(m.drops))
        if m.spoil:
            drops_cell = f"{len(m.drops)} +{len(m.spoil)}s"
        rows.append(fmt_row([
            str(m.id),
            m.name or "(no name)",
            str(m.level),
            m.race,
            str(m.hp),
            str(m.p_atk),
            str(m.m_atk),
            str(m.p_def),
            str(m.m_def),
            str(m.atk_range),
            str(m.exp),
            str(m.sp),
            aggro,
            str(len(m.skills)),
            drops_cell,
        ]))
    return "\n".join(rows)


def render_boss_drop_table(drops: list[DropItem], item_names: dict[int, str], kind: str) -> str:
    hdr_cells = ["Id", "Name", "Min", "Max", "Chance %"]
    sep_cells = ["---:", "---", "---:", "---:", "---:"]
    if kind == "drop":
        hdr_cells.insert(4, "Group %")
        sep_cells.insert(4, "---:")
    rows = [fmt_row(hdr_cells), fmt_row(sep_cells)]
    for d in drops:
        cells = [
            str(d.item_id),
            item_names.get(d.item_id, ""),
            str(d.min_q),
            str(d.max_q),
            f"{d.chance:g}",
        ]
        if kind == "drop":
            cells.insert(4, f"{d.group_chance:g}")
        rows.append(fmt_row(cells))
    return "\n".join(rows)


def build_doc(mobs: list[Mob], item_names: dict[int, str]) -> str:
    out: list[str] = []
    w = out.append

    w("# Monster & Combat NPC Catalogue (HighFive)")
    w("")
    w("## Overview")
    w("")
    w("Every combat-relevant NPC the client can target, drawn from the L2JMobius "
      "server's `dist/game/data/stats/npcs/*.xml`. Scope:")
    w("")
    w("- **Monsters** — regular mobs (`type=\"Monster\"` / `L2Monster`).")
    w("- **Bosses** — `RaidBoss`, `GrandBoss`.")
    w("- **Specials** — festival monsters, rift invaders, feedable / tamed beasts, chests.")
    w("- **Combat NPCs** — guards, defenders, fort commanders, quest guards, decoys, friendly mobs.")
    w("")
    w("Excluded: merchants, teleporters, trainers, warehouse keepers, doormen, "
      "village masters, clan hall / fort managers, pets, summons, effect points, "
      "static towers, territory wards. None of those ever appear as an attack target.")
    w("")
    w("- **Regenerate with:** `python scripts/gen_mobs_doc.py`. Output is deterministic.")
    w("- **Related:** packet-level combat flow — see [PROTOCOL.md](PROTOCOL.md). "
      "Skills referenced by `Skills` column — see [SKILLS.md](SKILLS.md). "
      "Item ids in drop/spoil tables — see [ITEMS.md](ITEMS.md).")
    w("")
    w("### Column meanings")
    w("")
    w("| Column | Meaning |")
    w("|--------|---------|")
    w("| **Id** | `npcId` on the wire (`NpcInfo 0x16`, `AttackableDeath`, etc.). |")
    w("| **Name** | Display name as shipped in the XML. Entries with `usingServerSideName=true` pull their name from the client's own `.dat` and may be empty here. |")
    w("| **Lv** | Level (unsigned). |")
    w("| **Race** | From `Race.java` enum (HUMAN, UNDEAD, DEMONIC, DRAGON, BEAST, …). |")
    w("| **HP** | Max HP at full health (integer-truncated from the decimal in XML). |")
    w("| **pAtk / mAtk** | Physical / magical attack from `<stats><attack>`. |")
    w("| **pDef / mDef** | Physical / magical defence from `<stats><defence>`. |")
    w("| **Rng** | Physical attack range (melee ≈ 40, bow ≈ 500+). |")
    w("| **Exp / SP** | Awarded to the killing party on death. |")
    w("| **Aggro** | `<ai aggroRange>` — radius at which the mob pulls unprovoked. Blank = non-aggressive. |")
    w("| **Skills** | Count of `<skillList><skill>` entries (includes passives & racial skills). |")
    w("| **Drops** | Count of `<drop>` item entries; `+Ns` suffix = N spoil items. |")
    w("")

    # group by type
    by_type: dict[str, list[Mob]] = defaultdict(list)
    for m in mobs:
        by_type[m.type].append(m)

    # Summary table
    w("## Summary counts")
    w("")
    w("| Type | Count |")
    w("|------|---:|")
    total = 0
    for tkey, label in TYPE_ORDER:
        c = len(by_type.get(tkey, ()))
        if c == 0:
            continue
        total += c
        w(f"| `{tkey}` — {label} | {c} |")
    w(f"| **Total** | **{total}** |")
    w("")

    # Per-type tables
    for tkey, label in TYPE_ORDER:
        lst = by_type.get(tkey)
        if not lst:
            continue
        w(f"## {label} ({len(lst)})")
        w("")
        w(render_mob_table(lst))
        w("")

    # Boss drop detail appendix
    w("## Boss drop detail")
    w("")
    w("Per-mob drop + spoil listings for RaidBoss and GrandBoss only. "
      "`Group %` is the drop-group roll chance — the per-item `Chance %` is "
      "conditional on the group rolling. For regular monsters, read the source XML "
      "(`dist/game/data/stats/npcs/*.xml`) — inlining ~8 000 sub-tables would make "
      "this document several megabytes.")
    w("")
    for tkey in ("GrandBoss", "RaidBoss"):
        lst = by_type.get(tkey, [])
        if not lst:
            continue
        w(f"### {tkey} ({len(lst)})")
        w("")
        for m in lst:
            if not m.drops and not m.spoil:
                continue
            title = f"#### {m.id} — {m.name or '(no name)'} (Lv {m.level})"
            w(title)
            w("")
            if m.drops:
                w("**Drop:**")
                w("")
                w(render_boss_drop_table(m.drops, item_names, "drop"))
                w("")
            if m.spoil:
                w("**Spoil:**")
                w("")
                w(render_boss_drop_table(m.spoil, item_names, "spoil"))
                w("")

    # Notes
    w("## Notes & gotchas")
    w("")
    w("- `id` vs `displayId` — some NPCs render with the appearance of a different id "
      "(`displayId` attribute on `<npc>`). The wire `NpcInfo` packet carries the "
      "**template id** (`id`); the client then looks up appearance data for `displayId`. "
      "This doc lists `id`.")
    w("- `usingServerSideName=\"true\"` → the server tells the client to pull the name "
      "from its own `.dat` files rather than the XML `name` attribute. Those rows may "
      "appear blank in the Name column.")
    w("- Non-aggressive mobs have no `<ai aggroRange>` (blank in `Aggro` column); they "
      "still retaliate when hit.")
    w("- Drop `Chance %` is already a percentage (0–100), not a 0–1 fraction or the "
      "raw 0–1 000 000 server integer. The XML file ships percentages directly.")
    w("- Receiving an unknown `npcId` in `NpcInfo` must never desync the game XOR "
      "stream: log and drop the packet, but still advance the key rotation in "
      "[game_crypt.py](../src/l2py/crypto/game_crypt.py) — the same rule as for "
      "unknown opcodes.")
    w("")

    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", type=Path, default=DEFAULT_SERVER)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    npcs_dir = args.server / "dist" / "game" / "data" / "stats" / "npcs"
    items_dir = args.server / "dist" / "game" / "data" / "stats" / "items"
    if not npcs_dir.is_dir():
        ap.error(f"npcs dir not found: {npcs_dir}")
    if not items_dir.is_dir():
        ap.error(f"items dir not found: {items_dir}")

    mobs = load_mobs(npcs_dir)
    item_names = load_item_names(items_dir)
    doc = build_doc(mobs, item_names)
    args.out.write_text(doc, encoding="utf-8", newline="\n")
    print(f"Wrote {args.out} ({len(doc):,} bytes, {len(mobs):,} mobs scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
