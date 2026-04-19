# In-game Actions (HighFive / L2JMobius CT 2.6)

## Overview

Every client→server packet that corresponds to a user-initiated gameplay *action*: targeting, attack, skill, item, drop, sit/stand, run/walk, pet & servitor controls, airship steering, private stores, socials, shortcut registration, HTML/NPC bypasses, and the unified `RequestActionUse (0x56)` dispatcher that handles F-key shortcuts and summon abilities.

Scope:

- In: every packet the *HighFive* client emits as a reaction to a user action in the world. The canonical list is [§ Packet map](#packet-map).
- In: the full `RequestActionUse` action-id catalogue (0–73, 1000–1098, 5000–5015), sourced from `RequestActionUse.java`.
- In: the filtered allow-list that applies while the player is transformed (`ACTIONS_ON_TRANSFORM`).
- Out: generic movement (`MoveToLocation 0x0F`) is only cross-linked — see [PROTOCOL.md](PROTOCOL.md).
- Out: chat, party/clan/ally management, trade, warehouse, quest dialogs, macros, recipes.
- Out: item/skill/class catalogues — see [ITEMS.md](ITEMS.md), [SKILLS.md](SKILLS.md), [RACES_CLASSES.md](RACES_CLASSES.md).

Regenerate with: `python scripts/gen_actions_doc.py` (output is deterministic).

Related docs:

- [PROTOCOL.md](PROTOCOL.md) — framing, crypto, login/game handshake.
- [INVENTORY.md](INVENTORY.md) — item record on the wire, UseItem / RequestDropItem / RequestDestroyItem flows.
- [SKILLS.md](SKILLS.md) — skill id table referenced by `RequestMagicSkillUse`.
- [CONSTANTS.md](CONSTANTS.md) — social-id list, system-message ids, failure reason codes.

### Wire conventions

All fields are little-endian. Strings are UTF-16LE, null-terminated (matching the rest of the protocol). `u8` = 1 byte, `u16` = 2 bytes, `i32` = 4 bytes, `i64` = 8 bytes. Every packet is wrapped in the usual `u16 length` frame and encrypted with the game-channel XOR cipher once `CryptInit` has completed — see [PROTOCOL.md](PROTOCOL.md) and [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md).

## Packet map

Every opcode that an HighFive client sends when the user performs an interactive action.

| Opcode | Enum (ClientPackets.java) | Handler | Description |
| ---: | --- | --- | --- |
| 0x01 | `ATTACK` | `AttackRequest` | Attack (legacy alias; identical body to 0x32) |
| 0x0F | `MOVE_TO_LOCATION` | `MoveToLocation` | MoveToLocation — click-to-move |
| 0x17 | `REQUEST_DROP_ITEM` | `RequestDropItem` | RequestDropItem — drop items to the ground |
| 0x19 | `USE_ITEM` | `UseItem` | UseItem — consume / equip / toggle an inventory item |
| 0x1F | `ACTION` | `Action` | Action — click on any world object |
| 0x22 | `REQUEST_LINK_HTML` | `RequestLinkHtml` | RequestLinkHtml — HTML link bypass |
| 0x23 | `REQUEST_BYPASS_TO_SERVER` | `RequestBypassToServer` | RequestBypassToServer — NPC/admin/community command |
| 0x32 | `ATTACK_REQUEST` | `AttackRequest` | AttackRequest — forced auto-attack toggle |
| 0x39 | `REQUEST_MAGIC_SKILL_USE` | `RequestMagicSkillUse` | RequestMagicSkillUse — cast a skill by id |
| 0x3D | `REQUEST_SHORT_CUT_REG` | `RequestShortcutReg` | RequestShortcutReg — register action-bar slot |
| 0x3F | `REQUEST_SHORT_CUT_DEL` | `RequestShortcutDel` | RequestShortcutDel — delete action-bar slot |
| 0x48 | `REQUEST_TARGET_CANCELD` | `RequestTargetCanceld` | RequestTargetCancel — cancel target or abort cast |
| 0x56 | `REQUEST_ACTION_USE` | `RequestActionUse` | RequestActionUse — grand-unified action dispatcher |

> The legacy opcode `0x01 ATTACK` and the canonical `0x32 ATTACK_REQUEST` share the same handler class (`AttackRequest`) and identical body layout — the HighFive client only emits `0x32`.

## 1. Targeting — `Action` 0x1F

Sent whenever the player clicks (or shift-clicks) a world object — NPC, mob, another player, pet, item on the ground, door, artefact, static object.

```
offset  size  field
  0     u16   length (framing, see PROTOCOL.md)
  2     u8    opcode = 0x1F
  3     i32   objectId         -- target's world objectId
  7     i32   originX          -- player position at click time
 11     i32   originY
 15     i32   originZ
 19     u8    actionId         -- 0 = simple click, 1 = shift-click
```

Server dispatch is polymorphic on the target type. The per-type behaviour lives in `dist/game/data/scripts/handlers/actionhandlers/` (and the `actionshifthandlers/` mirror for shift-click):

| Target type | Simple click (actionId 0) | Shift click (actionId 1) |
| --- | --- | --- |
| Npc | Select / talk / auto-attack if hostile | Info panel (HTML, NpcInfoExtended) |
| Player | Select / follow | Info panel / GM detail |
| Pet / Summon | Select (owner) or target (non-owner) | Pet status window |
| Item (on ground) | Select, then `PICK_UP` intention (move to + grab) | Inspect item |
| Door | Select, open if unlocked & accessible | Door info |
| StaticObject | Select; sit if `type==1` (chair/throne/bench) | Static info |
| Artefact | Select (used during sieges) | Artefact info |
| Decoy / Trap | Select | Info |

A chair-sit at simple-click range (`INTERACTION_DISTANCE`) sends `ChairSit` to the player and broadcasts it; the player also transitions to the sitting state — see action id 0 in [§ 9](#9-requestactionuse-0x56).

## 2. Cancel target / cancel cast — `RequestTargetCancel` 0x48

Sent by pressing `Esc` with a target selected, or by clicking an empty area.

```
offset  size  field
  3     u16   unselect    -- 0 = abort-cast-then-drop-target
                          -- non-zero = drop-target (or airship-helm deselect)
```

Server behaviour:

- If `unselect == 0` and the player is mid-cast, the cast is aborted first; target is preserved.
- Otherwise the current target is cleared. If the player is an airship captain, captaincy is released instead.
- The packet is ignored while an `ATTACK_LOCK` effect is active.

## 3. Attack — `AttackRequest` 0x32

Sent by double-clicking a hostile target, pressing the attack hotkey, or clicking the Attack action-bar button. Legacy opcode `0x01 ATTACK` has the same layout.

```
offset  size  field
  3     i32   objectId         -- target's world objectId
  7     i32   originX          -- player position at click time
 11     i32   originY
 15     i32   originZ
 19     u8    attackId         -- 0 = normal click, 1 = shift-click (forced)
```

Constraints enforced by `AttackRequest`:

- Not while in a boat / airship as non-captain.
- Target must be visible, targetable, and in the same instance.
- Not while in a private store or trade.

## 4. Skill use — `RequestMagicSkillUse` 0x39

Emitted when a skill icon is clicked, a skill shortcut is triggered, or a skill hotkey is pressed.

```
offset  size  field
  3     i32   magicId          -- skill id (see SKILLS.md)
  7     i32   ctrlPressed      -- 0 / 1 (force on non-hostile)
 11     u8    shiftPressed     -- 0 / 1 (no-move: cancel if out of range)
```

## 5. Item use — `UseItem` 0x19

Equip toggle, potion, scroll, soul/spirit-shot activation, quest item, etc.

```
offset  size  field
  3     i32   objectId         -- inventory item objectId
  7     i32   ctrlPressed      -- 0 / 1
```

Dispatched through the server `ItemHandler` registry; actual behaviour depends on the item template (see [INVENTORY.md](INVENTORY.md) and [ITEMS.md](ITEMS.md)).

## 6. Drop item — `RequestDropItem` 0x17

```
offset  size  field
  3     i32   objectId
  7     i64   count
 15     i32   x                -- drop location
 19     i32   y
 23     i32   z
```

Server rejects the drop if the item is equipped, marked as quest/pet-only, untradable, in a locked inventory, or if the player is in a no-drop zone.

## 7. Bypass — `RequestBypassToServer` 0x23

Triggered by clicking a hyperlink in an NPC HTML page, a community-board page, an item-HTML page, or from code behind the tutorial/help UI.

```
offset  size  field
  3     str   command          -- UTF-16LE, null-terminated
```

Namespaces (most common):

- `admin_*` — GM commands (access-level gated).
- `npc_<objectId>_*` — NPC dialog continuations (Chat, Buy, QuestTalk, Teleport).
- `item_<objectId>_*` — item-bound HTML buttons.
- `_bbs*`, `_mail*`, `_friend*`, `_block*` — community-board actions.
- `_olympiad*`, `manor_menu_select?*`, `report` — misc UI flows.

Bypass strings are validated against the HTML template that last offered them, to block spoofing.

## MoveToLocation 0x0F (click-to-move)

Documented in [PROTOCOL.md](PROTOCOL.md) — cross-referenced here because click-to-move is technically an "action". Body: `i32 targetX, targetY, targetZ, originX, originY, originZ, i32 movementMode` (`0` = cursor keys, `1` = mouse).

## RequestLinkHtml 0x22

Sent when the user clicks an NPC-HTML anchor that targets a *local* `link` file (as opposed to a server bypass). Body: `str link` (UTF-16LE null-terminated). Server loads the named HTML from the current NPC's HTML cache and echoes it back.

## 9. `RequestActionUse` 0x56 — the grand-unified action packet

Most of what an F-key, summon-panel button, or social emote does ends up here.

```
offset  size  field
  3     i32   actionId         -- see action catalogue below
  7     i32   ctrlPressed      -- 0 / 1
 11     u8    shiftPressed     -- 0 / 1
```

Server pre-checks (in `RequestActionUse.runImpl`):

- Player alive, not fake-dead (except `actionId == 0`), not out-of-control.
- `BOT_PENALTY` effect: each effect's `checkCondition(actionId)` must allow the action.
- If transformed, the `actionId` must be in [`ACTIONS_ON_TRANSFORM`](#94-actions_on_transform-allow-list-while-transformed) (binary search).

### 9.1 Core player actions (0–74)

Sit/stand, walk/run, private stores, socials, pet & servitor controls, mount, airship, couple actions, bot-report.

| Id | Description |
| ---: | --- |
| 0 | Sit/Stand |
| 1 | Walk/Run |
| 10 | Private Store - Sell |
| 12 | Greeting |
| 13 | Victory |
| 14 | Advance |
| 15 | Change Movement Mode (Pets) |
| 16 | Attack (Pets) |
| 17 | Stop (Pets) |
| 19 | Unsummon Pet |
| 21 | Change Movement Mode (Servitors) |
| 22 | Attack (Servitors) |
| 23 | Stop (Servitors) |
| 24 | Yes |
| 25 | No |
| 26 | Bow |
| 28 | Private Store - Buy |
| 29 | Unaware |
| 30 | Social Waiting |
| 31 | Laugh |
| 32 | Wild Hog Cannon - Wild Cannon |
| 33 | Applaud |
| 34 | Dance |
| 35 | Sorrow |
| 36 | Soulless - Toxic Smoke |
| 37 | Dwarven Manufacture |
| 38 | Mount/Dismount |
| 39 | Soulless - Parasite Burst |
| 41 | Wild Hog Cannon - Attack |
| 42 | Kai the Cat - Self Damage Shield |
| 43 | Merrow the Unicorn - Hydro Screw |
| 44 | Big Boom - Boom Attack |
| 45 | Boxer the Unicorn - Master Recharge |
| 46 | Mew the Cat - Mega Storm Strike |
| 47 | Silhouette - Steal Blood |
| 48 | Mechanic Golem - Mech. Cannon |
| 51 | General Manufacture |
| 52 | Unsummon Servitor |
| 53 | Move to target (Servitors) |
| 54 | Move to target (Pets) |
| 61 | Private Store Package Sell |
| 62 | Charm |
| 65 | Bot Report Button |
| 66 | Shyness |
| 67 | Steer |
| 68 | Cancel Control |
| 69 | Destination Map |
| 70 | Exit Airship |

Fields that compose common subsets:

- **Posture:** 0 Sit/Stand, 1 Walk/Run.
- **Private stores:** 10 Sell (basic), 28 Buy, 37 Dwarven Manufacture, 51 General Manufacture, 61 Sell (package).
- **Pet controls:** 15 Follow/Stop toggle, 16 Attack, 17 Stop, 19 Unsummon, 54 Move to target.
- **Servitor controls:** 21 Follow/Stop toggle, 22 Attack, 23 Stop, 52 Unsummon, 53 Move to target.
- **Mount:** 38 Mount / Dismount (requires a strider summon).
- **Airship (captain):** 67 Steer, 68 Cancel control, 69 Destination map, 70 Exit.
- **Couple socials:** 71, 72, 73 — send `ExAskCoupleAction` to the partner after range/state checks (distance 15–125, both sides not in combat / store / siege / mount / transform / chaotic state).
- **Bot report:** 65 (only if `BOTREPORT_ENABLE` is on).
- **Socials 12–35, 62, 66:** see [§ 11 Social actions](#11-social-actions).

### 9.2 Summon skill actions (1000–1098)

Each entry triggers a summon ability on the current target (or self for Buff/Heal types), subject to `validateSummon` and `canControl` checks.

| Id | Description |
| ---: | --- |
| 1000 | Siege Golem - Siege Hammer |
| 1001 | Sin Eater - Ultimate Bombastic Buster |
| 1003 | Wind Hatchling/Strider - Wild Stun |
| 1004 | Wind Hatchling/Strider - Wild Defense |
| 1005 | Star Hatchling/Strider - Bright Burst |
| 1006 | Star Hatchling/Strider - Bright Heal |
| 1007 | Feline Queen - Blessing of Queen |
| 1008 | Feline Queen - Gift of Queen |
| 1009 | Feline Queen - Cure of Queen |
| 1010 | Unicorn Seraphim - Blessing of Seraphim |
| 1011 | Unicorn Seraphim - Gift of Seraphim |
| 1012 | Unicorn Seraphim - Cure of Seraphim |
| 1013 | Nightshade - Curse of Shade |
| 1014 | Nightshade - Mass Curse of Shade |
| 1015 | Nightshade - Shade Sacrifice |
| 1016 | Cursed Man - Cursed Blow |
| 1017 | Cursed Man - Cursed Strike |
| 1031 | Feline King - Slash |
| 1032 | Feline King - Spinning Slash |
| 1033 | Feline King - Hold of King |
| 1034 | Magnus the Unicorn - Whiplash |
| 1035 | Magnus the Unicorn - Tridal Wave |
| 1036 | Spectral Lord - Corpse Kaboom |
| 1037 | Spectral Lord - Dicing Death |
| 1038 | Spectral Lord - Dark Curse |
| 1039 | Swoop Cannon - Cannon Fodder |
| 1040 | Swoop Cannon - Big Bang |
| 1041 | Great Wolf - Bite Attack |
| 1042 | Great Wolf - Maul |
| 1043 | Great Wolf - Cry of the Wolf |
| 1044 | Great Wolf - Awakening |
| 1045 | Great Wolf - Howl |
| 1046 | Strider - Roar |
| 1047 | Divine Beast - Bite |
| 1048 | Divine Beast - Stun Attack |
| 1049 | Divine Beast - Fire Breath |
| 1050 | Divine Beast - Roar |
| 1051 | Feline Queen - Bless The Body |
| 1052 | Feline Queen - Bless The Soul |
| 1053 | Feline Queen - Haste |
| 1054 | Unicorn Seraphim - Acumen |
| 1055 | Unicorn Seraphim - Clarity |
| 1056 | Unicorn Seraphim - Empower |
| 1057 | Unicorn Seraphim - Wild Magic |
| 1058 | Nightshade - Death Whisper |
| 1059 | Nightshade - Focus |
| 1060 | Nightshade - Guidance |
| 1061 | Wild Beast Fighter, White Weasel - Death blow |
| 1062 | Wild Beast Fighter - Double attack |
| 1063 | Wild Beast Fighter - Spin attack |
| 1064 | Wild Beast Fighter - Meteor Shower |
| 1065 | Fox Shaman, Wild Beast Fighter, White Weasel, Fairy Princess - Awakening |
| 1066 | Fox Shaman, Spirit Shaman - Thunder Bolt |
| 1067 | Fox Shaman, Spirit Shaman - Flash |
| 1068 | Fox Shaman, Spirit Shaman - Lightning Wave |
| 1069 | Fox Shaman, Fairy Princess - Flare |
| 1070 | White Weasel, Fairy Princess, Improved Baby Buffalo, Improved Baby Kookaburra, Improved Baby Cougar, Spirit Shaman, Toy Knight, Turtle Ascetic - Buff control |
| 1071 | Tigress - Power Strike |
| 1072 | Toy Knight - Piercing attack |
| 1073 | Toy Knight - Whirlwind |
| 1074 | Toy Knight - Lance Smash |
| 1075 | Toy Knight - Battle Cry |
| 1076 | Turtle Ascetic - Power Smash |
| 1077 | Turtle Ascetic - Energy Burst |
| 1078 | Turtle Ascetic - Shockwave |
| 1079 | Turtle Ascetic - Howl |
| 1080 | Phoenix Rush |
| 1081 | Phoenix Cleanse |
| 1082 | Phoenix Flame Feather |
| 1083 | Phoenix Flame Beak |
| 1084 | Switch State |
| 1086 | Panther Cancel |
| 1087 | Panther Dark Claw |
| 1088 | Panther Fatal Claw |
| 1089 | Deinonychus - Tail Strike |
| 1090 | Guardian's Strider - Strider Bite |
| 1091 | Guardian's Strider - Strider Fear |
| 1092 | Guardian's Strider - Strider Dash |
| 1093 | Maguen - Maguen Strike |
| 1094 | Maguen - Maguen Wind Walk |
| 1095 | Elite Maguen - Maguen Power Strike |
| 1096 | Elite Maguen - Elite Maguen Wind Walk |
| 1097 | Maguen - Maguen Return |
| 1098 | Elite Maguen - Maguen Party Return |

### 9.3 Ancient / event summon actions (5000–5015)

Actions for the quest-given Baby Rudolph, the Toy Dwarf set (Deseloph, Hyum, Rekang, Lilias, Lapham, Mafum), and their seasonal variants.

| Id | Description |
| ---: | --- |
| 5000 | Baby Rudolph - Reindeer Scratch |
| 5001 | Deseloph, Hyum, Rekang, Lilias, Lapham, Mafum - Rosy Seduction |
| 5002 | Deseloph, Hyum, Rekang, Lilias, Lapham, Mafum - Critical Seduction |
| 5003 | Hyum, Lapham, Hyum, Lapham - Thunder Bolt |
| 5004 | Hyum, Lapham, Hyum, Lapham - Flash |
| 5005 | Hyum, Lapham, Hyum, Lapham - Lightning Wave |
| 5006 | Deseloph, Hyum, Rekang, Lilias, Lapham, Mafum, Deseloph, Hyum, Rekang, Lilias, Lapham, Mafum - Buff Control |
| 5007 | Deseloph, Lilias, Deseloph, Lilias - Piercing Attack |
| 5008 | Deseloph, Lilias, Deseloph, Lilias - Spin Attack |
| 5009 | Deseloph, Lilias, Deseloph, Lilias - Smash |
| 5010 | Deseloph, Lilias, Deseloph, Lilias - Ignite |
| 5011 | Rekang, Mafum, Rekang, Mafum - Power Smash |
| 5012 | Rekang, Mafum, Rekang, Mafum - Energy Burst |
| 5013 | Rekang, Mafum, Rekang, Mafum - Shockwave |
| 5014 | Rekang, Mafum, Rekang, Mafum - Ignite |
| 5015 | Deseloph, Hyum, Rekang, Lilias, Lapham, Mafum, Deseloph, Hyum, Rekang, Lilias, Lapham, Mafum - Switch Stance |

### 9.4 `ACTIONS_ON_TRANSFORM` allow-list while transformed

While the player is transformed, only these 135 action ids are accepted. Others are rejected with `ActionFailed` and a server-side warning.

```
   1,    2,    3,    4,    5,    6,    7,    8
   9,   11,   15,   16,   17,   18,   19,   21
  22,   23,   32,   36,   39,   40,   41,   42
  43,   44,   45,   46,   47,   48,   50,   52
  53,   54,   55,   56,   57,   63,   64,   65
  70, 1000, 1001, 1003, 1004, 1005, 1006, 1007
1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015
1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023
1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031
1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039
1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047
1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055
1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063
1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071
1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079
1080, 1081, 1082, 1083, 1084, 1089, 1090, 1091
1092, 1093, 1094, 1095, 1096, 1097, 1098
```

## 10. Shortcuts — `RequestShortcutReg` 0x3D / `RequestShortcutDel` 0x3F

The client action bar has **12 slots × 10 pages = 120 shortcut cells**. Each cell is an `(type, id, level, characterType)` tuple.

### 10.1 `ShortcutType` enum (0–6)

| Ord | Name | id refers to |
| ---: | --- | --- |
| 0 | NONE | (empty) |
| 1 | ITEM | inventory item objectId |
| 2 | SKILL | skill id (see [SKILLS.md](SKILLS.md)) |
| 3 | ACTION | RequestActionUse action id (see [§ 9](#9-requestactionuse-0x56)) |
| 4 | MACRO | macro id from the macro list |
| 5 | RECIPE | recipe id |
| 6 | BOOKMARK | teleport bookmark id |

### 10.2 `RequestShortcutReg` 0x3D

```
offset  size  field
  3     i32   type             -- ShortcutType ordinal (0..6)
  7     i32   slot             -- encoded slot: slot + page*12   (0..119)
 11     i32   id               -- itemObjectId / skillId / actionId / ...
 15     i32   level            -- skill level (0 for non-SKILL)
 19     i32   characterType    -- 1 = player, 2 = summon
```

Server validates `type ∈ [0,6]` and `page ∈ [0,10]`; on success stores the shortcut and broadcasts `ShortcutRegister` back to the client.

### 10.3 `RequestShortcutDel` 0x3F

```
offset  size  field
  3     i32   slot             -- encoded slot (slot + page*12)
```

### 10.4 Initial push — `ShortcutInit` (server 0x45)

On `EnterWorld`, the server sends every stored shortcut. Each record is: `i32 type, i32 slot, i32 id, i32 level, i32 characterType` (`type`-specific fields may differ for MACRO/RECIPE — check `ShortcutInit.java`).

### 10.5 F1–F12 resolution

F-keys have no dedicated packets. They are **pure client-side accelerators**: the client looks up slot `N` on the currently active page and emits the packet matching that slot's `ShortcutType`:

| Shortcut type | Packet emitted when F-key is pressed |
| --- | --- |
| ACTION | `RequestActionUse 0x56` with `actionId = shortcut.id` |
| SKILL | `RequestMagicSkillUse 0x39` with `magicId = shortcut.id, level = shortcut.level` |
| ITEM | `UseItem 0x19` with `objectId = shortcut.id` |
| MACRO | Replayed locally: a sequence of `Say2 0x49`, `RequestBypassToServer 0x23`, `UseItem 0x19`, or `RequestActionUse 0x56` packets |
| RECIPE | `RequestRecipeBookOpen 0xB5` → `RequestRecipeItemMakeSelf 0xB8` |
| BOOKMARK | `RequestBypassToServer 0x23` with a teleport command |

The action bar's default F1..F12 mapping is stored in the *client-side* `.dat` files (`shortcutdefault-*.dat` etc.) — it is NOT transmitted by the server. The well-known defaults are listed in [§ 12](#12-client-default-f-key-bindings) for reference only.

## 11. Social actions

A social emote is requested with `RequestActionUse 0x56`. The server validates it (blocked while fishing, see `tryBroadcastSocial`) and broadcasts `SocialAction (server 0x27)` with `(objectId, socialId)`.

| Action id (0x56) | Social id (0x27) | Emote |
| ---: | ---: | --- |
| 12 | 2 | Greeting |
| 13 | 3 | Victory |
| 14 | 4 | Advance |
| 24 | 6 | Yes |
| 25 | 5 | No |
| 26 | 7 | Bow |
| 29 | 8 | Unaware |
| 30 | 9 | Social Waiting |
| 31 | 10 | Laugh |
| 33 | 11 | Applaud |
| 34 | 12 | Dance |
| 35 | 13 | Sorrow |
| 62 | 14 | Charm |
| 66 | 15 | Shyness |

Additional socials:

- `socialId = 2122` is broadcast automatically on level-up; no client packet.
- Couple socials (`ExAskCoupleAction`) are requested via action ids 71, 72, 73 — see [§ 9.1](#91-core-player-actions-074).

## 12. Client default F-key bindings

These are the HighFive client defaults — informational only; users can rebind them and server only sees the resulting packet.

| Key | Default binding |
| --- | --- |
| F1 | Help — open the in-game help window (client-local, no packet) |
| F2 | Attack — action id 16 (Pet Attack) or generic attack on current target |
| F3 | Target Next Enemy — client-local target cycling, then sends Action 0x1F |
| F4 | Target Self — client-local, then sends Action 0x1F on own objectId |
| F5 | Pick Up — client sends Action 0x1F on nearest drop |
| F6 | Sit / Stand — RequestActionUse 0x56 action id 0 |
| F7 | Walk / Run — RequestActionUse 0x56 action id 1 |
| F8 | Assist — target the target of current target (client-local, then Action) |
| F9 | Party Info — client-local UI toggle |
| F10 | Main Menu — client-local UI toggle |
| F11 | Inventory — client-local UI toggle |
| F12 | Communication — client-local UI toggle |

Common additional hotkeys that translate into the packets above:

- `Space` / dedicated Attack key → `AttackRequest 0x32` on current target.
- `Tab` → Target Next Enemy (client-local cycling + `Action 0x1F`).
- `Ctrl+Tab` → Target Next Party Member.
- `Shift+click` on a target → `Action 0x1F` with `actionId = 1` (info panel) or `AttackRequest 0x32` with forced flag, depending on target.
- `Ctrl+click` on a skill → `RequestMagicSkillUse 0x39` with `ctrlPressed = 1` (force on non-hostile).
- `Esc` → `RequestTargetCancel 0x48`.
- `Sit` / `Run` toggles → `RequestActionUse 0x56` action ids `0` / `1`.
- `Pick up` (default `F5`) → `Action 0x1F` on nearest on-ground item's objectId.

## 13. Regeneration

Tables in [§ 9.1](#91-core-player-actions-074), [§ 9.2](#92-summon-skill-actions-10001098), [§ 9.3](#93-ancient--event-summon-actions-50005015), and [§ 9.4](#94-actions_on_transform-allow-list-while-transformed) are extracted from the L2JMobius server source by [`scripts/gen_actions_doc.py`](../scripts/gen_actions_doc.py). Regenerate after bumping the server submodule:

```
python scripts/gen_actions_doc.py --server c:\MyProg\l2J-Mobius-CT-2.6-HighFive --out docs\ACTIONS.md
```

