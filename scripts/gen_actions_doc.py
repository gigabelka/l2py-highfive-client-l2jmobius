"""Generate docs/ACTIONS.md from L2JMobius CT 2.6 HighFive server sources.

In-game *actions* are the things a user does at the keyboard/mouse:
target, attack, pick up, use skill, use item, drop, sit/stand, run/walk,
socials, pet commands, airship controls, private stores, and anything
triggered by F1-F12 action-bar slots.

Unlike items/skills/npcs, L2JMobius has no ActionData.xml — the action
catalogue lives in Java. This script therefore parses:

  - `java/.../network/clientpackets/RequestActionUse.java`
        for the full `switch (_actionId)` -> `case N: // <comment>` table.
  - `java/.../network/serverpackets/ExBasicActionList.java`
        for the `ACTIONS_ON_TRANSFORM` and `DEFAULT_ACTION_LIST` arrays.
  - `java/.../network/ClientPackets.java`
        to confirm the opcode -> handler mapping used in the packet map.

The rest of the document (packet hex layouts, targeting dispatch, shortcut
system, F-key resolution) is hand-emitted text below — it is not machine
extractable with any reasonable effort.

Output is deterministic: running twice yields byte-identical markdown.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

DEFAULT_SERVER = Path(r"c:\MyProg\l2J-Mobius-CT-2.6-HighFive")
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "docs" / "ACTIONS.md"


# ---------------------------------------------------------------------------
# Java-source parsing
# ---------------------------------------------------------------------------

CASE_RE = re.compile(r"^\s*case\s+(\d+):\s*//\s*(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class ActionEntry:
    id: int
    comment: str


def parse_action_cases(java_text: str) -> list[ActionEntry]:
    seen: dict[int, str] = {}
    for m in CASE_RE.finditer(java_text):
        aid = int(m.group(1))
        cmt = m.group(2).strip()
        seen.setdefault(aid, cmt)
    return [ActionEntry(i, c) for i, c in sorted(seen.items())]


ARRAY_RE = re.compile(
    r"public\s+static\s+final\s+int\[\]\s+ACTIONS_ON_TRANSFORM\s*=\s*\{([^}]*)\}", re.S
)


def parse_actions_on_transform(java_text: str) -> list[int]:
    m = ARRAY_RE.search(java_text)
    if not m:
        raise RuntimeError("ACTIONS_ON_TRANSFORM array not found")
    nums = re.findall(r"\d+", m.group(1))
    return sorted({int(n) for n in nums})


CLIENT_PACKETS_RE = re.compile(
    r"^\s*([A-Z0-9_]+)\s*\(\s*0x([0-9A-Fa-f]+)\s*,\s*([A-Za-z0-9_]+)?(?:::new)?",
    re.MULTILINE,
)


def parse_client_packets(java_text: str) -> dict[int, tuple[str, str]]:
    """Return {opcode: (enum_name, handler_class_or_empty)}."""
    out: dict[int, tuple[str, str]] = {}
    for m in CLIENT_PACKETS_RE.finditer(java_text):
        name, hex_, handler = m.group(1), m.group(2), m.group(3) or ""
        if name in ("PACKET_ARRAY",):
            continue
        out[int(hex_, 16)] = (name, handler)
    return out


# ---------------------------------------------------------------------------
# Static tables — hand-curated from reading the handlers
# ---------------------------------------------------------------------------

# Opcodes this document describes. Every one is cross-checked against
# ClientPackets.java at runtime.
PACKET_MAP: list[tuple[int, str, str]] = [
    # (opcode, short description, section anchor)
    (0x01, "Attack (legacy alias; identical body to 0x32)", "#3-attack--attackrequest-0x32"),
    (0x0F, "MoveToLocation — click-to-move", "#movetolocation-0x0f-click-to-move"),
    (0x17, "RequestDropItem — drop items to the ground", "#6-drop-item--requestdropitem-0x17"),
    (0x19, "UseItem — consume / equip / toggle an inventory item", "#5-item-use--useitem-0x19"),
    (0x1F, "Action — click on any world object", "#1-targeting--action-0x1f"),
    (0x22, "RequestLinkHtml — HTML link bypass", "#requestlinkhtml-0x22"),
    (
        0x23,
        "RequestBypassToServer — NPC/admin/community command",
        "#7-bypass--requestbypasstoserver-0x23",
    ),
    (0x32, "AttackRequest — forced auto-attack toggle", "#3-attack--attackrequest-0x32"),
    (0x39, "RequestMagicSkillUse — cast a skill by id", "#4-skill-use--requestmagicskilluse-0x39"),
    (0x3D, "RequestShortcutReg — register action-bar slot", "#10-shortcuts"),
    (0x3F, "RequestShortcutDel — delete action-bar slot", "#10-shortcuts"),
    (
        0x48,
        "RequestTargetCancel — cancel target or abort cast",
        "#2-cancel-target--cancel-cast--requesttargetcancel-0x48",
    ),
    (0x56, "RequestActionUse — grand-unified action dispatcher", "#9-requestactionuse-0x56"),
]


SOCIAL_ACTIONS: list[tuple[int, int, str]] = [
    # (action_id passed to RequestActionUse, social_id broadcast in SocialAction)
    (12, 2, "Greeting"),
    (13, 3, "Victory"),
    (14, 4, "Advance"),
    (24, 6, "Yes"),
    (25, 5, "No"),
    (26, 7, "Bow"),
    (29, 8, "Unaware"),
    (30, 9, "Social Waiting"),
    (31, 10, "Laugh"),
    (33, 11, "Applaud"),
    (34, 12, "Dance"),
    (35, 13, "Sorrow"),
    (62, 14, "Charm"),
    (66, 15, "Shyness"),
]


# Default F1-F12 defaults are encoded into the client `.dat` files, not the
# server. The server only observes whichever shortcut each slot resolves to.
# These are the well-known Chronicle 1+ defaults shipped with the NCsoft
# HighFive client; they are mentioned here only as a reference.
DEFAULT_FKEYS: list[tuple[str, str]] = [
    ("F1", "Help — open the in-game help window (client-local, no packet)"),
    ("F2", "Attack — action id 16 (Pet Attack) or generic attack on current target"),
    ("F3", "Target Next Enemy — client-local target cycling, then sends Action 0x1F"),
    ("F4", "Target Self — client-local, then sends Action 0x1F on own objectId"),
    ("F5", "Pick Up — client sends Action 0x1F on nearest drop"),
    ("F6", "Sit / Stand — RequestActionUse 0x56 action id 0"),
    ("F7", "Walk / Run — RequestActionUse 0x56 action id 1"),
    ("F8", "Assist — target the target of current target (client-local, then Action)"),
    ("F9", "Party Info — client-local UI toggle"),
    ("F10", "Main Menu — client-local UI toggle"),
    ("F11", "Inventory — client-local UI toggle"),
    ("F12", "Communication — client-local UI toggle"),
]


# ---------------------------------------------------------------------------
# Markdown emission
# ---------------------------------------------------------------------------


def fmt_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def build_doc(
    actions: list[ActionEntry],
    transform_allowed: list[int],
    client_packets: dict[int, tuple[str, str]],
) -> str:
    out: list[str] = []
    w = out.append

    w("# In-game Actions (HighFive / L2JMobius CT 2.6)")
    w("")
    w("## Overview")
    w("")
    w(
        "Every client→server packet that corresponds to a user-initiated gameplay *action*: targeting, attack, skill, item, drop, sit/stand, run/walk, pet & servitor controls, airship steering, private stores, socials, shortcut registration, HTML/NPC bypasses, and the unified `RequestActionUse (0x56)` dispatcher that handles F-key shortcuts and summon abilities."
    )
    w("")
    w("Scope:")
    w("")
    w(
        "- In: every packet the *HighFive* client emits as a reaction to a user action in the world. The canonical list is [§ Packet map](#packet-map)."
    )
    w(
        "- In: the full `RequestActionUse` action-id catalogue (0–73, 1000–1098, 5000–5015), sourced from `RequestActionUse.java`."
    )
    w(
        "- In: the filtered allow-list that applies while the player is transformed (`ACTIONS_ON_TRANSFORM`)."
    )
    w(
        "- Out: generic movement (`MoveToLocation 0x0F`) is only cross-linked — see [PROTOCOL.md](PROTOCOL.md)."
    )
    w("- Out: chat, party/clan/ally management, trade, warehouse, quest dialogs, macros, recipes.")
    w(
        "- Out: item/skill/class catalogues — see [ITEMS.md](ITEMS.md), [SKILLS.md](SKILLS.md), [RACES_CLASSES.md](RACES_CLASSES.md)."
    )
    w("")
    w("Regenerate with: `python scripts/gen_actions_doc.py` (output is deterministic).")
    w("")
    w("Related docs:")
    w("")
    w("- [PROTOCOL.md](PROTOCOL.md) — framing, crypto, login/game handshake.")
    w(
        "- [INVENTORY.md](INVENTORY.md) — item record on the wire, UseItem / RequestDropItem / RequestDestroyItem flows."
    )
    w("- [SKILLS.md](SKILLS.md) — skill id table referenced by `RequestMagicSkillUse`.")
    w("- [CONSTANTS.md](CONSTANTS.md) — social-id list, system-message ids, failure reason codes.")
    w("")
    w("### Wire conventions")
    w("")
    w(
        "All fields are little-endian. Strings are UTF-16LE, null-terminated (matching the rest of the protocol). `u8` = 1 byte, `u16` = 2 bytes, `i32` = 4 bytes, `i64` = 8 bytes. Every packet is wrapped in the usual `u16 length` frame and encrypted with the game-channel XOR cipher once `CryptInit` has completed — see [PROTOCOL.md](PROTOCOL.md) and [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md)."
    )
    w("")

    # ---------------------- Packet map ----------------------
    w("## Packet map")
    w("")
    w("Every opcode that an HighFive client sends when the user performs an interactive action.")
    w("")
    w(fmt_row(["Opcode", "Enum (ClientPackets.java)", "Handler", "Description"]))
    w(fmt_row(["---:", "---", "---", "---"]))
    for op, desc, _anchor in PACKET_MAP:
        enum_name, handler = client_packets.get(op, ("**missing**", ""))
        w(fmt_row([f"0x{op:02X}", f"`{enum_name}`", f"`{handler}`" if handler else "—", desc]))
    w("")
    w(
        "> The legacy opcode `0x01 ATTACK` and the canonical `0x32 ATTACK_REQUEST` share the same handler class (`AttackRequest`) and identical body layout — the HighFive client only emits `0x32`."
    )
    w("")

    # ---------------------- 1. Action (targeting) ----------------------
    w("## 1. Targeting — `Action` 0x1F")
    w("")
    w(
        "Sent whenever the player clicks (or shift-clicks) a world object — NPC, mob, another player, pet, item on the ground, door, artefact, static object."
    )
    w("")
    w("```")
    w("offset  size  field")
    w("  0     u16   length (framing, see PROTOCOL.md)")
    w("  2     u8    opcode = 0x1F")
    w("  3     i32   objectId         -- target's world objectId")
    w("  7     i32   originX          -- player position at click time")
    w(" 11     i32   originY")
    w(" 15     i32   originZ")
    w(" 19     u8    actionId         -- 0 = simple click, 1 = shift-click")
    w("```")
    w("")
    w(
        "Server dispatch is polymorphic on the target type. The per-type behaviour lives in `dist/game/data/scripts/handlers/actionhandlers/` (and the `actionshifthandlers/` mirror for shift-click):"
    )
    w("")
    w(fmt_row(["Target type", "Simple click (actionId 0)", "Shift click (actionId 1)"]))
    w(fmt_row(["---", "---", "---"]))
    w(
        fmt_row(
            ["Npc", "Select / talk / auto-attack if hostile", "Info panel (HTML, NpcInfoExtended)"]
        )
    )
    w(fmt_row(["Player", "Select / follow", "Info panel / GM detail"]))
    w(fmt_row(["Pet / Summon", "Select (owner) or target (non-owner)", "Pet status window"]))
    w(
        fmt_row(
            [
                "Item (on ground)",
                "Select, then `PICK_UP` intention (move to + grab)",
                "Inspect item",
            ]
        )
    )
    w(fmt_row(["Door", "Select, open if unlocked & accessible", "Door info"]))
    w(fmt_row(["StaticObject", "Select; sit if `type==1` (chair/throne/bench)", "Static info"]))
    w(fmt_row(["Artefact", "Select (used during sieges)", "Artefact info"]))
    w(fmt_row(["Decoy / Trap", "Select", "Info"]))
    w("")
    w(
        "A chair-sit at simple-click range (`INTERACTION_DISTANCE`) sends `ChairSit` to the player and broadcasts it; the player also transitions to the sitting state — see action id 0 in [§ 9](#9-requestactionuse-0x56)."
    )
    w("")

    # ---------------------- 2. Target cancel ----------------------
    w("## 2. Cancel target / cancel cast — `RequestTargetCancel` 0x48")
    w("")
    w("Sent by pressing `Esc` with a target selected, or by clicking an empty area.")
    w("")
    w("```")
    w("offset  size  field")
    w("  3     u16   unselect    -- 0 = abort-cast-then-drop-target")
    w("                          -- non-zero = drop-target (or airship-helm deselect)")
    w("```")
    w("")
    w("Server behaviour:")
    w("")
    w(
        "- If `unselect == 0` and the player is mid-cast, the cast is aborted first; target is preserved."
    )
    w(
        "- Otherwise the current target is cleared. If the player is an airship captain, captaincy is released instead."
    )
    w("- The packet is ignored while an `ATTACK_LOCK` effect is active.")
    w("")

    # ---------------------- 3. Attack ----------------------
    w("## 3. Attack — `AttackRequest` 0x32")
    w("")
    w(
        "Sent by double-clicking a hostile target, pressing the attack hotkey, or clicking the Attack action-bar button. Legacy opcode `0x01 ATTACK` has the same layout."
    )
    w("")
    w("```")
    w("offset  size  field")
    w("  3     i32   objectId         -- target's world objectId")
    w("  7     i32   originX          -- player position at click time")
    w(" 11     i32   originY")
    w(" 15     i32   originZ")
    w(" 19     u8    attackId         -- 0 = normal click, 1 = shift-click (forced)")
    w("```")
    w("")
    w("Constraints enforced by `AttackRequest`:")
    w("")
    w("- Not while in a boat / airship as non-captain.")
    w("- Target must be visible, targetable, and in the same instance.")
    w("- Not while in a private store or trade.")
    w("")

    # ---------------------- 4. Skill use ----------------------
    w("## 4. Skill use — `RequestMagicSkillUse` 0x39")
    w("")
    w(
        "Emitted when a skill icon is clicked, a skill shortcut is triggered, or a skill hotkey is pressed."
    )
    w("")
    w("```")
    w("offset  size  field")
    w("  3     i32   magicId          -- skill id (see SKILLS.md)")
    w("  7     i32   ctrlPressed      -- 0 / 1 (force on non-hostile)")
    w(" 11     u8    shiftPressed     -- 0 / 1 (no-move: cancel if out of range)")
    w("```")
    w("")

    # ---------------------- 5. UseItem ----------------------
    w("## 5. Item use — `UseItem` 0x19")
    w("")
    w("Equip toggle, potion, scroll, soul/spirit-shot activation, quest item, etc.")
    w("")
    w("```")
    w("offset  size  field")
    w("  3     i32   objectId         -- inventory item objectId")
    w("  7     i32   ctrlPressed      -- 0 / 1")
    w("```")
    w("")
    w(
        "Dispatched through the server `ItemHandler` registry; actual behaviour depends on the item template (see [INVENTORY.md](INVENTORY.md) and [ITEMS.md](ITEMS.md))."
    )
    w("")

    # ---------------------- 6. Drop ----------------------
    w("## 6. Drop item — `RequestDropItem` 0x17")
    w("")
    w("```")
    w("offset  size  field")
    w("  3     i32   objectId")
    w("  7     i64   count")
    w(" 15     i32   x                -- drop location")
    w(" 19     i32   y")
    w(" 23     i32   z")
    w("```")
    w("")
    w(
        "Server rejects the drop if the item is equipped, marked as quest/pet-only, untradable, in a locked inventory, or if the player is in a no-drop zone."
    )
    w("")

    # ---------------------- 7. Bypass ----------------------
    w("## 7. Bypass — `RequestBypassToServer` 0x23")
    w("")
    w(
        "Triggered by clicking a hyperlink in an NPC HTML page, a community-board page, an item-HTML page, or from code behind the tutorial/help UI."
    )
    w("")
    w("```")
    w("offset  size  field")
    w("  3     str   command          -- UTF-16LE, null-terminated")
    w("```")
    w("")
    w("Namespaces (most common):")
    w("")
    w("- `admin_*` — GM commands (access-level gated).")
    w("- `npc_<objectId>_*` — NPC dialog continuations (Chat, Buy, QuestTalk, Teleport).")
    w("- `item_<objectId>_*` — item-bound HTML buttons.")
    w("- `_bbs*`, `_mail*`, `_friend*`, `_block*` — community-board actions.")
    w("- `_olympiad*`, `manor_menu_select?*`, `report` — misc UI flows.")
    w("")
    w(
        "Bypass strings are validated against the HTML template that last offered them, to block spoofing."
    )
    w("")

    # ---------------------- MoveToLocation (brief) ----------------------
    w("## MoveToLocation 0x0F (click-to-move)")
    w("")
    w(
        'Documented in [PROTOCOL.md](PROTOCOL.md) — cross-referenced here because click-to-move is technically an "action". Body: `i32 targetX, targetY, targetZ, originX, originY, originZ, i32 movementMode` (`0` = cursor keys, `1` = mouse).'
    )
    w("")

    # ---------------------- RequestLinkHtml ----------------------
    w("## RequestLinkHtml 0x22")
    w("")
    w(
        "Sent when the user clicks an NPC-HTML anchor that targets a *local* `link` file (as opposed to a server bypass). Body: `str link` (UTF-16LE null-terminated). Server loads the named HTML from the current NPC's HTML cache and echoes it back."
    )
    w("")

    # ---------------------- 9. RequestActionUse ----------------------
    w("## 9. `RequestActionUse` 0x56 — the grand-unified action packet")
    w("")
    w("Most of what an F-key, summon-panel button, or social emote does ends up here.")
    w("")
    w("```")
    w("offset  size  field")
    w("  3     i32   actionId         -- see action catalogue below")
    w("  7     i32   ctrlPressed      -- 0 / 1")
    w(" 11     u8    shiftPressed     -- 0 / 1")
    w("```")
    w("")
    w("Server pre-checks (in `RequestActionUse.runImpl`):")
    w("")
    w("- Player alive, not fake-dead (except `actionId == 0`), not out-of-control.")
    w("- `BOT_PENALTY` effect: each effect's `checkCondition(actionId)` must allow the action.")
    w(
        "- If transformed, the `actionId` must be in [`ACTIONS_ON_TRANSFORM`](#94-actions_on_transform-allow-list-while-transformed) (binary search)."
    )
    w("")

    # Split the action list into ranges.
    core = [a for a in actions if 0 <= a.id <= 74]
    summon1000 = [a for a in actions if 1000 <= a.id < 2000]
    summon5000 = [a for a in actions if 5000 <= a.id < 6000]

    w("### 9.1 Core player actions (0–74)")
    w("")
    w(
        "Sit/stand, walk/run, private stores, socials, pet & servitor controls, mount, airship, couple actions, bot-report."
    )
    w("")
    w(fmt_row(["Id", "Description"]))
    w(fmt_row(["---:", "---"]))
    for a in core:
        w(fmt_row([str(a.id), a.comment]))
    w("")
    w("Fields that compose common subsets:")
    w("")
    w("- **Posture:** 0 Sit/Stand, 1 Walk/Run.")
    w(
        "- **Private stores:** 10 Sell (basic), 28 Buy, 37 Dwarven Manufacture, 51 General Manufacture, 61 Sell (package)."
    )
    w(
        "- **Pet controls:** 15 Follow/Stop toggle, 16 Attack, 17 Stop, 19 Unsummon, 54 Move to target."
    )
    w(
        "- **Servitor controls:** 21 Follow/Stop toggle, 22 Attack, 23 Stop, 52 Unsummon, 53 Move to target."
    )
    w("- **Mount:** 38 Mount / Dismount (requires a strider summon).")
    w("- **Airship (captain):** 67 Steer, 68 Cancel control, 69 Destination map, 70 Exit.")
    w(
        "- **Couple socials:** 71, 72, 73 — send `ExAskCoupleAction` to the partner after range/state checks (distance 15–125, both sides not in combat / store / siege / mount / transform / chaotic state)."
    )
    w("- **Bot report:** 65 (only if `BOTREPORT_ENABLE` is on).")
    w("- **Socials 12–35, 62, 66:** see [§ 11 Social actions](#11-social-actions).")
    w("")

    w("### 9.2 Summon skill actions (1000–1098)")
    w("")
    w(
        "Each entry triggers a summon ability on the current target (or self for Buff/Heal types), subject to `validateSummon` and `canControl` checks."
    )
    w("")
    w(fmt_row(["Id", "Description"]))
    w(fmt_row(["---:", "---"]))
    for a in summon1000:
        w(fmt_row([str(a.id), a.comment]))
    w("")

    w("### 9.3 Ancient / event summon actions (5000–5015)")
    w("")
    w(
        "Actions for the quest-given Baby Rudolph, the Toy Dwarf set (Deseloph, Hyum, Rekang, Lilias, Lapham, Mafum), and their seasonal variants."
    )
    w("")
    w(fmt_row(["Id", "Description"]))
    w(fmt_row(["---:", "---"]))
    for a in summon5000:
        w(fmt_row([str(a.id), a.comment]))
    w("")

    w("### 9.4 `ACTIONS_ON_TRANSFORM` allow-list while transformed")
    w("")
    w(
        f"While the player is transformed, only these {len(transform_allowed)} action ids are accepted. Others are rejected with `ActionFailed` and a server-side warning."
    )
    w("")
    w("```")
    # emit 8 per row
    for i in range(0, len(transform_allowed), 8):
        chunk = transform_allowed[i : i + 8]
        w(", ".join(f"{x:>4}" for x in chunk))
    w("```")
    w("")

    # ---------------------- 10. Shortcuts ----------------------
    w("## 10. Shortcuts — `RequestShortcutReg` 0x3D / `RequestShortcutDel` 0x3F")
    w("")
    w(
        "The client action bar has **12 slots × 10 pages = 120 shortcut cells**. Each cell is an `(type, id, level, characterType)` tuple."
    )
    w("")
    w("### 10.1 `ShortcutType` enum (0–6)")
    w("")
    w(fmt_row(["Ord", "Name", "id refers to"]))
    w(fmt_row(["---:", "---", "---"]))
    w(fmt_row(["0", "NONE", "(empty)"]))
    w(fmt_row(["1", "ITEM", "inventory item objectId"]))
    w(fmt_row(["2", "SKILL", "skill id (see [SKILLS.md](SKILLS.md))"]))
    w(fmt_row(["3", "ACTION", "RequestActionUse action id (see [§ 9](#9-requestactionuse-0x56))"]))
    w(fmt_row(["4", "MACRO", "macro id from the macro list"]))
    w(fmt_row(["5", "RECIPE", "recipe id"]))
    w(fmt_row(["6", "BOOKMARK", "teleport bookmark id"]))
    w("")
    w("### 10.2 `RequestShortcutReg` 0x3D")
    w("")
    w("```")
    w("offset  size  field")
    w("  3     i32   type             -- ShortcutType ordinal (0..6)")
    w("  7     i32   slot             -- encoded slot: slot + page*12   (0..119)")
    w(" 11     i32   id               -- itemObjectId / skillId / actionId / ...")
    w(" 15     i32   level            -- skill level (0 for non-SKILL)")
    w(" 19     i32   characterType    -- 1 = player, 2 = summon")
    w("```")
    w("")
    w(
        "Server validates `type ∈ [0,6]` and `page ∈ [0,10]`; on success stores the shortcut and broadcasts `ShortcutRegister` back to the client."
    )
    w("")
    w("### 10.3 `RequestShortcutDel` 0x3F")
    w("")
    w("```")
    w("offset  size  field")
    w("  3     i32   slot             -- encoded slot (slot + page*12)")
    w("```")
    w("")
    w("### 10.4 Initial push — `ShortcutInit` (server 0x45)")
    w("")
    w(
        "On `EnterWorld`, the server sends every stored shortcut. Each record is: `i32 type, i32 slot, i32 id, i32 level, i32 characterType` (`type`-specific fields may differ for MACRO/RECIPE — check `ShortcutInit.java`)."
    )
    w("")
    w("### 10.5 F1–F12 resolution")
    w("")
    w(
        "F-keys have no dedicated packets. They are **pure client-side accelerators**: the client looks up slot `N` on the currently active page and emits the packet matching that slot's `ShortcutType`:"
    )
    w("")
    w(fmt_row(["Shortcut type", "Packet emitted when F-key is pressed"]))
    w(fmt_row(["---", "---"]))
    w(fmt_row(["ACTION", "`RequestActionUse 0x56` with `actionId = shortcut.id`"]))
    w(
        fmt_row(
            [
                "SKILL",
                "`RequestMagicSkillUse 0x39` with `magicId = shortcut.id, level = shortcut.level`",
            ]
        )
    )
    w(fmt_row(["ITEM", "`UseItem 0x19` with `objectId = shortcut.id`"]))
    w(
        fmt_row(
            [
                "MACRO",
                "Replayed locally: a sequence of `Say2 0x49`, `RequestBypassToServer 0x23`, `UseItem 0x19`, or `RequestActionUse 0x56` packets",
            ]
        )
    )
    w(fmt_row(["RECIPE", "`RequestRecipeBookOpen 0xB5` → `RequestRecipeItemMakeSelf 0xB8`"]))
    w(fmt_row(["BOOKMARK", "`RequestBypassToServer 0x23` with a teleport command"]))
    w("")
    w(
        "The action bar's default F1..F12 mapping is stored in the *client-side* `.dat` files (`shortcutdefault-*.dat` etc.) — it is NOT transmitted by the server. The well-known defaults are listed in [§ 12](#12-client-default-f-key-bindings) for reference only."
    )
    w("")

    # ---------------------- 11. Socials ----------------------
    w("## 11. Social actions")
    w("")
    w(
        "A social emote is requested with `RequestActionUse 0x56`. The server validates it (blocked while fishing, see `tryBroadcastSocial`) and broadcasts `SocialAction (server 0x27)` with `(objectId, socialId)`."
    )
    w("")
    w(fmt_row(["Action id (0x56)", "Social id (0x27)", "Emote"]))
    w(fmt_row(["---:", "---:", "---"]))
    for aid, sid, name in SOCIAL_ACTIONS:
        w(fmt_row([str(aid), str(sid), name]))
    w("")
    w("Additional socials:")
    w("")
    w("- `socialId = 2122` is broadcast automatically on level-up; no client packet.")
    w(
        "- Couple socials (`ExAskCoupleAction`) are requested via action ids 71, 72, 73 — see [§ 9.1](#91-core-player-actions-074)."
    )
    w("")

    # ---------------------- 12. Default F-keys ----------------------
    w("## 12. Client default F-key bindings")
    w("")
    w(
        "These are the HighFive client defaults — informational only; users can rebind them and server only sees the resulting packet."
    )
    w("")
    w(fmt_row(["Key", "Default binding"]))
    w(fmt_row(["---", "---"]))
    for k, v in DEFAULT_FKEYS:
        w(fmt_row([k, v]))
    w("")
    w("Common additional hotkeys that translate into the packets above:")
    w("")
    w("- `Space` / dedicated Attack key → `AttackRequest 0x32` on current target.")
    w("- `Tab` → Target Next Enemy (client-local cycling + `Action 0x1F`).")
    w("- `Ctrl+Tab` → Target Next Party Member.")
    w(
        "- `Shift+click` on a target → `Action 0x1F` with `actionId = 1` (info panel) or `AttackRequest 0x32` with forced flag, depending on target."
    )
    w(
        "- `Ctrl+click` on a skill → `RequestMagicSkillUse 0x39` with `ctrlPressed = 1` (force on non-hostile)."
    )
    w("- `Esc` → `RequestTargetCancel 0x48`.")
    w("- `Sit` / `Run` toggles → `RequestActionUse 0x56` action ids `0` / `1`.")
    w("- `Pick up` (default `F5`) → `Action 0x1F` on nearest on-ground item's objectId.")
    w("")

    # ---------------------- 13. Regeneration ----------------------
    w("## 13. Regeneration")
    w("")
    w(
        "Tables in [§ 9.1](#91-core-player-actions-074), [§ 9.2](#92-summon-skill-actions-10001098), [§ 9.3](#93-ancient--event-summon-actions-50005015), and [§ 9.4](#94-actions_on_transform-allow-list-while-transformed) are extracted from the L2JMobius server source by [`scripts/gen_actions_doc.py`](../scripts/gen_actions_doc.py). Regenerate after bumping the server submodule:"
    )
    w("")
    w("```")
    w(
        r"python scripts/gen_actions_doc.py --server c:\MyProg\l2J-Mobius-CT-2.6-HighFive --out docs\ACTIONS.md"
    )
    w("```")
    w("")

    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", type=Path, default=DEFAULT_SERVER)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    net = args.server / "java" / "org" / "l2jmobius" / "gameserver" / "network"
    req_action = net / "clientpackets" / "RequestActionUse.java"
    basic_list = net / "serverpackets" / "ExBasicActionList.java"
    client_enum = net / "ClientPackets.java"

    for p in (req_action, basic_list, client_enum):
        if not p.is_file():
            ap.error(f"missing server source file: {p}")

    actions = parse_action_cases(req_action.read_text(encoding="utf-8"))
    transform_allowed = parse_actions_on_transform(basic_list.read_text(encoding="utf-8"))
    client_packets = parse_client_packets(client_enum.read_text(encoding="utf-8"))

    # Sanity-check: every opcode we describe must exist in the server enum.
    missing = [op for op, _, _ in PACKET_MAP if op not in client_packets]
    if missing:
        raise SystemExit(f"opcodes not found in ClientPackets.java: {[hex(o) for o in missing]}")

    doc = build_doc(actions, transform_allowed, client_packets)
    args.out.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"Wrote {args.out} ({len(doc):,} bytes, {len(actions)} actions, "
        f"{len(transform_allowed)} transform-allowed ids)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
