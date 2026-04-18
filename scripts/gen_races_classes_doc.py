"""Generate docs/RACES_CLASSES.md from L2JMobius CT 2.6 HighFive server data.

Joins four server sources into a single reference:

- `classList.xml`                            -> classId -> name, parentClassId
- `PlayerClass.java` (enum)                  -> race, isMage, isSummoner flags
- `templates/{StartingClass,1stClass,2ndClass,3rdClass}/*.xml`
                                             -> base stats, HP/MP/CP curves,
                                                collision, spawn points
- `initialEquipment.xml`                     -> starting inventory per root class
- `experience.xml`                           -> shared XP table (milestones only)

Inventory-slot caps are read from `PlayerConfig.java`'s compile-time constants.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_SERVER = Path(r"c:\MyProg\l2J-Mobius-CT-2.6-HighFive")
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "docs" / "RACES_CLASSES.md"

TIER_DIRS = ("StartingClass", "1stClass", "2ndClass", "3rdClass")
TIER_LABEL = {
    "StartingClass": "Starting",
    "1stClass": "1st",
    "2ndClass": "2nd",
    "3rdClass": "3rd",
}
TIER_MIN_LEVEL = {"StartingClass": 1, "1stClass": 1, "2ndClass": 20, "3rdClass": 76}

RACE_ORDER = ("HUMAN", "ELF", "DARK_ELF", "ORC", "DWARF", "KAMAEL")
RACE_LABEL = {
    "HUMAN": "Human",
    "ELF": "Elf",
    "DARK_ELF": "Dark Elf",
    "ORC": "Orc",
    "DWARF": "Dwarf",
    "KAMAEL": "Kamael",
}

MILESTONE_LEVELS = (1, 20, 40, 60, 76, 80, 85)


@dataclass
class ClassEntry:
    class_id: int
    name: str
    parent_id: int | None
    race: str = ""
    is_mage: bool = False
    is_summoner: bool = False
    enum_name: str = ""


@dataclass
class LevelRow:
    level: int
    hp: float
    mp: float
    cp: float
    hp_regen: float
    mp_regen: float
    cp_regen: float


@dataclass
class Template:
    class_id: int
    tier: str
    file_name: str
    base: dict = field(default_factory=dict)
    collision_m: tuple[float, float] = (0.0, 0.0)
    collision_f: tuple[float, float] = (0.0, 0.0)
    move: dict = field(default_factory=dict)
    spawn_count: int = 0
    levels: dict[int, LevelRow] = field(default_factory=dict)


# ---------------------------------------------------------------- parsing --


def parse_class_list(path: Path) -> dict[int, ClassEntry]:
    out: dict[int, ClassEntry] = {}
    root = ET.parse(path).getroot()
    for el in root.findall("class"):
        cid = int(el.attrib["classId"])
        parent = el.attrib.get("parentClassId")
        out[cid] = ClassEntry(
            class_id=cid,
            name=el.attrib["name"],
            parent_id=int(parent) if parent is not None else None,
        )
    return out


# Enum ctor shapes:
#   NAME(id, isMage, Race.R, PARENT)
#   NAME(id, isMage, isSummoner, Race.R, PARENT)
_ENUM_RE = re.compile(
    r"^\s*([A-Z_]+)\((\d+),\s*(true|false),"
    r"(?:\s*(true|false),)?"
    r"\s*Race\.([A-Z_]+),\s*([A-Z_]+|null)\s*\)",
    re.MULTILINE,
)


def parse_player_class_enum(path: Path) -> dict[int, tuple[str, str, bool, bool]]:
    """classId -> (enum_name, race, is_mage, is_summoner)."""
    text = path.read_text(encoding="utf-8")
    # Trim to the enum body to avoid accidental matches in methods.
    body_start = text.find("public enum PlayerClass")
    body = text[body_start:] if body_start >= 0 else text
    out: dict[int, tuple[str, str, bool, bool]] = {}
    for m in _ENUM_RE.finditer(body):
        name, cid, flag1, flag2, race, _parent = m.groups()
        is_mage = flag1 == "true"
        is_summoner = flag2 == "true"
        out[int(cid)] = (name, race, is_mage, is_summoner)
    return out


def _node_text(el: ET.Element, tag: str, default: str = "") -> str:
    child = el.find(tag)
    return child.text.strip() if child is not None and child.text else default


def parse_template(path: Path, tier: str) -> Template | None:
    root = ET.parse(path).getroot()
    cid_el = root.find("classId")
    if cid_el is None or cid_el.text is None:
        return None
    cid = int(cid_el.text)
    tpl = Template(class_id=cid, tier=tier, file_name=path.name)

    static = root.find("staticData")
    if static is not None:
        for tag in (
            "baseSTR",
            "baseDEX",
            "baseCON",
            "baseINT",
            "baseWIT",
            "baseMEN",
            "basePAtk",
            "baseMAtk",
            "basePAtkSpd",
            "baseMAtkSpd",
            "baseCritRate",
            "baseAtkRange",
            "baseAtkType",
        ):
            val = _node_text(static, tag)
            if val:
                tpl.base[tag] = val

        cp = static.find("creationPoints")
        if cp is not None:
            tpl.spawn_count = len(cp.findall("node"))

        for sex, key in (("collisionMale", "collision_m"), ("collisionFemale", "collision_f")):
            node = static.find(sex)
            if node is not None:
                r = float(_node_text(node, "radius", "0") or 0)
                h = float(_node_text(node, "height", "0") or 0)
                if key == "collision_m":
                    tpl.collision_m = (r, h)
                else:
                    tpl.collision_f = (r, h)

        mv = static.find("baseMoveSpd")
        if mv is not None:
            for tag in ("walk", "run", "slowSwim", "fastSwim"):
                v = _node_text(mv, tag)
                if v:
                    tpl.move[tag] = v

    lvl_data = root.find("lvlUpgainData")
    if lvl_data is not None:
        for lvl in lvl_data.findall("level"):
            n = int(lvl.attrib["val"])
            tpl.levels[n] = LevelRow(
                level=n,
                hp=float(_node_text(lvl, "hp", "0") or 0),
                mp=float(_node_text(lvl, "mp", "0") or 0),
                cp=float(_node_text(lvl, "cp", "0") or 0),
                hp_regen=float(_node_text(lvl, "hpRegen", "0") or 0),
                mp_regen=float(_node_text(lvl, "mpRegen", "0") or 0),
                cp_regen=float(_node_text(lvl, "cpRegen", "0") or 0),
            )
    return tpl


def load_templates(players_dir: Path) -> dict[int, Template]:
    out: dict[int, Template] = {}
    for tier in TIER_DIRS:
        tdir = players_dir / "templates" / tier
        if not tdir.is_dir():
            continue
        for path in sorted(tdir.glob("*.xml")):
            tpl = parse_template(path, tier)
            if tpl is not None:
                out[tpl.class_id] = tpl
    return out


def load_item_names(items_dir: Path) -> dict[int, str]:
    out: dict[int, str] = {}
    for xml in sorted(items_dir.glob("*.xml")):
        root = ET.parse(xml).getroot()
        for el in root.findall("item"):
            try:
                out[int(el.attrib["id"])] = el.attrib.get("name", "")
            except (KeyError, ValueError):
                continue
    return out


@dataclass
class EquipEntry:
    item_id: int
    count: int
    equipped: bool


def parse_initial_equipment(path: Path) -> dict[int, list[EquipEntry]]:
    out: dict[int, list[EquipEntry]] = {}
    root = ET.parse(path).getroot()
    for eq in root.findall("equipment"):
        cid = int(eq.attrib["classId"])
        rows: list[EquipEntry] = []
        for item in eq.findall("item"):
            rows.append(
                EquipEntry(
                    item_id=int(item.attrib["id"]),
                    count=int(item.attrib.get("count", "1")),
                    equipped=item.attrib.get("equipped", "false") == "true",
                )
            )
        out[cid] = rows
    return out


def parse_experience(path: Path) -> tuple[dict[int, int], int]:
    out: dict[int, int] = {}
    root = ET.parse(path).getroot()
    max_level = int(root.attrib.get("maxLevel", "85"))
    for el in root.findall("experience"):
        out[int(el.attrib["level"])] = int(el.attrib["tolevel"])
    return out, max_level


# ----------------------------------------------------------------- model --


def class_tier(cid: int, templates: dict[int, Template]) -> str:
    tpl = templates.get(cid)
    return tpl.tier if tpl else _fallback_tier(cid)


def _fallback_tier(cid: int) -> str:
    # 3rd classes: 88..118 and Kamael 131..136 (Doombringer, Soul Hounds, Trickster, Judicator)
    if 88 <= cid <= 118 or cid in (131, 132, 133, 134, 136):
        return "3rdClass"
    return ""


def class_type_label(entry: ClassEntry) -> str:
    if entry.is_summoner:
        return "Summoner"
    if entry.is_mage:
        # Priest/healer classes have CLERIC/ORACLE/ELDER/BISHOP/etc lineage; we
        # do not try to guess Priest vs Mage without a heuristic — keep "Mage".
        return "Mage"
    return "Fighter"


# ------------------------------------------------------------- rendering --


def fmt_float(v: float) -> str:
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:g}"


def md_escape(s: str) -> str:
    return s.replace("|", r"\|")


def render(
    classes: dict[int, ClassEntry],
    templates: dict[int, Template],
    equip: dict[int, list[EquipEntry]],
    item_names: dict[int, str],
    xp: dict[int, int],
    max_level: int,
) -> str:
    lines: list[str] = []
    out = lines.append

    # ---- Header -----------------------------------------------------------
    out("# Races and Classes (HighFive)")
    out("")
    out("## Overview")
    out("")
    out(
        "Complete enumeration of playable races, every `classId` the server knows, "
        "the profession-change tree, and the per-class base stats & growth curves "
        "that the client relies on to interpret `CharInfo` / `UserInfo` / "
        "`CharacterCreate` packets."
    )
    out("")
    out(
        "- **Scope:** live playable classes only. NPC, pet, and summon races/classes are out of scope."
    )
    out(
        "- **Regenerate with:** `python scripts/gen_races_classes_doc.py`. Output is deterministic."
    )
    out(
        "- **Related:** equip rules & paperdoll / inventory caps in [INVENTORY.md](INVENTORY.md); skill trees in [SKILLS.md](SKILLS.md); items in [ITEMS.md](ITEMS.md)."
    )
    out("")
    out("### Gotchas")
    out("")
    out(
        "- Class-change gates: tier 1 → tier 2 at **level 20**, tier 2 → tier 3 at **level 40**, tier 3 (noblesse awaken) at **level 76**. Level cap is **85**."
    )
    out("- **Kamael** have *no mage or priest classes* — all Kamael classes are fighters.")
    out(
        "- **Kamael are gender-locked** at character creation: male soldiers (123) can only become Trooper / Male Soul Breaker / Male Soul Hound / Berserker / Doombringer; females (124) → Warder / Female Soul Breaker / Female Soul Hound / Arbalester / Trickster / Inspector / Judicator. No cross-gender advancement."
    )
    out(
        "- **Dwarf inventory** starts at **100 slots**; all other races at **80**. Quest items use a separate 100-slot bucket. GM accounts have 250. All limits extendable by the `INV_LIM` stat (belts, etc.) — report via `ExStorageMaxCount` (0xFE 0x2F)."
    )
    out(
        "- Collision radius & height in `UserInfo` / `CharInfo` are gender-specific — use `collisionMale` vs `collisionFemale` from the template."
    )
    out(
        "- 1st-class templates exist for a class, but a character at level 1 uses the root (Starting) template curve until the first class change at L20."
    )
    out("")

    # ---- Races ------------------------------------------------------------
    out("## Races")
    out("")
    out("| Race | Starting classIds | Inventory slots | Notes |")
    out("|------|-------------------|----------------:|-------|")
    race_start: dict[str, list[int]] = {r: [] for r in RACE_ORDER}
    for cid, c in classes.items():
        if c.parent_id is None and c.race in race_start:
            race_start[c.race].append(cid)
    notes = {
        "HUMAN": "Both fighter and mage lines. Most versatile race.",
        "ELF": "Balanced. Higher DEX/WIT; lower CON/STR.",
        "DARK_ELF": "Highest offensive stats; lowest HP.",
        "ORC": "Fighter-oriented; highest STR/CON. Mage line exists (shaman) but spell list is limited.",
        "DWARF": "Fighter-only. **100 inventory slots**. Unique craft (Warsmith) & spoil (Bounty Hunter) lines.",
        "KAMAEL": "Introduced in CT 2.3. Fighter-only; gender-locked classes. Cannot use bows — uses crossbows/rapiers instead.",
    }
    for race in RACE_ORDER:
        ids = ", ".join(str(i) for i in sorted(race_start[race]))
        slots = "100" if race == "DWARF" else "80"
        out(f"| {RACE_LABEL[race]} | {ids} | {slots} | {notes[race]} |")
    out("")
    out(
        "Inventory-slot constants (NoDwarf=80, Dwarf=100, GM=250, Quest=100) — full detail in [INVENTORY.md § Capacity model](INVENTORY.md#capacity-model)."
    )
    out("")

    # ---- Class hierarchy --------------------------------------------------
    out("## Class hierarchy")
    out("")
    out(f"Total classes: **{len(classes)}**. One table per race, sorted by `classId`.")
    out("")
    for race in RACE_ORDER:
        members = sorted(
            [c for c in classes.values() if c.race == race],
            key=lambda c: c.class_id,
        )
        if not members:
            continue
        out(f"### {RACE_LABEL[race]} ({len(members)} classes)")
        out("")
        out("| classId | Class | Parent | Tier | Type |")
        out("|--------:|-------|--------|------|------|")
        for c in members:
            parent = "—" if c.parent_id is None else f"{c.parent_id} ({classes[c.parent_id].name})"
            tier = class_tier(c.class_id, templates)
            tier_lbl = TIER_LABEL.get(tier, "—")
            out(
                f"| {c.class_id} | {md_escape(c.name)} | {parent} | {tier_lbl} | "
                f"{class_type_label(c)} |"
            )
        out("")

    # ---- Starting-class base stats ---------------------------------------
    out("## Starting-class base stats (level 1)")
    out("")
    out(
        "The 11 root templates every character is created from. These values feed directly into the initial `UserInfo` packet."
    )
    out("")
    out(
        "| Id | Class | STR | DEX | CON | INT | WIT | MEN | "
        "HP | MP | CP | HPreg | MPreg | CPreg | "
        "pAtk | mAtk | atkSpd | walk | run | "
        "col♂ r/h | col♀ r/h | spawns |"
    )
    out(
        "|---:|-------|---:|---:|---:|---:|---:|---:|"
        "---:|---:|---:|---:|---:|---:|"
        "---:|---:|---:|---:|---:|"
        "---|---|---:|"
    )
    starting_ids = sorted(cid for cid, t in templates.items() if t.tier == "StartingClass")
    for cid in starting_ids:
        t = templates[cid]
        c = classes.get(cid)
        name = c.name if c else t.file_name
        lv1 = t.levels.get(1)
        if lv1 is None:
            continue
        cm = f"{fmt_float(t.collision_m[0])}/{fmt_float(t.collision_m[1])}"
        cf = f"{fmt_float(t.collision_f[0])}/{fmt_float(t.collision_f[1])}"
        out(
            f"| {cid} | {md_escape(name)} | "
            f"{t.base.get('baseSTR', '')} | {t.base.get('baseDEX', '')} | "
            f"{t.base.get('baseCON', '')} | {t.base.get('baseINT', '')} | "
            f"{t.base.get('baseWIT', '')} | {t.base.get('baseMEN', '')} | "
            f"{fmt_float(lv1.hp)} | {fmt_float(lv1.mp)} | {fmt_float(lv1.cp)} | "
            f"{fmt_float(lv1.hp_regen)} | {fmt_float(lv1.mp_regen)} | {fmt_float(lv1.cp_regen)} | "
            f"{t.base.get('basePAtk', '')} | {t.base.get('baseMAtk', '')} | "
            f"{t.base.get('basePAtkSpd', '')} | "
            f"{t.move.get('walk', '')} | {t.move.get('run', '')} | "
            f"{cm} | {cf} | {t.spawn_count} |"
        )
    out("")

    # ---- Growth curve snapshot -------------------------------------------
    out("## Growth curve (HP / MP / CP)")
    out("")
    out("Milestone levels only. Full per-level curves live in the template XMLs.")
    out("")
    header = (
        "| Id | Class | "
        + " | ".join(f"L{lv} HP" for lv in MILESTONE_LEVELS)
        + " | "
        + " | ".join(f"L{lv} MP" for lv in MILESTONE_LEVELS)
        + " |"
    )
    sep = "|---:|-------|" + "|".join(["---:"] * (2 * len(MILESTONE_LEVELS))) + "|"
    out(header)
    out(sep)
    for cid in starting_ids:
        t = templates[cid]
        c = classes.get(cid)
        name = c.name if c else t.file_name
        hps = " | ".join(
            fmt_float(t.levels[lv].hp) if lv in t.levels else "—" for lv in MILESTONE_LEVELS
        )
        mps = " | ".join(
            fmt_float(t.levels[lv].mp) if lv in t.levels else "—" for lv in MILESTONE_LEVELS
        )
        out(f"| {cid} | {md_escape(name)} | {hps} | {mps} |")
    out("")

    # ---- Starting equipment ----------------------------------------------
    out("## Starting equipment")
    out("")
    out(
        "One entry per root class. Items flagged `equipped=true` are placed on the paperdoll; everything else lands in the main inventory."
    )
    out("")
    out("| classId | Class | Equipped on paperdoll | In inventory |")
    out("|--------:|-------|-----------------------|--------------|")

    def _fmt_item(e: EquipEntry) -> str:
        nm = item_names.get(e.item_id, f"item_{e.item_id}")
        tail = f" ×{e.count}" if e.count != 1 else ""
        return f"{e.item_id} {nm}{tail}"

    for cid in sorted(equip):
        c = classes.get(cid)
        name = c.name if c else f"classId {cid}"
        eq = equip[cid]
        on = ", ".join(_fmt_item(e) for e in eq if e.equipped) or "—"
        off = ", ".join(_fmt_item(e) for e in eq if not e.equipped) or "—"
        out(f"| {cid} | {md_escape(name)} | {md_escape(on)} | {md_escape(off)} |")
    out("")

    # ---- Experience milestones -------------------------------------------
    out("## Experience table (milestones)")
    out("")
    out(
        "Shared across every class. The `tolevel` value is the **cumulative XP at which the player reaches that level** (exp needed to hit L2 = tolevel of L2)."
    )
    out("")
    out("| Level | Cumulative XP (tolevel) |")
    out("|------:|-------------------------|")
    for lvl in (2, 10, 20, 40, 60, 76, 80, 85):
        if lvl in xp:
            out(f"| {lvl} | {xp[lvl]:,} |")
    out("")
    out(
        f"Server-defined level cap: **{max_level}** (the XP table contains rows up to level {max(xp)} for interpolation, but the server will not grant XP beyond the cap)."
    )
    out("")

    # ---- Profession gates ------------------------------------------------
    out("## Profession-change gates")
    out("")
    out("| From tier | To tier | Required level | Notes |")
    out("|-----------|---------|---------------:|-------|")
    out("| Starting (root) | 1st | 20 | First occupation choice at Village Master. |")
    out("| 1st | 2nd | 40 | Requires second-class quest completion. |")
    out("| 2nd | 3rd | 76 | Requires noblesse awakening (3rd-class quest). |")
    out("")

    # ---- Summoners --------------------------------------------------------
    summoners = sorted(c.class_id for c in classes.values() if c.is_summoner)
    out("## Pet-capable (summoner) classes")
    out("")
    out(
        "Summoner classIds: "
        + ", ".join(f"{cid} ({classes[cid].name})" for cid in summoners)
        + "."
    )
    out("")
    out(
        "These classes maintain a servitor pet; `NpcInfo` frames for the servitor "
        "share the channel with the owner's packets and must be routed separately."
    )
    out("")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", type=Path, default=DEFAULT_SERVER)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    players_dir = args.server / "dist" / "game" / "data" / "stats" / "players"
    items_dir = args.server / "dist" / "game" / "data" / "stats" / "items"
    enum_path = (
        args.server
        / "java"
        / "org"
        / "l2jmobius"
        / "gameserver"
        / "model"
        / "actor"
        / "enums"
        / "player"
        / "PlayerClass.java"
    )

    classes = parse_class_list(players_dir / "classList.xml")
    enum_info = parse_player_class_enum(enum_path)
    for cid, c in classes.items():
        info = enum_info.get(cid)
        if info:
            c.enum_name, c.race, c.is_mage, c.is_summoner = info

    templates = load_templates(players_dir)
    equip = parse_initial_equipment(players_dir / "initialEquipment.xml")
    item_names = load_item_names(items_dir)
    xp, max_level = parse_experience(players_dir / "experience.xml")

    text = render(classes, templates, equip, item_names, xp, max_level)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(
        f"wrote {args.out} ({len(text):,} bytes, {len(classes)} classes, {len(templates)} templates)"
    )


if __name__ == "__main__":
    main()
