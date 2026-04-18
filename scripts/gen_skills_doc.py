"""Generate docs/SKILLS.md from L2JMobius CT 2.6 HighFive server skill-tree XMLs.

Reads 1st/2nd/3rd-class skill trees and emits a single Markdown reference
listing every class with a compact table of the class skills it can learn.
"""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

DEFAULT_SERVER = Path(r"c:\MyProg\l2J-Mobius-CT-2.6-HighFive")
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "docs" / "SKILLS.md"
TIERS = ("1stClass", "2ndClass", "3rdClass")
TIER_LABELS = {"1stClass": "1st Class", "2ndClass": "2nd Class", "3rdClass": "3rd Class"}


@dataclass
class SkillRow:
    skill_id: int
    name: str
    max_level: int
    first_get_level: int
    total_sp: int


@dataclass
class ClassTree:
    tier: str
    file_name: str
    class_id: int
    parent_class_id: int
    skills: list[SkillRow]


def parse_tree(path: Path, tier: str) -> ClassTree | None:
    root = ET.parse(path).getroot()
    tree_el = root.find("skillTree")
    if tree_el is None:
        return None
    class_id = int(tree_el.attrib.get("classId", "-1"))
    parent_class_id = int(tree_el.attrib.get("parentClassId", "-1"))

    grouped: dict[int, list[ET.Element]] = defaultdict(list)
    for el in tree_el.findall("skill"):
        sid = int(el.attrib["skillId"])
        grouped[sid].append(el)

    rows: list[SkillRow] = []
    for sid, items in grouped.items():
        name = items[0].attrib.get("skillName", f"skill_{sid}")
        max_level = max(int(e.attrib["skillLevel"]) for e in items)
        first_get_level = min(int(e.attrib["getLevel"]) for e in items)
        total_sp = sum(int(e.attrib.get("levelUpSp", "0")) for e in items)
        rows.append(SkillRow(sid, name, max_level, first_get_level, total_sp))

    rows.sort(key=lambda r: (r.first_get_level, r.skill_id))
    return ClassTree(
        tier=tier,
        file_name=path.stem,
        class_id=class_id,
        parent_class_id=parent_class_id,
        skills=rows,
    )


def load_all(server_root: Path) -> list[ClassTree]:
    base = server_root / "dist" / "game" / "data" / "stats" / "players" / "skillTrees"
    out: list[ClassTree] = []
    for tier in TIERS:
        tier_dir = base / tier
        for xml_path in sorted(tier_dir.glob("*.xml")):
            parsed = parse_tree(xml_path, tier)
            if parsed is not None:
                out.append(parsed)
    return out


def anchor(name: str) -> str:
    return name.lower().replace(" ", "-").replace("'", "").replace("/", "")


def format_sp(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def render(trees: list[ClassTree]) -> str:
    by_id: dict[int, ClassTree] = {t.class_id: t for t in trees}

    def parent_name(parent_id: int) -> str:
        if parent_id < 0:
            return "—"
        parent = by_id.get(parent_id)
        return parent.file_name if parent else f"classId {parent_id}"

    lines: list[str] = []
    lines.append("# Character Skills (L2JMobius CT 2.6 HighFive)")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(
        "This file enumerates every class skill that a playable character can "
        "learn on a vanilla L2JMobius CT 2.6 HighFive server."
    )
    lines.append("")
    lines.append("- **Scope:** 1st/2nd/3rd class skill trees only. Fishing, collect, "
                 "transfer, transform, sub-class, sub-pledge, noble, hero, GM, and "
                 "clan trees are intentionally excluded.")
    lines.append("- **Source of truth:** "
                 "`dist/game/data/stats/players/skillTrees/{1stClass,2ndClass,3rdClass}/*.xml` "
                 "in the L2JMobius CT 2.6 HighFive server tree.")
    lines.append("- **Regenerate with:** `python scripts/gen_skills_doc.py`. The "
                 "output is deterministic — rerunning on unchanged server data "
                 "produces a byte-identical file.")
    lines.append("")
    lines.append("### Column meanings")
    lines.append("")
    lines.append("| Column | Meaning |")
    lines.append("|--------|---------|")
    lines.append("| **Id** | `skillId` — stable numeric identifier used on the wire "
                 "(e.g. in `MagicSkillUse`, `AcquireSkill`). |")
    lines.append("| **Skill** | `skillName` as shipped by the server. |")
    lines.append("| **Max Lvl** | Highest `skillLevel` this class can reach for that "
                 "skill in its own tree. |")
    lines.append("| **Learned At** | Lowest character `getLevel` at which any "
                 "sub-level of this skill becomes available. |")
    lines.append("| **SP Total** | Sum of `levelUpSp` across every `<skill>` row in "
                 "this class's tree for that `skillId` (cumulative SP to "
                 "reach Max Lvl from the bottom). |")
    lines.append("")
    lines.append("### Notes")
    lines.append("")
    lines.append("- Per-sub-level rows in the XML are coalesced: one table row per "
                 "`skillId`. Expand the raw XML if you need the per-sub-level SP "
                 "breakdown.")
    lines.append("- Classes inherit skills from their parents in L2 canon, but "
                 "each class's XML already contains only the skills that class "
                 "itself grants — parent skills are *not* duplicated here.")
    lines.append("- Per-level skill mechanics (damage, effects, cooldowns, MP "
                 "cost, target type) are **not** covered in this spec. See "
                 "`dist/game/data/stats/skills/*.xml` on the server for those.")
    lines.append("")

    lines.append("## Class index")
    lines.append("")
    lines.append("| Tier | Class Id | Class | Parent | # Skills |")
    lines.append("|------|---------:|-------|--------|---------:|")
    for t in trees:
        label = TIER_LABELS[t.tier]
        link = f"[{t.file_name}](#{anchor(t.file_name)})"
        lines.append(
            f"| {label} | {t.class_id} | {link} | {parent_name(t.parent_class_id)} "
            f"| {len(t.skills)} |"
        )
    lines.append("")

    for tier in TIERS:
        lines.append(f"## {TIER_LABELS[tier]} Skills")
        lines.append("")
        tier_trees = [t for t in trees if t.tier == tier]
        for t in tier_trees:
            lines.append(
                f"### {t.file_name}  (classId {t.class_id}, parent "
                f"{parent_name(t.parent_class_id)})"
            )
            lines.append("")
            if not t.skills:
                lines.append("_No skills defined in the class tree._")
                lines.append("")
                continue
            lines.append("| Id | Skill | Max Lvl | Learned At | SP Total |")
            lines.append("|---:|-------|--------:|-----------:|---------:|")
            for s in t.skills:
                lines.append(
                    f"| {s.skill_id} | {s.name} | {s.max_level} "
                    f"| {s.first_get_level} | {format_sp(s.total_sp)} |"
                )
            lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", type=Path, default=DEFAULT_SERVER,
                        help="Path to L2J-Mobius-CT-2.6-HighFive checkout root.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="Path to the output Markdown file.")
    args = parser.parse_args()

    trees = load_all(args.server)
    if not trees:
        raise SystemExit(f"No class skill trees found under {args.server!s}")

    text = render(trees)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {len(trees)} class sections to {args.out}")


if __name__ == "__main__":
    main()
