# Races and Classes (HighFive)

## Overview

Complete enumeration of playable races, every `classId` the server knows, the profession-change tree, and the per-class base stats & growth curves that the client relies on to interpret `CharInfo` / `UserInfo` / `CharacterCreate` packets.

- **Scope:** live playable classes only. NPC, pet, and summon races/classes are out of scope.
- **Regenerate with:** `python scripts/gen_races_classes_doc.py`. Output is deterministic.
- **Related:** equip rules & paperdoll / inventory caps in [INVENTORY.md](INVENTORY.md); skill trees in [SKILLS.md](SKILLS.md); items in [ITEMS.md](ITEMS.md).

### Gotchas

- Class-change gates: tier 1 → tier 2 at **level 20**, tier 2 → tier 3 at **level 40**, tier 3 (noblesse awaken) at **level 76**. Level cap is **85**.
- **Kamael** have *no mage or priest classes* — all Kamael classes are fighters.
- **Kamael are gender-locked** at character creation: male soldiers (123) can only become Trooper / Male Soul Breaker / Male Soul Hound / Berserker / Doombringer; females (124) → Warder / Female Soul Breaker / Female Soul Hound / Arbalester / Trickster / Inspector / Judicator. No cross-gender advancement.
- **Dwarf inventory** starts at **100 slots**; all other races at **80**. Quest items use a separate 100-slot bucket. GM accounts have 250. All limits extendable by the `INV_LIM` stat (belts, etc.) — report via `ExStorageMaxCount` (0xFE 0x2F).
- Collision radius & height in `UserInfo` / `CharInfo` are gender-specific — use `collisionMale` vs `collisionFemale` from the template.
- 1st-class templates exist for a class, but a character at level 1 uses the root (Starting) template curve until the first class change at L20.

## Races

| Race | Starting classIds | Inventory slots | Notes |
|------|-------------------|----------------:|-------|
| Human | 0, 10 | 80 | Both fighter and mage lines. Most versatile race. |
| Elf | 18, 25 | 80 | Balanced. Higher DEX/WIT; lower CON/STR. |
| Dark Elf | 31, 38 | 80 | Highest offensive stats; lowest HP. |
| Orc | 44, 49 | 80 | Fighter-oriented; highest STR/CON. Mage line exists (shaman) but spell list is limited. |
| Dwarf | 53 | 100 | Fighter-only. **100 inventory slots**. Unique craft (Warsmith) & spoil (Bounty Hunter) lines. |
| Kamael | 123, 124 | 80 | Introduced in CT 2.3. Fighter-only; gender-locked classes. Cannot use bows — uses crossbows/rapiers instead. |

Inventory-slot constants (NoDwarf=80, Dwarf=100, GM=250, Quest=100) — full detail in [INVENTORY.md § Capacity model](INVENTORY.md#capacity-model).

## Class hierarchy

Total classes: **103**. One table per race, sorted by `classId`.

### Human (29 classes)

| classId | Class | Parent | Tier | Type |
|--------:|-------|--------|------|------|
| 0 | Human Fighter | — | Starting | Fighter |
| 1 | Warrior | 0 (Human Fighter) | 1st | Fighter |
| 2 | Gladiator | 1 (Warrior) | 2nd | Fighter |
| 3 | Warlord | 1 (Warrior) | 2nd | Fighter |
| 4 | Human Knight | 0 (Human Fighter) | 1st | Fighter |
| 5 | Paladin | 4 (Human Knight) | 2nd | Fighter |
| 6 | Dark Avenger | 4 (Human Knight) | 2nd | Fighter |
| 7 | Rogue | 0 (Human Fighter) | 1st | Fighter |
| 8 | Treasure Hunter | 7 (Rogue) | 2nd | Fighter |
| 9 | Hawkeye | 7 (Rogue) | 2nd | Fighter |
| 10 | Human Mystic | — | Starting | Mage |
| 11 | Human Wizard | 10 (Human Mystic) | 1st | Mage |
| 12 | Sorcerer | 11 (Human Wizard) | 2nd | Mage |
| 13 | Necromancer | 11 (Human Wizard) | 2nd | Mage |
| 14 | Warlock | 11 (Human Wizard) | 2nd | Summoner |
| 15 | Cleric | 10 (Human Mystic) | 1st | Mage |
| 16 | Bishop | 15 (Cleric) | 2nd | Mage |
| 17 | Prophet | 15 (Cleric) | 2nd | Mage |
| 88 | Duelist | 2 (Gladiator) | 3rd | Fighter |
| 89 | Dreadnought | 3 (Warlord) | 3rd | Fighter |
| 90 | Phoenix Knight | 5 (Paladin) | 3rd | Fighter |
| 91 | Hell Knight | 6 (Dark Avenger) | 3rd | Fighter |
| 92 | Sagittarius | 9 (Hawkeye) | 3rd | Fighter |
| 93 | Adventurer | 8 (Treasure Hunter) | 3rd | Fighter |
| 94 | Archmage | 12 (Sorcerer) | 3rd | Mage |
| 95 | Soultaker | 13 (Necromancer) | 3rd | Mage |
| 96 | Arcana Lord | 14 (Warlock) | 3rd | Summoner |
| 97 | Cardinal | 16 (Bishop) | 3rd | Mage |
| 98 | Hierophant | 17 (Prophet) | 3rd | Mage |

### Elf (20 classes)

| classId | Class | Parent | Tier | Type |
|--------:|-------|--------|------|------|
| 18 | Elven Fighter | — | Starting | Fighter |
| 19 | Elven Knight | 18 (Elven Fighter) | 1st | Fighter |
| 20 | Temple Knight | 19 (Elven Knight) | 2nd | Fighter |
| 21 | Sword Singer | 19 (Elven Knight) | 2nd | Fighter |
| 22 | Elven Scout | 18 (Elven Fighter) | 1st | Fighter |
| 23 | Plains Walker | 22 (Elven Scout) | 2nd | Fighter |
| 24 | Silver Ranger | 22 (Elven Scout) | 2nd | Fighter |
| 25 | Elven Mystic | — | Starting | Mage |
| 26 | Elven Wizard | 25 (Elven Mystic) | 1st | Mage |
| 27 | Spellsinger | 26 (Elven Wizard) | 2nd | Mage |
| 28 | Elemental Summoner | 26 (Elven Wizard) | 2nd | Summoner |
| 29 | Elven Oracle | 25 (Elven Mystic) | 1st | Mage |
| 30 | Elven Elder | 29 (Elven Oracle) | 2nd | Mage |
| 99 | Eva's Templar | 20 (Temple Knight) | 3rd | Fighter |
| 100 | Sword Muse | 21 (Sword Singer) | 3rd | Fighter |
| 101 | Wind Rider | 23 (Plains Walker) | 3rd | Fighter |
| 102 | Moonlight Sentinel | 24 (Silver Ranger) | 3rd | Fighter |
| 103 | Mystic Muse | 27 (Spellsinger) | 3rd | Mage |
| 104 | Elemental Master | 26 (Elven Wizard) | 3rd | Summoner |
| 105 | Eva's Saint | 30 (Elven Elder) | 3rd | Mage |

### Dark Elf (20 classes)

| classId | Class | Parent | Tier | Type |
|--------:|-------|--------|------|------|
| 31 | Dark Fighter | — | Starting | Fighter |
| 32 | Palus Knight | 31 (Dark Fighter) | 1st | Fighter |
| 33 | Shillien Knight | 32 (Palus Knight) | 2nd | Fighter |
| 34 | Bladedancer | 33 (Shillien Knight) | 2nd | Fighter |
| 35 | Assassin | 31 (Dark Fighter) | 1st | Fighter |
| 36 | Abyss Walker | 35 (Assassin) | 2nd | Fighter |
| 37 | Phantom Ranger | 35 (Assassin) | 2nd | Fighter |
| 38 | Dark Mystic | — | Starting | Mage |
| 39 | Dark Wizard | 38 (Dark Mystic) | 1st | Mage |
| 40 | Spellhowler | 39 (Dark Wizard) | 2nd | Mage |
| 41 | Phantom Summoner | 39 (Dark Wizard) | 2nd | Summoner |
| 42 | Shillien Oracle | 38 (Dark Mystic) | 1st | Mage |
| 43 | Shillien Elder | 42 (Shillien Oracle) | 2nd | Mage |
| 106 | Shillien Templar | 33 (Shillien Knight) | 3rd | Fighter |
| 107 | Spectral Dancer | 34 (Bladedancer) | 3rd | Fighter |
| 108 | Ghost Hunter | 36 (Abyss Walker) | 3rd | Fighter |
| 109 | Ghost Sentinel | 37 (Phantom Ranger) | 3rd | Fighter |
| 110 | Storm Screamer | 40 (Spellhowler) | 3rd | Mage |
| 111 | Spectral Master | 41 (Phantom Summoner) | 3rd | Summoner |
| 112 | Shillien Saint | 43 (Shillien Elder) | 3rd | Mage |

### Orc (13 classes)

| classId | Class | Parent | Tier | Type |
|--------:|-------|--------|------|------|
| 44 | Orc Fighter | — | Starting | Fighter |
| 45 | Orc Raider | 44 (Orc Fighter) | 1st | Fighter |
| 46 | Destroyer | 45 (Orc Raider) | 2nd | Fighter |
| 47 | Monk | 44 (Orc Fighter) | 1st | Fighter |
| 48 | Tyrant | 47 (Monk) | 2nd | Fighter |
| 49 | Orc Mystic | — | Starting | Mage |
| 50 | Orc Shaman | 49 (Orc Mystic) | 1st | Mage |
| 51 | Overlord | 50 (Orc Shaman) | 2nd | Mage |
| 52 | Warcryer | 50 (Orc Shaman) | 2nd | Mage |
| 113 | Titan | 46 (Destroyer) | 3rd | Fighter |
| 114 | Grand Khavatari | 48 (Tyrant) | 3rd | Fighter |
| 115 | Dominator | 51 (Overlord) | 3rd | Mage |
| 116 | Doom Cryer | 52 (Warcryer) | 3rd | Mage |

### Dwarf (7 classes)

| classId | Class | Parent | Tier | Type |
|--------:|-------|--------|------|------|
| 53 | Dwarf Fighter | — | Starting | Fighter |
| 54 | Scavenger | 53 (Dwarf Fighter) | 1st | Fighter |
| 55 | Bounty Hunter | 54 (Scavenger) | 2nd | Fighter |
| 56 | Artisan | 53 (Dwarf Fighter) | 1st | Fighter |
| 57 | Warsmith | 56 (Artisan) | 2nd | Fighter |
| 117 | Fortune Seeker | 55 (Bounty Hunter) | 3rd | Fighter |
| 118 | Maestro | 57 (Warsmith) | 3rd | Fighter |

### Kamael (14 classes)

| classId | Class | Parent | Tier | Type |
|--------:|-------|--------|------|------|
| 123 | Male Kamael Soldier | — | Starting | Fighter |
| 124 | Female Kamael Soldier | — | Starting | Fighter |
| 125 | Trooper | 123 (Male Kamael Soldier) | 1st | Fighter |
| 126 | Warder | 124 (Female Kamael Soldier) | 1st | Fighter |
| 127 | Berserker | 125 (Trooper) | 2nd | Fighter |
| 128 | Male Soul Breaker | 125 (Trooper) | 2nd | Fighter |
| 129 | Female Soul Breaker | 126 (Warder) | 2nd | Fighter |
| 130 | Arbalester | 126 (Warder) | 2nd | Fighter |
| 131 | Doombringer | 127 (Berserker) | 3rd | Fighter |
| 132 | Male Soul Hound | 128 (Male Soul Breaker) | 3rd | Fighter |
| 133 | Female Soul Hound | 129 (Female Soul Breaker) | 3rd | Fighter |
| 134 | Trickster | 130 (Arbalester) | 3rd | Fighter |
| 135 | Inspector | 126 (Warder) | 2nd | Fighter |
| 136 | Judicator | 135 (Inspector) | 3rd | Fighter |

## Starting-class base stats (level 1)

The 11 root templates every character is created from. These values feed directly into the initial `UserInfo` packet.

| Id | Class | STR | DEX | CON | INT | WIT | MEN | HP | MP | CP | HPreg | MPreg | CPreg | pAtk | mAtk | atkSpd | walk | run | col♂ r/h | col♀ r/h | spawns |
|---:|-------|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|
| 0 | Human Fighter | 40 | 30 | 43 | 21 | 11 | 25 | 80 | 30 | 32 | 2 | 0.9 | 2 | 4 | 6 | 300 | 80 | 115 | 9/23 | 8/23.5 | 4 |
| 10 | Human Mystic | 22 | 21 | 27 | 41 | 20 | 39 | 101 | 40 | 50.5 | 2 | 0.9 | 2 | 3 | 6 | 300 | 78 | 120 | 7.5/22.8 | 6.5/22.5 | 4 |
| 18 | Elven Fighter | 36 | 35 | 36 | 23 | 14 | 26 | 89 | 30 | 35.6 | 2 | 0.9 | 2 | 4 | 6 | 300 | 90 | 125 | 7.5/24 | 7.5/23 | 6 |
| 25 | Elven Mystic | 21 | 24 | 25 | 37 | 23 | 40 | 104 | 40 | 52 | 2 | 0.9 | 2 | 3 | 6 | 300 | 85 | 122 | 7.5/24 | 7.5/23 | 6 |
| 31 | Dark Fighter | 41 | 34 | 32 | 25 | 12 | 26 | 94 | 30 | 37.6 | 2 | 0.9 | 2 | 4 | 6 | 300 | 85 | 122 | 7.5/24 | 7/23.5 | 6 |
| 38 | Dark Mystic | 23 | 23 | 24 | 44 | 19 | 37 | 106 | 40 | 53 | 2 | 0.9 | 2 | 3 | 6 | 300 | 85 | 122 | 7.5/24 | 7/23.5 | 6 |
| 44 | Orc Fighter | 40 | 26 | 47 | 18 | 12 | 27 | 80 | 30 | 40 | 2 | 0.9 | 2 | 4 | 6 | 300 | 70 | 117 | 11/28 | 7/27 | 6 |
| 49 | Orc Mystic | 27 | 24 | 31 | 31 | 15 | 42 | 95 | 40 | 47.5 | 2 | 0.9 | 2 | 3 | 6 | 300 | 70 | 121 | 7/27.5 | 8/25.5 | 6 |
| 53 | Dwarf Fighter | 39 | 29 | 45 | 20 | 10 | 27 | 80 | 30 | 56 | 2 | 0.9 | 2 | 4 | 6 | 300 | 80 | 115 | 9/18 | 5/19 | 6 |
| 123 | Male Kamael Soldier | 41 | 33 | 31 | 29 | 11 | 25 | 95 | 30 | 47.5 | 2 | 0.9 | 2 | 4 | 6 | 300 | 87 | 122 | 8/25.2 | 8/25.2 | 6 |
| 124 | Female Kamael Soldier | 39 | 35 | 30 | 28 | 11 | 27 | 97 | 40 | 48.5 | 2 | 0.9 | 2 | 4 | 6 | 300 | 87 | 122 | 7/22.6 | 7/22.6 | 6 |

## Growth curve (HP / MP / CP)

Milestone levels only. Full per-level curves live in the template XMLs.

| Id | Class | L1 HP | L20 HP | L40 HP | L60 HP | L76 HP | L80 HP | L85 HP | L1 MP | L20 MP | L40 MP | L60 MP | L76 MP | L80 MP | L85 MP |
|---:|-------|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | Human Fighter | 80 | 327 | 637.7 | 1000.4 | 1328 | 1415.1 | 1526.9 | 30 | 144 | 287.4 | 454.8 | 606 | 646.2 | 697.8 |
| 10 | Human Mystic | 101 | 424 | 830.3 | 1304.6 | 1733 | 1846.9 | 1993.1 | 40 | 192 | 383.2 | 606.4 | 808 | 861.6 | 930.4 |
| 18 | Elven Fighter | 89 | 355 | 689.6 | 1080.2 | 1433 | 1526.8 | 1647.2 | 30 | 144 | 287.4 | 454.8 | 606 | 646.2 | 697.8 |
| 25 | Elven Mystic | 104 | 427 | 833.3 | 1307.6 | 1736 | 1849.9 | 1996.1 | 40 | 192 | 383.2 | 606.4 | 808 | 861.6 | 930.4 |
| 31 | Dark Fighter | 94 | 379 | 737.5 | 1156 | 1534 | 1634.5 | 1763.5 | 30 | 144 | 287.4 | 454.8 | 606 | 646.2 | 697.8 |
| 38 | Dark Mystic | 106 | 429 | 835.3 | 1309.6 | 1738 | 1851.9 | 1998.1 | 40 | 192 | 383.2 | 606.4 | 808 | 861.6 | 930.4 |
| 44 | Orc Fighter | 80 | 346 | 680.6 | 1071.2 | 1424 | 1517.8 | 1638.2 | 30 | 144 | 287.4 | 454.8 | 606 | 646.2 | 697.8 |
| 49 | Orc Mystic | 95 | 418 | 824.3 | 1298.6 | 1727 | 1840.9 | 1987.1 | 40 | 192 | 383.2 | 606.4 | 808 | 861.6 | 930.4 |
| 53 | Dwarf Fighter | 80 | 346 | 680.6 | 1071.2 | 1424 | 1517.8 | 1638.2 | 30 | 144 | 287.4 | 454.8 | 606 | 646.2 | 697.8 |
| 123 | Male Kamael Soldier | 95 | 380 | 738.5 | 1157 | 1535 | 1635.5 | 1764.5 | 30 | 144 | 287.4 | 454.8 | 606 | 646.2 | 697.8 |
| 124 | Female Kamael Soldier | 97 | 439 | 869.2 | 1371.4 | 1825 | 1945.6 | 2100.4 | 40 | 192 | 383.2 | 606.4 | 808 | 861.6 | 930.4 |

## Starting equipment

One entry per root class. Items flagged `equipped=true` are placed on the paperdoll; everything else lands in the main inventory.

| classId | Class | Equipped on paperdoll | In inventory |
|--------:|-------|-----------------------|--------------|
| 0 | Human Fighter | 2369 Squire's Sword, 1146 Squire's Shirt, 1147 Squire's Pants | 10 Dagger, 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 10 | Human Mystic | 6 Apprentice's Wand, 425 Apprentice's Tunic, 461 Apprentice's Stockings | 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 18 | Elven Fighter | 2369 Squire's Sword, 1146 Squire's Shirt, 1147 Squire's Pants | 10 Dagger, 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 25 | Elven Mystic | 6 Apprentice's Wand, 425 Apprentice's Tunic, 461 Apprentice's Stockings | 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 31 | Dark Fighter | 2369 Squire's Sword, 1146 Squire's Shirt, 1147 Squire's Pants | 10 Dagger, 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 38 | Dark Mystic | 6 Apprentice's Wand, 425 Apprentice's Tunic, 461 Apprentice's Stockings | 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 44 | Orc Fighter | 2368 Training Gloves, 1146 Squire's Shirt, 1147 Squire's Pants | 2369 Squire's Sword, 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 49 | Orc Mystic | 2368 Training Gloves, 425 Apprentice's Tunic, 461 Apprentice's Stockings | 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 53 | Dwarf Fighter | 2370 Guild Member's Club, 1146 Squire's Shirt, 1147 Squire's Pants | 10 Dagger, 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 123 | Male Kamael Soldier | 2369 Squire's Sword, 1146 Squire's Shirt, 1147 Squire's Pants | 10 Dagger, 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |
| 124 | Female Kamael Soldier | 2369 Squire's Sword, 1146 Squire's Shirt, 1147 Squire's Pants | 10 Dagger, 5588 Tutorial Guide, 10650 Adventurer's Scroll of Escape ×5, 12753 Kamael Village Teleportation Scroll ×10 |

## Experience table (milestones)

Shared across every class. The `tolevel` value is the **cumulative XP at which the player reaches that level** (exp needed to hit L2 = tolevel of L2).

| Level | Cumulative XP (tolevel) |
|------:|-------------------------|
| 2 | 68 |
| 10 | 48,229 |
| 20 | 835,862 |
| 40 | 15,422,929 |
| 60 | 126,509,653 |
| 76 | 931,275,828 |
| 80 | 3,075,966,164 |
| 85 | 13,180,481,103 |

Server-defined level cap: **85** (the XP table contains rows up to level 87 for interpolation, but the server will not grant XP beyond the cap).

## Profession-change gates

| From tier | To tier | Required level | Notes |
|-----------|---------|---------------:|-------|
| Starting (root) | 1st | 20 | First occupation choice at Village Master. |
| 1st | 2nd | 40 | Requires second-class quest completion. |
| 2nd | 3rd | 76 | Requires noblesse awakening (3rd-class quest). |

## Pet-capable (summoner) classes

Summoner classIds: 14 (Warlock), 28 (Elemental Summoner), 41 (Phantom Summoner), 96 (Arcana Lord), 104 (Elemental Master), 111 (Spectral Master).

These classes maintain a servitor pet; `NpcInfo` frames for the servitor share the channel with the owner's packets and must be routed separately.

