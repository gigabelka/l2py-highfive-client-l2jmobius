# Lineage 2 HighFive — Character Inventory Specification

**Chronicle:** HighFive
**Server flavor:** L2J Mobius (CT 2.6 HighFive)
**Scope:** the character's personal inventory — the items a player carries and equips on their own body. This document covers the **paperdoll** (every slot on the character model), the **equippable item catalogue** (weapons, armor, accessories), **adena**, the on‑wire layout of a single item record, and the narrow set of client↔server packets that list / use / equip / unequip / drop / destroy items belonging to the character.

Explicitly **out of scope** (covered elsewhere or intentionally not documented here): warehouse and clan warehouse, freight / mail, pet inventory, trade window, private stores, quest items, recipe books.

This complements [PROTOCOL.md](PROTOCOL.md) (framing, primitives, handshake), [CONSTANTS.md](CONSTANTS.md) (opcode tables), and [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md) (game XOR cipher). Server file paths (`c:\MyProg\l2J-Mobius-CT-2.6-HighFive\`) are cited for cross‑checking only. All integer fields are little‑endian; see [PROTOCOL.md — Common primitives](PROTOCOL.md#common-primitives) for `u8`/`u16`/`u32`/`u64` definitions.

---

## Overview

The character inventory is a single flat list of `Item` instances owned by the player. Equipping an item moves it from the "free" part of the inventory onto one of the 25 **paperdoll** slots; unequipping moves it back. The inventory itself remains the storage — paperdoll slots are just indexes into the same container.

Inventory model (server):

```
PlayerInventory  (extends Inventory, ItemContainer)
├── free items        ← carried but not worn
├── paperdoll[25]     ← one reference per slot, may be null
└── adena / ancient-adena fast-access fields
```

`Player.getInventory()` returns a `PlayerInventory`; every item the character owns passes through it. Equip/unequip is an in‑place pointer move between the `_paperdoll[]` array and the free list — no new `objectId` is ever assigned.

Source: [Inventory.java](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/itemcontainer/Inventory.java), [PlayerInventory.java](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/itemcontainer/PlayerInventory.java).

---

## Capacity, weight, adena

Capacity is expressed in *slots*, not weight; weight is tracked separately and only affects movement speed. Defaults from [PlayerConfig.java:125-132, 205, 380-383, 492](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/config/PlayerConfig.java):

| Config key | Default | Applies to |
|---|---:|---|
| `MaximumSlotsForNoDwarf` | `80` | Inventory slots — Human / Elf / Dark Elf / Orc / Kamael |
| `MaximumSlotsForDwarf` | `100` | Inventory slots — Dwarf |
| `MaximumSlotsForGMPlayer` | `250` | Inventory slots — GM accounts |
| `MaximumSlotsForQuestItems` | `100` | Quest item bucket (separate — not used here) |
| `MaxAdena` | `99 900 000 000` | Adena hard cap; negative ⇒ `Long.MAX_VALUE` |

At runtime the effective inventory cap is extended by `Stat.INV_LIM` (e.g. `+8` from an equipped belt) and reported to the client via `ExStorageMaxCount` (see below).

Weight:

| Constant | Value | Source |
|---|---:|---|
| `MAX_ARMOR_WEIGHT` | `12 000` | `Inventory.MAX_ARMOR_WEIGHT` — soft threshold for the movement‑speed penalty |

Adena (and its Kamaloka counterpart, Ancient Adena) are ordinary stackable items with fixed template ids, but the server caches them as dedicated fields inside `PlayerInventory` for O(1) lookup:

| Concept | Item id | Notes |
|---|---:|---|
| Adena | `57` | `Inventory.ADENA_ID` — universal currency |
| Ancient Adena | `5575` | `Inventory.ANCIENT_ADENA_ID` — Kamaloka / Seven Signs currency |

---

## Paperdoll slots

The character model has **25** equipment positions, numbered `0..24`. The index itself appears on the wire as the `location` field of any equipped item (see [On‑wire item record](#onwire-item-record)). From [Inventory.java:80-105](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/itemcontainer/Inventory.java).

| Index | Constant | Slot | What goes here |
|------:|---|---|---|
| 0 | `PAPERDOLL_UNDER` | Under | Shirt / underwear |
| 1 | `PAPERDOLL_HEAD` | Head | Helmet / circlet / hat |
| 2 | `PAPERDOLL_HAIR` | Hair | Hair accessory 1 (ribbon, headband) |
| 3 | `PAPERDOLL_HAIR2` | Hair 2 | Hair accessory 2 (earrings‑style, worn together with slot 2) |
| 4 | `PAPERDOLL_NECK` | Neck | Necklace |
| 5 | `PAPERDOLL_RHAND` | Right hand | Weapon (one‑handed or two‑handed — see [Two‑handed rule](#two-handed-weapons-and-full-armor)) |
| 6 | `PAPERDOLL_CHEST` | Chest | Chest armor, full armor, or all‑dress |
| 7 | `PAPERDOLL_LHAND` | Left hand | Shield, sigil, arrows, or bolts (mutually exclusive with a two‑handed weapon) |
| 8 | `PAPERDOLL_REAR` | Right ear | Earring |
| 9 | `PAPERDOLL_LEAR` | Left ear | Earring |
| 10 | `PAPERDOLL_GLOVES` | Gloves | Gloves |
| 11 | `PAPERDOLL_LEGS` | Legs | Leggings (cleared when a full‑armor chestpiece is equipped) |
| 12 | `PAPERDOLL_FEET` | Feet | Boots |
| 13 | `PAPERDOLL_RFINGER` | Right finger | Ring |
| 14 | `PAPERDOLL_LFINGER` | Left finger | Ring |
| 15 | `PAPERDOLL_LBRACELET` | Left wrist | Bracelet |
| 16 | `PAPERDOLL_RBRACELET` | Right wrist | Talisman‑carrying bracelet — determines how many `DECO*` slots are usable |
| 17 | `PAPERDOLL_DECO1` | Talisman 1 | Talisman — enabled only if the R_BRACELET template exposes ≥ 1 talisman slot |
| 18 | `PAPERDOLL_DECO2` | Talisman 2 | same, ≥ 2 |
| 19 | `PAPERDOLL_DECO3` | Talisman 3 | same, ≥ 3 |
| 20 | `PAPERDOLL_DECO4` | Talisman 4 | same, ≥ 4 |
| 21 | `PAPERDOLL_DECO5` | Talisman 5 | same, ≥ 5 |
| 22 | `PAPERDOLL_DECO6` | Talisman 6 | same, ≥ 6 |
| 23 | `PAPERDOLL_CLOAK` | Back | Cloak |
| 24 | `PAPERDOLL_BELT` | Waist | Belt (often also extends `INV_LIM`) |
| — | `PAPERDOLL_TOTALSLOTS = 25` | — | |

All 25 slots are available to **every playable class of every race** — the layout is race/class‑independent. What differs between classes is only *which* templates pass the equip checks (see [Per‑class equipability](#perclass-equipability)).

### Slot‑group interactions

Some templates cover more than one slot conceptually. The server represents this as a single paperdoll entry plus forced clears of the shadowed slots:

| Template kind | Primary slot | Clears on equip |
|---|---|---|
| One‑handed weapon (`R_HAND`) | 5 RHAND | — |
| Two‑handed weapon / bow / polearm (`LR_HAND`) | 5 RHAND | 7 LHAND |
| Shield / sigil / arrows / bolts (`L_HAND`) | 7 LHAND | — |
| Chest armor (`CHEST`) | 6 CHEST | — |
| Full armor (`FULL_ARMOR`) | 6 CHEST | 11 LEGS |
| All‑dress (`ALLDRESS`, formal wear) | 6 CHEST | 1 HEAD, 10 GLOVES, 11 LEGS, 12 FEET |
| Two‑slot hair (`HAIRALL`) | 2 HAIR | 3 HAIR2 |

When such an item is equipped, the `InventoryUpdate (0x21)` sent to the client carries one `MODIFIED` record per affected slot (the newly equipped item + all unequipped items that had to make room).

---

## Body‑part bitmasks

Every item template carries a single `bodyPart` bitmask — the `u32` written into the on‑wire item record tells the client which slot (or slot group) this item belongs to. From [BodyPart.java:35-72](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/item/enums/BodyPart.java).

| Mask (hex) | Name | Paperdoll target |
|---:|---|---|
| `0x0000` | `NONE` | not equippable (adena, etc.) |
| `0x0001` | `UNDERWEAR` | 0 UNDER |
| `0x0002` | `R_EAR` | 8 REAR |
| `0x0004` | `L_EAR` | 9 LEAR |
| `0x0006` | `LR_EAR` | first free of {8, 9} |
| `0x0008` | `NECK` | 4 NECK |
| `0x0010` | `R_FINGER` | 13 RFINGER |
| `0x0020` | `L_FINGER` | 14 LFINGER |
| `0x0030` | `LR_FINGER` | first free of {13, 14} |
| `0x0040` | `HEAD` | 1 HEAD |
| `0x0080` | `R_HAND` | 5 RHAND |
| `0x0100` | `L_HAND` | 7 LHAND |
| `0x0200` | `GLOVES` | 10 GLOVES |
| `0x0400` | `CHEST` | 6 CHEST |
| `0x0800` | `LEGS` | 11 LEGS |
| `0x1000` | `FEET` | 12 FEET |
| `0x2000` | `BACK` | 23 CLOAK |
| `0x4000` | `LR_HAND` | 5 RHAND (clears 7 LHAND) |
| `0x8000` | `FULL_ARMOR` | 6 CHEST (clears 11 LEGS) |
| `0x010000` | `HAIR` | 2 HAIR |
| `0x020000` | `ALLDRESS` | 6 CHEST (clears HEAD/GLOVES/LEGS/FEET) |
| `0x040000` | `HAIR2` | 3 HAIR2 |
| `0x080000` | `HAIRALL` | 2 HAIR (clears 3 HAIR2) |
| `0x100000` | `R_BRACELET` | 16 RBRACELET |
| `0x200000` | `L_BRACELET` | 15 LBRACELET |
| `0x400000` | `DECO` | first free of {17..22} |
| `0x10000000` | `BELT` | 24 BELT |

Pet body‑part values (negative ids `-100..-104` — `WOLF`, `HATCHLING`, `STRIDER`, `BABYPET`, `GREATWOLF`) are **not character inventory**, only referenced here for completeness. They never equip onto a character paperdoll.

Resolution of combo masks is centralised in `BodyPart.getPaperdollIndex()` at [BodyPart.java:142-164](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/item/enums/BodyPart.java).

---

## Item categories

What a character can wear / hold splits into three top‑level families:

- **Weapons** — equip into RHAND (or RHAND+LHAND for two‑handers). See [WeaponType](#weapon-subtype-weapontype).
- **Armor** — equip into UNDER/HEAD/CHEST/LEGS/GLOVES/FEET/CLOAK, plus shields/sigils into LHAND. See [ArmorType](#armor-subtype-armortype).
- **Accessories** — jewelry: necklace, earrings, rings, bracelets, talismans.

Each item template has two coarse type numbers that are sent on the wire (`type2`) or used only server‑side (`type1`):

### `type1` — top‑level category (from [ItemTemplate.java:67-69](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/item/ItemTemplate.java))

| Value | Name | Items |
|---:|---|---|
| `0` | `TYPE1_WEAPON_RING_EARRING_NECKLACE` | Weapons and jewelry (neck/earring/ring) |
| `1` | `TYPE1_SHIELD_ARMOR` | Shields and body armor |
| `4` | `TYPE1_ITEM_QUESTITEM_ADENA` | Etc items, adena, quest items |

### `type2` — subcategory (written into the on‑wire item record, [ItemTemplate.java:71-76](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/item/ItemTemplate.java))

| Value | Name | Typical content |
|---:|---|---|
| `0` | `TYPE2_WEAPON` | Weapons |
| `1` | `TYPE2_SHIELD_ARMOR` | Shields, armor |
| `2` | `TYPE2_ACCESSORY` | Necklace, earring, ring, bracelet, talisman |
| `3` | `TYPE2_QUEST` | (quest — out of scope here) |
| `4` | `TYPE2_MONEY` | Adena, Ancient Adena |
| `5` | `TYPE2_OTHER` | Potions, shots, consumables (not equippable — but can be *used*) |

### Weapon subtype (`WeaponType`)

From [WeaponType.java:25-43](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/item/type/WeaponType.java). Two‑handed subtypes are marked with `(LR_HAND)`.

| Name | Notes |
|---|---|
| `SWORD` | One or two‑handed sword |
| `BLUNT` | Mace / hammer |
| `DAGGER` | One‑handed dagger |
| `BOW` | Two‑handed, ranged *(LR_HAND)*, consumes arrows in LHAND |
| `POLE` | Polearm *(LR_HAND)* |
| `NONE` | Fist / no‑weapon marker |
| `DUAL` | Dual swords *(LR_HAND)* |
| `ETC` | Non‑combat tool |
| `FIST` | Knuckles |
| `DUALFIST` | Dual knuckles *(LR_HAND)* |
| `FISHINGROD` | Fishing rod *(LR_HAND)* — consumes lures in LHAND |
| `RAPIER` | Kamael‑only one‑handed |
| `ANCIENTSWORD` | Kamael‑only two‑handed *(LR_HAND)* |
| `CROSSBOW` | Kamael‑only *(LR_HAND)*, consumes bolts in LHAND |
| `FLAG` | Combat flag (siege only) |
| `OWNTHING` | Placeholder |
| `DUALDAGGER` | Dual daggers *(LR_HAND)* |

### Armor subtype (`ArmorType`)

From [ArmorType.java](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/item/type/ArmorType.java).

| Name | Notes |
|---|---|
| `NONE` | Robe‑less accessories / underwear |
| `LIGHT` | Light armor (daggers, rogues, light‑armor warriors) |
| `HEAVY` | Heavy armor (knights, warlords) — forbidden for Kamael |
| `MAGIC` | Robe (mages, healers) — forbidden for Kamael |
| `SIGIL` | Magic off‑hand for nukers — goes into LHAND |
| `SHIELD` | Physical off‑hand — goes into LHAND |

### Crystal grade (`CrystalType`)

The equipment grade badge and crystallisation yield. From [CrystalType.java:23-32](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/item/type/CrystalType.java).

| Grade | Level | Crystal item id |
|---|---:|---:|
| `NONE` | 0 | — |
| `D` | 1 | 1458 |
| `C` | 2 | 1459 |
| `B` | 3 | 1460 |
| `A` | 4 | 1461 |
| `S` | 5 | 1462 |
| `S80` | 6 | 1462 |
| `S84` | 7 | 1462 |

---

## Per‑class equipability

The paperdoll layout is identical across every class; the **equip checks** in `UseItem` differ only by race and by class‑category (fighter / mystic). The authoritative logic is in [UseItem.java:219-314](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/clientpackets/UseItem.java).

Hard rules enforced server‑side:

| Race | Forbidden | Exclusive |
|---|---|---|
| Kamael | `ArmorType.HEAVY`, `ArmorType.MAGIC`, `WeaponType.NONE` (fists as a weapon class) | `WeaponType.RAPIER`, `WeaponType.ANCIENTSWORD`, `WeaponType.CROSSBOW` |
| Human / Dwarf / Elf / Dark Elf / Orc | `WeaponType.RAPIER`, `WeaponType.ANCIENTSWORD`, `WeaponType.CROSSBOW` | `HEAVY` / `LIGHT` / `MAGIC` armor all allowed (subject to class fit) |

Soft rules (template‑level — mostly driven by XML `<cond>` blocks, not the wire): each weapon/armor template declares min class id, min level, and allowed sub‑classes. The client does *not* see these conditions directly — it only sees the equip result. A successful `UseItem` produces `InventoryUpdate (0x21)` with the newly equipped record flipping `isEquipped` to `1`; a rejection produces a `SystemMessage` (e.g. `YOU_DO_NOT_MEET_THE_REQUIRED_CONDITION_TO_EQUIP_THAT_ITEM`) and no inventory update.

### Talisman slots

The number of active DECO slots is `0` by default and only grows when a talisman‑carrying bracelet is equipped into `PAPERDOLL_RBRACELET` (slot 16). The server computes this via `Inventory.getTalismanSlots()`; trying to equip a talisman when the count is `0` yields the standard "condition" rejection. Talisman slots are per‑character and apply to every class equally.

---

## On‑wire item record

Every character‑inventory packet (`ItemList`, `InventoryUpdate`, `ExQuestItemList`) emits one record per item through the same writer — `AbstractItemPacket.writeItem(ItemInfo, …)` at [AbstractItemPacket.java:55-71](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/serverpackets/AbstractItemPacket.java).

| Off. | Field | Type | Size | Notes |
|---:|---|---|---:|---|
| 0 | `objectId` | `u32` | 4 | Unique instance id; stable for the whole session. |
| 4 | `itemId` | `u32` | 4 | Template id (display id). |
| 8 | `location` | `u32` | 4 | Equipped items: paperdoll slot index (0..24). Free items: `0`. |
| 12 | `count` | `u64` | 8 | Stack count. Always `1` for non‑stackables. |
| 20 | `type2` | `u16` | 2 | See [type2](#type2--subcategory). |
| 22 | `customType1` | `u16` | 2 | Lottery / race‑ticket tag. Usually `0`. |
| 24 | `isEquipped` | `u16` | 2 | `0` = in bag, `1` = on paperdoll. |
| 26 | `bodyPart` | `u32` | 4 | Body‑part mask (see [Body‑part bitmasks](#bodypart-bitmasks)). |
| 30 | `enchantLevel` | `u16` | 2 | `+N`. |
| 32 | `customType2` | `u16` | 2 | Misc flag. Usually `0`. |
| 34 | `augmentationId` | `u32` | 4 | Combined augmentation id (`0` = not augmented). Low 16 bits = skill1, high 16 = skill2. |
| 38 | `mana` | `i32` | 4 | Shadow‑item remaining mana (`-1` = not a shadow item). |
| 42 | `time` | `i32` | 4 | Remaining lifetime in seconds, or the sentinel `-9999` for items with no time limit. |
| 46 | `attackElementType` | `i16` | 2 | `-2` = none. `0..5` = Fire / Water / Wind / Earth / Holy / Dark. |
| 48 | `attackElementPower` | `u16` | 2 | |
| 50 | `defElem[0..5]` | `u16[6]` | 12 | Elemental defense in the same order as attack type. |
| 62 | `enchantOption[0..N-1]` | `u16[N]` | `2N` | Augmentation / special‑enchant option list. `N` is determined by the item template — `0` for most, `3` for items that carry them. No count byte on the wire. |

**Fixed part:** 62 bytes. Total = `62 + 2 * N`.

Values come from `ItemInfo`, which snapshots the live `Item` at packet build time. See [ItemInfo.java:30-144](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/model/ItemInfo.java).

---

## Server → Client packets

Only the packets that carry the character's own inventory state are documented here. Warehouse, pet, trade, and auction packets are intentionally excluded.

### `ItemList` (opcode `0x11`)

Full character inventory snapshot (quest items filtered out). Sent on EnterWorld and whenever the server forces a resync. After sending it, the server also emits `ExQuestItemList` (out of scope). From [ItemList.java:51-72](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/serverpackets/ItemList.java).

| Off. | Field | Type | Notes |
|---:|---|---|---|
| 0 | `0x11` | `u8` | opcode |
| 1 | `showWindow` | `u16` | `1` = open the inventory window; `0` = silent refresh |
| 3 | `itemCount` | `u16` | |
| 5 | `items[itemCount]` | item record | see [On‑wire item record](#onwire-item-record) |
| — | inventory‑block trailer | | `u16 blockCount` (usually `0`); if > 0: `u8 mode` + `u32[blockCount] ids` |

### `InventoryUpdate` (opcode `0x21`)

Incremental delta — carries only the items whose state changed (equipped, unequipped, stack grew/shrank, item destroyed, etc.). Built via [InventoryUpdate.java](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/serverpackets/InventoryUpdate.java) / [AbstractInventoryUpdate.java:116-129](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/serverpackets/AbstractInventoryUpdate.java).

| Off. | Field | Type | Notes |
|---:|---|---|---|
| 0 | `0x21` | `u8` | opcode |
| 1 | `changeCount` | `u16` | |
| 3 | for each: `changeType` (`u16`) + item record | | |

Change types:

| Value | Name | Client action |
|---:|---|---|
| `1` | ADDED | Insert new record (match by `objectId`). |
| `2` | MODIFIED | Replace fields of existing record (e.g. `isEquipped` toggled, stack count changed). |
| `3` | REMOVED | Drop the record from the client‑side list. |

### `ExStorageMaxCount` (extended opcode `0xFE 0x2F`)

Per‑category caps for the client‑side slots indicator. Sent once shortly after `EnterWorld`. From [ExStorageMaxCount.java:54-67](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/serverpackets/ExStorageMaxCount.java).

Only two fields are relevant for *the character's inventory* itself — the rest belong to warehouse/store/recipe UIs and are listed for completeness:

| Off. | Field | Type | Relevant to character inventory |
|---:|---|---|---|
| 0 | `0xFE` | `u8` | header |
| 1 | `0x002F` | `u16` | header |
| 3 | `inventory` | `u32` | **yes** — base inventory cap (race‑ and GM‑dependent) |
| 7 | `warehouse` | `u32` | no |
| 11 | `clanWarehouse` | `u32` | no |
| 15 | `privateSellSlots` | `u32` | no |
| 19 | `privateBuySlots` | `u32` | no |
| 23 | `dwarfRecipeBook` | `u32` | no |
| 27 | `commonRecipeBook` | `u32` | no |
| 31 | `inventoryExtraSlots` | `u32` | **yes** — bonus from `Stat.INV_LIM` (belt etc.); effective cap = `inventory + inventoryExtraSlots` |
| 35 | `inventoryQuestItems` | `u32` | (quest bucket — out of scope) |

---

## Client → Server packets

Only the packets that the character uses to act on its **own** inventory.

### `UseItem` (opcode `0x19`)

The one request that covers both "use" and "equip/unequip". If the item is equippable, the server toggles its paperdoll state; otherwise the corresponding item handler runs (potion drink, scroll read, soulshot charge, etc.). From [UseItem.java:66-71](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/clientpackets/UseItem.java).

| Off. | Field | Type | Notes |
|---:|---|---|---|
| 0 | `0x19` | `u8` | opcode |
| 1 | `objectId` | `u32` | Item instance id from the inventory. |
| 5 | `ctrlPressed` | `u32` | Non‑zero ⇒ Ctrl held (bypasses a few client‑side nag dialogs). |

Reply: `InventoryUpdate (0x21)` on success, `SystemMessage` on rejection.

### `RequestUnEquipItem` (opcode `0x16`)

Vacate a specific paperdoll slot (used when the client wants to *explicitly* unequip rather than toggle). From [RequestUnEquipItem.java:42-47](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/clientpackets/RequestUnEquipItem.java).

| Off. | Field | Type | Notes |
|---:|---|---|---|
| 0 | `0x16` | `u8` | opcode |
| 1 | `paperdollSlot` | `u32` | Slot index (0..24). Server runs it through `BodyPart.fromPaperdollSlot`. |

Reply: `InventoryUpdate (0x21)`.

### `RequestDropItem` (opcode `0x17`)

Drop `count` of the item onto the ground at the given world coordinates. The server rejects drops further than 150 units in XY or ±50 in Z, drops of quest items, drops of augmented items, and drops in no‑drop zones. From [RequestDropItem.java:52-60](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/clientpackets/RequestDropItem.java).

| Off. | Field | Type | Notes |
|---:|---|---|---|
| 0 | `0x17` | `u8` | opcode |
| 1 | `objectId` | `u32` | |
| 5 | `count` | `u64` | Must be ≤ stack count; `1` for non‑stackables. |
| 13 | `x` | `i32` | |
| 17 | `y` | `i32` | |
| 21 | `z` | `i32` | |

Reply: `InventoryUpdate` plus a ground `SpawnItem (0x05)` / `DropItem (0x16)` for nearby observers (covered in [PROTOCOL.md](PROTOCOL.md)).

### `RequestDestroyItem` (opcode `0x60`)

Permanently destroy `count` of an item. If the item is currently equipped the server unequips it first (sending one `InventoryUpdate`), then destroys (another `InventoryUpdate`). From [RequestDestroyItem.java:48-53](../../l2J-Mobius-CT-2.6-HighFive/java/org/l2jmobius/gameserver/network/clientpackets/RequestDestroyItem.java).

| Off. | Field | Type | Notes |
|---:|---|---|---|
| 0 | `0x60` | `u8` | opcode |
| 1 | `objectId` | `u32` | |
| 5 | `count` | `u64` | |

### `RequestItemList` (opcode `0x14`)

Empty body. Asks the server to resend `ItemList`. Rarely needed — the server sends updates proactively.

| Off. | Field | Type |
|---:|---|---|
| 0 | `0x14` | `u8` |

---

## Gotchas

- **`location` depends on `isEquipped`.** For equipped items it is the paperdoll slot index; for free items it is `0`. Always read the two fields together.
- **`time = -9999` is a sentinel**, not a real duration. Anything ≥ `0` is remaining seconds on a shadow / time‑limited item.
- **`attackElementType = -2`** means "no attribute". The `defElem[6]` vector always has exactly 6 entries in fixed order: Fire, Water, Wind, Earth, Holy, Dark.
- **Enchant options are variable‑length with no on‑wire count.** The client must know the template's option count to parse the record. For character equipment this is `0` almost always and `3` for items with enchant bonuses — if you don't need enchant effects, you can treat the tail as the start of the next record only after confirming the template has `N = 0`.
- **Two‑handed and full‑armor equips fan out into multiple `MODIFIED` entries in a single `InventoryUpdate`** — one for the new item and one per slot it had to clear. Don't assume one change per packet.
- **`UseItem` is the single path for both equip and use.** There is no separate "equip" opcode. A pending cast or attack delays the equip — the server may reply only after the attack animation ends.
- **Unknown opcode must never drop the stream.** Inventory‑adjacent `Ex…` opcodes are version‑sensitive; log and skip, but keep advancing the game XOR key rotation (see [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md)).
- **Adena is just item `57`.** Receiving or spending adena appears in `InventoryUpdate` like any other stackable. The server enforces `MAX_ADENA` on the *server side* — a transaction that would overflow is rejected with a system message, not silently clamped.
- **The paperdoll layout is fixed at 25 slots for every class of every race.** Only the *contents* differ (race/class equip checks). Don't special‑case the layout per class.

---

## Client‑side implementation status (this repo)

As of this writing [`src/l2py/protocol/game/server_packets.py`](../src/l2py/protocol/game/server_packets.py) and [`src/l2py/protocol/game/client_packets.py`](../src/l2py/protocol/game/client_packets.py) contain only login / handshake / character‑selection packets. **None of the inventory packets above are implemented yet.** Suggested porting order:

1. `ItemList (0x11)` — establishes the on‑wire item record; everything else reuses it.
2. `InventoryUpdate (0x21)` — required for any reactive state.
3. `ExStorageMaxCount (0xFE 0x2F)` — needed to compute "bag full" correctly at runtime.
4. `UseItem (0x19)` + `RequestUnEquipItem (0x16)` — minimum equip control.
5. `RequestDestroyItem (0x60)`, `RequestDropItem (0x17)` — item disposal.

---

## Cross‑reference

- [PROTOCOL.md](PROTOCOL.md) — framing, primitives, non‑inventory packets (UserInfo, EnterWorld, etc.).
- [CONSTANTS.md](CONSTANTS.md) — opcode tables, system message ids.
- [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md) — game XOR cipher and per‑packet key rotation.
- [CHECKLIST.md](CHECKLIST.md) — porting checklist.

Server sources used (paths relative to `c:\MyProg\l2J-Mobius-CT-2.6-HighFive\java\`):

- `org/l2jmobius/gameserver/model/itemcontainer/{Inventory, PlayerInventory, ItemContainer}.java`
- `org/l2jmobius/gameserver/model/item/enums/BodyPart.java`
- `org/l2jmobius/gameserver/model/item/type/{WeaponType, ArmorType, CrystalType}.java`
- `org/l2jmobius/gameserver/model/item/instance/Item.java`
- `org/l2jmobius/gameserver/model/item/ItemTemplate.java`
- `org/l2jmobius/gameserver/model/ItemInfo.java`
- `org/l2jmobius/gameserver/network/serverpackets/{AbstractItemPacket, AbstractInventoryUpdate, ItemList, InventoryUpdate, ExStorageMaxCount}.java`
- `org/l2jmobius/gameserver/network/clientpackets/{UseItem, RequestUnEquipItem, RequestDropItem, RequestDestroyItem}.java`
- `org/l2jmobius/gameserver/config/PlayerConfig.java`
