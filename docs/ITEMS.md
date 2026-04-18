# Character Equipment & Money Catalogue (L2JMobius CT 2.6 HighFive)

## Overview

Every item that a character of any class can place into their personal inventory and — if applicable — wear on the paperdoll. Scope:

- **Money:** Adena, Ancient Adena.
- **Weapons:** every `type="Weapon"` template, grouped by `weapon_type`.
- **Armor:** every `type="Armor"` template that equips onto a body slot (chest / legs / gloves / feet / head / underwear / cloak) and full-armor / all-dress variants.
- **Off-hand:** shields and sigils (`bodypart=lhand`).
- **Jewelry & accessories:** necklace, earring, ring, bracelet, talisman, belt, hair.

Excluded: etc items (potions, shots, scrolls, recipes, materials, arrows/bolts, quest items), pet-only gear, and entries named `(Not In Use)`.

- **Source of truth:** `dist/game/data/stats/items/*.xml` in the L2JMobius CT 2.6 HighFive server tree.
- **Regenerate with:** `python scripts/gen_items_doc.py`. Output is deterministic.
- **Related:** paperdoll slot layout, equip rules, on-wire item record — see [INVENTORY.md](INVENTORY.md).

### Column meanings

| Column | Meaning |
|--------|---------|
| **Id** | Template id — value written into the `itemId` field of every on-wire item record. |
| **Name** | Display name as shipped by the server. |
| **Grade** | Crystal grade (`NONE` / `D` / `C` / `B` / `A` / `S` / `S80` / `S84`). |
| **Body** | `bodypart` attribute — target paperdoll slot (see [INVENTORY.md](INVENTORY.md)). |
| **Weight** | Item weight; summed into `Player.currentLoad`. |
| **pAtk / mAtk / Atk.Spd** | Weapon stats from the item template. |
| **pDef / mDef** | Armor / jewelry stats from the item template. |

## Money

| Id | Name | Template type | Notes |
|---:|------|---------------|-------|
| 57 | Adena | `EtcItem` | Universal currency; capped at `PlayerConfig.MAX_ADENA` (default 99 900 000 000). |
| 5575 | Ancient Adena | `EtcItem` | Kamaloka / Seven Signs currency. |

## Weapons (3893)

Grouped by `weapon_type`. Two-handed weapon types (`bodypart=lrhand`) occupy the RHAND slot and implicitly clear LHAND.

### SWORD (858)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1 | Short Sword | NONE | rhand | 1600 | 8 | 6 | 379 |
| 2 | Long Sword | NONE | rhand | 1560 | 24 | 17 | 379 |
| 3 | Broadsword | NONE | rhand | 1590 | 11 | 9 | 379 |
| 66 | Gladius | NONE | rhand | 1570 | 17 | 12 | 379 |
| 67 | Orcish Sword | NONE | rhand | 1570 | 17 | 12 | 379 |
| 68 | Falchion | NONE | rhand | 1530 | 31 | 21 | 379 |
| 120 | Sword of Reflection | NONE | rhand | 1550 | 24 | 17 | 379 |
| 121 | Sword of Watershadow | NONE | rhand | 1540 | 24 | 17 | 379 |
| 122 | Handmade Sword | NONE | rhand | 1570 | 17 | 12 | 379 |
| 738 | Sword of Solidarity | NONE | rhand | 1300 | 12 | 9 | 379 |
| 743 | Sword of Sentinel | NONE | rhand | 1300 | 14 | 11 | 379 |
| 975 | Blood Saber | NONE | rhand | 1450 | 14 | 11 | 379 |
| 981 | Red Sunset Sword | NONE | lrhand | 1300 | 16 | 10 | 325 |
| 1142 | Rusted Bronze Sword | NONE | rhand | 1400 | 18 | 21 | 379 |
| 1295 | Long Sword | NONE | rhand | 200 | 22 | 6 | 379 |
| 1296 | Gladius | NONE | rhand | 300 | 22 | 6 | 379 |
| 1297 | Bastard Sword | NONE | rhand | 400 | 22 | 6 | 379 |
| 1298 | Caliburs | NONE | rhand | 500 | 22 | 6 | 379 |
| 1333 | Brandish | NONE | lrhand | 2250 | 21 | 12 | 325 |
| 1510 | Butcher's Sword | NONE | rhand | 1450 | 13 | 10 | 379 |
| 2369 | Squire's Sword | NONE | rhand | 1600 | 6 | 5 | 379 |
| 2505 | Iron Canine | NONE | rhand | 100 |  |  | 277 |
| 2915 | Old Knight Sword | NONE | rhand | 3200 | 24 | 17 | 379 |
| 3027 | Old Knight Sword | NONE | lrhand | 2100 | 29 | 17 | 325 |
| 3029 | Sword of Binding | NONE | rhand | 1200 | 17 | 12 | 379 |
| 3439 | Shining Canine | NONE | rhand | 100 |  |  | 277 |
| 3902 | Ghost Canine | NONE | rhand | 100 |  |  | 277 |
| 3903 | Mithril Canine | NONE | rhand | 100 |  |  | 277 |
| 3904 | Sylvan Canine | NONE | rhand | 100 |  |  | 277 |
| 3905 | Orikarukon Canine | NONE | rhand | 100 |  |  | 277 |
| 3906 | Fang of Saltydog | NONE | rhand | 100 |  |  | 277 |
| 3907 | Fang of Cerberus | NONE | rhand | 100 |  |  | 277 |
| 3908 | Fang of Coyote | NONE | rhand | 100 |  |  | 277 |
| 3909 | Crystallized Ice Canine | NONE | rhand | 100 |  |  | 277 |
| 3910 | Fang of the Blue Wolf | NONE | rhand | 100 |  |  | 277 |
| 3911 | Fang of Fenrir | NONE | rhand | 100 |  |  | 277 |
| 3919 | Serpent Fang | NONE | rhand | 100 |  |  | 277 |
| 3920 | Viperbite | NONE | rhand | 100 |  |  | 277 |
| 3921 | Shadow Fang | NONE | rhand | 100 |  |  | 277 |
| 3922 | Alya Fang | NONE | rhand | 100 |  |  | 277 |
| 3923 | Torturer | NONE | rhand | 100 |  |  | 277 |
| 3924 | Unuk Alhay Fang | NONE | rhand | 100 |  |  | 277 |
| 3925 | Antiplague | NONE | rhand | 100 |  |  | 277 |
| 4027 | Bouquet | NONE | rhand | 0 | 8 | 6 | 379 |
| 4202 | Chrono Cithara | NONE | rhand | 0 | 1 | 1 | 379 |
| 4219 | Dream Sword | NONE | rhand | 1530 | 31 | 21 | 379 |
| 4237 | Hatchling's Level 65 Weapon | NONE | rhand | 100 |  |  | 277 |
| 4238 | Hatchling's Level 75 Weapon | NONE | rhand | 100 |  |  | 277 |
| 5176 | Serpentine Spike | NONE | rhand | 100 |  |  | 277 |
| 5177 | Drake Horn | NONE | rhand | 100 |  |  | 277 |
| 5178 | Assault Alicorn | NONE | rhand | 100 |  |  | 277 |
| 5179 | Draconic Slicer | NONE | rhand | 100 |  |  | 277 |
| 5180 | Ohpdian Lance | NONE | rhand | 100 |  |  | 277 |
| 5181 | Diamond Drill | NONE | rhand | 100 |  |  | 277 |
| 5187 | Serpentine Grinder | NONE | rhand | 100 |  |  | 277 |
| 5188 | Fang of Dahak | NONE | rhand | 100 |  |  | 277 |
| 5189 | Crimson Blood Fang | NONE | rhand | 100 |  |  | 277 |
| 5190 | Draconic Chopper | NONE | rhand | 100 |  |  | 277 |
| 5191 | Diabolic Grinder | NONE | rhand | 100 |  |  | 277 |
| 5217 | Wolf's Level 75 Weapon | NONE | rhand | 100 |  |  | 277 |
| 5284 | Zweihander | NONE | lrhand | 1530 | 38 | 21 | 325 |
| 6354 | Falchion - for Beginners | NONE | rhand | 1530 | 31 | 21 | 379 |
| 6717 | Monster Only(Einhasad Warrior) | NONE | rhand | 1560 | 24 | 17 | 379 |
| 7821 | Apprentice Adventurer's Long Sword | NONE | rhand | 1560 | 24 | 17 | 379 |
| 7903 | Frintezza's Sword | NONE | lrhand | 2180 | 78 | 39 | 325 |
| 8204 | Monster Only (Follower of Frintezza Calibur) | NONE | rhand | 1560 |  |  | 379 |
| 8209 | Monster Only (Lidia Von Helmann Sword) | NONE | rhand | 1560 |  |  | 379 |
| 8211 | Monster Only (Monk Warrior Sword) | NONE | rhand | 1560 |  |  | 379 |
| 8215 | Monster Only (Zombie Enlisted Man Sword) | NONE | lrhand | 2090 |  |  | 325 |
| 8217 | Monster Only (Zombie Gateguard Spear) | NONE | rhand | 1560 |  |  | 379 |
| 8219 | Monster Only (Zombie Laborer Sword) | NONE | rhand | 1560 |  |  | 379 |
| 8222 | Monster Only (Follower of Frintezza Tran Calibur) | NONE | rhand | 1560 |  |  | 379 |
| 8530 | For Monsters Only (Squire's Sword) | NONE | rhand | 1600 | 6 | 5 | 379 |
| 8581 | Long Sword (Event) | NONE | rhand | 1560 | 24 | 17 | 379 |
| 8973 | Shadow Item: Falchion | NONE | rhand | 510 | 31 | 21 | 379 |
| 9644 | For NPC (Crossbow) | NONE | rhand | 1530 | 31 | 21 | 379 |
| 9645 | For NPC (Sword) | NONE | rhand | 1530 | 31 | 21 | 379 |
| 9646 | For NPC (Rapier) | NONE | rhand | 1530 | 31 | 21 | 379 |
| 9656 | Enchanted Wolf Fang | NONE | rhand | 100 |  |  | 277 |
| 9657 | Enchanted Coyote Fang | NONE | rhand | 100 |  |  | 277 |
| 9658 | Enchanted Saltydog Fang | NONE | rhand | 100 |  |  | 277 |
| 9659 | Enchanted Cerberus Fang | NONE | rhand | 100 |  |  | 277 |
| 9660 | Orichalcum Fang | NONE | rhand | 100 |  |  | 277 |
| 9661 | Enchanted Fenrir Fang | NONE | rhand | 100 |  |  | 277 |
| 9901 | Improved Falchion | NONE | rhand | 1530 | 31 | 21 | 379 |
| 10128 | For Monster only (Crossbow) | NONE | rhand | 1530 | 31 | 21 | 379 |
| 10167 | Pig Lollipop | NONE | rhand | 0 | 1 | 1 | 379 |
| 10479 | Shadow Item - Long Sword | NONE | rhand | 1560 | 24 | 17 | 379 |
| 11132 | Enchanted Cerberus Fang | NONE | rhand | 100 |  |  | 277 |
| 12793 | O Stick - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 12794 | X Stick - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 12795 | Scissors Stick - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 12796 | Rock Stick - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 12797 | Paper Stick - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 12798 | Snowman Transformation Stick | NONE | rhand | 0 | 1 | 1 | 379 |
| 12799 | Scarecrow Transformation Stick | NONE | rhand | 0 | 1 | 1 | 379 |
| 12800 | Pumpkin Transformation Stick - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 12801 | Condolence Flowerpot A | NONE | rhand | 0 | 1 | 1 | 379 |
| 12802 | Condolence Flowerpot B | NONE | rhand | 0 | 1 | 1 | 379 |
| 12803 | Congratulatory Flowerpot A | NONE | rhand | 0 | 1 | 1 | 379 |
| 12804 | Congratulatory Flowerpot B | NONE | rhand | 0 | 1 | 1 | 379 |
| 12805 | Flower Arrangement | NONE | rhand | 0 | 1 | 1 | 379 |
| 12806 | Bomb | NONE | rhand | 0 | 1 | 1 | 379 |
| 12807 | Direction Board | NONE | rhand | 0 | 1 | 1 | 379 |
| 12808 | Fruit Basket | NONE | rhand | 0 | 1 | 1 | 379 |
| 12809 | Arranged Clams | NONE | rhand | 0 | 1 | 1 | 379 |
| 12810 | Halloween Pumpkin | NONE | rhand | 0 | 1 | 1 | 379 |
| 12814 | Shadow Item - Gatekeeper Transformation Stick | NONE | rhand | 0 | 1 | 1 | 379 |
| 13062 | Exclusive to Monsters (Employee's Friend) | NONE | lrhand | 1740 | 442 | 163 | 325 |
| 13154 | Player Commendation - Falchion - Player Commendation Weapon | NONE | rhand | 1530 | 31 | 21 | 379 |
| 13248 | O Stick - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13249 | X Stick - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13250 | Scissors Stick - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13251 | Rock-type Stick - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13252 | Paper-type Stick - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13253 | Pumpkin Transformation Stick - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13319 | O Stick (Event) - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13320 | X Stick (Event) - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13321 | Scissors Stick (Event) - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13322 | Rock-type Stick (Event) - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13323 | Paper-type Stick (Event) - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13324 | Pumpkin Transformation Stick (Event) - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13334 | O Stick (Event) - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13335 | X Stick (Event) - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13336 | Scissors Stick (Event) - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13337 | Rock-type Stick (Event) - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13338 | Paper-type Stick (Event) - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13339 | Pumpkin Transformation Stick (Event) - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 13524 | Gracian Soldier One-handed Sword | NONE | rhand | 1500 | 24 | 17 | 379 |
| 13556 | Airship Helm | NONE | rhand | 0 | 1 | 1 | 379 |
| 13557 | Airship Cannon | NONE | rhand | 0 | 1 | 1 | 379 |
| 13558 | Airship Cannon Briquet | NONE | rhand | 0 | 1 | 1 | 379 |
| 13755 | Olympiad Warrior's Weapon (undetermined) | NONE | rhand | 1500 | 24 | 17 | 379 |
| 13979 | Exclusive to Monsters (Dragon Steed Troop Battle Infantry Sword) | NONE | rhand | 1560 | 24 | 17 | 379 |
| 13984 | Exclusive to Monsters (Death Slayer_1hs) | NONE | rhand | 1560 | 24 | 17 | 379 |
| 14056 | Snow Kung Transformation Stick - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14057 | Scarecrow Jack Transformation Stick - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14058 | Tin Golem Transformation Stick - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14069 | Snow Kung Transformation Stick (event) - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14070 | Scarecrow Jack Transformation Stick (Event) - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14071 | Tin Golem Transformation Stick (event) - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14088 | Snow Kung Transformation Stick - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14089 | Scarecrow Jack Transformation Stick - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14090 | Tin Golem Transformation Stick - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14096 | Snow Kung Transformation Stick (event) - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14097 | Scarecrow Jack Transformation Stick (Event) - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14098 | Tin Golem Transformation Stick (event) - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14621 | Santa Claus' Sirra Blade | NONE | rhand | 1300 | 51 | 38 | 379 |
| 14622 | Santa Claus' Sword of Ipos | NONE | lrhand | 1820 | 62 | 38 | 325 |
| 14629 | Santa Claus' Themis Tongue | NONE | rhand | 820 | 41 | 51 | 379 |
| 14774 | Wild Rose Pig Candy - 14-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 14780 | Baguette's Bread Sword | NONE | rhand | 1350 |  |  |  |
| 14782 | Baguette's Two-handed Sword | NONE | lrhand | 2250 |  |  |  |
| 14788 | Baguette's Magic Sword | NONE | rhand | 830 |  |  |  |
| 15342 | Aqua Elf Transforming Harp - 60-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 15344 | Aqua Elf Transforming Harp (Event) - 60-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 15436 | Halloween Transformation Stick - 7-day limited period | NONE | rhand | 10 | 1 | 1 | 379 |
| 17175 | Balloon Stick of Cheers - Red | NONE | rhand | 0 | 1 | 1 | 379 |
| 17176 | Balloon Stick of Cheers - Orange | NONE | rhand | 0 | 1 | 1 | 379 |
| 17177 | Balloon Stick of Cheers - Yellow | NONE | rhand | 0 | 1 | 1 | 379 |
| 17178 | Balloon Stick of Cheers - Green | NONE | rhand | 0 | 1 | 1 | 379 |
| 17179 | Balloon Stick of Cheers - Blue | NONE | rhand | 0 | 1 | 1 | 379 |
| 17180 | Balloon Stick of Cheers - Indigo Blue | NONE | rhand | 0 | 1 | 1 | 379 |
| 17181 | Balloon Stick of Cheers - Purple | NONE | rhand | 0 | 1 | 1 | 379 |
| 17182 | Balloon Stick of Cheers - Black | NONE | rhand | 0 | 1 | 1 | 379 |
| 17183 | Balloon Stick of Cheers - White | NONE | rhand | 0 | 1 | 1 | 379 |
| 20255 | Baguette Sword - 7-day limited period | NONE | rhand | 500 | 1 | 2 | 379 |
| 20257 | Baguette Dual Sword - 7-day limited period | NONE | lrhand | 500 | 1 | 2 | 325 |
| 20263 | Baguette Magic Sword - 7-day limited period | NONE | rhand | 500 | 1 | 2 | 379 |
| 20971 | Trejuo Transformation Stick - Blessed Child Transformation | NONE | rhand | 0 | 1 | 1 | 379 |
| 20972 | Sujin Transformation Stick - Blessed Child Transformation | NONE | rhand | 0 | 1 | 1 | 379 |
| 21015 | Balloon Stick of Cheers - Red | NONE | rhand | 0 | 1 | 1 | 379 |
| 21016 | Balloon Stick of Cheers - Orange | NONE | rhand | 0 | 1 | 1 | 379 |
| 21017 | Balloon Stick of Cheers - Yellow | NONE | rhand | 0 | 1 | 1 | 379 |
| 21018 | Balloon Stick of Cheers - Green | NONE | rhand | 0 | 1 | 1 | 379 |
| 21019 | Balloon Stick of Cheers - Blue | NONE | rhand | 0 | 1 | 1 | 379 |
| 21020 | Balloon Stick of Cheers - Indigo Blue | NONE | rhand | 0 | 1 | 1 | 379 |
| 21021 | Balloon Stick of Cheers - Purple | NONE | rhand | 0 | 1 | 1 | 379 |
| 21022 | Balloon Stick of Cheers - Black | NONE | rhand | 0 | 1 | 1 | 379 |
| 21023 | Balloon Stick of Cheers - White | NONE | rhand | 0 | 1 | 1 | 379 |
| 21367 | Aqua Elf Transformation Harp - 7-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 21368 | Aqua Elf Transformation Harp - 7-day limited period (event) | NONE | rhand | 0 | 1 | 1 | 379 |
| 21369 | Aqua Elf Transformation Harp - 30-day limited period | NONE | rhand | 0 | 1 | 1 | 379 |
| 21370 | Aqua Elf Transformation Harp - 30-day limited period (event) | NONE | rhand | 0 | 1 | 1 | 379 |
| 21371 | Aqua Elf Transformation Harp | NONE | rhand | 0 | 1 | 1 | 379 |
| 21372 | Aqua Elf Transformation Harp - Event | NONE | rhand | 0 | 1 | 1 | 379 |
| 22281 | Sujin Transformation Stick - 7-day limited period (event) | NONE | rhand | 0 | 1 | 1 | 379 |
| 22283 | Trejuo Transformation Stick - 7-day limited period (event) | NONE | rhand | 0 | 1 | 1 | 379 |
| 69 | Bastard Sword | D | rhand | 1510 | 51 | 32 | 379 |
| 70 | Claymore | D | lrhand | 2090 | 112 | 54 | 325 |
| 83 | Sword of Magic | D | rhand | 970 | 43 | 45 | 379 |
| 123 | Saber | D | rhand | 1520 | 40 | 26 | 379 |
| 124 | Two-Handed Sword | D | lrhand | 2180 | 78 | 39 | 325 |
| 125 | Spinebone Sword | D | rhand | 1510 | 51 | 32 | 379 |
| 126 | Artisan's Sword | D | rhand | 1500 | 51 | 32 | 379 |
| 127 | Crimson Sword | D | rhand | 1490 | 64 | 39 | 379 |
| 128 | Knight's Sword | D | rhand | 1500 | 51 | 32 | 379 |
| 129 | Sword of Revolution | D | rhand | 1450 | 79 | 47 | 379 |
| 130 | Elven Sword | D | rhand | 1470 | 64 | 39 | 379 |
| 143 | Sword of Mystic | D | rhand | 980 | 43 | 45 | 379 |
| 144 | Sword of Occult | D | rhand | 970 | 43 | 45 | 379 |
| 2499 | Elven Long Sword | D | rhand | 1440 | 92 | 54 | 379 |
| 5285 | Heavy Sword | D | lrhand | 1520 | 49 | 26 | 325 |
| 5791 | Tomb Guard A | D | lrhand | 2180 | 78 | 39 | 325 |
| 5792 | Tomb Guard B | D | lrhand | 2180 | 78 | 39 | 325 |
| 5795 | Tomb Guard A | D | lrhand | 2180 | 78 | 39 | 325 |
| 5796 | Tomb Guard B | D | lrhand | 2180 | 78 | 39 | 325 |
| 6723 | Monster Only(Vampire Warrior) | D | lrhand | 2090 | 112 | 54 | 325 |
| 7826 | Traveler's Bastard Sword | D | rhand | 1510 | 51 | 32 | 379 |
| 7880 | Steel Sword | D | lrhand | 2100 | 49 | 26 | 325 |
| 7881 | Titan Sword | D | lrhand | 2020 | 96 | 47 | 325 |
| 7885 | Priest Sword | D | rhand | 1520 | 32 | 35 | 379 |
| 7886 | Sword of Magic Fog | D | rhand | 1450 | 63 | 63 | 379 |
| 8532 | For Monsters Only (Spinebone Sword) | D | rhand | 1510 | 51 | 32 | 379 |
| 8533 | For Monsters Only (Crimson Sword) | D | rhand | 1490 | 64 | 39 | 379 |
| 8586 | Bastard Sword (Event) | D | rhand | 1510 | 51 | 32 | 379 |
| 8821 | Shadow Item: Two Handed Sword | D | lrhand | 730 | 78 | 39 | 325 |
| 8822 | Shadow Item: Crimson Sword | D | rhand | 500 | 64 | 39 | 379 |
| 8982 | Shadow Item: Two Handed Sword | D | lrhand | 730 | 78 | 39 | 325 |
| 8983 | Shadow Item: Crimson Sword | D | rhand | 500 | 64 | 39 | 379 |
| 9137 | Sword of Valakas (2-Handed) | D | lrhand | 2180 | 78 | 39 | 325 |
| 11605 | Common Item - Steel Sword | D | lrhand | 700 | 49 | 26 | 325 |
| 11611 | Common Item - Priest Sword | D | rhand | 507 | 32 | 35 | 379 |
| 11614 | Common Item - Saber | D | rhand | 507 | 40 | 26 | 379 |
| 11625 | Common Item - Heavy Sword | D | lrhand | 507 | 49 | 26 | 325 |
| 11628 | Common Item - Knight's Sword | D | rhand | 500 | 51 | 32 | 379 |
| 11635 | Common Item - Bastard Sword | D | rhand | 503 | 51 | 32 | 379 |
| 11636 | Common Item - Spinebone Sword | D | rhand | 503 | 51 | 32 | 379 |
| 11643 | Common Item - Artisan's Sword | D | rhand | 500 | 51 | 32 | 379 |
| 11655 | Common Item - Sword of Magic | D | rhand | 323 | 43 | 45 | 379 |
| 11656 | Common Item - Sword of Mystic | D | rhand | 327 | 43 | 45 | 379 |
| 11657 | Common Item - Sword of Occult | D | rhand | 323 | 43 | 45 | 379 |
| 11667 | Common Item - Two-Handed Sword | D | lrhand | 727 | 78 | 39 | 325 |
| 11670 | Common Item - Elven Sword | D | rhand | 490 | 64 | 39 | 379 |
| 11675 | Common Item - Crimson Sword | D | rhand | 497 | 64 | 39 | 379 |
| 11696 | Common Item - Sword of Magic Fog | D | rhand | 483 | 63 | 63 | 379 |
| 11710 | Common Item - Titan Sword | D | lrhand | 673 | 96 | 47 | 325 |
| 11714 | Common Item - Sword of Revolution | D | rhand | 483 | 79 | 47 | 379 |
| 11733 | Common Item - Elven Long Sword | D | rhand | 480 | 92 | 54 | 379 |
| 11736 | Common Item - Claymore | D | lrhand | 697 | 112 | 54 | 325 |
| 13164 | Player Commendation - Claymore - Player Commendation Weapon | D | lrhand | 2090 | 112 | 54 | 325 |
| 13174 | Player Commendation - Elven Long Sword - Player Commendation Weapon | D | rhand | 1440 | 92 | 54 | 379 |
| 13842 | Tiat Two-Handed Weapon | D | lrhand | 2180 | 78 | 39 | 325 |
| 13983 | Exclusive to Monsters (Death Knight_2hs) | D | lrhand | 2180 | 78 | 39 | 325 |
| 14606 | Gracian Soldier Two-Handed Sword | D | lrhand | 2180 | 78 | 39 | 325 |
| 15051 | Elven Long Sword of Fortune - 30-day limited period | D | rhand | 1440 | 92 | 54 | 379 |
| 15055 | Claymore of Fortune - 30-day limited period | D | lrhand | 2090 | 112 | 54 | 325 |
| 15165 | Elven Long Sword of Fortune - 10-day limited period | D | rhand | 1440 | 92 | 54 | 379 |
| 15169 | Claymore of Fortune - 10-day limited period | D | lrhand | 2090 | 112 | 54 | 325 |
| 16939 | Elven Long Sword of Fortune - 90-day limited period | D | rhand | 1440 | 92 | 54 | 379 |
| 16943 | Claymore of Fortune - 90-day limited period | D | lrhand | 2090 | 112 | 54 | 325 |
| 20109 | Sword of Revolution (Event) - 4-hour limited period | D | rhand | 483 | 79 | 47 | 379 |
| 20110 | Titan Sword (Event) - 4-hour limited period | D | lrhand | 673 | 96 | 47 | 325 |
| 20639 | Common Item - Elven Long Sword | D | rhand | 100 | 92 | 54 | 379 |
| 21732 | Sword of Revolution - Event | D | rhand | 1450 | 79 | 47 | 379 |
| 21733 | Titan Sword - Event | D | lrhand | 2020 | 96 | 47 | 325 |
| 21741 | Sword of Magic Fog - Event | D | rhand | 1450 | 63 | 63 | 379 |
| 71 | Flamberge | C | lrhand | 2010 | 130 | 61 | 325 |
| 72 | Stormbringer | C | rhand | 1430 | 107 | 61 | 379 |
| 73 | Shamshir | C | rhand | 1420 | 122 | 68 | 379 |
| 74 | Katana | C | rhand | 1420 | 122 | 68 | 379 |
| 75 | Caliburs | C | rhand | 1400 | 139 | 76 | 379 |
| 76 | Sword of Delusion | C | rhand | 1400 | 139 | 76 | 379 |
| 77 | Tsurugi | C | rhand | 1400 | 139 | 76 | 379 |
| 84 | Homunkulus's Sword | C | rhand | 950 | 111 | 101 | 379 |
| 131 | Spirit Sword | C | rhand | 1420 | 122 | 68 | 379 |
| 132 | Sword of Limit | C | rhand | 1400 | 139 | 76 | 379 |
| 133 | Raid Sword | C | rhand | 1420 | 122 | 68 | 379 |
| 134 | Sword of Nightmare | C | rhand | 1400 | 139 | 76 | 379 |
| 135 | Samurai Longsword | C | rhand | 1380 | 156 | 83 | 379 |
| 145 | Sword of Whispering Death | C | rhand | 920 | 111 | 101 | 379 |
| 4681 | Stormbringer - Critical Anger | C | rhand | 1430 | 107 | 61 | 379 |
| 4682 | Stormbringer - Focus | C | rhand | 1430 | 107 | 61 | 379 |
| 4683 | Stormbringer - Light | C | rhand | 1430 | 107 | 61 | 379 |
| 4684 | Shamshir - Guidance | C | rhand | 1420 | 122 | 68 | 379 |
| 4685 | Shamshir - Back Blow | C | rhand | 1420 | 122 | 68 | 379 |
| 4686 | Shamshir - Rsk. Evasion | C | rhand | 1420 | 122 | 68 | 379 |
| 4687 | Katana - Focus | C | rhand | 1420 | 122 | 68 | 379 |
| 4688 | Katana - Critical Damage | C | rhand | 1420 | 122 | 68 | 379 |
| 4689 | Katana - Haste | C | rhand | 1420 | 122 | 68 | 379 |
| 4690 | Spirit Sword - Critical Damage | C | rhand | 1420 | 122 | 68 | 379 |
| 4691 | Spirit Sword - Critical Poison | C | rhand | 1420 | 122 | 68 | 379 |
| 4692 | Spirit Sword - Haste | C | rhand | 1420 | 122 | 68 | 379 |
| 4693 | Raid Sword - Focus | C | rhand | 1420 | 122 | 68 | 379 |
| 4694 | Raid Sword - Critical Drain | C | rhand | 1420 | 122 | 68 | 379 |
| 4695 | Raid Sword - Critical Poison | C | rhand | 1420 | 122 | 68 | 379 |
| 4696 | Caliburs - Guidance | C | rhand | 1400 | 139 | 76 | 379 |
| 4697 | Caliburs - Focus | C | rhand | 1400 | 139 | 76 | 379 |
| 4698 | Caliburs - Critical Damage | C | rhand | 1400 | 139 | 76 | 379 |
| 4699 | Sword of Delusion - Focus | C | rhand | 1400 | 139 | 76 | 379 |
| 4700 | Sword of Delusion - Health | C | rhand | 1400 | 139 | 76 | 379 |
| 4701 | Sword of Delusion - Rsk. Haste | C | rhand | 1400 | 139 | 76 | 379 |
| 4702 | Tsurugi - Focus | C | rhand | 1400 | 139 | 76 | 379 |
| 4703 | Tsurugi - Critical Damage | C | rhand | 1400 | 139 | 76 | 379 |
| 4704 | Tsurugi - Haste | C | rhand | 1400 | 139 | 76 | 379 |
| 4705 | Sword of Nightmare - Health | C | rhand | 1400 | 139 | 76 | 379 |
| 4706 | Sword of Nightmare - Focus | C | rhand | 1400 | 139 | 76 | 379 |
| 4707 | Sword of Nightmare - Light | C | rhand | 1400 | 139 | 76 | 379 |
| 4708 | Samurai Longsword - Focus | C | rhand | 1380 | 156 | 83 | 379 |
| 4709 | Samurai Longsword - Critical Damage | C | rhand | 1380 | 156 | 83 | 379 |
| 4710 | Samurai Longsword - Haste | C | rhand | 1380 | 156 | 83 | 379 |
| 4711 | Flamberge - Critical Damage | C | lrhand | 2010 | 130 | 61 | 325 |
| 4712 | Flamberge - Focus | C | lrhand | 2010 | 130 | 61 | 325 |
| 4713 | Flamberge - Light | C | lrhand | 2010 | 130 | 61 | 325 |
| 5286 | Berserker Blade | C | lrhand | 1380 | 190 | 83 | 325 |
| 5793 | Tomb Savant A | C | rhand | 1380 | 156 | 83 | 379 |
| 5794 | Tomb Savant B | C | rhand | 1380 | 156 | 83 | 379 |
| 5797 | Tomb Savant A | C | rhand | 1380 | 156 | 83 | 379 |
| 5798 | Tomb Savant B | C | rhand | 1380 | 156 | 83 | 379 |
| 5800 | Nephilim Lord | C | rhand | 1380 | 156 | 83 | 379 |
| 5801 | For NPC (Dusk) | C | rhand | 1380 | 156 | 83 | 379 |
| 5802 | For NPC (Dawn) | C | rhand | 1380 | 156 | 83 | 379 |
| 6307 | Sword of Limit - Guidance | C | rhand | 1400 | 139 | 76 | 379 |
| 6308 | Sword of Limit - Critical Drain | C | rhand | 1400 | 139 | 76 | 379 |
| 6309 | Sword of Limit - Health | C | rhand | 1400 | 139 | 76 | 379 |
| 6310 | Sword of Whispering Death - Empower | C | rhand | 920 | 111 | 101 | 379 |
| 6311 | Sword of Whispering Death - M. Atk. | C | rhand | 920 | 111 | 101 | 379 |
| 6312 | Sword of Whispering Death - Magic Silence | C | rhand | 920 | 111 | 101 | 379 |
| 6313 | Homunkulus's Sword - Acumen | C | rhand | 950 | 111 | 101 | 379 |
| 6314 | Homunkulus's Sword - Conversion | C | rhand | 950 | 111 | 101 | 379 |
| 6315 | Homunkulus's Sword - Magic Paralyze | C | rhand | 950 | 111 | 101 | 379 |
| 6347 | Berserker Blade - Focus | C | lrhand | 1380 | 190 | 83 | 325 |
| 6348 | Berserker Blade - Critical Damage | C | lrhand | 1380 | 190 | 83 | 325 |
| 6349 | Berserker Blade - Haste | C | lrhand | 1380 | 190 | 83 | 325 |
| 7882 | Pa'agrian Sword | C | lrhand | 1980 | 169 | 76 | 325 |
| 7887 | Mysterious Sword | C | rhand | 1430 | 85 | 81 | 379 |
| 7888 | Ecliptic Sword | C | rhand | 1380 | 125 | 111 | 379 |
| 8102 | Pa'agrian Sword - Focus | C | lrhand | 1980 | 169 | 76 | 325 |
| 8103 | Pa'agrian Sword - Health | C | lrhand | 1980 | 169 | 76 | 325 |
| 8104 | Pa'agrian Sword - Critical Drain | C | lrhand | 1980 | 169 | 76 | 325 |
| 8111 | Mysterious Sword - Acumen | C | rhand | 1430 | 85 | 81 | 379 |
| 8112 | Mysterious Sword - M. Atk. | C | rhand | 1430 | 85 | 81 | 379 |
| 8113 | Mysterious Sword - Magic Weakness | C | rhand | 1430 | 85 | 81 | 379 |
| 8114 | Ecliptic Sword - Empower | C | rhand | 1380 | 125 | 111 | 379 |
| 8115 | Ecliptic Sword - M. Atk. | C | rhand | 1380 | 125 | 111 | 379 |
| 8116 | Ecliptic Sword - Magic Silence | C | rhand | 1380 | 125 | 111 | 379 |
| 8830 | Shadow Item: Katana | C | rhand | 480 | 122 | 68 | 379 |
| 8839 | Shadow Item: Sword of Delusion | C | rhand | 470 | 139 | 76 | 379 |
| 8846 | Shadow Item: Pa'agrian Sword | C | lrhand | 660 | 169 | 76 | 325 |
| 8926 | Shadow Item: Sword of Delusion | C | rhand | 470 | 139 | 76 | 379 |
| 8933 | Shadow Item: Pa'agrian Sword | C | lrhand | 660 | 169 | 76 | 325 |
| 8935 | Test Rapier | C | rhand | 1380 | 156 | 83 | 379 |
| 8991 | Shadow Item: Sword of Delusion | C | rhand | 470 | 139 | 76 | 379 |
| 8998 | Shadow Item: Pa'agrian Sword | C | lrhand | 660 | 169 | 76 | 325 |
| 9136 | Sword of Valakas (1-Handed) | C | rhand | 1380 | 156 | 83 | 379 |
| 11748 | Common Item - Mysterious Sword | C | rhand | 477 | 85 | 81 | 379 |
| 11756 | Common Item - Stormbringer | C | rhand | 477 | 107 | 61 | 379 |
| 11766 | Common Item - Flamberge | C | lrhand | 670 | 130 | 61 | 325 |
| 11778 | Common Item - Raid Sword | C | rhand | 473 | 122 | 68 | 379 |
| 11783 | Common Item - Shamshir | C | rhand | 473 | 122 | 68 | 379 |
| 11789 | Common Item - Spirit Sword | C | rhand | 473 | 122 | 68 | 379 |
| 11794 | Common Item - Katana | C | rhand | 473 | 122 | 68 | 379 |
| 11801 | Common Item - Sword of Limit | C | rhand | 467 | 139 | 76 | 379 |
| 11805 | Common Item - Sword of Whispering Death | C | rhand | 307 | 111 | 101 | 379 |
| 11807 | Common Item - Sword of Delusion | C | rhand | 467 | 139 | 76 | 379 |
| 11813 | Common Item - Pa'agrian Sword | C | lrhand | 660 | 169 | 76 | 325 |
| 11815 | Common Item - Sword of Nightmare | C | rhand | 467 | 139 | 76 | 379 |
| 11820 | Common Item - Tsurugi | C | rhand | 467 | 139 | 76 | 379 |
| 11821 | Common Item - Caliburs | C | rhand | 467 | 139 | 76 | 379 |
| 11829 | Common Item - Homunkulus's Sword | C | rhand | 317 | 111 | 101 | 379 |
| 11843 | Common Item - Berserker Blade | C | lrhand | 460 | 190 | 83 | 325 |
| 11850 | Common Item - Ecliptic Sword | C | rhand | 460 | 125 | 111 | 379 |
| 11853 | Common Item - Samurai Long Sword | C | rhand | 460 | 156 | 83 | 379 |
| 13178 | Player Commendation - Samurai Long Sword - Player Commendation Weapon | C | rhand | 1380 | 156 | 83 | 379 |
| 13191 | Player Commendation - Ecliptic Sword - Player Commendation Weapon | C | rhand | 1380 | 125 | 111 | 379 |
| 15034 | Homunkulus's Sword of Fortune - 30-day limited period | C | rhand | 950 | 111 | 101 | 379 |
| 15050 | Samurai Longsword of Fortune - 30-day limited period | C | rhand | 1380 | 156 | 83 | 379 |
| 15054 | Berserker Blade of Fortune - 30-day limited period | C | lrhand | 1380 | 190 | 83 | 325 |
| 15148 | Homunkulus's Sword of Fortune - 10-day limited period | C | rhand | 950 | 111 | 101 | 379 |
| 15164 | Samurai Longsword of Fortune - 10-day limited period | C | rhand | 1380 | 156 | 83 | 379 |
| 15168 | Berserker Blade of Fortune - 10-day limited period | C | lrhand | 1380 | 190 | 83 | 325 |
| 15403 | Player Commendation - Berserker Blade - Player Commendation Weapon | C | lrhand | 1380 | 190 | 83 | 325 |
| 16922 | Homunkulus's Sword of Fortune - 90-day limited period | C | rhand | 950 | 111 | 101 | 379 |
| 16938 | Samurai Longsword of Fortune - 90-day limited period | C | rhand | 1380 | 156 | 83 | 379 |
| 16942 | Berserker Blade of Fortune - 90-day limited period | C | lrhand | 1380 | 190 | 83 | 325 |
| 20123 | Samurai Longsword (Event) - 4-hour limited period | C | rhand | 460 | 156 | 83 | 379 |
| 20124 | Berserker Blade (Event) - 4-hour limited period | C | lrhand | 460 | 190 | 83 | 325 |
| 78 | Great Sword | B | lrhand | 1930 | 213 | 91 | 325 |
| 79 | Sword of Damascus | B | rhand | 1350 | 194 | 99 | 379 |
| 142 | Keshanberk | B | rhand | 1370 | 175 | 91 | 379 |
| 146 | Ghoulbane | B | rhand | 910 | 140 | 122 | 379 |
| 148 | Sword of Valhalla | B | rhand | 900 | 140 | 122 | 379 |
| 4714 | Keshanberk - Guidance | B | rhand | 1370 | 175 | 91 | 379 |
| 4715 | Keshanberk - Focus | B | rhand | 1370 | 175 | 91 | 379 |
| 4716 | Keshanberk - Back Blow | B | rhand | 1370 | 175 | 91 | 379 |
| 4717 | Sword of Damascus - Focus | B | rhand | 1350 | 194 | 99 | 379 |
| 4718 | Sword of Damascus - Critical Damage | B | rhand | 1350 | 194 | 99 | 379 |
| 4719 | Sword of Damascus - Haste | B | rhand | 1350 | 194 | 99 | 379 |
| 4723 | Great Sword - Health | B | lrhand | 1930 | 213 | 91 | 325 |
| 4724 | Great Sword - Critical Damage | B | lrhand | 1930 | 213 | 91 | 325 |
| 4725 | Great Sword - Focus | B | lrhand | 1930 | 213 | 91 | 325 |
| 7722 | Sword of Valhalla - Acumen | B | rhand | 900 | 140 | 122 | 379 |
| 7723 | Sword of Valhalla - Magic Weakness | B | rhand | 900 | 140 | 122 | 379 |
| 7724 | Sword of Valhalla - Magic Regeneration | B | rhand | 900 | 140 | 122 | 379 |
| 7883 | Guardian Sword | B | lrhand | 1930 | 236 | 99 | 325 |
| 7889 | Wizard's Tear | B | rhand | 1350 | 155 | 132 | 379 |
| 8105 | Guardian Sword - Critical Drain | B | lrhand | 1930 | 236 | 99 | 325 |
| 8106 | Guardian Sword - Health | B | lrhand | 1930 | 236 | 99 | 325 |
| 8107 | Guardian Sword - Critical Bleed | B | lrhand | 1930 | 236 | 99 | 325 |
| 8117 | Wizard's Tear - Acumen | B | rhand | 1350 | 155 | 132 | 379 |
| 8118 | Wizard's Tear - M. Atk. | B | rhand | 1350 | 155 | 132 | 379 |
| 8119 | Wizard's Tear - Conversion | B | rhand | 1350 | 155 | 132 | 379 |
| 8849 | Shadow Item: Great Sword | B | lrhand | 650 | 213 | 91 | 325 |
| 8852 | Shadow Item: Keshanberk | B | rhand | 460 | 175 | 91 | 379 |
| 8853 | Shadow Item: Sword of Valhalla | B | rhand | 300 | 140 | 122 | 379 |
| 9001 | Shadow Item: Great Sword | B | lrhand | 650 | 213 | 91 | 325 |
| 9004 | Shadow Item: Keshanberk | B | rhand | 460 | 175 | 91 | 379 |
| 9005 | Shadow Item: Sword of Valhalla | B | rhand | 300 | 140 | 122 | 379 |
| 10870 | Great Sword - Lightning | B | lrhand | 1930 | 213 | 91 | 325 |
| 10871 | Great Sword - Lightning - Health | B | lrhand | 1930 | 213 | 91 | 325 |
| 10872 | Great Sword - Lightning - Critical Damage | B | lrhand | 1930 | 213 | 91 | 325 |
| 10873 | Great Sword - Lightning - Focus | B | lrhand | 1930 | 213 | 91 | 325 |
| 10893 | Sword of Valhalla - Nature | B | rhand | 900 | 140 | 122 | 379 |
| 10894 | Sword of Valhalla - Nature - Acumen | B | rhand | 900 | 140 | 122 | 379 |
| 10895 | Sword of Valhalla - Nature - Magic Weakness | B | rhand | 900 | 140 | 122 | 379 |
| 10896 | Sword of Valhalla - Nature - Magic Regeneration | B | rhand | 900 | 140 | 122 | 379 |
| 10930 | Keshanberk - Destruction | B | rhand | 1370 | 175 | 91 | 379 |
| 10931 | Keshanberk - Destruction - Guidance | B | rhand | 1370 | 175 | 91 | 379 |
| 10932 | Keshanberk - Destruction - Focus | B | rhand | 1370 | 175 | 91 | 379 |
| 10933 | Keshanberk - Destruction - Back Blow | B | rhand | 1370 | 175 | 91 | 379 |
| 10955 | Guardian Sword - Great Gale | B | lrhand | 1930 | 236 | 99 | 325 |
| 10956 | Guardian Sword - Great Gale - Critical Drain | B | lrhand | 1930 | 236 | 99 | 325 |
| 10957 | Guardian Sword - Great Gale - Health | B | lrhand | 1930 | 236 | 99 | 325 |
| 10958 | Guardian Sword - Great Gale - Critical Bleed | B | lrhand | 1930 | 236 | 99 | 325 |
| 10959 | Sword of Damascus - Earth | B | rhand | 1350 | 194 | 99 | 379 |
| 10960 | Sword of Damascus - Earth - Focus | B | rhand | 1350 | 194 | 99 | 379 |
| 10961 | Sword of Damascus - Earth - Critical Damage | B | rhand | 1350 | 194 | 99 | 379 |
| 10962 | Sword of Damascus - Earth - Haste | B | rhand | 1350 | 194 | 99 | 379 |
| 11005 | Wizard's Tear - Cleverness | B | rhand | 1350 | 155 | 132 | 379 |
| 11006 | Wizard's Tear - Cleverness - Acumen | B | rhand | 1350 | 155 | 132 | 379 |
| 11007 | Wizard's Tear - Cleverness - M. Atk. | B | rhand | 1350 | 155 | 132 | 379 |
| 11008 | Wizard's Tear - Cleverness - Conversion | B | rhand | 1350 | 155 | 132 | 379 |
| 11889 | Common Item - Great Sword | B | lrhand | 643 | 213 | 91 | 325 |
| 11900 | Common Item - Sword of Valhalla | B | rhand | 300 | 140 | 122 | 379 |
| 11916 | Common Item - Keshanberk | B | rhand | 457 | 175 | 91 | 379 |
| 11929 | Common Item - Guardian Sword | B | lrhand | 643 | 236 | 99 | 325 |
| 11930 | Common Item - Sword of Damascus | B | rhand | 450 | 194 | 99 | 379 |
| 11943 | Common Item - Wizard's Tear | B | rhand | 450 | 155 | 132 | 379 |
| 13194 | Player Commendation - Damascus Sword - Player Commendation Weapon | B | rhand | 1350 | 194 | 99 | 379 |
| 13203 | Player Commendation - Guardian's Sword - Player Commendation Weapon | B | lrhand | 1930 | 236 | 99 | 325 |
| 13204 | Player Commendation - Wizard's Tear - Player Commendation Weapon | B | rhand | 1350 | 155 | 132 | 379 |
| 15033 | Wizard's Tear of Fortune - 30-day limited period | B | rhand | 1350 | 155 | 132 | 379 |
| 15049 | Fortune Sword of Damascus - 30-day limited period | B | rhand | 1350 | 194 | 99 | 379 |
| 15053 | Guardian Sword of Fortune - 30-day limited period | B | lrhand | 1930 | 236 | 99 | 325 |
| 15147 | Wizard's Tear of Fortune - 10-day limited period | B | rhand | 1350 | 155 | 132 | 379 |
| 15163 | Fortune Sword of Damascus - 10-day limited period | B | rhand | 1350 | 194 | 99 | 379 |
| 15167 | Guardian Sword of Fortune - 10-day limited period | B | lrhand | 1930 | 236 | 99 | 325 |
| 16921 | Wizard's Tear of Fortune - 90-day limited period | B | rhand | 1350 | 155 | 132 | 379 |
| 16937 | Fortune Sword of Damascus - 90-day limited period | B | rhand | 1350 | 194 | 99 | 379 |
| 16941 | Guardian Sword of Fortune - 90-day limited period | B | lrhand | 1930 | 236 | 99 | 325 |
| 20137 | Sword of Damascus (Event) - 4-hour limited period | B | rhand | 450 | 194 | 99 | 379 |
| 20138 | Guardian Sword (Event) - 4-hour limited period | B | lrhand | 643 | 236 | 99 | 325 |
| 80 | Tallum Blade | A | rhand | 1330 | 213 | 107 | 379 |
| 81 | Dragon Slayer | A | lrhand | 1840 | 282 | 114 | 325 |
| 85 | Phantom Sword | A | rhand | 860 | 170 | 143 | 379 |
| 147 | Tear of Darkness | A | rhand | 830 | 170 | 143 | 379 |
| 149 | Sword of Life | A | rhand | 840 | 170 | 143 | 379 |
| 150 | Elemental Sword | A | rhand | 830 | 170 | 143 | 379 |
| 151 | Sword of Miracles | A | rhand | 840 | 186 | 152 | 379 |
| 2500 | Dark Legion's Edge | A | rhand | 1320 | 232 | 114 | 379 |
| 4720 | Tallum Blade - Health | A | rhand | 1330 | 213 | 107 | 379 |
| 4721 | Tallum Blade - Rsk. Evasion | A | rhand | 1330 | 213 | 107 | 379 |
| 4722 | Tallum Blade - Rsk. Haste | A | rhand | 1330 | 213 | 107 | 379 |
| 5635 | Tallum Blade - Critical Poison | A | rhand | 1330 | 213 | 107 | 379 |
| 5636 | Tallum Blade - Haste | A | rhand | 1330 | 213 | 107 | 379 |
| 5637 | Tallum Blade - Anger | A | rhand | 1330 | 213 | 107 | 379 |
| 5638 | Elemental Sword - M. Atk. | A | rhand | 830 | 170 | 143 | 379 |
| 5639 | Elemental Sword - Magic Paralyze | A | rhand | 830 | 170 | 143 | 379 |
| 5640 | Elemental Sword - Empower | A | rhand | 830 | 170 | 143 | 379 |
| 5641 | Sword of Miracles - M. Atk. | A | rhand | 840 | 186 | 152 | 379 |
| 5642 | Sword of Miracles - Magic Silence | A | rhand | 840 | 186 | 152 | 379 |
| 5643 | Sword of Miracles - Acumen | A | rhand | 840 | 186 | 152 | 379 |
| 5644 | Dragon Slayer - Health | A | lrhand | 1840 | 282 | 114 | 325 |
| 5645 | Dragon Slayer - Critical Bleed | A | lrhand | 1840 | 282 | 114 | 325 |
| 5646 | Dragon Slayer - Critical Drain | A | lrhand | 1840 | 282 | 114 | 325 |
| 5647 | Dark Legion's Edge - Critical Damage | A | rhand | 1320 | 232 | 114 | 379 |
| 5648 | Dark Legion's Edge - Health | A | rhand | 1320 | 232 | 114 | 379 |
| 5649 | Dark Legion's Edge - Rsk. Focus | A | rhand | 1320 | 232 | 114 | 379 |
| 7884 | Infernal Master | A | lrhand | 1900 | 259 | 107 | 325 |
| 8108 | Infernal Master - Haste | A | lrhand | 1900 | 259 | 107 | 325 |
| 8109 | Infernal Master - Critical Damage | A | lrhand | 1900 | 259 | 107 | 325 |
| 8110 | Infernal Master - Focus | A | lrhand | 1900 | 259 | 107 | 325 |
| 8678 | Sirra's Blade | A | rhand | 1300 | 251 | 121 | 379 |
| 8679 | Sword of Ipos | A | lrhand | 1820 | 305 | 121 | 325 |
| 8686 | Themis' Tongue | A | rhand | 820 | 202 | 161 | 379 |
| 8788 | Sirra's Blade - Haste | A | rhand | 1300 | 251 | 121 | 379 |
| 8789 | Sirra's Blade - Health | A | rhand | 1300 | 251 | 121 | 379 |
| 8790 | Sirra's Blade - Critical Poison | A | rhand | 1300 | 251 | 121 | 379 |
| 8791 | Sword of Ipos - Focus | A | lrhand | 1820 | 305 | 121 | 325 |
| 8792 | Sword of Ipos - Haste | A | lrhand | 1820 | 305 | 121 | 325 |
| 8793 | Sword of Ipos - Health | A | lrhand | 1820 | 305 | 121 | 325 |
| 8812 | Themis' Tongue - Mana Up | A | rhand | 820 | 202 | 161 | 379 |
| 8813 | Themis' Tongue - Mental Shield | A | rhand | 820 | 202 | 161 | 379 |
| 8814 | Themis' Tongue - Magic Focus | A | rhand | 820 | 202 | 161 | 379 |
| 8859 | Shadow Item: Tallum Blade | A | rhand | 450 | 213 | 107 | 379 |
| 8867 | Shadow Item: Inferno Master | A | lrhand | 640 | 259 | 107 | 325 |
| 9011 | Shadow Item: Tallum Blade | A | rhand | 450 | 213 | 107 | 379 |
| 9019 | Shadow Item: Inferno Master | A | lrhand | 640 | 259 | 107 | 325 |
| 9021 | Shadow Item: Dragon Slayer | A | lrhand | 613 | 282 | 114 | 325 |
| 9022 | Shadow Item: Sword of Miracles | A | rhand | 280 | 186 | 152 | 379 |
| 9029 | Shadow Item: Dark Legion's Edge | A | rhand | 440 | 232 | 114 | 379 |
| 10667 | Sirra's Blade {PvP} - Haste | A | rhand | 1300 | 251 | 121 | 379 |
| 10668 | Sirra's Blade {PvP} - Health | A | rhand | 1300 | 251 | 121 | 379 |
| 10669 | Sirra's Blade {PvP} - Critical Poison | A | rhand | 1300 | 251 | 121 | 379 |
| 10670 | Sword of Ipos {PvP} - Focus | A | lrhand | 1820 | 305 | 121 | 325 |
| 10671 | Sword of Ipos {PvP} - Haste | A | lrhand | 1820 | 305 | 121 | 325 |
| 10672 | Sword of Ipos {PvP} - Health | A | lrhand | 1820 | 305 | 121 | 325 |
| 10691 | Themis' Tongue {PvP} - Mana Up | A | rhand | 820 | 201 | 162 | 379 |
| 10692 | Themis' Tongue {PvP} - Mental Shield | A | rhand | 820 | 201 | 162 | 379 |
| 10693 | Themis' Tongue {PvP} - Magic Focus | A | rhand | 820 | 201 | 162 | 379 |
| 11041 | Elemental Sword - Hail | A | rhand | 830 | 170 | 143 | 379 |
| 11042 | Elemental Sword - Hail - M. Atk. | A | rhand | 830 | 170 | 143 | 379 |
| 11043 | Elemental Sword - Hail - Magic Paralyze | A | rhand | 830 | 170 | 143 | 379 |
| 11044 | Elemental Sword - Hail - Empower | A | rhand | 830 | 170 | 143 | 379 |
| 11049 | Infernal Master - Concentration | A | lrhand | 1900 | 259 | 107 | 325 |
| 11050 | Infernal Master - Concentration - Haste | A | lrhand | 1900 | 259 | 107 | 325 |
| 11051 | Infernal Master - Concentration - Critical Damage | A | lrhand | 1900 | 259 | 107 | 325 |
| 11052 | Infernal Master - Concentration - Focus | A | lrhand | 1900 | 259 | 107 | 325 |
| 11058 | Tallum Blade - Destruction | A | rhand | 1330 | 213 | 107 | 379 |
| 11059 | Tallum Blade - Destruction - Critical Poison | A | rhand | 1330 | 213 | 107 | 379 |
| 11060 | Tallum Blade - Destruction - Haste | A | rhand | 1330 | 213 | 107 | 379 |
| 11061 | Tallum Blade - Destruction - Anger | A | rhand | 1330 | 213 | 107 | 379 |
| 11080 | Dark Legion's Edge - Thunder | A | rhand | 1320 | 232 | 114 | 379 |
| 11081 | Dark Legion's Edge - Thunder - Critical Damage | A | rhand | 1320 | 232 | 114 | 379 |
| 11082 | Dark Legion's Edge - Thunder - Health | A | rhand | 1320 | 232 | 114 | 379 |
| 11083 | Dark Legion's Edge - Thunder - Rsk. Focus | A | rhand | 1320 | 232 | 114 | 379 |
| 11096 | Dragon Slayer - Evil Spirit | A | lrhand | 1840 | 282 | 114 | 325 |
| 11097 | Dragon Slayer - Evil Spirit - Health | A | lrhand | 1840 | 282 | 114 | 325 |
| 11098 | Dragon Slayer - Evil Spirit - Critical Bleed | A | lrhand | 1840 | 282 | 114 | 325 |
| 11099 | Dragon Slayer - Evil Spirit - Critical Drain | A | lrhand | 1840 | 282 | 114 | 325 |
| 11108 | Sword of Miracles - Holy Spirit | A | rhand | 840 | 186 | 152 | 379 |
| 11109 | Sword of Miracles - Holy Spirit - M. Atk. | A | rhand | 840 | 186 | 152 | 379 |
| 11110 | Sword of Miracles - Holy Spirit - Magic Silence | A | rhand | 840 | 186 | 152 | 379 |
| 11111 | Sword of Miracles - Holy Spirit - Acumen | A | rhand | 840 | 186 | 152 | 379 |
| 11161 | Sword of Ipos - Earth | A | lrhand | 1820 | 305 | 121 | 325 |
| 11162 | Sword of Ipos - Earth - Focus | A | lrhand | 1820 | 305 | 121 | 325 |
| 11163 | Sword of Ipos - Earth - Haste | A | lrhand | 1820 | 305 | 121 | 325 |
| 11164 | Sword of Ipos - Earth - Health | A | lrhand | 1820 | 305 | 121 | 325 |
| 11169 | Sirra's Blade - Landslide | A | rhand | 1300 | 251 | 121 | 379 |
| 11170 | Sirra's Blade - Landslide - Haste | A | rhand | 1300 | 251 | 121 | 379 |
| 11171 | Sirra's Blade - Landslide - Health | A | rhand | 1300 | 251 | 121 | 379 |
| 11172 | Sirra's Blade - Landslide - Critical Poison | A | rhand | 1300 | 251 | 121 | 379 |
| 11182 | Themis' Tongue - Cleverness | A | rhand | 820 | 202 | 161 | 379 |
| 11183 | Themis' Tongue - Cleverness - Mana Up | A | rhand | 820 | 202 | 161 | 379 |
| 11184 | Themis' Tongue - Cleverness - Mental Shield | A | rhand | 820 | 202 | 161 | 379 |
| 11185 | Themis' Tongue - Cleverness - Magic Focus | A | rhand | 820 | 202 | 161 | 379 |
| 11952 | Common Item - Elemental Sword | A | rhand | 277 | 170 | 143 | 379 |
| 11954 | Common Item - Inferno Master | A | lrhand | 633 | 259 | 107 | 325 |
| 11957 | Common Item - Tallum Blade | A | rhand | 443 | 213 | 107 | 379 |
| 11964 | Common Item - Dark Legion's Edge | A | rhand | 440 | 232 | 114 | 379 |
| 11968 | Common Item - Dragon Slayer | A | lrhand | 613 | 282 | 114 | 325 |
| 11971 | Common Item - Sword of Miracles | A | rhand | 280 | 186 | 152 | 379 |
| 11984 | Common Item - Sword of Ipos | A | lrhand | 607 | 305 | 121 | 325 |
| 11986 | Common Item - Sirra's Blade | A | rhand | 433 | 251 | 121 | 379 |
| 11990 | Common Item - Themis' Tongue | A | rhand | 273 | 202 | 162 | 379 |
| 12873 | Sword of Ipos - Earth {PvP} - Focus | A | lrhand | 1820 | 305 | 121 | 325 |
| 12874 | Sword of Ipos - Earth {PvP} - Haste | A | lrhand | 1820 | 305 | 121 | 325 |
| 12875 | Sword of Ipos - Earth {PvP} - Health | A | lrhand | 1820 | 305 | 121 | 325 |
| 12879 | Sirra's Blade - Landslide {PvP} - Haste | A | rhand | 1300 | 251 | 121 | 379 |
| 12880 | Sirra's Blade - Landslide {PvP} - Health | A | rhand | 1300 | 251 | 121 | 379 |
| 12881 | Sirra's Blade - Landslide {PvP} - Critical Poison | A | rhand | 1300 | 251 | 121 | 379 |
| 12889 | Themis' Tongue - Cleverness {PvP} - Mana Up | A | rhand | 820 | 202 | 161 | 379 |
| 12890 | Themis' Tongue - Cleverness {PvP} - Mental Shield | A | rhand | 820 | 202 | 161 | 379 |
| 12891 | Themis' Tongue - Cleverness {PvP} - Magic Focus | A | rhand | 820 | 202 | 161 | 379 |
| 13042 | Ancient Legacy Sword | A | lrhand | 643 | 259 | 143 | 325 |
| 13043 | Enhanced Ancient Legacy Sword | A | lrhand | 643 | 279 | 153 | 325 |
| 13044 | Complete Ancient Legacy Sword | A | lrhand | 643 | 299 | 163 | 325 |
| 13210 | Player Commendation - Sirra's Blade - Player Commendation Weapon | A | rhand | 1300 | 251 | 121 | 379 |
| 13211 | Player Commendation - Sword of Ipos - Player Commendation Weapon | A | lrhand | 1820 | 305 | 121 | 325 |
| 13218 | Player Commendation - Themis' Tongue - Player Commendation Weapon | A | rhand | 820 | 202 | 161 | 379 |
| 13845 | Attribute Master Yin's Sword | A | rhand | 1560 | 140 | 120 | 379 |
| 13881 | Attribute Master Yang's Sword | A | rhand | 1560 | 140 | 120 | 379 |
| 15032 | Sword of Miracles of Fortune - 30-day limited period | A | rhand | 840 | 186 | 152 | 379 |
| 15048 | Sirra's Blade of Fortune - 30-day limited period | A | rhand | 1300 | 251 | 121 | 379 |
| 15052 | Fortune Sword of Ipos - 30-day limited period | A | lrhand | 1820 | 305 | 121 | 325 |
| 15146 | Sword of Miracles of Fortune - 10-day limited period | A | rhand | 840 | 186 | 152 | 379 |
| 15162 | Sirra's Blade of Fortune - 10-day limited period | A | rhand | 1300 | 251 | 121 | 379 |
| 15166 | Fortune Sword of Ipos - 10-day limited period | A | lrhand | 1820 | 305 | 121 | 325 |
| 16920 | Sword of Miracles of Fortune - 90-day limited period | A | rhand | 840 | 186 | 152 | 379 |
| 16936 | Sirra's Blade of Fortune - 90-day limited period | A | rhand | 1300 | 251 | 121 | 379 |
| 16940 | Fortune Sword of Ipos - 90-day limited period | A | lrhand | 1820 | 305 | 121 | 325 |
| 20151 | Dark Legion's Edge (Event) - 4-hour limited period | A | rhand | 440 | 232 | 114 | 379 |
| 20152 | Dragon Slayer (Event) - 4-hour limited period | A | lrhand | 613 | 282 | 114 | 325 |
| 21973 | Mardil's Fan | A | rhand | 840 | 186 | 152 | 379 |
| 21974 | Mardil's Fan - M. Atk. | A | rhand | 840 | 186 | 152 | 379 |
| 21975 | Mardil's Fan - Magic Silence | A | rhand | 840 | 186 | 152 | 379 |
| 21976 | Mardil's Fan - Acumen | A | rhand | 840 | 186 | 152 | 379 |
| 21977 | Mardil's Fan - Holy Spirit | A | rhand | 840 | 186 | 152 | 379 |
| 21978 | Mardil's Fan - Holy Spirit - M. Atk. | A | rhand | 840 | 186 | 152 | 379 |
| 21979 | Mardil's Fan - Holy Spirit - Magic Silence | A | rhand | 840 | 186 | 152 | 379 |
| 21980 | Mardil's Fan - Holy Spirit - Acumen | A | rhand | 840 | 186 | 152 | 379 |
| 82 | Gaz Blade | S | rhand | 1300 | 257 | 124 | 379 |
| 6364 | Forgotten Blade | S | rhand | 1300 | 281 | 132 | 379 |
| 6372 | Heaven's Divider | S | lrhand | 1380 | 342 | 132 | 325 |
| 6581 | Forgotten Blade - Haste | S | rhand | 1300 | 281 | 132 | 379 |
| 6582 | Forgotten Blade - Health | S | rhand | 1300 | 281 | 132 | 379 |
| 6583 | Forgotten Blade - Focus | S | rhand | 1300 | 281 | 132 | 379 |
| 6605 | Heavens Divider - Haste | S | lrhand | 1380 | 342 | 132 | 325 |
| 6606 | Heavens Divider - Health | S | lrhand | 1380 | 342 | 132 | 325 |
| 6607 | Heavens Divider - Focus | S | lrhand | 1380 | 342 | 132 | 325 |
| 6611 | Infinity Blade | S | rhand | 1300 | 524 | 230 | 379 |
| 6612 | Infinity Cleaver | S | lrhand | 1300 | 638 | 230 | 325 |
| 9442 | Dynasty Sword | S | rhand | 1520 | 333 | 151 | 379 |
| 9443 | Dynasty Blade | S | lrhand | 1740 | 405 | 151 | 325 |
| 9444 | Dynasty Phantom | S | rhand | 1520 | 267 | 202 | 379 |
| 9854 | Dynasty Sword - Focus | S | rhand | 1520 | 333 | 151 | 379 |
| 9855 | Dynasty Sword - Health | S | rhand | 1520 | 333 | 151 | 379 |
| 9856 | Dynasty Sword - Light | S | rhand | 1520 | 333 | 151 | 379 |
| 9857 | Dynasty Blade - Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 9858 | Dynasty Blade - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 9859 | Dynasty Blade - Light | S | lrhand | 1740 | 405 | 151 | 325 |
| 9860 | Dynasty Phantom - Acumen | S | rhand | 1520 | 267 | 202 | 379 |
| 9861 | Dynasty Phantom - Mana Up | S | rhand | 1520 | 267 | 202 | 379 |
| 9862 | Dynasty Phantom - Conversion | S | rhand | 1520 | 267 | 202 | 379 |
| 10710 | Forgotten Blade {PvP} - Haste | S | rhand | 1300 | 281 | 132 | 379 |
| 10711 | Forgotten Blade {PvP} - Health | S | rhand | 1300 | 281 | 132 | 379 |
| 10712 | Forgotten Blade {PvP} - Focus | S | rhand | 1300 | 281 | 132 | 379 |
| 10713 | Heavens Divider {PvP} - Haste | S | lrhand | 1380 | 342 | 132 | 325 |
| 10714 | Heavens Divider {PvP} - Health | S | lrhand | 1380 | 342 | 132 | 325 |
| 10715 | Heavens Divider {PvP} - Focus | S | lrhand | 1380 | 342 | 132 | 325 |
| 10750 | Dynasty Sword {PvP} - Focus | S | rhand | 1520 | 333 | 151 | 379 |
| 10751 | Dynasty Sword {PvP} - Health | S | rhand | 1520 | 333 | 151 | 379 |
| 10752 | Dynasty Sword {PvP} - Light | S | rhand | 1520 | 333 | 151 | 379 |
| 10753 | Dynasty Blade {PvP} - Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 10754 | Dynasty Blade {PvP} - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 10755 | Dynasty Blade {PvP} - Light | S | lrhand | 1740 | 405 | 151 | 325 |
| 10771 | Dynasty Phantom {PvP} - Acumen | S | rhand | 1520 | 267 | 202 | 379 |
| 10772 | Dynasty Phantom {PvP} - Mana Up | S | rhand | 1520 | 267 | 202 | 379 |
| 10773 | Dynasty Phantom {PvP} - Conversion | S | rhand | 1520 | 267 | 202 | 379 |
| 11235 | Forgotten Blade - Lightning | S | rhand | 1300 | 281 | 132 | 379 |
| 11236 | Forgotten Blade - Lightning - Haste | S | rhand | 1300 | 281 | 132 | 379 |
| 11237 | Forgotten Blade - Lightning - Health | S | rhand | 1300 | 281 | 132 | 379 |
| 11238 | Forgotten Blade - Lightning - Focus | S | rhand | 1300 | 281 | 132 | 379 |
| 11239 | Heaven's Divider - Thunder | S | lrhand | 1380 | 342 | 132 | 325 |
| 11240 | Heaven's Divider - Thunder - Haste | S | lrhand | 1380 | 342 | 132 | 325 |
| 11241 | Heaven's Divider - Thunder - Health | S | lrhand | 1380 | 342 | 132 | 325 |
| 11242 | Heaven's Divider - Thunder - Focus | S | lrhand | 1380 | 342 | 132 | 325 |
| 11268 | Dynasty Blade - Great Gale | S | lrhand | 1740 | 405 | 151 | 325 |
| 11269 | Dynasty Blade - Great Gale - Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 11270 | Dynasty Blade - Great Gale - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 11271 | Dynasty Blade - Great Gale - Light | S | lrhand | 1740 | 405 | 151 | 325 |
| 11272 | Dynasty Sword - Earth | S | rhand | 1520 | 333 | 151 | 379 |
| 11273 | Dynasty Sword - Earth - Focus | S | rhand | 1520 | 333 | 151 | 379 |
| 11274 | Dynasty Sword - Earth - Health | S | rhand | 1520 | 333 | 151 | 379 |
| 11275 | Dynasty Sword - Earth - Light | S | rhand | 1520 | 333 | 151 | 379 |
| 11292 | Dynasty Phantom - Nature | S | rhand | 1520 | 267 | 202 | 379 |
| 11293 | Dynasty Phantom - Nature - Acumen | S | rhand | 1520 | 267 | 202 | 379 |
| 11294 | Dynasty Phantom - Nature - Mana Up | S | rhand | 1520 | 267 | 202 | 379 |
| 11295 | Dynasty Phantom - Nature - Conversion | S | rhand | 1520 | 267 | 202 | 379 |
| 12004 | Common Item - Forgotten Blade | S | rhand | 433 | 281 | 132 | 379 |
| 12005 | Common Item - Heaven's Divider | S | lrhand | 460 | 342 | 132 | 325 |
| 12929 | Forgotten Blade - Lightning {PvP} - Haste | S | rhand | 1300 | 281 | 132 | 379 |
| 12930 | Forgotten Blade - Lightning {PvP} - Health | S | rhand | 1300 | 281 | 132 | 379 |
| 12931 | Forgotten Blade - Lightning {PvP} - Focus | S | rhand | 1300 | 281 | 132 | 379 |
| 12932 | Heavens Divider - Thunder {PvP} - Haste | S | lrhand | 1380 | 342 | 132 | 325 |
| 12933 | Heavens Divider - Thunder {PvP} - Health | S | lrhand | 1380 | 342 | 132 | 325 |
| 12934 | Heavens Divider - Thunder {PvP} - Focus | S | lrhand | 1380 | 342 | 132 | 325 |
| 12954 | Dynasty Blade - Great Gale {PvP} - Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 12955 | Dynasty Blade - Great Gale {PvP} - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 12956 | Dynasty Blade - Great Gale {PvP} - Light | S | lrhand | 1740 | 405 | 151 | 325 |
| 12957 | Dynasty Sword - Earth {PvP} - Focus | S | rhand | 1520 | 333 | 151 | 379 |
| 12958 | Dynasty Sword - Earth {PvP} - Health | S | rhand | 1520 | 333 | 151 | 379 |
| 12959 | Dynasty Sword - Earth {PvP} - Light | S | rhand | 1520 | 333 | 151 | 379 |
| 12972 | Dynasty Phantom - Nature {PvP} - Acumen | S | rhand | 1520 | 267 | 202 | 379 |
| 12973 | Dynasty Phantom - Nature {PvP} - Mana Up | S | rhand | 1520 | 267 | 202 | 379 |
| 12974 | Dynasty Phantom - Nature {PvP} - Conversion | S | rhand | 1520 | 267 | 202 | 379 |
| 14561 | Slasher of Val Turner Family | S | lrhand | 1035 | 376 | 119 | 325 |
| 14562 | Sword of Ashton Family | S | rhand | 975 | 310 | 119 | 379 |
| 14564 | Slasher of Esthus Family | S | lrhand | 1035 | 376 | 119 | 325 |
| 15310 | Sacred Sword of Einhasad | S | rhand | 150 | 7 | 5 | 379 |
| 15313 | Player Commendation - Forgotten Blade - Player Recommendation Weapon | S | rhand | 1300 | 281 | 132 | 379 |
| 15320 | Player Commendation - Heaven's Divider - Player Recommendation Weapon | S | lrhand | 1380 | 342 | 132 | 325 |
| 20165 | Forgotten Blade (Event) - 4-hour limited period | S | rhand | 433 | 281 | 132 | 379 |
| 20166 | Heaven's Divider (Event) - 4-hour limited period | S | lrhand | 460 | 342 | 132 | 325 |
| 21825 | Forgotten Blade of Fortune - 90-day limited period | S | rhand | 1300 | 281 | 132 | 379 |
| 21826 | Heaven's Divider of Fortune - 90-day limited period | S | lrhand | 1380 | 342 | 132 | 325 |
| 21833 | Dynasty Phantom of Fortune - 90-day limited period | S | rhand | 1520 | 267 | 202 | 379 |
| 21837 | Dynasty Sword of Fortune - 90-day limited period | S | rhand | 1520 | 333 | 151 | 379 |
| 21838 | Dynasty Blade of Fortune - 90-day limited period | S | lrhand | 1740 | 405 | 151 | 325 |
| 21959 | Blood Brother | S | lrhand | 1740 | 405 | 151 | 325 |
| 21960 | Blood Brother - Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 21961 | Blood Brother - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 21962 | Blood Brother - Light | S | lrhand | 1740 | 405 | 151 | 325 |
| 21963 | Blood Brother {PvP} - Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 21964 | Blood Brother {PvP} - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 21965 | Blood Brother {PvP} - Light | S | lrhand | 1740 | 405 | 151 | 325 |
| 21966 | Blood Brother - Great Gale | S | lrhand | 1740 | 405 | 151 | 325 |
| 21967 | Blood Brother - Great Gale - Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 21968 | Blood Brother - Great Gale - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 21969 | Blood Brother - Great Gale - Light | S | lrhand | 1740 | 405 | 151 | 325 |
| 21970 | Blood Brother - Great Gale {PvP} - Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 21971 | Blood Brother - Great Gale {PvP} - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 21972 | Blood Brother - Great Gale {PvP} - Light | S | lrhand | 1740 | 405 | 151 | 325 |
| 10215 | Icarus Sawsword | S80 | rhand | 1520 | 363 | 163 | 379 |
| 10217 | Icarus Spirit | S80 | rhand | 1520 | 290 | 217 | 379 |
| 10218 | Icarus Heavy Arms | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 10434 | Icarus Sawsword - Focus | S80 | rhand | 1520 | 363 | 163 | 379 |
| 10435 | Icarus Sawsword - Health | S80 | rhand | 1520 | 363 | 163 | 379 |
| 10436 | Icarus Sawsword - Light | S80 | rhand | 1520 | 363 | 163 | 379 |
| 10437 | Icarus Heavy Arms - Focus | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 10438 | Icarus Heavy Arms - Health | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 10439 | Icarus Heavy Arms - Light | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 10440 | Icarus Spirit - Acumen | S80 | rhand | 1520 | 290 | 217 | 379 |
| 10441 | Icarus Spirit - Mana Up | S80 | rhand | 1520 | 290 | 217 | 379 |
| 10442 | Icarus Spirit - Conversion | S80 | rhand | 1520 | 290 | 217 | 379 |
| 11305 | Icarus Sawsword - Destruction | S80 | rhand | 1520 | 363 | 163 | 379 |
| 11306 | Icarus Sawsword - Destruction - Focus | S80 | rhand | 1520 | 363 | 163 | 379 |
| 11307 | Icarus Sawsword - Destruction - Health | S80 | rhand | 1520 | 363 | 163 | 379 |
| 11308 | Icarus Sawsword - Destruction - Light | S80 | rhand | 1520 | 363 | 163 | 379 |
| 11317 | Icarus Spirit - Nature | S80 | rhand | 1520 | 290 | 217 | 379 |
| 11318 | Icarus Spirit - Nature - Acumen | S80 | rhand | 1520 | 290 | 217 | 379 |
| 11319 | Icarus Spirit - Nature - Mana Up | S80 | rhand | 1520 | 290 | 217 | 379 |
| 11320 | Icarus Spirit - Nature - Conversion | S80 | rhand | 1520 | 290 | 217 | 379 |
| 11341 | Icarus Heavy Arms - Lightning | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 11342 | Icarus Heavy Arms - Lightning - Focus | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 11343 | Icarus Heavy Arms - Lightning - Health | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 11344 | Icarus Heavy Arms - Lightning - Light | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 14363 | Icarus Sawsword {PvP} | S80 | rhand | 1520 | 363 | 163 | 379 |
| 14365 | Icarus Spirit {PvP} | S80 | rhand | 1520 | 290 | 217 | 379 |
| 14366 | Icarus Heavy Arms {PvP} | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 14376 | Icarus Sawsword {PvP} - Focus | S80 | rhand | 1520 | 363 | 163 | 379 |
| 14377 | Icarus Sawsword {PvP} - Health | S80 | rhand | 1520 | 363 | 163 | 379 |
| 14378 | Icarus Sawsword {PvP} - Light | S80 | rhand | 1520 | 363 | 163 | 379 |
| 14379 | Icarus Heavy Arms {PvP} - Focus | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 14380 | Icarus Heavy Arms {PvP} - Health | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 14381 | Icarus Heavy Arms {PvP} - Light | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 14382 | Icarus Spirit {PvP} - Acumen | S80 | rhand | 1520 | 290 | 217 | 379 |
| 14383 | Icarus Spirit {PvP} - Mana Up | S80 | rhand | 1520 | 290 | 217 | 379 |
| 14384 | Icarus Spirit {PvP} - Conversion | S80 | rhand | 1520 | 290 | 217 | 379 |
| 14417 | Icarus Sawsword - Destruction {PvP} | S80 | rhand | 1520 | 363 | 163 | 379 |
| 14418 | Icarus Sawsword - Destruction {PvP} - Focus | S80 | rhand | 1520 | 363 | 163 | 379 |
| 14419 | Icarus Sawsword - Destruction {PvP} - Health | S80 | rhand | 1520 | 363 | 163 | 379 |
| 14420 | Icarus Sawsword - Destruction {PvP} - Light | S80 | rhand | 1520 | 363 | 163 | 379 |
| 14429 | Icarus Spirit - Nature {PvP} | S80 | rhand | 1520 | 290 | 217 | 379 |
| 14430 | Icarus Spirit - Nature {PvP} - Acumen | S80 | rhand | 1520 | 290 | 217 | 379 |
| 14431 | Icarus Spirit - Nature {PvP} - Mana Up | S80 | rhand | 1520 | 290 | 217 | 379 |
| 14432 | Icarus Spirit - Nature {PvP} - Conversion | S80 | rhand | 1520 | 290 | 217 | 379 |
| 14453 | Icarus Heavy Arms - Lightning {PvP} | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 14454 | Icarus Heavy Arms - Lightning {PvP} - Focus | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 14455 | Icarus Heavy Arms - Lightning {PvP} - Health | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 14456 | Icarus Heavy Arms - Lightning {PvP} - Light | S80 | lrhand | 1740 | 442 | 163 | 325 |
| 15280 | Transparent 1HS (for NPC) | S80 | rhand | 1560 | 24 | 17 | 379 |
| 15281 | Transparent 2HS (for NPC) | S80 | lrhand | 2180 | 78 | 39 | 325 |
| 13457 | Vesper Cutter | S84 | rhand | 1520 | 396 | 176 | 379 |
| 13458 | Vesper Slasher | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 13459 | Vesper Buster | S84 | rhand | 1520 | 317 | 234 | 379 |
| 14118 | Vesper Cutter - Haste | S84 | rhand | 1520 | 396 | 176 | 379 |
| 14119 | Vesper Cutter - Health | S84 | rhand | 1520 | 396 | 176 | 379 |
| 14120 | Vesper Cutter - Focus | S84 | rhand | 1520 | 396 | 176 | 379 |
| 14121 | Vesper Slasher - Haste | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14122 | Vesper Slasher - Health | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14123 | Vesper Slasher - Focus | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14124 | Vesper Buster - Mana Up | S84 | rhand | 1520 | 317 | 234 | 379 |
| 14125 | Vesper Buster - Acumen | S84 | rhand | 1520 | 317 | 234 | 379 |
| 14126 | Vesper Buster - Magic Hold | S84 | rhand | 1520 | 317 | 234 | 379 |
| 14463 | Vesper Cutter {PvP} | S84 | rhand | 1520 | 396 | 176 | 379 |
| 14464 | Vesper Slasher {PvP} | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14465 | Vesper Buster {PvP} | S84 | rhand | 1520 | 317 | 234 | 379 |
| 14478 | Vesper Cutter {PvP} - Haste | S84 | rhand | 1520 | 396 | 176 | 379 |
| 14479 | Vesper Cutter {PvP} - Health | S84 | rhand | 1520 | 396 | 176 | 379 |
| 14480 | Vesper Cutter {PvP} - Focus | S84 | rhand | 1520 | 396 | 176 | 379 |
| 14481 | Vesper Slasher {PvP} - Haste | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14482 | Vesper Slasher {PvP} - Health | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14483 | Vesper Slasher {PvP} - Focus | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14484 | Vesper Buster {PvP} - Mana Up | S84 | rhand | 1520 | 317 | 234 | 379 |
| 14485 | Vesper Buster {PvP} - Acumen | S84 | rhand | 1520 | 317 | 234 | 379 |
| 14486 | Vesper Buster {PvP} - Magic Hold | S84 | rhand | 1520 | 317 | 234 | 379 |
| 15544 | Eternal Core Sword | S84 | rhand | 1520 | 437 | 192 | 379 |
| 15548 | Lava Saw | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15553 | Archangel Sword | S84 | rhand | 1520 | 350 | 256 | 379 |
| 15558 | Periel Sword | S84 | rhand | 1520 | 415 | 183 | 379 |
| 15562 | Feather Eye Blade | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15567 | Veniplant Sword | S84 | rhand | 1520 | 332 | 244 | 379 |
| 15676 | Triumph Blade | S84 | rhand | 1520 | 396 | 183 | 379 |
| 15680 | Triumph Two Hand Sword | S84 | lrhand | 1740 | 482 | 183 | 325 |
| 15685 | Triumph Magic Sword | S84 | rhand | 1520 | 317 | 244 | 379 |
| 15829 | Periel Sword - Health | S84 | rhand | 1520 | 415 | 183 | 379 |
| 15830 | Periel Sword - Focus | S84 | rhand | 1520 | 415 | 183 | 379 |
| 15831 | Periel Sword - Haste | S84 | rhand | 1520 | 415 | 183 | 379 |
| 15841 | Feather Eye Blade - Health | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15842 | Feather Eye Blade - Focus | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15843 | Feather Eye Blade - Haste | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15856 | Veniplant Sword - Acumen | S84 | rhand | 1520 | 332 | 244 | 379 |
| 15857 | Veniplant Sword - Magic Hold | S84 | rhand | 1520 | 332 | 244 | 379 |
| 15858 | Veniplant Sword - Mana Up | S84 | rhand | 1520 | 332 | 244 | 379 |
| 15871 | Eternal Core Sword - Focus | S84 | rhand | 1520 | 437 | 192 | 379 |
| 15872 | Eternal Core Sword - Haste | S84 | rhand | 1520 | 437 | 192 | 379 |
| 15873 | Eternal Core Sword - Health | S84 | rhand | 1520 | 437 | 192 | 379 |
| 15883 | Lava Saw - Focus | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15884 | Lava Saw - Haste | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15885 | Lava Saw - Health | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15898 | Archangel Sword - Magic Hold | S84 | rhand | 1520 | 350 | 256 | 379 |
| 15899 | Archangel Sword - Mana Up | S84 | rhand | 1520 | 350 | 256 | 379 |
| 15900 | Archangel Sword - Acumen | S84 | rhand | 1520 | 350 | 256 | 379 |
| 15913 | Eternal Core Sword {PvP} | S84 | rhand | 1520 | 437 | 192 | 379 |
| 15917 | Lava Saw {PvP} | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15922 | Archangel Sword {PvP} | S84 | rhand | 1520 | 350 | 256 | 379 |
| 15927 | Periel Sword {PvP} | S84 | rhand | 1520 | 415 | 183 | 379 |
| 15931 | Feather Eye Blade {PvP} | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15936 | Veniplant Sword {PvP} | S84 | rhand | 1520 | 332 | 244 | 379 |
| 15941 | Periel Sword {PvP} - Health | S84 | rhand | 1520 | 415 | 183 | 379 |
| 15942 | Periel Sword {PvP} - Focus | S84 | rhand | 1520 | 415 | 183 | 379 |
| 15943 | Periel Sword {PvP} - Haste | S84 | rhand | 1520 | 415 | 183 | 379 |
| 15953 | Feather Eye Blade {PvP} - Health | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15954 | Feather Eye Blade {PvP} - Focus | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15955 | Feather Eye Blade {PvP} - Haste | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15968 | Veniplant Sword {PvP} - Acumen | S84 | rhand | 1520 | 332 | 244 | 379 |
| 15969 | Veniplant Sword {PvP} - Magic Hold | S84 | rhand | 1520 | 332 | 244 | 379 |
| 15970 | Veniplant Sword {PvP} - Mana Up | S84 | rhand | 1520 | 332 | 244 | 379 |
| 15983 | Eternal Core Sword {PvP} - Focus | S84 | rhand | 1520 | 437 | 192 | 379 |
| 15984 | Eternal Core Sword {PvP} - Haste | S84 | rhand | 1520 | 437 | 192 | 379 |
| 15985 | Eternal Core Sword {PvP} - Health | S84 | rhand | 1520 | 437 | 192 | 379 |
| 15995 | Lava Saw {PvP} - Focus | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15996 | Lava Saw {PvP} - Haste | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15997 | Lava Saw {PvP} - Health | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 16010 | Archangel Sword {PvP} - Magic Hold | S84 | rhand | 1520 | 350 | 256 | 379 |
| 16011 | Archangel Sword {PvP} - Mana Up | S84 | rhand | 1520 | 350 | 256 | 379 |
| 16012 | Archangel Sword {PvP} - Acumen | S84 | rhand | 1520 | 350 | 256 | 379 |
| 16042 | Vesper Cutter - Thunder | S84 | rhand | 1520 | 396 | 176 | 379 |
| 16043 | Vesper Slasher - Gale | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16044 | Vesper Buster - Cleverness | S84 | rhand | 1520 | 317 | 234 | 379 |
| 16056 | Vesper Cutter - Thunder - Haste | S84 | rhand | 1520 | 396 | 176 | 379 |
| 16057 | Vesper Cutter - Thunder - Health | S84 | rhand | 1520 | 396 | 176 | 379 |
| 16058 | Vesper Cutter - Thunder - Focus | S84 | rhand | 1520 | 396 | 176 | 379 |
| 16059 | Vesper Slasher - Gale - Haste | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16060 | Vesper Slasher - Gale - Health | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16061 | Vesper Slasher - Gale - Focus | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16062 | Vesper Buster - Cleverness - Mana Up | S84 | rhand | 1520 | 317 | 234 | 379 |
| 16063 | Vesper Buster - Cleverness - Acumen | S84 | rhand | 1520 | 317 | 234 | 379 |
| 16064 | Vesper Buster - Cleverness - Magic Hold | S84 | rhand | 1520 | 317 | 234 | 379 |
| 16134 | Vesper Cutter- Thunder {PvP} | S84 | rhand | 1520 | 396 | 176 | 379 |
| 16135 | Vesper Slasher- Gale {PvP} | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16136 | Vesper Buster - Cleverness {PvP} | S84 | rhand | 1520 | 317 | 234 | 379 |
| 16179 | Vesper Cutter- Thunder {PvP} - Haste | S84 | rhand | 1520 | 396 | 176 | 379 |
| 16180 | Vesper Cutter- Thunder {PvP} - Health | S84 | rhand | 1520 | 396 | 176 | 379 |
| 16181 | Vesper Cutter- Thunder {PvP} - Focus | S84 | rhand | 1520 | 396 | 176 | 379 |
| 16182 | Vesper Slasher- Gale {PvP} - Haste | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16183 | Vesper Slasher- Gale {PvP} - Health | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16184 | Vesper Slasher- Gale {PvP} - Focus | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16185 | Vesper Buster - Cleverness {PvP} - Mana Up | S84 | rhand | 1520 | 317 | 234 | 379 |
| 16186 | Vesper Buster - Cleverness {PvP} - Acumen | S84 | rhand | 1520 | 317 | 234 | 379 |
| 16187 | Vesper Buster - Cleverness {PvP} - Magic Hold | S84 | rhand | 1520 | 317 | 234 | 379 |
| 21919 | Hellblade | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21920 | Hellblade - Haste | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21921 | Hellblade - Health | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21922 | Hellblade - Focus | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21923 | Hellblade {PvP} | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21924 | Hellblade {PvP} - Haste | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21925 | Hellblade {PvP} - Health | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21926 | Hellblade {PvP} - Focus | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21927 | Hellblade - Lightning | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21928 | Hellblade - Lightning - Haste | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21929 | Hellblade - Lightning - Health | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21930 | Hellblade - Lightning - Focus | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21931 | Hellblade - Lightning {PvP} | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21932 | Hellblade - Lightning {PvP} - Haste | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21933 | Hellblade - Lightning {PvP} - Health | S84 | rhand | 1520 | 396 | 176 | 379 |
| 21934 | Hellblade - Lightning {PvP} - Focus | S84 | rhand | 1520 | 396 | 176 | 379 |

### BLUNT (898)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 4 | Club | NONE | rhand | 1870 | 8 | 6 | 379 |
| 5 | Mace | NONE | rhand | 1880 | 11 | 9 | 379 |
| 6 | Apprentice's Wand | NONE | rhand | 1350 | 5 | 7 | 379 |
| 7 | Apprentice's Rod | NONE | rhand | 1330 | 6 | 8 | 379 |
| 8 | Willow Staff | NONE | lrhand | 1080 | 11 | 13 | 325 |
| 9 | Cedar Staff | NONE | lrhand | 1090 | 16 | 18 | 325 |
| 87 | Iron Hammer | NONE | rhand | 1850 | 31 | 21 | 379 |
| 152 | Heavy Chisel | NONE | rhand | 1890 | 10 | 8 | 379 |
| 153 | Sigil | NONE | rhand | 1850 | 12 | 9 | 379 |
| 154 | Dwarven Mace | NONE | rhand | 1860 | 17 | 12 | 379 |
| 155 | Flanged Mace | NONE | rhand | 1800 | 31 | 21 | 379 |
| 176 | Apprentice's Staff | NONE | lrhand | 1070 | 23 | 24 | 325 |
| 177 | Mage Staff | NONE | lrhand | 1050 | 30 | 31 | 325 |
| 744 | Staff of Sentinel | NONE | lrhand | 1800 | 13 | 15 | 325 |
| 747 | Wand of Adept | NONE | rhand | 1300 | 11 | 13 | 379 |
| 748 | Gallint's Oak Wand | NONE | lrhand | 1350 | 10 | 11 | 325 |
| 754 | Red Sunset Staff | NONE | lrhand | 1700 | 13 | 14 | 325 |
| 1300 | Apprentice's Rod | NONE | rhand | 80 | 22 | 6 | 379 |
| 1301 | Big Hammer | NONE | rhand | 300 | 22 | 6 | 379 |
| 1304 | Conjuror's Staff | NONE | lrhand | 150 | 15 | 17 | 325 |
| 1511 | Silversmith Hammer | NONE | rhand | 1860 | 13 | 10 | 379 |
| 2370 | Guild Member's Club | NONE | rhand | 1910 | 6 | 5 | 379 |
| 2373 | Eldritch Staff | NONE | lrhand | 1050 | 13 | 13 | 325 |
| 2501 | Bone Club | NONE | rhand | 1850 | 24 | 17 | 379 |
| 4221 | Ubiquitous Axe | NONE | rhand | 1850 | 31 | 21 | 379 |
| 6355 | Mage Staff - for Beginners | NONE | lrhand | 1050 | 30 | 31 | 325 |
| 6716 | Monster Only(Silenos Shaman) | NONE | lrhand | 1080 | 11 | 12 | 325 |
| 6718 | Monster Only(Einhasad Shaman) | NONE | lrhand | 1560 | 24 | 17 | 325 |
| 7058 | Chrono Darbuka | NONE | lrhand | 0 | 1 | 1 | 325 |
| 7816 | Apprentice Adventurer's Staff | NONE | lrhand | 1070 | 23 | 24 | 325 |
| 7817 | Apprentice Adventurer's Bone Club | NONE | rhand | 1850 | 24 | 17 | 379 |
| 8212 | Monster Only (Solina Brother Mace) | NONE | rhand | 1570 |  |  | 379 |
| 8213 | Monster Only (Solina Father Mace) | NONE | rhand | 1570 |  |  | 379 |
| 8218 | Monster Only (Zombie Laborer Axe) | NONE | rhand | 1570 |  |  | 379 |
| 8576 | Apprentice's Staff (Event) | NONE | lrhand | 1070 | 23 | 24 | 325 |
| 8577 | Bone Club (Event) | NONE | rhand | 1850 | 24 | 17 | 379 |
| 8974 | Shadow Item: Iron Hammer | NONE | rhand | 617 | 31 | 21 | 379 |
| 8976 | Shadow Item: Flanged Mace | NONE | rhand | 600 | 31 | 21 | 379 |
| 8977 | Shadow Item: Mage Staff | NONE | lrhand | 350 | 30 | 31 | 325 |
| 9903 | Improved Iron Hammer | NONE | rhand | 1850 | 31 | 21 | 379 |
| 9907 | Improved Flanged Mace | NONE | rhand | 1800 | 31 | 21 | 379 |
| 9908 | Improved Mage Staff | NONE | lrhand | 1050 | 30 | 31 | 325 |
| 10474 | Shadow Item - Apprentice's Staff | NONE | lrhand | 1070 | 23 | 24 | 325 |
| 10475 | Shadow Item - Bone Club | NONE | rhand | 1850 | 24 | 17 | 379 |
| 13061 | Exclusive to Monsters (Baroness' Employee) | NONE | rhand | 1080 | 267 | 202 | 379 |
| 13155 | Player Commendation - Iron Hammer - Player Commendation Weapon | NONE | rhand | 1850 | 31 | 21 | 379 |
| 13157 | Player Commendation - Flanged Mace - Player Commendation Weapon | NONE | rhand | 1800 | 31 | 21 | 379 |
| 13158 | Player Commendation - Mage's Wand - Player Commendation Weapon | NONE | lrhand | 1050 | 30 | 31 | 325 |
| 13539 | Staff of Master Yogi | NONE | lrhand | 10 | 11 | 12 | 325 |
| 13981 | Exclusive to Monsters (Mounted Troops Tactics) | NONE | lrhand | 1080 | 11 | 12 | 325 |
| 14623 | Santa Claus' Barakiel Axe | NONE | rhand | 1550 | 51 | 38 | 379 |
| 14624 | Santa Claus' Behemoth Tuning Fork | NONE | lrhand | 1890 | 62 | 38 | 325 |
| 14630 | Santa Claus' Hand of Cabrio | NONE | rhand | 1510 | 50 | 51 | 379 |
| 14631 | Santa Claus' Daimon Crystal | NONE | lrhand | 880 | 62 | 56 | 325 |
| 14783 | Baguette's Mace | NONE | rhand | 1640 |  |  |  |
| 14789 | Baguette's Staff | NONE | rhand | 990 |  |  |  |
| 14790 | Baguette's Two-handed Staff | NONE | lrhand | 340 |  |  |  |
| 20258 | Baguette Mace - 7-day limited period | NONE | rhand | 500 | 1 | 2 | 379 |
| 20259 | Baguette Heavy Hammer - 7-day limited period | NONE | lrhand | 500 | 1 | 2 | 325 |
| 20264 | Baguette Staff - 7-day limited period | NONE | rhand | 500 | 1 | 2 | 379 |
| 20265 | Baguette Great Staff - 7-day limited period | NONE | lrhand | 500 | 1 | 2 | 325 |
| 20600 | Twilight Staff - Dance of Shadow - 7-day limited period | NONE | lrhand | 0 | 1 | 1 | 379 |
| 86 | Tomahawk | D | rhand | 1780 | 51 | 32 | 379 |
| 88 | Morning Star | D | rhand | 1720 | 79 | 47 | 379 |
| 90 | Goat Head Staff | D | lrhand | 1000 | 77 | 69 | 325 |
| 156 | Hand Axe | D | rhand | 1820 | 40 | 26 | 379 |
| 157 | Spiked Club | D | rhand | 1750 | 64 | 39 | 379 |
| 158 | Tarbar | D | rhand | 1730 | 79 | 47 | 379 |
| 159 | Bonebreaker | D | rhand | 1720 | 92 | 54 | 379 |
| 166 | Heavy Mace | D | rhand | 1800 | 40 | 26 | 379 |
| 167 | Scalpel | D | rhand | 1810 | 40 | 26 | 379 |
| 168 | Work Hammer | D | rhand | 1790 | 40 | 26 | 379 |
| 169 | Skull Breaker | D | rhand | 1740 | 79 | 47 | 379 |
| 172 | Heavy Bone Club | D | rhand | 1730 | 79 | 47 | 379 |
| 178 | Bone Staff | D | lrhand | 1060 | 39 | 39 | 325 |
| 179 | Mace of Prayer | D | rhand | 1300 | 41 | 43 | 379 |
| 180 | Mace of Judgment | D | rhand | 1280 | 41 | 43 | 379 |
| 181 | Mace of Miracle | D | rhand | 1250 | 41 | 43 | 379 |
| 182 | Doom Hammer | D | rhand | 1200 | 41 | 43 | 379 |
| 183 | Mystic Staff | D | lrhand | 1040 | 50 | 47 | 325 |
| 184 | Conjuror's Staff | D | lrhand | 1030 | 50 | 47 | 325 |
| 185 | Staff of Mana | D | lrhand | 1040 | 50 | 47 | 325 |
| 186 | Staff of Magic | D | lrhand | 1020 | 62 | 57 | 325 |
| 187 | Atuba Hammer | D | lrhand | 1010 | 90 | 79 | 325 |
| 188 | Ghost Staff | D | lrhand | 1000 | 90 | 79 | 325 |
| 189 | Staff of Life | D | rhand | 1180 | 74 | 72 | 379 |
| 190 | Atuba Mace | D | lrhand | 1010 | 90 | 79 | 325 |
| 749 | 0 | D | lrhand | 100 | 21 | 32 | 325 |
| 7822 | Traveler's Mace | D | rhand | 1300 | 41 | 43 | 379 |
| 7825 | Traveler's Staff | D | lrhand | 1040 | 50 | 47 | 325 |
| 7829 | Traveler's Tomahawk | D | rhand | 1780 | 51 | 32 | 379 |
| 7890 | Priest Mace | D | rhand | 1720 | 63 | 63 | 379 |
| 7896 | Titan Hammer | D | lrhand | 2100 | 96 | 47 | 325 |
| 8528 | For Monsters Only (Doom Hammer) | D | rhand | 1200 | 41 | 43 | 379 |
| 8531 | For Monsters Only (Bone Staff) | D | lrhand | 1060 | 39 | 35 | 325 |
| 8582 | Mace of Prayer (Event) | D | rhand | 1300 | 41 | 43 | 379 |
| 8585 | Staff of Mana (Event) | D | lrhand | 1040 | 50 | 47 | 325 |
| 8589 | Tomahawk (Event) | D | rhand | 1780 | 51 | 32 | 379 |
| 8823 | Shadow Item: Spiked Club | D | rhand | 590 | 64 | 39 | 379 |
| 8824 | Shadow Item: Staff of Magic | D | lrhand | 340 | 62 | 57 | 325 |
| 8984 | Shadow Item: Spiked Club | D | rhand | 590 | 64 | 39 | 379 |
| 8985 | Shadow Item: Staff of Magic | D | lrhand | 340 | 62 | 57 | 325 |
| 11610 | Common Item - Bone Staff | D | lrhand | 353 | 39 | 39 | 325 |
| 11615 | Common Item - Scalpel | D | rhand | 603 | 40 | 26 | 379 |
| 11618 | Common Item - Work Hammer | D | rhand | 597 | 40 | 26 | 379 |
| 11623 | Common Item - Hand Axe | D | rhand | 607 | 40 | 26 | 379 |
| 11626 | Common Item - Heavy Mace | D | rhand | 600 | 40 | 26 | 379 |
| 11627 | Common Item - Mace of Prayer | D | rhand | 433 | 41 | 43 | 379 |
| 11630 | Common Item - Doom Hammer | D | rhand | 400 | 41 | 43 | 379 |
| 11633 | Common Item - Staff of Mana | D | lrhand | 347 | 50 | 47 | 325 |
| 11634 | Common Item - Mystic Staff | D | lrhand | 347 | 50 | 47 | 325 |
| 11638 | Common Item - Mace of Judgment | D | rhand | 427 | 41 | 43 | 379 |
| 11641 | Common Item - Mace of Miracle | D | rhand | 417 | 41 | 43 | 379 |
| 11644 | Common Item - Conjuror's Staff | D | lrhand | 343 | 50 | 47 | 325 |
| 11645 | Common Item - Tomahawk | D | rhand | 593 | 51 | 32 | 379 |
| 11663 | Common Item - Staff of Magic | D | lrhand | 340 | 62 | 57 | 325 |
| 11666 | Common Item - Spiked Club | D | rhand | 583 | 64 | 39 | 379 |
| 11686 | Common Item - Morning Star | D | rhand | 573 | 79 | 47 | 379 |
| 11692 | Common Item - Priest Mace | D | rhand | 573 | 63 | 63 | 379 |
| 11693 | Common Item - Goat Head Staff | D | lrhand | 333 | 77 | 69 | 325 |
| 11697 | Common Item - Skull Breaker | D | rhand | 580 | 79 | 47 | 379 |
| 11708 | Common Item - Tarbar | D | rhand | 577 | 79 | 47 | 379 |
| 11711 | Common Item - Titan Hammer | D | lrhand | 700 | 96 | 47 | 325 |
| 11713 | Common Item - Heavy Bone Club | D | rhand | 577 | 79 | 47 | 379 |
| 11727 | Common Item - Bonebreaker | D | rhand | 573 | 92 | 54 | 379 |
| 11729 | Common Item - Staff of Life | D | rhand | 393 | 74 | 72 | 379 |
| 11731 | Common Item - Atuba Mace | D | lrhand | 337 | 90 | 79 | 325 |
| 11732 | Common Item - Atuba Hammer | D | lrhand | 337 | 90 | 79 | 325 |
| 11737 | Common Item - Ghost Staff | D | lrhand | 333 | 90 | 79 | 325 |
| 13165 | Player Commendation - Bonebreaker - Player Commendation Weapon | D | rhand | 1720 | 92 | 54 | 379 |
| 13166 | Player Commendation - Atuba Hammer - Player Commendation Weapon | D | lrhand | 1010 | 90 | 79 | 325 |
| 13167 | Player Commendation - Ghost's Wand - Player Commendation Weapon | D | lrhand | 1000 | 90 | 79 | 325 |
| 13168 | Player Commendation - Hall of Life - Player Commendation Weapon | D | rhand | 1180 | 74 | 79 | 379 |
| 13169 | Player Commendation - Atuba Mace - Player Commendation Weapon | D | lrhand | 1010 | 90 | 79 | 325 |
| 15035 | Fortune Staff of Life - 30-day limited period | D | rhand | 1180 | 74 | 72 | 379 |
| 15047 | Bonebreaker of Fortune - 30-day limited period | D | rhand | 1720 | 92 | 54 | 379 |
| 15149 | Fortune Staff of Life - 10-day limited period | D | rhand | 1180 | 74 | 72 | 379 |
| 15161 | Bonebreaker of Fortune - 10-day limited period | D | rhand | 1720 | 92 | 54 | 379 |
| 16923 | Fortune Staff of Life - 90-day limited period | D | rhand | 1180 | 74 | 72 | 379 |
| 16935 | Bonebreaker of Fortune - 90-day limited period | D | rhand | 1720 | 92 | 54 | 379 |
| 20112 | Tarbar (Event) - 4-hour limited period | D | rhand | 577 | 79 | 47 | 379 |
| 20113 | Titan Hammer (Event) - 4-hour limited period | D | lrhand | 700 | 96 | 47 | 325 |
| 20114 | Priest Mace (Event) - 4-hour limited period | D | rhand | 573 | 63 | 63 | 379 |
| 20115 | Goat Head Staff (Event) - 4-hour limited period | D | lrhand | 333 | 77 | 63 | 325 |
| 20649 | Common Item - Ghost Staff | D | lrhand | 100 | 90 | 79 | 325 |
| 21734 | Priest Mace - Event | D | rhand | 1720 | 63 | 63 | 379 |
| 21735 | Tarbar - Event | D | rhand | 1730 | 79 | 47 | 379 |
| 21736 | Goat Head Staff - Event | D | lrhand | 1000 | 77 | 69 | 325 |
| 21737 | Titan Hammer - Event | D | lrhand | 2100 | 96 | 47 | 325 |
| 89 | Big Hammer | C | rhand | 1710 | 107 | 61 | 379 |
| 160 | Battle Axe | C | rhand | 1720 | 107 | 61 | 379 |
| 161 | Silver Axe | C | rhand | 1690 | 107 | 61 | 379 |
| 162 | War Axe | C | rhand | 1660 | 139 | 76 | 379 |
| 173 | Skull Graver | C | rhand | 1640 | 107 | 61 | 379 |
| 174 | Nirvana Axe | C | rhand | 1150 | 111 | 101 | 379 |
| 191 | Heavy Doom Hammer | C | lrhand | 1020 | 103 | 89 | 325 |
| 192 | Crystal Staff | C | lrhand | 1020 | 103 | 89 | 325 |
| 193 | Stick of Faith | C | rhand | 1160 | 85 | 81 | 379 |
| 194 | Heavy Doom Axe | C | lrhand | 1010 | 103 | 89 | 325 |
| 195 | Cursed Staff | C | lrhand | 1000 | 119 | 100 | 325 |
| 196 | Stick of Eternity | C | rhand | 1130 | 111 | 101 | 379 |
| 197 | Paradia Staff | C | lrhand | 1010 | 135 | 111 | 325 |
| 198 | Inferno Staff | C | lrhand | 1000 | 135 | 111 | 325 |
| 199 | Pa'agrian Hammer | C | lrhand | 1010 | 135 | 111 | 325 |
| 200 | Sage's Staff | C | lrhand | 1000 | 135 | 111 | 325 |
| 201 | Club of Nature | C | rhand | 1100 | 111 | 101 | 379 |
| 202 | Mace of Underworld | C | rhand | 1090 | 111 | 101 | 379 |
| 203 | Pa'agrian Axe | C | lrhand | 990 | 141 | 114 | 325 |
| 204 | Deadman's Staff | C | lrhand | 1010 | 152 | 122 | 325 |
| 205 | Ghoul's Staff | C | lrhand | 1000 | 152 | 122 | 325 |
| 206 | Demon's Staff | C | lrhand | 990 | 152 | 122 | 325 |
| 2502 | Dwarven War Hammer | C | rhand | 1670 | 122 | 68 | 379 |
| 2503 | Yaksa Mace | C | rhand | 1640 | 156 | 83 | 379 |
| 4726 | Big Hammer - Health | C | rhand | 1710 | 107 | 61 | 379 |
| 4727 | Big Hammer - Rsk. Focus | C | rhand | 1710 | 107 | 61 | 379 |
| 4728 | Big Hammer - Haste | C | rhand | 1710 | 107 | 61 | 379 |
| 4729 | Battle Axe - Anger | C | rhand | 1720 | 107 | 61 | 379 |
| 4730 | Battle Axe - Rsk. Focus | C | rhand | 1720 | 107 | 61 | 379 |
| 4731 | Battle Axe - Haste | C | rhand | 1720 | 107 | 61 | 379 |
| 4732 | Silver Axe - Anger | C | rhand | 1690 | 107 | 61 | 379 |
| 4733 | Silver Axe - Rsk. Focus | C | rhand | 1690 | 107 | 61 | 379 |
| 4734 | Silver Axe - Haste | C | rhand | 1690 | 107 | 61 | 379 |
| 4735 | Skull Graver - Anger | C | rhand | 1640 | 107 | 61 | 379 |
| 4736 | Skull Graver - Health | C | rhand | 1640 | 107 | 61 | 379 |
| 4737 | Skull Graver - Rsk. Focus | C | rhand | 1640 | 107 | 61 | 379 |
| 4738 | Dwarven War Hammer - Anger | C | rhand | 1670 | 122 | 68 | 379 |
| 4739 | Dwarven War Hammer - Health | C | rhand | 1670 | 122 | 68 | 379 |
| 4740 | Dwarven War Hammer - Haste | C | rhand | 1670 | 122 | 68 | 379 |
| 4741 | War Axe - Anger | C | rhand | 1660 | 139 | 76 | 379 |
| 4742 | War Axe - Health | C | rhand | 1660 | 139 | 76 | 379 |
| 4743 | War Axe - Haste | C | rhand | 1660 | 139 | 76 | 379 |
| 4744 | Yaksa Mace - Anger | C | rhand | 1640 | 156 | 83 | 379 |
| 4745 | Yaksa Mace - Health | C | rhand | 1640 | 156 | 83 | 379 |
| 4746 | Yaksa Mace - Rsk. Focus | C | rhand | 1640 | 156 | 83 | 379 |
| 4864 | Heavy Doom Hammer - Magic Regeneration | C | lrhand | 1020 | 103 | 89 | 325 |
| 4865 | Heavy Doom Hammer - Mental Shield | C | lrhand | 1020 | 103 | 89 | 325 |
| 4866 | Heavy Doom Hammer - Magic Hold | C | lrhand | 1020 | 103 | 89 | 325 |
| 4867 | Crystal Staff - Rsk. Evasion | C | lrhand | 1020 | 103 | 89 | 325 |
| 4868 | Crystal Staff - Mana Up | C | lrhand | 1020 | 103 | 89 | 325 |
| 4869 | Crystal Staff - Blessed Body | C | lrhand | 1020 | 103 | 89 | 325 |
| 4870 | Heavy Doom Axe - Magic Poison | C | lrhand | 1010 | 103 | 89 | 325 |
| 4871 | Heavy Doom Axe - Magic Weakness | C | lrhand | 1010 | 103 | 89 | 325 |
| 4872 | Heavy Doom Axe - Magic Chaos | C | lrhand | 1010 | 103 | 89 | 325 |
| 4873 | Cursed Staff - Magic Hold | C | lrhand | 1000 | 119 | 100 | 325 |
| 4874 | Cursed Staff - Magic Poison | C | lrhand | 1000 | 119 | 100 | 325 |
| 4875 | Cursed Staff - Magic Weakness | C | lrhand | 1000 | 119 | 100 | 325 |
| 4876 | Paradia Staff - Magic Regeneration | C | lrhand | 1010 | 135 | 111 | 325 |
| 4877 | Paradia Staff - Mental Shield | C | lrhand | 1010 | 135 | 111 | 325 |
| 4878 | Paradia Staff - Magic Hold | C | lrhand | 1010 | 135 | 111 | 325 |
| 4879 | Pa'agrian Hammer - Rsk. Evasion | C | lrhand | 1010 | 135 | 111 | 325 |
| 4880 | Pa'agrian Hammer - Magic Poison | C | lrhand | 1010 | 135 | 111 | 325 |
| 4881 | Pa'agrian Hammer - Magic Weakness | C | lrhand | 1010 | 135 | 111 | 325 |
| 4882 | Sage's Staff - Magic Hold | C | lrhand | 1000 | 135 | 111 | 325 |
| 4883 | Sage's Staff - Magic Poison | C | lrhand | 1000 | 135 | 111 | 325 |
| 4884 | Sage's Staff - Magic Weakness | C | lrhand | 1000 | 135 | 111 | 325 |
| 4885 | Pa'agrian Axe - Mana Up | C | lrhand | 990 | 141 | 114 | 325 |
| 4886 | Pa'agrian Axe - Magic Weakness | C | lrhand | 990 | 141 | 114 | 325 |
| 4887 | Pa'agrian Axe - Magic Chaos | C | lrhand | 990 | 141 | 114 | 325 |
| 4888 | Deadman's Staff - Magic Regeneration | C | lrhand | 1010 | 152 | 122 | 325 |
| 4889 | Deadman's Staff - Mental Shield | C | lrhand | 1010 | 152 | 122 | 325 |
| 4890 | Deadman's Staff - Magic Hold | C | lrhand | 1010 | 152 | 122 | 325 |
| 4891 | Ghoul's Staff - Rsk. Evasion | C | lrhand | 1000 | 152 | 122 | 325 |
| 4892 | Ghoul's Staff - Mana Up | C | lrhand | 1000 | 152 | 122 | 325 |
| 4893 | Ghoul's Staff - Blessed Body | C | lrhand | 1000 | 152 | 122 | 325 |
| 4894 | Demon's Staff - Magic Poison | C | lrhand | 990 | 152 | 122 | 325 |
| 4895 | Demon's Staff - Magic Weakness | C | lrhand | 990 | 152 | 122 | 325 |
| 4896 | Demon's Staff - Magic Chaos | C | lrhand | 990 | 152 | 122 | 325 |
| 6719 | Monster Only(Ketra Orc Chieftain) | C | lrhand | 990 | 141 | 104 | 325 |
| 7701 | Stick of Faith - Mana Up | C | rhand | 1160 | 85 | 81 | 379 |
| 7702 | Stick of Faith - Magic Hold | C | rhand | 1160 | 85 | 81 | 379 |
| 7703 | Stick of Faith - Magic Shield | C | rhand | 1160 | 85 | 81 | 379 |
| 7704 | Stick of Eternity - Empower | C | rhand | 1130 | 111 | 101 | 379 |
| 7705 | Stick of Eternity - Rsk. Evasion | C | rhand | 1130 | 111 | 101 | 379 |
| 7706 | Stick of Eternity - Blessed Body | C | rhand | 1130 | 111 | 101 | 379 |
| 7707 | Nirvana Axe - M. Atk. | C | rhand | 1150 | 111 | 101 | 379 |
| 7708 | Nirvana Axe - Magic Poison | C | rhand | 1150 | 111 | 101 | 379 |
| 7709 | Nirvana Axe - Magic Weakness | C | rhand | 1150 | 111 | 101 | 379 |
| 7710 | Club of Nature - Acumen | C | rhand | 1100 | 111 | 101 | 379 |
| 7711 | Club of Nature - Mental Shield | C | rhand | 1100 | 111 | 101 | 379 |
| 7712 | Club of Nature - Magic Hold | C | rhand | 1100 | 111 | 101 | 379 |
| 7713 | Mace of Underworld - Mana Up | C | rhand | 1090 | 111 | 101 | 379 |
| 7714 | Mace of Underworld - Magic Silence | C | rhand | 1090 | 111 | 101 | 379 |
| 7715 | Mace of Underworld - Conversion | C | rhand | 1090 | 111 | 101 | 379 |
| 7716 | Inferno Staff - Acumen | C | lrhand | 1000 | 135 | 111 | 325 |
| 7717 | Inferno Staff - Magic Silence | C | lrhand | 1000 | 135 | 111 | 325 |
| 7718 | Inferno Staff - Magic Paralyze | C | lrhand | 1000 | 135 | 111 | 325 |
| 7891 | Ecliptic Axe | C | rhand | 1640 | 125 | 111 | 379 |
| 7897 | Dwarven Hammer | C | lrhand | 2010 | 190 | 83 | 325 |
| 7898 | Karik Horn | C | lrhand | 2020 | 169 | 76 | 325 |
| 8120 | Dwarven Hammer - Health | C | lrhand | 2010 | 190 | 83 | 325 |
| 8121 | Dwarven Hammer - Anger | C | lrhand | 2010 | 190 | 83 | 325 |
| 8122 | Dwarven Hammer - Critical Bleed | C | lrhand | 2010 | 190 | 83 | 325 |
| 8123 | Karik Horn - Focus | C | lrhand | 2020 | 169 | 76 | 325 |
| 8124 | Karik Horn - Haste | C | lrhand | 2020 | 169 | 76 | 325 |
| 8125 | Karik Horn - Critical Drain | C | lrhand | 2020 | 169 | 76 | 325 |
| 8138 | Ecliptic Axe - Conversion | C | rhand | 1640 | 125 | 111 | 379 |
| 8139 | Ecliptic Axe - M. Atk. | C | rhand | 1640 | 125 | 111 | 379 |
| 8140 | Ecliptic Axe - Magic Hold | C | rhand | 1640 | 125 | 111 | 379 |
| 8832 | Shadow Item: Cursed Staff | C | lrhand | 340 | 119 | 100 | 325 |
| 8836 | Shadow Item: Dwarven War Hammer | C | rhand | 560 | 122 | 68 | 379 |
| 8841 | Shadow Item: Stick of Eternity | C | rhand | 380 | 111 | 101 | 379 |
| 8842 | Shadow Item: Inferno Staff | C | lrhand | 340 | 135 | 111 | 325 |
| 8843 | Shadow Item: Pa'agrian Hammer | C | lrhand | 340 | 135 | 111 | 325 |
| 8928 | Shadow Item: Stick of Eternity | C | rhand | 380 | 111 | 101 | 379 |
| 8929 | Shadow Item: Inferno Staff | C | lrhand | 340 | 135 | 111 | 325 |
| 8930 | Shadow Item: Pa'agrian Hammer | C | lrhand | 340 | 135 | 111 | 325 |
| 8993 | Shadow Item: Stick of Eternity | C | rhand | 380 | 111 | 101 | 379 |
| 8994 | Shadow Item: Inferno Staff | C | lrhand | 340 | 135 | 111 | 325 |
| 8995 | Shadow Item: Pa'agrian Hammer | C | lrhand | 340 | 135 | 111 | 325 |
| 10011 | Shadow Item - War Axe | C | rhand | 533 | 139 | 76 | 379 |
| 10125 | Shadow Item - War Axe | C | rhand | 533 | 139 | 76 | 379 |
| 11750 | Common Item - Battle Axe | C | rhand | 573 | 107 | 61 | 379 |
| 11755 | Common Item - Skull Graver | C | rhand | 547 | 107 | 61 | 379 |
| 11757 | Common Item - Stick of Faith | C | rhand | 387 | 85 | 81 | 379 |
| 11761 | Common Item - Silver Axe | C | rhand | 563 | 107 | 61 | 379 |
| 11764 | Common Item - Crystal Staff | C | lrhand | 340 | 103 | 89 | 325 |
| 11765 | Common Item - Big Hammer | C | rhand | 570 | 107 | 61 | 379 |
| 11767 | Common Item - Heavy Doom Axe | C | lrhand | 337 | 103 | 89 | 325 |
| 11768 | Common Item - Heavy Doom Hammer | C | lrhand | 340 | 103 | 89 | 325 |
| 11777 | Common Item - Dwarven War Hammer | C | rhand | 557 | 122 | 68 | 379 |
| 11793 | Common Item - Cursed Staff | C | lrhand | 333 | 119 | 100 | 325 |
| 11799 | Common Item - Stick of Eternity | C | rhand | 377 | 111 | 101 | 379 |
| 11802 | Common Item - Nirvana Axe | C | rhand | 383 | 111 | 101 | 379 |
| 11804 | Common Item - Club of Nature | C | rhand | 367 | 111 | 101 | 379 |
| 11806 | Common Item - Mace of Underworld | C | rhand | 363 | 111 | 101 | 379 |
| 11816 | Common Item - War Axe | C | rhand | 553 | 139 | 76 | 379 |
| 11819 | Common Item - Inferno Staff | C | lrhand | 333 | 135 | 111 | 325 |
| 11822 | Common Item - Karik Horn | C | lrhand | 673 | 169 | 76 | 325 |
| 11824 | Common Item - Pa'agrian Hammer | C | lrhand | 337 | 135 | 111 | 325 |
| 11825 | Common Item - Paradia Staff | C | lrhand | 337 | 135 | 111 | 325 |
| 11828 | Common Item - Sage's Staff | C | lrhand | 333 | 135 | 111 | 325 |
| 11833 | Common Item - Pa'agrian Axe | C | lrhand | 330 | 141 | 114 | 325 |
| 11838 | Common Item - Ghoul's Staff | C | lrhand | 333 | 152 | 122 | 325 |
| 11840 | Common Item - Dwarven Hammer | C | lrhand | 670 | 190 | 83 | 325 |
| 11842 | Common Item - Deadman's Staff | C | lrhand | 337 | 152 | 122 | 325 |
| 11855 | Common Item - Demon's Staff | C | lrhand | 330 | 152 | 122 | 325 |
| 11856 | Common Item - Yaksa Mace | C | rhand | 547 | 156 | 83 | 379 |
| 11859 | Common Item - Ecliptic Axe | C | rhand | 547 | 125 | 111 | 379 |
| 13179 | Player Commendation - Ghost's Wand - Player Commendation Weapon | C | lrhand | 1010 | 152 | 122 | 325 |
| 13180 | Player Commendation - Ghoul's Wand - Player Commendation Weapon | C | lrhand | 1000 | 152 | 122 | 325 |
| 13181 | Player Commendation - Devil's Wand - Player Commendation Weapon | C | lrhand | 990 | 152 | 122 | 325 |
| 13186 | Player Commendation - Yaksa Mace - Player Commendation Weapon | C | rhand | 1640 | 156 | 83 | 379 |
| 13192 | Player Commendation - Ecliptic Axe - Player Commendation Weapon | C | rhand | 1640 | 125 | 111 | 379 |
| 13193 | Player Commendation - Dwarven Hammer - Player Commendation Weapon | C | lrhand | 2010 | 190 | 83 | 325 |
| 13789 | Red Boing Hammer | C | rhand | 1710 | 107 | 61 | 379 |
| 13790 | Blue Boing Hammer | C | rhand | 1710 | 107 | 61 | 379 |
| 13791 | Small Red Boing Hammer | C | rhand | 1710 | 107 | 61 | 379 |
| 13792 | Small Blue Boing Hammer | C | rhand | 1710 | 107 | 61 | 379 |
| 13971 | Red Boing Fantasy Hammer | C | rhand | 1710 | 1 | 61 | 379 |
| 13972 | Blue Boing Fantasy Hammer | C | rhand | 1710 | 1 | 61 | 379 |
| 13973 | Small Red Boing Fantasy Hammer | C | rhand | 1710 | 1 | 61 | 379 |
| 13974 | Small Blue Boing Fantasy Hammer | C | rhand | 1710 | 1 | 61 | 379 |
| 15046 | Yaksa Mace of Fortune - 30-day limited period | C | rhand | 1640 | 156 | 83 | 379 |
| 15160 | Yaksa Mace of Fortune - 10-day limited period | C | rhand | 1640 | 156 | 83 | 379 |
| 16934 | Yaksa Mace of Fortune - 90-day limited period | C | rhand | 1640 | 156 | 83 | 379 |
| 20126 | Yaksa Mace (Event) - 4-hour limited period | C | rhand | 547 | 156 | 83 | 379 |
| 20127 | Dwarven Hammer (Event) - 4-hour limited period | C | lrhand | 670 | 190 | 83 | 325 |
| 20128 | Ecliptic Axe (Event) - 4-hour limited period | C | rhand | 547 | 125 | 111 | 379 |
| 20129 | Demon's Staff (Event) - 4-hour limited period | C | lrhand | 330 | 152 | 111 | 325 |
| 91 | Heavy War Axe | B | rhand | 1620 | 175 | 91 | 379 |
| 92 | Sprite's Staff | B | lrhand | 960 | 170 | 134 | 325 |
| 171 | Deadman's Glory | B | rhand | 1600 | 194 | 99 | 379 |
| 175 | Art of Battle Axe | B | rhand | 1570 | 194 | 99 | 379 |
| 207 | Staff of Phantom | B | lrhand | 980 | 170 | 122 | 325 |
| 208 | Staff of Seal | B | lrhand | 970 | 170 | 122 | 325 |
| 209 | Divine Staff | B | lrhand | 960 | 189 | 132 | 325 |
| 210 | Staff of Evil Spirits | B | lrhand | 930 | 189 | 145 | 325 |
| 211 | Staff of Nobility | B | lrhand | 910 | 189 | 132 | 325 |
| 4747 | Heavy War Axe - Anger | B | rhand | 1620 | 175 | 91 | 379 |
| 4748 | Heavy War Axe - Health | B | rhand | 1620 | 175 | 91 | 379 |
| 4749 | Heavy War Axe - Rsk. Focus | B | rhand | 1620 | 175 | 91 | 379 |
| 4750 | Deadman's Glory - Anger | B | rhand | 1600 | 194 | 99 | 379 |
| 4751 | Deadman's Glory - Health | B | rhand | 1600 | 194 | 99 | 379 |
| 4752 | Deadman's Glory - Haste | B | rhand | 1600 | 194 | 99 | 379 |
| 4753 | Art of Battle Axe - Health | B | rhand | 1570 | 194 | 99 | 379 |
| 4754 | Art of Battle Axe - Rsk. Focus | B | rhand | 1570 | 194 | 99 | 379 |
| 4755 | Art of Battle Axe - Haste | B | rhand | 1570 | 194 | 99 | 379 |
| 4897 | Sprite's Staff - Magic Regeneration | B | lrhand | 960 | 170 | 134 | 325 |
| 4898 | Sprite's Staff - Mental Shield | B | lrhand | 960 | 170 | 134 | 325 |
| 4899 | Sprite's Staff - Magic Hold | B | lrhand | 960 | 170 | 134 | 325 |
| 4900 | Staff of Evil Spirits - Magic Focus | B | lrhand | 930 | 189 | 145 | 325 |
| 4901 | Staff of Evil Spirits - Blessed Body | B | lrhand | 930 | 189 | 145 | 325 |
| 4902 | Staff of Evil Spirits - Magic Poison | B | lrhand | 930 | 189 | 145 | 325 |
| 7834 | Art of Battle Axe | B | rhand | 1570 | 194 | 99 | 379 |
| 7892 | Spell Breaker | B | rhand | 1620 | 140 | 122 | 379 |
| 7893 | Kaim Vanul's Bones | B | rhand | 1570 | 155 | 132 | 379 |
| 7900 | Ice Storm Hammer | B | lrhand | 1950 | 213 | 91 | 325 |
| 7901 | Star Buster | B | lrhand | 1930 | 236 | 99 | 325 |
| 8129 | Ice Storm Hammer - Focus | B | lrhand | 1950 | 213 | 91 | 325 |
| 8130 | Ice Storm Hammer - Anger | B | lrhand | 1950 | 213 | 91 | 325 |
| 8131 | Ice Storm Hammer - Critical Bleed | B | lrhand | 1950 | 213 | 91 | 325 |
| 8132 | Star Buster - Health | B | lrhand | 1930 | 236 | 99 | 325 |
| 8133 | Star Buster - Haste | B | lrhand | 1930 | 236 | 99 | 325 |
| 8134 | Star Buster - Rsk. Focus | B | lrhand | 1930 | 236 | 99 | 325 |
| 8141 | Spell Breaker - Acumen | B | rhand | 1620 | 140 | 122 | 379 |
| 8142 | Spell Breaker - Mental Shield | B | rhand | 1620 | 140 | 122 | 379 |
| 8143 | Spell Breaker - Magic Hold | B | rhand | 1620 | 140 | 122 | 379 |
| 8144 | Kaim Vanul's Bones - Mana Up | B | rhand | 1570 | 155 | 132 | 379 |
| 8145 | Kaim Vanul's Bones - Magic Silence | B | rhand | 1570 | 155 | 132 | 379 |
| 8146 | Kaim Vanul's Bones - Conversion | B | rhand | 1570 | 155 | 132 | 379 |
| 8850 | Shadow Item: Heavy War Axe | B | rhand | 540 | 175 | 91 | 379 |
| 8851 | Shadow Item: Sprite's Staff | B | lrhand | 320 | 170 | 134 | 325 |
| 9002 | Shadow Item: Heavy War Axe | B | rhand | 540 | 175 | 91 | 379 |
| 9003 | Shadow Item: Sprite's Staff | B | lrhand | 320 | 170 | 134 | 325 |
| 10898 | Spell Breaker - Hail | B | rhand | 1620 | 140 | 122 | 379 |
| 10899 | Spell Breaker - Hail - Acumen | B | rhand | 1620 | 140 | 122 | 379 |
| 10900 | Spell Breaker - Hail - Mental Shield | B | rhand | 1620 | 140 | 122 | 379 |
| 10901 | Spell Breaker - Hail - Magic Hold | B | rhand | 1620 | 140 | 122 | 379 |
| 10906 | Ice Storm Hammer - Lightning | B | lrhand | 1950 | 213 | 91 | 325 |
| 10907 | Ice Storm Hammer - Lightning - Focus | B | lrhand | 1950 | 213 | 91 | 325 |
| 10908 | Ice Storm Hammer - Lightning - Anger | B | lrhand | 1950 | 213 | 91 | 325 |
| 10909 | Ice Storm Hammer - Lightning - Critical Bleed | B | lrhand | 1950 | 213 | 91 | 325 |
| 10916 | Sprite's Staff - Hail | B | lrhand | 960 | 170 | 134 | 325 |
| 10917 | Sprite's Staff - Hail - Magic Regeneration | B | lrhand | 960 | 170 | 134 | 325 |
| 10918 | Sprite's Staff - Hail - Mental Shield | B | lrhand | 960 | 170 | 134 | 325 |
| 10919 | Sprite's Staff - Hail - Magic Hold | B | lrhand | 960 | 170 | 134 | 325 |
| 10938 | Heavy War Axe - Earth | B | rhand | 1620 | 175 | 91 | 379 |
| 10939 | Heavy War Axe - Earth - Anger | B | rhand | 1620 | 175 | 91 | 379 |
| 10940 | Heavy War Axe - Earth - Health | B | rhand | 1620 | 175 | 91 | 379 |
| 10941 | Heavy War Axe - Earth - Rsk. Focus | B | rhand | 1620 | 175 | 91 | 379 |
| 10975 | Staff of Evil Spirits - Holy Spirit | B | lrhand | 930 | 189 | 145 | 325 |
| 10976 | Staff of Evil Spirits - Holy Spirit - Magic Focus | B | lrhand | 930 | 189 | 145 | 325 |
| 10977 | Staff of Evil Spirits - Holy Spirit - Blessed Body | B | lrhand | 930 | 189 | 145 | 325 |
| 10978 | Staff of Evil Spirits - Holy Spirit - Magic Poison | B | lrhand | 930 | 189 | 145 | 325 |
| 10979 | Deadman's Glory - Landslide | B | rhand | 1600 | 194 | 99 | 379 |
| 10980 | Deadman's Glory - Landslide - Anger | B | rhand | 1600 | 194 | 99 | 379 |
| 10981 | Deadman's Glory - Landslide - Health | B | rhand | 1600 | 194 | 99 | 379 |
| 10982 | Deadman's Glory - Landslide - Haste | B | rhand | 1600 | 194 | 99 | 379 |
| 10983 | Star Buster - Great Gale | B | lrhand | 1930 | 236 | 99 | 325 |
| 10984 | Star Buster - Great Gale - Health | B | lrhand | 1930 | 236 | 99 | 325 |
| 10985 | Star Buster - Great Gale - Haste | B | lrhand | 1930 | 236 | 99 | 325 |
| 10986 | Star Buster - Great Gale - Rsk. Focus | B | lrhand | 1930 | 236 | 99 | 325 |
| 10988 | Art of Battle Axe - Landslide | B | rhand | 1570 | 194 | 99 | 379 |
| 10989 | Art of Battle Axe - Landslide - Health | B | rhand | 1570 | 194 | 99 | 379 |
| 10990 | Art of Battle Axe - Landslide - Rsk. Focus | B | rhand | 1570 | 194 | 99 | 379 |
| 10991 | Art of Battle Axe - Landslide - Haste | B | rhand | 1570 | 194 | 99 | 379 |
| 10997 | Kaim Vanul's Bones - Earth | B | rhand | 1570 | 155 | 132 | 379 |
| 10998 | Kaim Vanul's Bones - Earth - Mana Up | B | rhand | 1570 | 155 | 132 | 379 |
| 10999 | Kaim Vanul's Bones - Earth - Magic Silence | B | rhand | 1570 | 155 | 132 | 379 |
| 11000 | Kaim Vanul's Bones - Earth - Conversion | B | rhand | 1570 | 155 | 132 | 379 |
| 11902 | Common Item - Spell Breaker | B | rhand | 540 | 140 | 122 | 379 |
| 11904 | Common Item - Ice Storm Hammer | B | lrhand | 650 | 213 | 91 | 325 |
| 11908 | Common Item - Sprite's Staff | B | lrhand | 320 | 170 | 134 | 325 |
| 11918 | Common Item - Heavy War Axe | B | rhand | 540 | 175 | 91 | 379 |
| 11934 | Common Item - Staff of Evil Spirits | B | lrhand | 310 | 189 | 145 | 325 |
| 11935 | Common Item - Deadman's Glory | B | rhand | 533 | 194 | 99 | 379 |
| 11936 | Common Item - Star Buster | B | lrhand | 643 | 236 | 99 | 325 |
| 11938 | Common Item - Art of Battle Axe | B | rhand | 523 | 194 | 99 | 379 |
| 11941 | Common Item - Kaim Vanul's Bones | B | rhand | 523 | 155 | 132 | 379 |
| 13196 | Player Commendation - Deadman's Glory - Player Commendation Weapon | B | rhand | 1600 | 194 | 99 | 379 |
| 13197 | Player Commendation - Art of Battle Axe - Player Commendation Weapon | B | rhand | 1570 | 194 | 99 | 379 |
| 13198 | Player Commendation - Staff of Evil Spirits - Player Commendation Weapon | B | lrhand | 930 | 189 | 145 | 325 |
| 13205 | Player Commendation - Kaim Vanul's Bones - Player Commendation Weapon | B | rhand | 1570 | 155 | 132 | 379 |
| 13206 | Player Commendation - Star Buster - Player Commendation Weapon | B | lrhand | 1930 | 236 | 99 | 325 |
| 13987 | Exclusive to Monsters (Savage Warrior) | B | rhand | 1620 | 175 | 91 | 379 |
| 15045 | Art of Battle Axe of Fortune - 30-day limited period | B | rhand | 1570 | 194 | 99 | 379 |
| 15159 | Art of Battle Axe of Fortune - 10-day limited period | B | rhand | 1570 | 194 | 99 | 379 |
| 16933 | Art of Battle Axe of Fortune - 90-day limited period | B | rhand | 1570 | 194 | 99 | 379 |
| 20140 | Art of Battle Axe (Event) - 4-hour limited period | B | rhand | 523 | 194 | 99 | 379 |
| 20141 | Star Buster (Event) - 4-hour limited period | B | lrhand | 643 | 236 | 99 | 325 |
| 20142 | Kaim Vanul's Bones (Event) - 4-hour limited period | B | rhand | 523 | 155 | 132 | 379 |
| 20143 | Staff of Evil Spirits (Event) - 4-hour limited period | B | lrhand | 310 | 189 | 132 | 325 |
| 164 | Elysian | A | rhand | 1580 | 232 | 114 | 379 |
| 212 | Dasparion's Staff | A | lrhand | 920 | 207 | 157 | 325 |
| 213 | Branch of the Mother Tree | A | lrhand | 900 | 226 | 167 | 325 |
| 2504 | Meteor Shower | A | rhand | 1600 | 213 | 107 | 379 |
| 4756 | Meteor Shower - Health | A | rhand | 1600 | 213 | 107 | 379 |
| 4757 | Meteor Shower - Focus | A | rhand | 1600 | 213 | 107 | 379 |
| 4758 | Meteor Shower - P.Focus | A | rhand | 1600 | 213 | 107 | 379 |
| 4903 | Dasparion's Staff | A | lrhand | 920 | 207 | 143 | 325 |
| 4904 | Dasparion's Staff | A | lrhand | 920 | 207 | 143 | 325 |
| 4905 | Dasparion's Staff | A | lrhand | 920 | 207 | 143 | 325 |
| 5596 | Dasparion's Staff - Mana Up | A | lrhand | 920 | 207 | 157 | 325 |
| 5597 | Dasparion's Staff - Conversion | A | lrhand | 920 | 207 | 157 | 325 |
| 5598 | Dasparion's Staff - Acumen | A | lrhand | 920 | 207 | 157 | 325 |
| 5599 | Meteor Shower - Focus | A | rhand | 1600 | 213 | 107 | 379 |
| 5600 | Meteor Shower - Critical Bleed | A | rhand | 1600 | 213 | 107 | 379 |
| 5601 | Meteor Shower - Rsk. Haste | A | rhand | 1600 | 213 | 107 | 379 |
| 5602 | Elysian - Health | A | rhand | 1580 | 232 | 114 | 379 |
| 5603 | Elysian - Anger | A | rhand | 1580 | 232 | 114 | 379 |
| 5604 | Elysian - Critical Drain | A | rhand | 1580 | 232 | 114 | 379 |
| 5605 | Branch of the Mother Tree - Conversion | A | lrhand | 900 | 226 | 167 | 325 |
| 5606 | Branch of the Mother Tree - Magic Damage | A | lrhand | 900 | 226 | 167 | 325 |
| 5607 | Branch of the Mother Tree - Acumen | A | lrhand | 900 | 226 | 167 | 325 |
| 7894 | Spiritual Eye | A | rhand | 1550 | 170 | 143 | 379 |
| 7895 | Flaming Dragon Skull | A | rhand | 1530 | 186 | 152 | 379 |
| 7899 | Destroyer Hammer | A | lrhand | 1910 | 259 | 107 | 325 |
| 7902 | Doom Crusher | A | lrhand | 1900 | 282 | 114 | 325 |
| 8126 | Destroyer Hammer - Health | A | lrhand | 1910 | 259 | 107 | 325 |
| 8127 | Destroyer Hammer - Haste | A | lrhand | 1910 | 259 | 107 | 325 |
| 8128 | Destroyer Hammer - Critical Drain | A | lrhand | 1910 | 259 | 107 | 325 |
| 8135 | Doom Crusher - Health | A | lrhand | 1900 | 282 | 114 | 325 |
| 8136 | Doom Crusher - Anger | A | lrhand | 1900 | 282 | 114 | 325 |
| 8137 | Doom Crusher - Rsk. Haste | A | lrhand | 1900 | 282 | 114 | 325 |
| 8147 | Spiritual Eye - Mana Up | A | rhand | 1550 | 170 | 143 | 379 |
| 8148 | Spiritual Eye - Magic Poison | A | rhand | 1550 | 170 | 143 | 379 |
| 8149 | Spiritual Eye - Acumen | A | rhand | 1550 | 170 | 143 | 379 |
| 8150 | Flaming Dragon Skull - Acumen | A | rhand | 1530 | 186 | 152 | 379 |
| 8151 | Flaming Dragon Skull - M. Atk. | A | rhand | 1530 | 186 | 152 | 379 |
| 8152 | Flaming Dragon Skull - Magic Silence | A | rhand | 1530 | 186 | 152 | 379 |
| 8680 | Barakiel's Axe | A | rhand | 1550 | 251 | 121 | 379 |
| 8681 | Behemoth's Tuning Fork | A | lrhand | 1890 | 305 | 121 | 325 |
| 8687 | Cabrio's Hand | A | rhand | 1510 | 202 | 161 | 379 |
| 8688 | Daimon Crystal | A | lrhand | 880 | 245 | 177 | 325 |
| 8763 | Elrokian Trap | A | rhand | 500 |  |  | 379 |
| 8794 | Barakiel's Axe - Health | A | rhand | 1550 | 251 | 121 | 379 |
| 8795 | Barakiel's Axe - Haste | A | rhand | 1550 | 251 | 121 | 379 |
| 8796 | Barakiel's Axe - Focus | A | rhand | 1550 | 251 | 121 | 379 |
| 8797 | Behemoth's Tuning Fork - Focus | A | lrhand | 1890 | 305 | 121 | 325 |
| 8798 | Behemoth's Tuning Fork - Health | A | lrhand | 1890 | 305 | 121 | 325 |
| 8799 | Behemoth's Tuning Fork - Anger | A | lrhand | 1890 | 305 | 121 | 325 |
| 8815 | Cabrio's Hand - Conversion | A | rhand | 1510 | 202 | 161 | 379 |
| 8816 | Cabrio's Hand - Mana Up | A | rhand | 1510 | 202 | 161 | 379 |
| 8817 | Cabrio's Hand - Magic Silence | A | rhand | 1510 | 202 | 161 | 379 |
| 8818 | Daimon Crystal - Mana Up | A | lrhand | 880 | 245 | 177 | 325 |
| 8819 | Daimon Crystal - Acumen | A | lrhand | 880 | 245 | 177 | 325 |
| 8820 | Daimon Crystal - Mental Shield | A | lrhand | 880 | 245 | 177 | 325 |
| 8861 | Shadow Item: Dasparion's Staff | A | lrhand | 310 | 207 | 157 | 325 |
| 8866 | Shadow Item: Meteor Shower | A | rhand | 540 | 213 | 107 | 379 |
| 9013 | Shadow Item: Dasparion's Staff | A | lrhand | 310 | 207 | 157 | 325 |
| 9018 | Shadow Item: Meteor Shower | A | rhand | 540 | 213 | 107 | 379 |
| 9023 | Shadow Item: Elysian | A | rhand | 527 | 232 | 114 | 379 |
| 9024 | Shadow Item: Branch of the Mother Tree | A | lrhand | 300 | 226 | 167 | 325 |
| 10673 | Barakiel's Axe {PvP} - Health | A | rhand | 1550 | 251 | 121 | 379 |
| 10674 | Barakiel's Axe {PvP} - Haste | A | rhand | 1550 | 251 | 121 | 379 |
| 10675 | Barakiel's Axe {PvP} - Focus | A | rhand | 1550 | 251 | 121 | 379 |
| 10676 | Behemoth's Tuning Fork {PvP} - Focus | A | lrhand | 1890 | 305 | 121 | 325 |
| 10677 | Behemoth's Tuning Fork {PvP} - Health | A | lrhand | 1890 | 305 | 121 | 325 |
| 10678 | Behemoth's Tuning Fork {PvP} - Anger | A | lrhand | 1890 | 305 | 121 | 325 |
| 10694 | Cabrio's Hand {PvP} - Conversion | A | rhand | 1510 | 201 | 162 | 379 |
| 10695 | Cabrio's Hand {PvP} - Mana Up | A | rhand | 1510 | 201 | 162 | 379 |
| 10696 | Cabrio's Hand {PvP} - Magic Silence | A | rhand | 1510 | 201 | 162 | 379 |
| 10697 | Daimon Crystal {PvP} - Mana Up | A | lrhand | 880 | 245 | 177 | 325 |
| 10698 | Daimon Crystal {PvP} - Acumen | A | lrhand | 880 | 245 | 177 | 325 |
| 10699 | Daimon Crystal {PvP} - Mental Shield | A | lrhand | 880 | 245 | 177 | 325 |
| 11017 | Dasparion's Staff - Hail | A | lrhand | 920 | 207 | 157 | 325 |
| 11018 | Dasparion's Staff - Hail - Mana Up | A | lrhand | 920 | 207 | 157 | 325 |
| 11019 | Dasparion's Staff - Hail - Conversion | A | lrhand | 920 | 207 | 157 | 325 |
| 11020 | Dasparion's Staff - Hail - Acumen | A | lrhand | 920 | 207 | 157 | 325 |
| 11029 | Meteor Shower - Earth | A | rhand | 1600 | 213 | 107 | 379 |
| 11030 | Meteor Shower - Earth - Focus | A | rhand | 1600 | 213 | 107 | 379 |
| 11031 | Meteor Shower - Earth - Critical Bleed | A | rhand | 1600 | 213 | 107 | 379 |
| 11032 | Meteor Shower - Earth - Rsk. Haste | A | rhand | 1600 | 213 | 107 | 379 |
| 11045 | Spiritual Eye - Hail | A | rhand | 1550 | 170 | 143 | 379 |
| 11046 | Spiritual Eye - Hail - Mana Up | A | rhand | 1550 | 170 | 143 | 379 |
| 11047 | Spiritual Eye - Hail - Magic Poison | A | rhand | 1550 | 170 | 143 | 379 |
| 11048 | Spiritual Eye - Hail - Acumen | A | rhand | 1550 | 170 | 143 | 379 |
| 11062 | Destroyer Hammer - Lightning | A | lrhand | 1910 | 259 | 107 | 325 |
| 11063 | Destroyer Hammer - Lightning - Health | A | lrhand | 1910 | 259 | 107 | 325 |
| 11064 | Destroyer Hammer - Lightning - Haste | A | lrhand | 1910 | 259 | 107 | 325 |
| 11065 | Destroyer Hammer - Lightning - Critical Drain | A | lrhand | 1910 | 259 | 107 | 325 |
| 11088 | Doom Crusher - Thunder | A | lrhand | 1900 | 282 | 114 | 325 |
| 11089 | Doom Crusher - Thunder - Health | A | lrhand | 1900 | 282 | 114 | 325 |
| 11090 | Doom Crusher - Thunder - Anger | A | lrhand | 1900 | 282 | 114 | 325 |
| 11091 | Doom Crusher - Thunder - Rsk. Haste | A | lrhand | 1900 | 282 | 114 | 325 |
| 11100 | Flaming Dragon Skull - Wisdom | A | rhand | 1530 | 186 | 152 | 379 |
| 11101 | Flaming Dragon Skull - Wisdom - Acumen | A | rhand | 1530 | 186 | 152 | 379 |
| 11102 | Flaming Dragon Skull - Wisdom - M. Atk. | A | rhand | 1530 | 186 | 152 | 379 |
| 11103 | Flaming Dragon Skull - Wisdom - Magic Silence | A | rhand | 1530 | 186 | 152 | 379 |
| 11104 | Branch of the Mother Tree - Nature | A | lrhand | 900 | 226 | 167 | 325 |
| 11105 | Branch of the Mother Tree - Nature - Conversion | A | lrhand | 900 | 226 | 167 | 325 |
| 11106 | Branch of the Mother Tree - Nature - Magic Damage | A | lrhand | 900 | 226 | 167 | 325 |
| 11107 | Branch of the Mother Tree - Nature - Acumen | A | lrhand | 900 | 226 | 167 | 325 |
| 11120 | Elysian - Great Gale | A | rhand | 1580 | 232 | 114 | 379 |
| 11121 | Elysian - Great Gale - Health | A | rhand | 1580 | 232 | 114 | 379 |
| 11122 | Elysian - Great Gale - Anger | A | rhand | 1580 | 232 | 114 | 379 |
| 11123 | Elysian - Great Gale - Critical Drain | A | rhand | 1580 | 232 | 114 | 379 |
| 11137 | Daimon Crystal - Wisdom | A | lrhand | 880 | 245 | 177 | 325 |
| 11138 | Daimon Crystal - Wisdom - Mana Up | A | lrhand | 880 | 245 | 177 | 325 |
| 11139 | Daimon Crystal - Wisdom - Acumen | A | lrhand | 880 | 245 | 177 | 325 |
| 11140 | Daimon Crystal - Wisdom - Mental Shield | A | lrhand | 880 | 245 | 177 | 325 |
| 11141 | Barakiel's Axe - On Fire | A | rhand | 1550 | 251 | 121 | 379 |
| 11142 | Barakiel's Axe - On Fire - Health | A | rhand | 1550 | 251 | 121 | 379 |
| 11143 | Barakiel's Axe - On Fire - Haste | A | rhand | 1550 | 251 | 121 | 379 |
| 11144 | Barakiel's Axe - On Fire - Focus | A | rhand | 1550 | 251 | 121 | 379 |
| 11149 | Behemoth's Tuning Fork - Destruction | A | lrhand | 1890 | 305 | 121 | 325 |
| 11150 | Behemoth's Tuning Fork - Destruction - Focus | A | lrhand | 1890 | 305 | 121 | 325 |
| 11151 | Behemoth's Tuning Fork - Destruction - Health | A | lrhand | 1890 | 305 | 121 | 325 |
| 11152 | Behemoth's Tuning Fork - Destruction - Anger | A | lrhand | 1890 | 305 | 121 | 325 |
| 11186 | Cabrio's Hand - Cleverness | A | rhand | 1510 | 202 | 161 | 379 |
| 11187 | Cabrio's Hand - Cleverness - Conversion | A | rhand | 1510 | 202 | 161 | 379 |
| 11188 | Cabrio's Hand - Cleverness - Mana Up | A | rhand | 1510 | 202 | 161 | 379 |
| 11189 | Cabrio's Hand - Cleverness - Magic Silence | A | rhand | 1510 | 202 | 161 | 379 |
| 11946 | Common Item - Dasparion's Staff | A | lrhand | 307 | 207 | 157 | 325 |
| 11949 | Common Item - Meteor Shower | A | rhand | 533 | 213 | 107 | 379 |
| 11953 | Common Item - Spiritual Eye | A | rhand | 517 | 170 | 143 | 379 |
| 11958 | Common Item - Destroyer Hammer | A | lrhand | 637 | 259 | 107 | 325 |
| 11966 | Common Item - Doom Crusher | A | lrhand | 633 | 282 | 114 | 325 |
| 11969 | Common Item - Flaming Dragon Skull | A | rhand | 510 | 186 | 152 | 379 |
| 11970 | Common Item - Branch of the Mother Tree | A | lrhand | 300 | 226 | 167 | 325 |
| 11974 | Common Item - Elysian | A | rhand | 527 | 232 | 114 | 379 |
| 11978 | Common Item - Daimon Crystal | A | lrhand | 293 | 245 | 177 | 325 |
| 11979 | Common Item - Barakiel's Axe | A | rhand | 517 | 251 | 121 | 379 |
| 11981 | Common Item - Behemoth's Tuning Fork | A | lrhand | 630 | 305 | 121 | 325 |
| 11991 | Common Item - Cabrio's Hand | A | rhand | 503 | 202 | 162 | 379 |
| 12855 | Daimon Crystal - Wisdom {PvP} - Mana Up | A | lrhand | 880 | 245 | 177 | 325 |
| 12856 | Daimon Crystal - Wisdom {PvP} - Acumen | A | lrhand | 880 | 245 | 177 | 325 |
| 12857 | Daimon Crystal - Wisdom {PvP} - Mental Shield | A | lrhand | 880 | 245 | 177 | 325 |
| 12858 | Barakiel's Axe - On Fire {PvP} - Health | A | rhand | 1550 | 251 | 121 | 379 |
| 12859 | Barakiel's Axe - On Fire {PvP} - Haste | A | rhand | 1550 | 251 | 121 | 379 |
| 12860 | Barakiel's Axe - On Fire {PvP} - Focus | A | rhand | 1550 | 251 | 121 | 379 |
| 12864 | Behemoth's Tuning Fork - Destruction {PvP} - Focus | A | lrhand | 1890 | 305 | 121 | 325 |
| 12865 | Behemoth's Tuning Fork - Destruction {PvP} - Health | A | lrhand | 1890 | 305 | 121 | 325 |
| 12866 | Behemoth's Tuning Fork - Destruction {PvP} - Anger | A | lrhand | 1890 | 305 | 121 | 325 |
| 12892 | Cabrio's Hand - Cleverness {PvP} - Conversion | A | rhand | 1510 | 202 | 161 | 379 |
| 12893 | Cabrio's Hand - Cleverness {PvP} - Mana Up | A | rhand | 1510 | 202 | 161 | 379 |
| 12894 | Cabrio's Hand - Cleverness {PvP} - Magic Silence | A | rhand | 1510 | 202 | 161 | 379 |
| 13212 | Player Commendation - Barakiel's Axe - Player Commendation Weapon | A | rhand | 1550 | 251 | 121 | 379 |
| 13213 | Player Commendation - Behemoth Tuning Fork - Player Commendation Weapon | A | lrhand | 1890 | 305 | 121 | 325 |
| 13219 | Player Commendation - Cabrio's Hand - Player Commendation Weapon | A | rhand | 1510 | 202 | 161 | 379 |
| 13220 | Player Commendation - Daimon Crystal - Player Commendation Weapon | A | lrhand | 880 | 245 | 177 | 325 |
| 15044 | Barakiel's Axe of Fortune - 30-day limited period | A | rhand | 1550 | 251 | 121 | 379 |
| 15158 | Barakiel's Axe of Fortune - 10-day limited period | A | rhand | 1550 | 251 | 121 | 379 |
| 16932 | Barakiel's Axe of Fortune - 90-day limited period | A | rhand | 1550 | 251 | 121 | 379 |
| 20154 | Elysian (Event) - 4-hour limited period | A | rhand | 527 | 232 | 114 | 379 |
| 20155 | Doom Crusher (Event) - 4-hour limited period | A | lrhand | 633 | 282 | 114 | 325 |
| 20156 | Flaming Dragon Skull (Event) - 4-hour limited period | A | rhand | 510 | 186 | 152 | 379 |
| 20157 | Branch of the Mother Tree (Event) - 4-hour limited period | A | lrhand | 300 | 226 | 152 | 325 |
| 165 | Yablonski's Hammer | S | rhand | 1570 | 251 | 121 | 379 |
| 214 | The Staff | S | lrhand | 910 | 245 | 162 | 325 |
| 6365 | Basalt Battlehammer | S | rhand | 1570 | 281 | 132 | 379 |
| 6366 | Imperial Staff | S | lrhand | 910 | 274 | 193 | 325 |
| 6369 | Dragon Hunter Axe | S | lrhand | 1820 | 342 | 132 | 325 |
| 6579 | Arcana Mace | S | rhand | 1300 | 225 | 175 | 379 |
| 6584 | Basalt Battlehammer - HP Drain | S | rhand | 1570 | 281 | 132 | 379 |
| 6585 | Basalt Battlehammer - Health | S | rhand | 1570 | 281 | 132 | 379 |
| 6586 | Basalt Battlehammer - HP Regeneration | S | rhand | 1570 | 281 | 132 | 379 |
| 6587 | Imperial Staff - Empower | S | lrhand | 910 | 274 | 193 | 325 |
| 6588 | Imperial Staff - MP Regeneration | S | lrhand | 910 | 274 | 193 | 325 |
| 6589 | Imperial Staff - Magic Hold | S | lrhand | 910 | 274 | 193 | 325 |
| 6596 | Dragon Hunter Axe - HP Regeneration | S | lrhand | 1820 | 342 | 132 | 325 |
| 6597 | Dragon Hunter Axe - Health | S | lrhand | 1820 | 342 | 132 | 325 |
| 6598 | Dragon Hunter Axe - HP Drain | S | lrhand | 1820 | 342 | 132 | 325 |
| 6608 | Arcana Mace - Acumen | S | rhand | 1300 | 225 | 175 | 379 |
| 6609 | Arcana Mace - MP Regeneration | S | rhand | 1300 | 225 | 175 | 379 |
| 6610 | Arcana Mace - Mana Up | S | rhand | 1300 | 225 | 175 | 379 |
| 6613 | Infinity Axe | S | rhand | 1300 | 524 | 230 | 379 |
| 6614 | Infinity Rod | S | rhand | 1300 | 420 | 307 | 379 |
| 6615 | Infinity Crusher | S | lrhand | 1300 | 638 | 230 | 325 |
| 6616 | Infinity Scepter | S | lrhand | 1300 | 511 | 337 | 325 |
| 9448 | Dynasty Cudgel | S | rhand | 1740 | 333 | 151 | 379 |
| 9449 | Dynasty Mace | S | rhand | 1080 | 267 | 202 | 379 |
| 9872 | Dynasty Cudgel - Anger | S | rhand | 1740 | 333 | 151 | 379 |
| 9873 | Dynasty Cudgel - Health | S | rhand | 1740 | 333 | 151 | 379 |
| 9874 | Dynasty Cudgel - Rsk. Focus | S | rhand | 1740 | 333 | 151 | 379 |
| 9875 | Dynasty Mace - Mana Up | S | rhand | 1080 | 267 | 202 | 379 |
| 9876 | Dynasty Mace - Conversion | S | rhand | 1080 | 267 | 202 | 379 |
| 9877 | Dynasty Mace - Acumen | S | rhand | 1080 | 267 | 202 | 379 |
| 10252 | Dynasty Staff | S | lrhand | 1080 | 325 | 222 | 325 |
| 10253 | Dynasty Crusher | S | lrhand | 1740 | 405 | 151 | 325 |
| 10527 | Dynasty Staff - Mana Up | S | lrhand | 1080 | 325 | 222 | 325 |
| 10528 | Dynasty Staff - Conversion | S | lrhand | 1080 | 325 | 222 | 325 |
| 10529 | Dynasty Staff - Acumen | S | lrhand | 1080 | 325 | 222 | 325 |
| 10530 | Dynasty Crusher - Anger | S | lrhand | 1740 | 405 | 151 | 325 |
| 10531 | Dynasty Crusher - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 10532 | Dynasty Crusher - Rsk. Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 10716 | Basalt Battlehammer {PvP} - HP Drain | S | rhand | 1570 | 281 | 132 | 379 |
| 10717 | Basalt Battlehammer {PvP} - Health | S | rhand | 1570 | 281 | 132 | 379 |
| 10718 | Basalt Battlehammer {PvP} - HP Regeneration | S | rhand | 1570 | 281 | 132 | 379 |
| 10719 | Dragon Hunter Axe {PvP} - HP Regeneration | S | lrhand | 1820 | 342 | 132 | 325 |
| 10720 | Dragon Hunter Axe {PvP} - Health | S | lrhand | 1820 | 342 | 132 | 325 |
| 10721 | Dragon Hunter Axe {PvP} - HP Drain | S | lrhand | 1820 | 342 | 132 | 325 |
| 10731 | Arcana Mace {PvP} - Acumen | S | rhand | 1300 | 225 | 175 | 379 |
| 10732 | Arcana Mace {PvP} - MP Regeneration | S | rhand | 1300 | 225 | 175 | 379 |
| 10733 | Arcana Mace {PvP} - Mana Up | S | rhand | 1300 | 225 | 175 | 379 |
| 10734 | Imperial Staff {PvP} - Empower | S | lrhand | 910 | 274 | 193 | 325 |
| 10735 | Imperial Staff {PvP} - MP Regeneration | S | lrhand | 910 | 274 | 193 | 325 |
| 10736 | Imperial Staff {PvP} - Magic Hold | S | lrhand | 910 | 274 | 193 | 325 |
| 10756 | Dynasty Cudgel {PvP} - Anger | S | rhand | 1740 | 333 | 151 | 379 |
| 10757 | Dynasty Cudgel {PvP} - Health | S | rhand | 1740 | 333 | 151 | 379 |
| 10758 | Dynasty Cudgel {PvP} - Rsk. Focus | S | rhand | 1740 | 333 | 151 | 379 |
| 10759 | Dynasty Crusher {PvP} - Anger | S | lrhand | 1740 | 405 | 151 | 325 |
| 10760 | Dynasty Crusher {PvP} - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 10761 | Dynasty Crusher {PvP} - Rsk. Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 10774 | Dynasty Mace {PvP} - Mana Up | S | rhand | 1080 | 267 | 202 | 379 |
| 10775 | Dynasty Mace {PvP} - Conversion | S | rhand | 1080 | 267 | 202 | 379 |
| 10776 | Dynasty Mace {PvP} - Acumen | S | rhand | 1080 | 267 | 202 | 379 |
| 10777 | Dynasty Staff {PvP} - Mana Up | S | lrhand | 1080 | 325 | 222 | 325 |
| 10778 | Dynasty Staff {PvP} - Conversion | S | lrhand | 1080 | 325 | 222 | 325 |
| 10779 | Dynasty Staff {PvP} - Acumen | S | lrhand | 1080 | 325 | 222 | 325 |
| 11202 | Dragon Hunter Axe - Thunder | S | lrhand | 1820 | 342 | 132 | 325 |
| 11203 | Dragon Hunter Axe - Thunder - HP Regeneration | S | lrhand | 1820 | 342 | 132 | 325 |
| 11204 | Dragon Hunter Axe - Thunder - Health | S | lrhand | 1820 | 342 | 132 | 325 |
| 11205 | Dragon Hunter Axe - Thunder - HP Drain | S | lrhand | 1820 | 342 | 132 | 325 |
| 11210 | Basalt Battlehammer - Concentration | S | rhand | 1570 | 281 | 132 | 379 |
| 11211 | Basalt Battlehammer - Concentration - HP Drain | S | rhand | 1570 | 281 | 132 | 379 |
| 11212 | Basalt Battlehammer - Concentration - Health | S | rhand | 1570 | 281 | 132 | 379 |
| 11213 | Basalt Battlehammer - Concentration - HP Regeneration | S | rhand | 1570 | 281 | 132 | 379 |
| 11222 | Arcana Mace - Nature | S | rhand | 1300 | 225 | 175 | 379 |
| 11223 | Arcana Mace - Nature - Acumen | S | rhand | 1300 | 225 | 175 | 379 |
| 11224 | Arcana Mace - Nature - MP Regeneration | S | rhand | 1300 | 225 | 175 | 379 |
| 11225 | Arcana Mace - Nature - Mana Up | S | rhand | 1300 | 225 | 175 | 379 |
| 11230 | Imperial Staff - Nature | S | lrhand | 910 | 274 | 193 | 325 |
| 11231 | Imperial Staff - Nature - Empower | S | lrhand | 910 | 274 | 193 | 325 |
| 11232 | Imperial Staff - Nature - MP Regeneration | S | lrhand | 910 | 274 | 193 | 325 |
| 11233 | Imperial Staff - Nature - Magic Hold | S | lrhand | 910 | 274 | 193 | 325 |
| 11256 | Dynasty Mace - Earth | S | rhand | 1080 | 267 | 202 | 379 |
| 11257 | Dynasty Mace - Earth - Mana Up | S | rhand | 1080 | 267 | 202 | 379 |
| 11258 | Dynasty Mace - Earth - Conversion | S | rhand | 1080 | 267 | 202 | 379 |
| 11259 | Dynasty Mace - Earth - Acumen | S | rhand | 1080 | 267 | 202 | 379 |
| 11276 | Dynasty Staff - Holy Spirit | S | lrhand | 1080 | 325 | 222 | 325 |
| 11277 | Dynasty Staff - Holy Spirit - Mana Up | S | lrhand | 1080 | 325 | 222 | 325 |
| 11278 | Dynasty Staff - Holy Spirit - Conversion | S | lrhand | 1080 | 325 | 222 | 325 |
| 11279 | Dynasty Staff - Holy Spirit - Acumen | S | lrhand | 1080 | 325 | 222 | 325 |
| 11280 | Dynasty Cudgel - Landslide | S | rhand | 1740 | 333 | 151 | 379 |
| 11281 | Dynasty Cudgel - Landslide - Anger | S | rhand | 1740 | 333 | 151 | 379 |
| 11282 | Dynasty Cudgel - Landslide - Health | S | rhand | 1740 | 333 | 151 | 379 |
| 11283 | Dynasty Cudgel - Landslide - Rsk. Focus | S | rhand | 1740 | 333 | 151 | 379 |
| 11284 | Dynasty Crusher - Great Gale | S | lrhand | 1740 | 405 | 151 | 325 |
| 11285 | Dynasty Crusher - Great Gale - Anger | S | lrhand | 1740 | 405 | 151 | 325 |
| 11286 | Dynasty Crusher - Great Gale - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 11287 | Dynasty Crusher - Great Gale - Rsk. Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 11995 | Common Item - Dragon Hunter Axe | S | lrhand | 607 | 342 | 132 | 325 |
| 11997 | Common Item - Basalt Battlehammer | S | rhand | 523 | 281 | 132 | 379 |
| 12000 | Common Item - Arcana Mace | S | rhand | 433 | 225 | 175 | 379 |
| 12002 | Common Item - Imperial Staff | S | lrhand | 303 | 274 | 193 | 325 |
| 12904 | Dragon Hunter Axe - Thunder {PvP} - HP Regeneration | S | lrhand | 1820 | 342 | 132 | 325 |
| 12905 | Dragon Hunter Axe - Thunder {PvP} - Health | S | lrhand | 1820 | 342 | 132 | 325 |
| 12906 | Dragon Hunter Axe - Thunder {PvP} - HP Drain | S | lrhand | 1820 | 342 | 132 | 325 |
| 12910 | Basalt Battlehammer - Concentration {PvP} - HP Drain | S | rhand | 1570 | 281 | 132 | 379 |
| 12911 | Basalt Battlehammer - Concentration {PvP} - Health | S | rhand | 1570 | 281 | 132 | 379 |
| 12912 | Basalt Battlehammer - Concentration {PvP} - HP Regeneration | S | rhand | 1570 | 281 | 132 | 379 |
| 12919 | Arcana Mace - Nature {PvP} - Acumen | S | rhand | 1300 | 225 | 175 | 379 |
| 12920 | Arcana Mace - Nature {PvP} - MP Regeneration | S | rhand | 1300 | 225 | 175 | 379 |
| 12921 | Arcana Mace - Nature {PvP} - Mana Up | S | rhand | 1300 | 225 | 175 | 379 |
| 12925 | Imperial Staff - Nature {PvP} - Empower | S | lrhand | 910 | 274 | 193 | 325 |
| 12926 | Imperial Staff - Nature {PvP} - MP Regeneration | S | lrhand | 910 | 274 | 193 | 325 |
| 12927 | Imperial Staff - Nature {PvP} - Magic Hold | S | lrhand | 910 | 274 | 193 | 325 |
| 12945 | Dynasty Mace - Earth {PvP} - Mana Up | S | rhand | 1080 | 267 | 202 | 379 |
| 12946 | Dynasty Mace - Earth {PvP} - Conversion | S | rhand | 1080 | 267 | 202 | 379 |
| 12947 | Dynasty Mace - Earth {PvP} - Acumen | S | rhand | 1080 | 267 | 202 | 379 |
| 12960 | Dynasty Staff - Holy Spirit {PvP} - Mana Up | S | lrhand | 1080 | 325 | 222 | 325 |
| 12961 | Dynasty Staff - Holy Spirit {PvP} - Conversion | S | lrhand | 1080 | 325 | 222 | 325 |
| 12962 | Dynasty Staff - Holy Spirit {PvP} - Acumen | S | lrhand | 1080 | 325 | 222 | 325 |
| 12963 | Dynasty Cudgel - Landslide {PvP} - Anger | S | rhand | 1740 | 333 | 151 | 379 |
| 12964 | Dynasty Cudgel - Landslide {PvP} - Health | S | rhand | 1740 | 333 | 151 | 379 |
| 12965 | Dynasty Cudgel - Landslide {PvP} - Rsk. Focus | S | rhand | 1740 | 333 | 151 | 379 |
| 12966 | Dynasty Crusher - Great Gale {PvP} - Anger | S | lrhand | 1740 | 405 | 151 | 325 |
| 12967 | Dynasty Crusher - Great Gale {PvP} - Health | S | lrhand | 1740 | 405 | 151 | 325 |
| 12968 | Dynasty Crusher - Great Gale {PvP} - Rsk. Focus | S | lrhand | 1740 | 405 | 151 | 325 |
| 14565 | Great Hammer of Esthus Family | S | lrhand | 1365 | 376 | 119 | 325 |
| 14566 | Staff of Dake Family | S | lrhand | 683 | 247 | 212 | 325 |
| 14567 | Hall of Dake Family | S | rhand | 975 | 203 | 193 | 379 |
| 14569 | Mace of Cadmus Family | S | rhand | 1178 | 310 | 119 | 379 |
| 14572 | Staff of Abygail Family | S | lrhand | 683 | 247 | 212 | 325 |
| 14573 | Great Hammer of Abygail Family | S | lrhand | 1365 | 376 | 119 | 325 |
| 14576 | Mace of Orwen Family | S | rhand | 1178 | 310 | 119 | 379 |
| 15314 | Player Commendation - Basalt Battlehammer - Player Recommendation Weapon | S | rhand | 1570 | 281 | 132 | 379 |
| 15315 | Player Commendation - Imperial Staff - Player Recommendation Weapon | S | lrhand | 910 | 274 | 193 | 325 |
| 15317 | Player Commendation - Dragon Hunter Axe - Player Recommendation Weapon | S | lrhand | 1820 | 342 | 132 | 325 |
| 15321 | Player Commendation - Arcana Macw - Player Recommendation Weapon | S | rhand | 1300 | 225 | 175 | 379 |
| 20168 | Basalt Battlehammer (Event) - 4-hour limited period | S | rhand | 523 | 281 | 132 | 379 |
| 20169 | Dragon Hunter Axe (Event) - 4-hour limited period | S | lrhand | 607 | 342 | 132 | 325 |
| 20170 | Arcana Mace (Event) - 4-hour limited period | S | rhand | 433 | 225 | 175 | 379 |
| 20171 | Imperial Staff (Event) - 4-hour limited period | S | lrhand | 303 | 274 | 175 | 325 |
| 21821 | Arcana Mace of Fortune - 90-day limited period | S | rhand | 1300 | 225 | 175 | 379 |
| 21824 | Basalt Battlehammer of Fortune - 90-day limited period | S | rhand | 1570 | 281 | 132 | 379 |
| 21836 | Dynasty Cudgel of Fortune - 90-day limited period | S | rhand | 1740 | 333 | 151 | 379 |
| 10220 | Icarus Hammer | S80 | rhand | 1740 | 363 | 163 | 379 |
| 10222 | Icarus Hall | S80 | rhand | 1080 | 290 | 217 | 379 |
| 10452 | Icarus Hammer - Anger | S80 | rhand | 1740 | 363 | 163 | 379 |
| 10453 | Icarus Hammer - Health | S80 | rhand | 1740 | 363 | 163 | 379 |
| 10454 | Icarus Hammer - Rsk. Focus | S80 | rhand | 1740 | 363 | 163 | 379 |
| 10455 | Icarus Hall - Mana Up | S80 | rhand | 1080 | 290 | 217 | 379 |
| 10456 | Icarus Hall - Conversion | S80 | rhand | 1080 | 290 | 217 | 379 |
| 10457 | Icarus Hall - Acumen | S80 | rhand | 1080 | 290 | 217 | 379 |
| 11333 | Icarus Hammer - Earth | S80 | rhand | 1740 | 363 | 163 | 379 |
| 11334 | Icarus Hammer - Earth - Anger | S80 | rhand | 1740 | 363 | 163 | 379 |
| 11335 | Icarus Hammer - Earth - Health | S80 | rhand | 1740 | 363 | 163 | 379 |
| 11336 | Icarus Hammer - Earth - Rsk. Focus | S80 | rhand | 1740 | 363 | 163 | 379 |
| 11345 | Icarus Hall - Hail | S80 | rhand | 1080 | 290 | 217 | 379 |
| 11346 | Icarus Hall - Hail - Mana Up | S80 | rhand | 1080 | 290 | 217 | 379 |
| 11347 | Icarus Hall - Hail - Conversion | S80 | rhand | 1080 | 290 | 217 | 379 |
| 11348 | Icarus Hall - Hail - Acumen | S80 | rhand | 1080 | 290 | 217 | 379 |
| 14368 | Icarus Hammer {PvP} | S80 | rhand | 1740 | 363 | 163 | 379 |
| 14370 | Icarus Hall {PvP} | S80 | rhand | 1080 | 290 | 217 | 379 |
| 14394 | Icarus Hammer {PvP} - Anger | S80 | rhand | 1740 | 363 | 163 | 379 |
| 14395 | Icarus Hammer {PvP} - Health | S80 | rhand | 1740 | 363 | 163 | 379 |
| 14396 | Icarus Hammer {PvP} - Rsk. Focus | S80 | rhand | 1740 | 363 | 163 | 379 |
| 14397 | Icarus Hall {PvP} - Mana Up | S80 | rhand | 1080 | 290 | 217 | 379 |
| 14398 | Icarus Hall {PvP} - Conversion | S80 | rhand | 1080 | 290 | 217 | 379 |
| 14399 | Icarus Hall {PvP} - Acumen | S80 | rhand | 1080 | 290 | 217 | 379 |
| 14445 | Icarus Hammer - Earth {PvP} | S80 | rhand | 1740 | 363 | 163 | 379 |
| 14446 | Icarus Hammer - Earth {PvP} - Anger | S80 | rhand | 1740 | 363 | 163 | 379 |
| 14447 | Icarus Hammer - Earth {PvP} - Health | S80 | rhand | 1740 | 363 | 163 | 379 |
| 14448 | Icarus Hammer - Earth {PvP} - Rsk. Focus | S80 | rhand | 1740 | 363 | 163 | 379 |
| 14457 | Icarus Hall - Hail {PvP} | S80 | rhand | 1080 | 290 | 217 | 379 |
| 14458 | Icarus Hall - Hail {PvP} - Mana Up | S80 | rhand | 1080 | 290 | 217 | 379 |
| 14459 | Icarus Hall - Hail {PvP} - Conversion | S80 | rhand | 1080 | 290 | 217 | 379 |
| 14460 | Icarus Hall - Hail {PvP} - Acumen | S80 | rhand | 1080 | 290 | 217 | 379 |
| 13463 | Vesper Avenger | S84 | rhand | 1740 | 396 | 176 | 379 |
| 13464 | Vesper Retributer | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 13465 | Vesper Caster | S84 | rhand | 1080 | 317 | 234 | 379 |
| 13466 | Vesper Singer | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 14136 | Vesper Avenger - HP Drain | S84 | rhand | 1740 | 396 | 176 | 379 |
| 14137 | Vesper Avenger - Health | S84 | rhand | 1740 | 396 | 176 | 379 |
| 14138 | Vesper Avenger - HP Regeneration | S84 | rhand | 1740 | 396 | 176 | 379 |
| 14139 | Vesper Retributer - HP Regeneration | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14140 | Vesper Retributer - Health | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14141 | Vesper Retributer - HP Drain | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14142 | Vesper Caster - Acumen | S84 | rhand | 1080 | 317 | 234 | 379 |
| 14143 | Vesper Caster - MP Regeneration | S84 | rhand | 1080 | 317 | 234 | 379 |
| 14144 | Vesper Caster - Mana Up | S84 | rhand | 1080 | 317 | 234 | 379 |
| 14145 | Vesper Singer - Empower | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 14146 | Vesper Singer - MP Regeneration | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 14147 | Vesper Singer - Magic Hold | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 14469 | Vesper Avenger {PvP} | S84 | rhand | 1740 | 396 | 176 | 379 |
| 14470 | Vesper Retributer {PvP} | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14471 | Vesper Caster {PvP} | S84 | rhand | 1080 | 317 | 234 | 379 |
| 14472 | Vesper Singer {PvP} | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 14496 | Vesper Avenger {PvP} - HP Drain | S84 | rhand | 1740 | 396 | 176 | 379 |
| 14497 | Vesper Avenger {PvP} - Health | S84 | rhand | 1740 | 396 | 176 | 379 |
| 14498 | Vesper Avenger {PvP} - HP Regeneration | S84 | rhand | 1740 | 396 | 176 | 379 |
| 14499 | Vesper Retributer {PvP} - HP Regeneration | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14500 | Vesper Retributer {PvP} - Health | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14501 | Vesper Retributer {PvP} - HP Drain | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 14502 | Vesper Caster {PvP} - Acumen | S84 | rhand | 1080 | 317 | 234 | 379 |
| 14503 | Vesper Caster {PvP} - MP Regeneration | S84 | rhand | 1080 | 317 | 234 | 379 |
| 14504 | Vesper Caster {PvP} - Mana Up | S84 | rhand | 1080 | 317 | 234 | 379 |
| 14505 | Vesper Singer {PvP} - Empower | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 14506 | Vesper Singer {PvP} - MP Regeneration | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 14507 | Vesper Singer {PvP} - Magic Hold | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 15546 | Eversor Mace | S84 | rhand | 1740 | 437 | 192 | 379 |
| 15547 | Contristo Hammer | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15551 | Sacredium | S84 | rhand | 1080 | 350 | 256 | 379 |
| 15552 | Cyclic Cane | S84 | lrhand | 1080 | 426 | 281 | 325 |
| 15560 | Vigwik Axe | S84 | rhand | 1740 | 415 | 183 | 379 |
| 15561 | Devilish Maul | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15565 | Rising Star | S84 | rhand | 1080 | 332 | 244 | 379 |
| 15566 | Black Visage | S84 | lrhand | 1080 | 404 | 268 | 325 |
| 15678 | Triumph Hammer | S84 | rhand | 1740 | 396 | 183 | 379 |
| 15679 | Triumph Crusher | S84 | lrhand | 1740 | 482 | 183 | 325 |
| 15683 | Triumph Staff | S84 | rhand | 1080 | 317 | 244 | 379 |
| 15684 | Triumph Two Hand Staff | S84 | lrhand | 1080 | 386 | 268 | 325 |
| 15835 | Vigwik Axe - Health | S84 | rhand | 1740 | 415 | 183 | 379 |
| 15836 | Vigwik Axe - HP Regeneration | S84 | rhand | 1740 | 415 | 183 | 379 |
| 15837 | Vigwik Axe - HP Drain | S84 | rhand | 1740 | 415 | 183 | 379 |
| 15838 | Devilish Maul - Health | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15839 | Devilish Maul - HP Drain | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15840 | Devilish Maul - HP Regeneration | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15850 | Rising Star - MP Regeneration | S84 | rhand | 1080 | 332 | 244 | 379 |
| 15851 | Rising Star - Mana Up | S84 | rhand | 1080 | 332 | 244 | 379 |
| 15852 | Rising Star - Acumen | S84 | rhand | 1080 | 332 | 244 | 379 |
| 15853 | Black Visage - MP Regeneration | S84 | lrhand | 1080 | 404 | 268 | 325 |
| 15854 | Black Visage - Magic Hold | S84 | lrhand | 1080 | 404 | 268 | 325 |
| 15855 | Black Visage - Empower | S84 | lrhand | 1080 | 404 | 268 | 325 |
| 15877 | Eversor Mace - HP Regeneration | S84 | rhand | 1740 | 437 | 192 | 379 |
| 15878 | Eversor Mace - HP Drain | S84 | rhand | 1740 | 437 | 192 | 379 |
| 15879 | Eversor Mace - Health | S84 | rhand | 1740 | 437 | 192 | 379 |
| 15880 | Contristo Hammer - HP Drain | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15881 | Contristo Hammer - HP Regeneration | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15882 | Contristo Hammer - Health | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15892 | Sacredium - Mana Up | S84 | rhand | 1080 | 350 | 256 | 379 |
| 15893 | Sacredium - Acumen | S84 | rhand | 1080 | 350 | 256 | 379 |
| 15894 | Sacredium - MP Regeneration | S84 | rhand | 1080 | 350 | 256 | 379 |
| 15895 | Cyclic Cane - Magic Hold | S84 | lrhand | 1080 | 426 | 281 | 325 |
| 15896 | Cyclic Cane - Empower | S84 | lrhand | 1080 | 426 | 281 | 325 |
| 15897 | Cyclic Cane - MP Regeneration | S84 | lrhand | 1080 | 426 | 281 | 325 |
| 15915 | Eversor Mace {PvP} | S84 | rhand | 1740 | 437 | 192 | 379 |
| 15916 | Contristo Hammer {PvP} | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15920 | Sacredium {PvP} | S84 | rhand | 1080 | 350 | 256 | 379 |
| 15921 | Cyclic Cane {PvP} | S84 | lrhand | 1080 | 426 | 281 | 325 |
| 15929 | Vigwik Axe {PvP} | S84 | rhand | 1740 | 415 | 183 | 379 |
| 15930 | Devilish Maul {PvP} | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15934 | Rising Star {PvP} | S84 | rhand | 1080 | 332 | 244 | 379 |
| 15935 | Black Visage {PvP} | S84 | lrhand | 1080 | 404 | 268 | 325 |
| 15947 | Vigwik Axe {PvP} - Health | S84 | rhand | 1740 | 415 | 183 | 379 |
| 15948 | Vigwik Axe {PvP} - HP Regeneration | S84 | rhand | 1740 | 415 | 183 | 379 |
| 15949 | Vigwik Axe {PvP} - HP Drain | S84 | rhand | 1740 | 415 | 183 | 379 |
| 15950 | Devilish Maul {PvP} - Health | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15951 | Devilish Maul {PvP} - HP Drain | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15952 | Devilish Maul {PvP} - HP Regeneration | S84 | lrhand | 1740 | 505 | 183 | 325 |
| 15962 | Rising Star {PvP} - MP Regeneration | S84 | rhand | 1080 | 332 | 244 | 379 |
| 15963 | Rising Star {PvP} - Mana Up | S84 | rhand | 1080 | 332 | 244 | 379 |
| 15964 | Rising Star {PvP} - Acumen | S84 | rhand | 1080 | 332 | 244 | 379 |
| 15965 | Black Visage {PvP} - MP Regeneration | S84 | lrhand | 1080 | 404 | 268 | 325 |
| 15966 | Black Visage {PvP} - Magic Hold | S84 | lrhand | 1080 | 404 | 268 | 325 |
| 15967 | Black Visage {PvP} - Empower | S84 | lrhand | 1080 | 404 | 268 | 325 |
| 15989 | Eversor Mace {PvP} - HP Regeneration | S84 | rhand | 1740 | 437 | 192 | 379 |
| 15990 | Eversor Mace {PvP} - HP Drain | S84 | rhand | 1740 | 437 | 192 | 379 |
| 15991 | Eversor Mace {PvP} - Health | S84 | rhand | 1740 | 437 | 192 | 379 |
| 15992 | Contristo Hammer {PvP} - HP Drain | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15993 | Contristo Hammer {PvP} - HP Regeneration | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 15994 | Contristo Hammer {PvP} - Health | S84 | lrhand | 1740 | 532 | 192 | 325 |
| 16004 | Sacredium {PvP} - Mana Up | S84 | rhand | 1080 | 350 | 256 | 379 |
| 16005 | Sacredium {PvP} - Acumen | S84 | rhand | 1080 | 350 | 256 | 379 |
| 16006 | Sacredium {PvP} - MP Regeneration | S84 | rhand | 1080 | 350 | 256 | 379 |
| 16007 | Cyclic Cane {PvP} - Magic Hold | S84 | lrhand | 1080 | 426 | 281 | 325 |
| 16008 | Cyclic Cane {PvP} - Empower | S84 | lrhand | 1080 | 426 | 281 | 325 |
| 16009 | Cyclic Cane {PvP} - MP Regeneration | S84 | lrhand | 1080 | 426 | 281 | 325 |
| 16048 | Vesper Avenger - Landslide | S84 | rhand | 1740 | 396 | 176 | 379 |
| 16049 | Vesper Retributer - Gale | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16050 | Vesper Caster - Cleverness | S84 | rhand | 1080 | 317 | 234 | 379 |
| 16051 | Vesper Singer - Hail | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 16074 | Vesper Avenger - Landslide - HP Drain | S84 | rhand | 1740 | 396 | 176 | 379 |
| 16075 | Vesper Avenger - Landslide - Health | S84 | rhand | 1740 | 396 | 176 | 379 |
| 16076 | Vesper Avenger - Landslide - HP Regeneration | S84 | rhand | 1740 | 396 | 176 | 379 |
| 16077 | Vesper Retributer - Gale - HP Regeneration | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16078 | Vesper Retributer - Gale - Health | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16079 | Vesper Retributer - Gale - HP Drain | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16080 | Vesper Caster - Cleverness - Acumen | S84 | rhand | 1080 | 317 | 234 | 379 |
| 16081 | Vesper Caster - Cleverness - MP Regeneration | S84 | rhand | 1080 | 317 | 234 | 379 |
| 16082 | Vesper Caster - Cleverness - Mana Up | S84 | rhand | 1080 | 317 | 234 | 379 |
| 16083 | Vesper Singer - Hail - Empower | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 16084 | Vesper Singer - Hail - MP Regeneration | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 16085 | Vesper Singer - Hail - Magic Hold | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 16140 | Vesper Avenger - Landslide {PvP} | S84 | rhand | 1740 | 396 | 176 | 379 |
| 16141 | Vesper Retributer - Gale {PvP} | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16142 | Vesper Caster - Cleverness {PvP} | S84 | rhand | 1080 | 317 | 234 | 379 |
| 16143 | Vesper Singer - Hail {PvP} | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 16197 | Vesper Avenger - Landslide {PvP} - HP Drain | S84 | rhand | 1740 | 396 | 176 | 379 |
| 16198 | Vesper Avenger - Landslide {PvP} - Health | S84 | rhand | 1740 | 396 | 176 | 379 |
| 16199 | Vesper Avenger - Landslide {PvP} - HP Regeneration | S84 | rhand | 1740 | 396 | 176 | 379 |
| 16200 | Vesper Retributer - Gale {PvP} - HP Regeneration | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16201 | Vesper Retributer - Gale {PvP} - Health | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16202 | Vesper Retributer - Gale {PvP} - HP Drain | S84 | lrhand | 1740 | 482 | 176 | 325 |
| 16203 | Vesper Caster - Cleverness {PvP} - Acumen | S84 | rhand | 1080 | 317 | 234 | 379 |
| 16204 | Vesper Caster - Cleverness {PvP} - MP Regeneration | S84 | rhand | 1080 | 317 | 234 | 379 |
| 16205 | Vesper Caster - Cleverness {PvP} - Mana Up | S84 | rhand | 1080 | 317 | 234 | 379 |
| 16206 | Vesper Singer - Hail {PvP} - Empower | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 16207 | Vesper Singer - Hail {PvP} - MP Regeneration | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 16208 | Vesper Singer - Hail {PvP} - Magic Hold | S84 | lrhand | 1080 | 386 | 257 | 325 |
| 21939 | Claw of Destruction | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21940 | Claw of Destruction - HP Drain | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21941 | Claw of Destruction - Health | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21942 | Claw of Destruction - HP Regeneration | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21943 | Claw of Destruction {PvP} | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21944 | Claw of Destruction {PvP} - HP Drain | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21945 | Claw of Destruction {PvP} - Health | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21946 | Claw of Destruction {PvP} - HP Regeneration | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21947 | Claw of Destruction - Landslide | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21948 | Claw of Destruction - Landslide - HP Drain | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21949 | Claw of Destruction - Landslide - Health | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21950 | Claw of Destruction - Landslide - HP Regeneration | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21951 | Claw of Destruction - Landslide {PvP} | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21952 | Claw of Destruction - Landslide {PvP} - HP Drain | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21953 | Claw of Destruction - Landslide {PvP} - Health | S84 | rhand | 1740 | 396 | 176 | 379 |
| 21954 | Claw of Destruction - Landslide {PvP} - HP Regeneration | S84 | rhand | 1740 | 396 | 176 | 379 |

### DAGGER (294)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 10 | Dagger | NONE | rhand | 1160 | 5 | 5 | 433 |
| 11 | Bone Dagger | NONE | rhand | 1150 | 7 | 6 | 433 |
| 12 | Knife | NONE | rhand | 1140 | 10 | 9 | 433 |
| 215 | Doom Dagger | NONE | rhand | 1130 | 10 | 9 | 433 |
| 216 | Dirk | NONE | rhand | 1130 | 15 | 12 | 433 |
| 217 | Shining Knife | NONE | rhand | 1120 | 21 | 17 | 433 |
| 218 | Throwing Knife | NONE | rhand | 1120 | 21 | 17 | 433 |
| 219 | Sword Breaker | NONE | rhand | 1110 | 27 | 21 | 433 |
| 946 | Skeleton Dagger | NONE | rhand | 1100 | 16 | 13 | 433 |
| 989 | Eldritch Dagger | NONE | rhand | 1130 | 11 | 10 | 433 |
| 1182 | Neti's Dagger | NONE | rhand | 1000 | 19 | 16 | 433 |
| 1305 | Knife | NONE | rhand | 120 | 30000 | 6 | 433 |
| 1306 | Crafted Dagger | NONE | rhand | 100 | 22 | 6 | 433 |
| 2372 | Dagger of Adept | NONE | rhand | 1050 | 11 | 10 | 433 |
| 2374 | Red Sunset Dagger | NONE | rhand | 1100 | 11 | 10 | 433 |
| 3471 | Cybellin's Dagger | NONE | rhand | 400 | 10 | 9 | 433 |
| 4220 | Dream Knife | NONE | rhand | 1110 | 27 | 21 | 433 |
| 4665 | Pipette Knife | NONE | rhand | 1140 | 10 | 9 | 433 |
| 7818 | Apprentice Adventurer's Knife | NONE | rhand | 1120 | 21 | 17 | 433 |
| 8529 | For Monsters Only (Knife) | NONE | rhand | 1140 | 10 | 9 | 433 |
| 8578 | Shining Knife (Event) | NONE | rhand | 1120 | 21 | 17 | 433 |
| 8978 | Shadow Item: Sword Breaker | NONE | rhand | 370 | 27 | 21 | 433 |
| 9904 | Improved Sword Breaker | NONE | rhand | 1110 | 27 | 21 | 433 |
| 10476 | Shadow Item - Shining Knife | NONE | rhand | 1120 | 21 | 17 | 433 |
| 13159 | Player Commendation - Sword Breaker - Player Commendation Weapon | NONE | rhand | 1110 | 27 | 21 | 433 |
| 14625 | Santa Claus' Naga Storm | NONE | rhand | 930 | 45 | 38 | 433 |
| 14781 | Baguette's Dagger | NONE | rhand | 1130 |  |  |  |
| 20256 | Baguette Dagger - 7-day limited period | NONE | rhand | 500 | 1 | 2 | 433 |
| 220 | Crafted Dagger | D | rhand | 1100 | 35 | 26 | 433 |
| 221 | Assassin Knife | D | rhand | 1100 | 35 | 26 | 433 |
| 222 | Poniard Dagger | D | rhand | 1090 | 45 | 32 | 433 |
| 223 | Kukuri | D | rhand | 1080 | 56 | 39 | 433 |
| 224 | Maingauche | D | rhand | 1070 | 69 | 47 | 433 |
| 225 | Mithril Dagger | D | rhand | 1060 | 80 | 54 | 433 |
| 238 | Dagger of Mana | D | rhand | 750 | 45 | 52 | 433 |
| 239 | Mystic Knife | D | rhand | 760 | 45 | 52 | 433 |
| 240 | Conjurer's Knife | D | rhand | 750 | 45 | 52 | 433 |
| 241 | Shilen Knife | D | rhand | 750 | 45 | 52 | 433 |
| 1471 | Silenos Blowgun | D | rhand | 300 | 5 | 5 | 433 |
| 1660 | Cursed Maingauche | D | rhand | 1070 | 62 | 42 | 433 |
| 2507 | Lizardspear | D | rhand | 300 | 5 | 5 | 433 |
| 4028 | Giant Cannon | D | rhand | 300 | 5 | 5 | 433 |
| 5127 | Dailaon Knife | D | rhand | 300 | 5 | 5 | 433 |
| 5128 | Crokian Blade | D | rhand | 300 | 5 | 5 | 433 |
| 5130 | Nos Sword | D | rhand | 300 | 5 | 5 | 433 |
| 5131 | Parhit Staff | D | rhand | 300 | 5 | 5 | 433 |
| 5132 | Giant Trident | D | rhand | 300 | 5 | 5 | 433 |
| 7830 | Traveler's Poniard Dagger | D | rhand | 1090 | 45 | 32 | 433 |
| 8590 | Poniard Dagger (Event) | D | rhand | 1090 | 45 | 32 | 433 |
| 8825 | Shadow Item: Kukuri | D | rhand | 360 | 56 | 39 | 433 |
| 8826 | Shadow Item: Dagger of Mana | D | rhand | 250 | 45 | 52 | 433 |
| 8986 | Shadow Item: Kukuri | D | rhand | 360 | 56 | 39 | 433 |
| 8987 | Shadow Item: Dagger of Mana | D | rhand | 250 | 45 | 52 | 433 |
| 9641 | Tears l1 | D | rhand | 300 | 5 | 5 | 433 |
| 9642 | Tears l2 | D | rhand | 300 | 5 | 5 | 433 |
| 9643 | Tears l3 | D | rhand | 300 | 5 | 5 | 433 |
| 11613 | Common Item - Crafted Dagger | D | rhand | 367 | 35 | 26 | 433 |
| 11617 | Common Item - Assassin Knife | D | rhand | 367 | 35 | 26 | 433 |
| 11646 | Common Item - Poniard Dagger | D | rhand | 363 | 45 | 32 | 433 |
| 11660 | Common Item - Shilen Knife | D | rhand | 250 | 45 | 52 | 433 |
| 11662 | Common Item - Dagger of Mana | D | rhand | 250 | 45 | 52 | 433 |
| 11664 | Common Item - Mystic Knife | D | rhand | 253 | 45 | 52 | 433 |
| 11672 | Common Item - Conjuror's Knife | D | rhand | 250 | 45 | 52 | 433 |
| 11673 | Common Item - Kukuri | D | rhand | 360 | 56 | 39 | 433 |
| 11685 | Common Item - Maingauche | D | rhand | 357 | 69 | 47 | 433 |
| 11706 | Common Item - Cursed Maingauche | D | rhand | 357 | 62 | 42 | 433 |
| 11726 | Common Item - Mithril Dagger | D | rhand | 353 | 80 | 54 | 433 |
| 13170 | Player Commendation - Mithril Dagger - Player Commendation Weapon | D | rhand | 1060 | 80 | 54 | 433 |
| 13843 | Draconic Peltast Weapon | D | rhand | 300 | 5 | 5 | 433 |
| 15039 | Mithril Dagger of Fortune - 30-day limited period | D | rhand | 1060 | 80 | 54 | 433 |
| 15153 | Mithril Dagger of Fortune - 10-day limited period | D | rhand | 1060 | 80 | 54 | 433 |
| 16927 | Mithril Dagger of Fortune - 90-day limited period | D | rhand | 1060 | 80 | 54 | 433 |
| 20111 | Maingauche (Event) - 4-hour limited period | D | rhand | 357 | 69 | 47 | 433 |
| 21731 | Maingauche - Event | D | rhand | 1070 | 69 | 47 | 433 |
| 226 | Cursed Dagger | C | rhand | 1040 | 94 | 61 | 433 |
| 227 | Stiletto | C | rhand | 1030 | 107 | 68 | 433 |
| 228 | Crystal Dagger | C | rhand | 1000 | 136 | 83 | 433 |
| 230 | Wolverine Needle | C | rhand | 1040 | 94 | 61 | 433 |
| 231 | Grace Dagger | C | rhand | 1020 | 122 | 76 | 433 |
| 232 | Dark Elven Dagger | C | rhand | 1050 | 94 | 61 | 433 |
| 233 | Dark Screamer | C | rhand | 1010 | 122 | 76 | 433 |
| 242 | Soulfire Dirk | C | rhand | 750 | 86 | 91 | 433 |
| 4759 | Cursed Dagger - Critical Bleed | C | rhand | 1040 | 94 | 61 | 433 |
| 4760 | Cursed Dagger - Critical Poison | C | rhand | 1040 | 94 | 61 | 433 |
| 4761 | Cursed Dagger - Rsk. Haste | C | rhand | 1040 | 94 | 61 | 433 |
| 4762 | Dark Elven Dagger - Focus | C | rhand | 1050 | 94 | 61 | 433 |
| 4763 | Dark Elven Dagger - Back Blow | C | rhand | 1050 | 94 | 61 | 433 |
| 4764 | Dark Elven Dagger - Mortal Strike | C | rhand | 1050 | 94 | 61 | 433 |
| 4765 | Stiletto - Critical Bleed | C | rhand | 1030 | 107 | 68 | 433 |
| 4766 | Stiletto - Critical Poison | C | rhand | 1030 | 107 | 68 | 433 |
| 4767 | Stiletto - Mortal Strike | C | rhand | 1030 | 107 | 68 | 433 |
| 4768 | Grace Dagger - Evasion | C | rhand | 1020 | 122 | 76 | 433 |
| 4769 | Grace Dagger - Focus | C | rhand | 1020 | 122 | 76 | 433 |
| 4770 | Grace Dagger - Back Blow | C | rhand | 1020 | 122 | 76 | 433 |
| 4771 | Dark Screamer - Evasion | C | rhand | 1010 | 122 | 76 | 433 |
| 4772 | Dark Screamer - Focus | C | rhand | 1010 | 122 | 76 | 433 |
| 4773 | Dark Screamer - Critical Bleed | C | rhand | 1010 | 122 | 76 | 433 |
| 4774 | Crystal Dagger - Critical Bleed | C | rhand | 1000 | 136 | 83 | 433 |
| 4775 | Crystal Dagger - Critical Poison | C | rhand | 1000 | 136 | 83 | 433 |
| 4776 | Crystal Dagger - Mortal Strike | C | rhand | 1000 | 136 | 83 | 433 |
| 6356 | Dark Elven Dagger - Rsk. Haste | C | rhand | 1050 | 94 | 61 | 433 |
| 6357 | Stiletto - Rsk. Haste | C | rhand | 1030 | 107 | 68 | 433 |
| 6358 | Crystal Dagger - Critical Damage | C | rhand | 1000 | 136 | 83 | 433 |
| 7810 | Soulfire Dirk - Mana Up | C | rhand | 750 | 86 | 91 | 433 |
| 7811 | Soulfire Dirk - Magic Hold | C | rhand | 750 | 86 | 91 | 433 |
| 7812 | Soulfire Dirk - Magic Silence | C | rhand | 750 | 86 | 91 | 433 |
| 8833 | Shadow Item: Stiletto | C | rhand | 350 | 107 | 68 | 433 |
| 8834 | Shadow Item: Soulfire Dirk | C | rhand | 250 | 86 | 91 | 433 |
| 8844 | Shadow Item: Dark Screamer | C | rhand | 340 | 122 | 76 | 433 |
| 8931 | Shadow Item: Dark Screamer | C | rhand | 340 | 122 | 76 | 433 |
| 8996 | Shadow Item: Dark Screamer | C | rhand | 340 | 122 | 76 | 433 |
| 11746 | Common Item - Wolverine Needle | C | rhand | 347 | 94 | 61 | 433 |
| 11747 | Common Item - Dark Elven Dagger | C | rhand | 350 | 94 | 61 | 433 |
| 11762 | Common Item - Cursed Dagger | C | rhand | 347 | 94 | 61 | 433 |
| 11779 | Common Item - Soulfire Dirk | C | rhand | 250 | 86 | 91 | 433 |
| 11788 | Common Item - Stiletto | C | rhand | 343 | 107 | 68 | 433 |
| 11800 | Common Item - Grace Dagger | C | rhand | 340 | 122 | 76 | 433 |
| 11803 | Common Item - Dark Screamer | C | rhand | 337 | 122 | 76 | 433 |
| 11863 | Common Item - Crystal Dagger | C | rhand | 333 | 136 | 83 | 433 |
| 13182 | Player Commendation - Crystal Dagger - Player Commendation Weapon | C | rhand | 1000 | 136 | 83 | 433 |
| 15038 | Dark Screamer of Fortune - 30-day limited period | C | rhand | 1010 | 122 | 76 | 433 |
| 15152 | Dark Screamer of Fortune - 10-day limited period | C | rhand | 1010 | 122 | 76 | 433 |
| 16926 | Dark Screamer of Fortune - 90-day limited period | C | rhand | 1010 | 122 | 76 | 433 |
| 20125 | Crystal Dagger (Event) - 4-hour limited period | C | rhand | 333 | 136 | 83 | 433 |
| 229 | Kris | B | rhand | 980 | 153 | 91 | 433 |
| 234 | Demon's Dagger | B | rhand | 970 | 170 | 99 | 433 |
| 243 | Hell Knife | B | rhand | 740 | 122 | 122 | 433 |
| 4777 | Kris - Evasion | B | rhand | 980 | 153 | 91 | 433 |
| 4778 | Kris - Focus | B | rhand | 980 | 153 | 91 | 433 |
| 4779 | Kris - Back Blow | B | rhand | 980 | 153 | 91 | 433 |
| 4780 | Demon's Dagger - Critical Bleed | B | rhand | 970 | 170 | 99 | 433 |
| 4781 | Demon's Dagger - Critical Poison | B | rhand | 970 | 170 | 99 | 433 |
| 4782 | Demon's Dagger - Mortal Strike | B | rhand | 970 | 170 | 99 | 433 |
| 4786 | Hell Knife - Focus | B | rhand | 740 | 122 | 122 | 433 |
| 4787 | Hell Knife - Back Blow | B | rhand | 740 | 122 | 122 | 433 |
| 4788 | Hell Knife - Mortal Strike | B | rhand | 740 | 122 | 122 | 433 |
| 6359 | Demon's Dagger - Critical Damage | B | rhand | 970 | 170 | 99 | 433 |
| 7813 | Hell Knife - Magic Regeneration | B | rhand | 740 | 122 | 122 | 433 |
| 7814 | Hell Knife - Mental Shield | B | rhand | 740 | 122 | 122 | 433 |
| 7815 | Hell Knife - Magic Weakness | B | rhand | 740 | 122 | 122 | 433 |
| 8854 | Shadow Item: Kris | B | rhand | 330 | 153 | 91 | 433 |
| 9006 | Shadow Item: Kris | B | rhand | 330 | 153 | 91 | 433 |
| 10926 | Kris - Confusion | B | rhand | 980 | 153 | 91 | 433 |
| 10927 | Kris - Confusion - Evasion | B | rhand | 980 | 153 | 91 | 433 |
| 10928 | Kris - Confusion - Focus | B | rhand | 980 | 153 | 91 | 433 |
| 10929 | Kris - Confusion - Back Blow | B | rhand | 980 | 153 | 91 | 433 |
| 10942 | Hell Knife - Confusion | B | rhand | 740 | 122 | 122 | 433 |
| 10943 | Hell Knife - Confusion - Magic Regeneration | B | rhand | 740 | 122 | 122 | 433 |
| 10944 | Hell Knife - Confusion - Mental Shield | B | rhand | 740 | 122 | 122 | 433 |
| 10945 | Hell Knife - Confusion - Magic Weakness | B | rhand | 740 | 122 | 122 | 433 |
| 10992 | Demon's Dagger - Great Gale | B | rhand | 970 | 170 | 99 | 433 |
| 10993 | Demon's Dagger - Great Gale - Critical Bleed | B | rhand | 970 | 170 | 99 | 433 |
| 10994 | Demon's Dagger - Great Gale - Critical Poison | B | rhand | 970 | 170 | 99 | 433 |
| 10995 | Demon's Dagger - Great Gale - Mortal Strike | B | rhand | 970 | 170 | 99 | 433 |
| 10996 | Demon's Dagger - Great Gale - Critical Damage | B | rhand | 970 | 170 | 99 | 433 |
| 11915 | Common Item - Kris | B | rhand | 327 | 153 | 91 | 433 |
| 11919 | Common Item - Hell Knife | B | rhand | 247 | 122 | 122 | 433 |
| 11939 | Common Item - Demon's Dagger | B | rhand | 323 | 170 | 99 | 433 |
| 11940 | Common Item - Demon's Dagger | B | rhand | 323 | 170 | 99 | 433 |
| 13199 | Player Commendation - Devil's Dagger - Player Commendation Weapon | B | rhand | 970 | 170 | 99 | 433 |
| 15037 | Kris of Fortune - 30-day limited period | B | rhand | 980 | 153 | 91 | 433 |
| 15151 | Kris of Fortune - 10-day limited period | B | rhand | 980 | 153 | 91 | 433 |
| 16925 | Kris of Fortune - 90-day limited period | B | rhand | 980 | 153 | 91 | 433 |
| 20139 | Demon's Dagger (Event) - 4-hour limited period | B | rhand | 323 | 170 | 99 | 433 |
| 235 | Bloody Orchid | A | rhand | 960 | 186 | 107 | 433 |
| 236 | Soul Separator | A | rhand | 950 | 203 | 114 | 433 |
| 4783 | Bloody Orchid - Evasion | A | rhand | 960 | 186 | 107 | 433 |
| 4784 | Bloody Orchid - Focus | A | rhand | 960 | 186 | 107 | 433 |
| 4785 | Bloody Orchid - Back Blow | A | rhand | 960 | 186 | 107 | 433 |
| 5614 | Bloody Orchid - Focus | A | rhand | 960 | 186 | 107 | 433 |
| 5615 | Bloody Orchid - Back Blow | A | rhand | 960 | 186 | 107 | 433 |
| 5616 | Bloody Orchid - Critical Bleed | A | rhand | 960 | 186 | 107 | 433 |
| 5617 | Soul Separator - Guidance | A | rhand | 950 | 203 | 114 | 433 |
| 5618 | Soul Separator - Critical Damage | A | rhand | 950 | 203 | 114 | 433 |
| 5619 | Soul Separator - Rsk. Haste | A | rhand | 950 | 203 | 114 | 433 |
| 8682 | Naga Storm | A | rhand | 930 | 220 | 121 | 433 |
| 8800 | Naga Storm - Focus | A | rhand | 930 | 220 | 121 | 433 |
| 8801 | Naga Storm - Critical Damage | A | rhand | 930 | 220 | 121 | 433 |
| 8802 | Naga Storm - Back Blow | A | rhand | 930 | 220 | 121 | 433 |
| 8862 | Shadow Item: Bloody Orchid | A | rhand | 320 | 186 | 107 | 433 |
| 9014 | Shadow Item: Bloody Orchid | A | rhand | 320 | 186 | 107 | 433 |
| 9025 | Shadow Item: Soul Separator | A | rhand | 317 | 203 | 114 | 433 |
| 10679 | Naga Storm {PvP} - Focus | A | rhand | 930 | 220 | 121 | 433 |
| 10680 | Naga Storm {PvP} - Critical Damage | A | rhand | 930 | 220 | 121 | 433 |
| 10681 | Naga Storm {PvP} - Back Blow | A | rhand | 930 | 220 | 121 | 433 |
| 11037 | Bloody Orchid - Confusion | A | rhand | 960 | 186 | 107 | 433 |
| 11038 | Bloody Orchid - Confusion - Focus | A | rhand | 960 | 186 | 107 | 433 |
| 11039 | Bloody Orchid - Confusion - Back Blow | A | rhand | 960 | 186 | 107 | 433 |
| 11040 | Bloody Orchid - Confusion - Critical Bleed | A | rhand | 960 | 186 | 107 | 433 |
| 11116 | Soul Separator - On Fire | A | rhand | 950 | 203 | 114 | 433 |
| 11117 | Soul Separator - On Fire - Guidance | A | rhand | 950 | 203 | 114 | 433 |
| 11118 | Soul Separator - On Fire - Critical Damage | A | rhand | 950 | 203 | 114 | 433 |
| 11119 | Soul Separator - On Fire - Rsk. Haste | A | rhand | 950 | 203 | 114 | 433 |
| 11133 | Naga Storm - Molar | A | rhand | 930 | 220 | 121 | 433 |
| 11134 | Naga Storm - Molar - Focus | A | rhand | 930 | 220 | 121 | 433 |
| 11135 | Naga Storm - Molar - Critical Damage | A | rhand | 930 | 220 | 121 | 433 |
| 11136 | Naga Storm - Molar - Back Blow | A | rhand | 930 | 220 | 121 | 433 |
| 11951 | Common Item - Bloody Orchid | A | rhand | 320 | 186 | 107 | 433 |
| 11973 | Common Item - Soul Separator | A | rhand | 317 | 203 | 114 | 433 |
| 11977 | Common Item - Naga Storm | A | rhand | 310 | 220 | 121 | 433 |
| 12852 | Naga Storm - Molar {PvP} - Focus | A | rhand | 930 | 220 | 121 | 433 |
| 12853 | Naga Storm - Molar {PvP} - Critical Damage | A | rhand | 930 | 220 | 121 | 433 |
| 12854 | Naga Storm - Molar {PvP} - Back Blow | A | rhand | 930 | 220 | 121 | 433 |
| 13214 | Player Commendation - Naga Storm - Player Commendation Weapon | A | rhand | 930 | 220 | 121 | 433 |
| 15036 | Naga Storm of Fortune - 30-day limited period | A | rhand | 930 | 220 | 121 | 433 |
| 15150 | Naga Storm of Fortune - 10-day limited period | A | rhand | 930 | 220 | 121 | 433 |
| 16924 | Naga Storm of Fortune - 90-day limited period | A | rhand | 930 | 220 | 121 | 433 |
| 20153 | Soul Separator (Event) - 4-hour limited period | A | rhand | 317 | 203 | 114 | 433 |
| 237 | Dragon's Tooth | S | rhand | 950 | 220 | 121 | 433 |
| 6367 | Angel Slayer | S | rhand | 950 | 246 | 132 | 433 |
| 6590 | Angel Slayer - Critical Damage | S | rhand | 950 | 246 | 132 | 433 |
| 6591 | Angel Slayer - HP Drain | S | rhand | 950 | 246 | 132 | 433 |
| 6592 | Angel Slayer - Haste | S | rhand | 950 | 246 | 132 | 433 |
| 6617 | Infinity Stinger | S | rhand | 1300 | 458 | 230 | 433 |
| 9446 | Dynasty Knife | S | rhand | 1520 | 291 | 151 | 433 |
| 9866 | Dynasty Knife - Focus | S | rhand | 1520 | 291 | 151 | 433 |
| 9867 | Dynasty Knife - Evasion | S | rhand | 1520 | 291 | 151 | 433 |
| 9868 | Dynasty Knife - Critical Damage | S | rhand | 1520 | 291 | 151 | 433 |
| 10722 | Angel Slayer {PvP} - Critical Damage | S | rhand | 950 | 246 | 132 | 433 |
| 10723 | Angel Slayer {PvP} - HP Drain | S | rhand | 950 | 246 | 132 | 433 |
| 10724 | Angel Slayer {PvP} - Haste | S | rhand | 950 | 246 | 132 | 433 |
| 10762 | Dynasty Knife {PvP} - Focus | S | rhand | 1520 | 291 | 151 | 433 |
| 10763 | Dynasty Knife {PvP} - Evasion | S | rhand | 1520 | 291 | 151 | 433 |
| 10764 | Dynasty Knife {PvP} - Critical Damage | S | rhand | 1520 | 291 | 151 | 433 |
| 11226 | Angel Slayer - Concentration | S | rhand | 950 | 246 | 132 | 433 |
| 11227 | Angel Slayer - Concentration - Critical Damage | S | rhand | 950 | 246 | 132 | 433 |
| 11228 | Angel Slayer - Concentration - HP Drain | S | rhand | 950 | 246 | 132 | 433 |
| 11229 | Angel Slayer - Concentration - Haste | S | rhand | 950 | 246 | 132 | 433 |
| 11247 | Dynasty Knife - Great Gale | S | rhand | 1520 | 291 | 151 | 433 |
| 11248 | Dynasty Knife - Great Gale - Focus | S | rhand | 1520 | 291 | 151 | 433 |
| 11249 | Dynasty Knife - Great Gale - Evasion | S | rhand | 1520 | 291 | 151 | 433 |
| 11250 | Dynasty Knife - Great Gale - Critical Damage | S | rhand | 1520 | 291 | 151 | 433 |
| 12001 | Common Item - Angel Slayer | S | rhand | 317 | 246 | 132 | 433 |
| 12922 | Angel Slayer - Concentration {PvP} - Critical Damage | S | rhand | 950 | 246 | 132 | 433 |
| 12923 | Angel Slayer - Concentration {PvP} - HP Drain | S | rhand | 950 | 246 | 132 | 433 |
| 12924 | Angel Slayer - Concentration {PvP} - Haste | S | rhand | 950 | 246 | 132 | 433 |
| 12938 | Dynasty Knife - Great Gale {PvP} - Focus | S | rhand | 1520 | 291 | 151 | 433 |
| 12939 | Dynasty Knife - Great Gale {PvP} - Evasion | S | rhand | 1520 | 291 | 151 | 433 |
| 12940 | Dynasty Knife - Great Gale {PvP} - Critical Damage | S | rhand | 1520 | 291 | 151 | 433 |
| 14560 | Dagger of Val Turner Family | S | rhand | 713 | 271 | 119 | 433 |
| 14575 | Dagger of Halter Family | S | rhand | 713 | 271 | 119 | 433 |
| 15316 | Player Commendation - Angel Slayer - Player Recommendation Weapon | S | rhand | 950 | 246 | 132 | 433 |
| 20167 | Angel Slayer (Event) - 4-hour limited period | S | rhand | 317 | 246 | 132 | 433 |
| 21822 | Angel Slayer of Fortune - 90-day limited period | S | rhand | 950 | 246 | 132 | 433 |
| 21834 | Dynasty Knife of Fortune - 90-day limited period | S | rhand | 1520 | 291 | 151 | 433 |
| 10216 | Icarus Disperser | S80 | rhand | 1520 | 318 | 163 | 433 |
| 10446 | Icarus Disperser - Focus | S80 | rhand | 1520 | 318 | 163 | 433 |
| 10447 | Icarus Disperser - Evasion | S80 | rhand | 1520 | 318 | 163 | 433 |
| 10448 | Icarus Disperser - Critical Damage | S80 | rhand | 1520 | 318 | 163 | 433 |
| 11301 | Icarus Disperser - Confusion | S80 | rhand | 1520 | 318 | 163 | 433 |
| 11302 | Icarus Disperser - Confusion - Focus | S80 | rhand | 1520 | 318 | 163 | 433 |
| 11303 | Icarus Disperser - Confusion - Evasion | S80 | rhand | 1520 | 318 | 163 | 433 |
| 11304 | Icarus Disperser - Confusion - Critical Damage | S80 | rhand | 1520 | 318 | 163 | 433 |
| 14364 | Icarus Disperser {PvP} | S80 | rhand | 1520 | 318 | 163 | 433 |
| 14388 | Icarus Disperser {PvP} - Focus | S80 | rhand | 1520 | 318 | 163 | 433 |
| 14389 | Icarus Disperser {PvP} - Evasion | S80 | rhand | 1520 | 318 | 163 | 433 |
| 14390 | Icarus Disperser {PvP} - Critical Damage | S80 | rhand | 1520 | 318 | 163 | 433 |
| 14413 | Icarus Disperser - Confusion {PvP} | S80 | rhand | 1520 | 318 | 163 | 433 |
| 14414 | Icarus Disperser - Confusion {PvP} - Focus | S80 | rhand | 1520 | 318 | 163 | 433 |
| 14415 | Icarus Disperser - Confusion {PvP} - Evasion | S80 | rhand | 1520 | 318 | 163 | 433 |
| 14416 | Icarus Disperser - Confusion {PvP} - Critical Damage | S80 | rhand | 1520 | 318 | 163 | 433 |
| 13460 | Vesper Shaper | S84 | rhand | 1520 | 346 | 176 | 433 |
| 14127 | Vesper Shaper - Critical Damage | S84 | rhand | 1520 | 346 | 176 | 433 |
| 14128 | Vesper Shaper - HP Drain | S84 | rhand | 1520 | 346 | 176 | 433 |
| 14129 | Vesper Shaper - Haste | S84 | rhand | 1520 | 346 | 176 | 433 |
| 14466 | Vesper Shaper {PvP} | S84 | rhand | 1520 | 346 | 176 | 433 |
| 14487 | Vesper Shaper {PvP} - Critical Damage | S84 | rhand | 1520 | 346 | 176 | 433 |
| 14488 | Vesper Shaper {PvP} - HP Drain | S84 | rhand | 1520 | 346 | 176 | 433 |
| 14489 | Vesper Shaper {PvP} - Haste | S84 | rhand | 1520 | 346 | 176 | 433 |
| 15545 | Mamba Edge | S84 | rhand | 1520 | 382 | 192 | 433 |
| 15559 | Skull Edge | S84 | rhand | 1520 | 363 | 183 | 433 |
| 15677 | Triumph Dagger | S84 | rhand | 1520 | 346 | 183 | 433 |
| 15832 | Skull Edge - HP Drain | S84 | rhand | 1520 | 363 | 183 | 433 |
| 15833 | Skull Edge - Haste | S84 | rhand | 1520 | 363 | 183 | 433 |
| 15834 | Skull Edge - Critical Damage | S84 | rhand | 1520 | 363 | 183 | 433 |
| 15874 | Mamba Edge - Haste | S84 | rhand | 1520 | 382 | 192 | 433 |
| 15875 | Mamba Edge - Critical Damage | S84 | rhand | 1520 | 382 | 192 | 433 |
| 15876 | Mamba Edge - HP Drain | S84 | rhand | 1520 | 382 | 192 | 433 |
| 15914 | Mamba Edge {PvP} | S84 | rhand | 1520 | 382 | 192 | 433 |
| 15928 | Skull Edge {PvP} | S84 | rhand | 1520 | 363 | 183 | 433 |
| 15944 | Skull Edge {PvP} - HP Drain | S84 | rhand | 1520 | 363 | 183 | 433 |
| 15945 | Skull Edge {PvP} - Haste | S84 | rhand | 1520 | 363 | 183 | 433 |
| 15946 | Skull Edge {PvP} - Critical Damage | S84 | rhand | 1520 | 363 | 183 | 433 |
| 15986 | Mamba Edge {PvP} - Haste | S84 | rhand | 1520 | 382 | 192 | 433 |
| 15987 | Mamba Edge {PvP} - Critical Damage | S84 | rhand | 1520 | 382 | 192 | 433 |
| 15988 | Mamba Edge {PvP} - HP Drain | S84 | rhand | 1520 | 382 | 192 | 433 |
| 16045 | Vesper Shaper - Gale | S84 | rhand | 1520 | 346 | 176 | 433 |
| 16065 | Vesper Shaper - Gale - Critical Damage | S84 | rhand | 1520 | 346 | 176 | 433 |
| 16066 | Vesper Shaper - Gale - HP Drain | S84 | rhand | 1520 | 346 | 176 | 433 |
| 16067 | Vesper Shaper - Gale - Haste | S84 | rhand | 1520 | 346 | 176 | 433 |
| 16137 | Vesper Shaper - Gale {PvP} | S84 | rhand | 1520 | 346 | 176 | 433 |
| 16188 | Vesper Shaper - Gale {PvP} - Critical Damage | S84 | rhand | 1520 | 346 | 176 | 433 |
| 16189 | Vesper Shaper - Gale {PvP} - HP Drain | S84 | rhand | 1520 | 346 | 176 | 433 |
| 16190 | Vesper Shaper - Gale {PvP} - Haste | S84 | rhand | 1520 | 346 | 176 | 433 |

### DUALDAGGER (22)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 14797 | Baguette's Two-handed Dagger | NONE | lrhand | 2150 |  |  |  |
| 13882 | Dynasty Dual Daggers | S | lrhand | 2150 | 304 | 157 | 433 |
| 14526 | Dynasty Dual Daggers - Great Gale | S | lrhand | 2150 | 304 | 157 | 433 |
| 14528 | Dynasty Dual Daggers - Great Gale {PvP} | S | lrhand | 2150 | 304 | 157 | 433 |
| 14558 | Dynasty Dual Daggers {PvP} | S | lrhand | 2150 | 304 | 157 | 433 |
| 13883 | Icarus Dual Daggers | S80 | lrhand | 2100 | 332 | 169 | 433 |
| 14461 | Icarus Dual Daggers {PvP} | S80 | lrhand | 2100 | 332 | 169 | 433 |
| 14527 | Icarus Dual Daggers - Confusion | S80 | lrhand | 2100 | 332 | 169 | 433 |
| 14529 | Icarus Dual Daggers - Confusion {PvP} | S80 | lrhand | 2100 | 332 | 169 | 433 |
| 15306 | Transparent Dual Dagger (for NPC) | S80 | lrhand | 2150 | 304 | 157 | 433 |
| 21935 | Butcher Blades | S80 | lrhand | 2100 | 332 | 169 | 433 |
| 21936 | Butcher Blades {PvP} | S80 | lrhand | 2100 | 332 | 169 | 433 |
| 21937 | Butcher Blades - Confusion | S80 | lrhand | 2100 | 332 | 169 | 433 |
| 21938 | Butcher Blades - Confusion {PvP} | S80 | lrhand | 2100 | 332 | 169 | 433 |
| 13884 | Vesper Dual Daggers | S84 | lrhand | 2050 | 360 | 181 | 433 |
| 14477 | Vesper Dual Daggers {PvP} | S84 | lrhand | 2050 | 360 | 181 | 433 |
| 16148 | Vesper Dual Daggers - Gale | S84 | lrhand | 2050 | 360 | 181 | 433 |
| 16149 | Vesper Dual Daggers - Gale {PvP} | S84 | lrhand | 2050 | 360 | 181 | 433 |
| 16152 | Skull Edge Dual Daggers | S84 | lrhand | 2050 | 415 | 183 | 433 |
| 16153 | Skull Edge Dual Daggers {PvP} | S84 | lrhand | 2050 | 415 | 183 | 433 |
| 16156 | Mamba Edge Dual Daggers | S84 | lrhand | 2050 | 437 | 192 | 433 |
| 16157 | Mamba Edge Dual Daggers {PvP} | S84 | lrhand | 2050 | 437 | 192 | 433 |

### DUAL (347)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1299 | Great Sword | NONE | lrhand | 500 | 200 | 6 | 325 |
| 8203 | Monster Only (Venom Sword) | NONE | lrhand | 1560 |  |  | 325 |
| 8206 | Monster Only (Heretic Priest Sword) | NONE | lrhand | 2080 |  |  | 325 |
| 8207 | Monster Only (Heretic Private Axe) | NONE | lrhand | 1560 |  |  | 325 |
| 8350 | Chrono Maracas | NONE | lrhand | 0 | 1 | 1 | 325 |
| 13528 | Test Dual Daggers | NONE | lrhand | 500 | 200 | 6 | 325 |
| 14674 | Santa Claus' Tallum Blade*Damascus | NONE | lrhand | 1890 | 61 | 51 | 325 |
| 14795 | Baguette's Dualsword | NONE | lrhand | 1520 |  |  |  |
| 20270 | Baguette's Dualsword - 7-day limited period | NONE | lrhand | 500 | 1 | 2 | 325 |
| 2516 | Saber*Saber | D | lrhand | 2530 | 73 | 37 | 325 |
| 2517 | Saber*Bastard Sword | D | lrhand | 2520 | 83 | 41 | 325 |
| 2518 | Saber*Spinebone Sword | D | lrhand | 2530 | 83 | 41 | 325 |
| 2519 | Saber*Artisan's Sword | D | lrhand | 2520 | 83 | 41 | 325 |
| 2520 | Saber*Knight's Sword | D | lrhand | 2510 | 83 | 41 | 325 |
| 2521 | Saber*Crimson Sword | D | lrhand | 2530 | 96 | 47 | 325 |
| 2522 | Saber*Elven Sword | D | lrhand | 2510 | 96 | 47 | 325 |
| 2525 | Bastard Sword*Bastard Sword | D | lrhand | 2470 | 96 | 47 | 325 |
| 2526 | Bastard Sword*Spinebone Sword | D | lrhand | 2470 | 96 | 47 | 325 |
| 2527 | Bastard Sword*Artisan's Sword | D | lrhand | 2480 | 96 | 47 | 325 |
| 2528 | Bastard Sword*Knight's Sword | D | lrhand | 2500 | 96 | 47 | 325 |
| 2529 | Bastard Sword*Crimson Sword | D | lrhand | 2470 | 107 | 51 | 325 |
| 2530 | Bastard Sword*Elven Sword | D | lrhand | 2460 | 107 | 51 | 325 |
| 2533 | Spinebone Sword*Spinebone Sword | D | lrhand | 2520 | 96 | 47 | 325 |
| 2534 | Spinebone Sword*Artisan's Sword | D | lrhand | 2460 | 96 | 47 | 325 |
| 2535 | Spinebone Sword*Knight's Sword | D | lrhand | 2470 | 96 | 47 | 325 |
| 2536 | Spinebone Sword*Crimson Sword | D | lrhand | 2520 | 107 | 51 | 325 |
| 2537 | Spinebone Sword*Elven Sword | D | lrhand | 2460 | 107 | 51 | 325 |
| 2540 | Artisan's Sword*Artisan's Sword | D | lrhand | 2480 | 96 | 47 | 325 |
| 2541 | Artisan's Sword*Knight's Sword | D | lrhand | 2470 | 96 | 47 | 325 |
| 2542 | Artisan's Sword*Crimson Sword | D | lrhand | 2450 | 107 | 51 | 325 |
| 2543 | Artisan's Sword*Elven Sword | D | lrhand | 2470 | 107 | 51 | 325 |
| 2546 | Knight's Sword*Knight's Sword | D | lrhand | 2460 | 96 | 47 | 325 |
| 2547 | Knight's Sword*Crimson Sword | D | lrhand | 2460 | 107 | 51 | 325 |
| 2548 | Knight's Sword*Elven Sword | D | lrhand | 2450 | 107 | 51 | 325 |
| 5129 | Doll Knife | D | lrhand | 300 | 200 | 6 | 325 |
| 9638 | Tears r1 | D | lrhand | 300 | 5 | 5 | 433 |
| 9639 | Tears r2 | D | lrhand | 300 | 5 | 5 | 433 |
| 9640 | Tears r3 | D | lrhand | 300 | 5 | 5 | 433 |
| 10278 | Monster Only (Behamah Dual) | D | lrhand | 2530 | 73 | 37 | 325 |
| 11658 | Common Item - Saber*Saber | D | lrhand | 843 | 73 | 37 | 325 |
| 11679 | Common Item - Saber*Knight's Sword | D | lrhand | 837 | 83 | 41 | 325 |
| 11680 | Common Item - Saber*Bastard Sword | D | lrhand | 840 | 83 | 41 | 325 |
| 11681 | Common Item - Saber*Spinebone Sword | D | lrhand | 843 | 83 | 41 | 325 |
| 11682 | Common Item - Saber*Artisan's Sword | D | lrhand | 840 | 83 | 41 | 325 |
| 11684 | Common Item - Knight's Sword*Knight's Sword | D | lrhand | 820 | 96 | 47 | 325 |
| 11687 | Common Item - Bastard Sword*Knight's Sword | D | lrhand | 833 | 96 | 47 | 325 |
| 11688 | Common Item - Bastard Sword*Bastard Sword | D | lrhand | 823 | 96 | 47 | 325 |
| 11689 | Common Item - Bastard Sword*Spinebone Sword | D | lrhand | 823 | 96 | 47 | 325 |
| 11690 | Common Item - Bastard Sword*Artisan's Sword | D | lrhand | 827 | 96 | 47 | 325 |
| 11694 | Common Item - Saber*Elven Sword | D | lrhand | 837 | 96 | 47 | 325 |
| 11695 | Common Item - Saber*Crimson Sword | D | lrhand | 843 | 96 | 47 | 325 |
| 11698 | Common Item - Spinebone Sword*Knight's Sword | D | lrhand | 823 | 96 | 47 | 325 |
| 11699 | Common Item - Spinebone Sword*Spinebone Sword | D | lrhand | 840 | 96 | 47 | 325 |
| 11700 | Common Item - Spinebone Sword*Artisan's Sword | D | lrhand | 820 | 96 | 47 | 325 |
| 11704 | Common Item - Artisan's Sword*Knight's Sword | D | lrhand | 823 | 96 | 47 | 325 |
| 11705 | Common Item - Artisan's Sword*Artisan's Sword | D | lrhand | 827 | 96 | 47 | 325 |
| 11716 | Common Item - Knight's Sword*Elven Sword | D | lrhand | 817 | 107 | 51 | 325 |
| 11717 | Common Item - Knight's Sword*Crimson Sword | D | lrhand | 820 | 107 | 51 | 325 |
| 11718 | Common Item - Bastard Sword*Elven Sword | D | lrhand | 820 | 107 | 51 | 325 |
| 11719 | Common Item - Bastard Sword*Crimson Sword | D | lrhand | 823 | 107 | 51 | 325 |
| 11720 | Common Item - Spinebone Sword*Elven Sword | D | lrhand | 820 | 107 | 51 | 325 |
| 11721 | Common Item - Spinebone Sword*Crimson Sword | D | lrhand | 840 | 107 | 51 | 325 |
| 11722 | Common Item - Artisan's Sword*Elven Sword | D | lrhand | 823 | 107 | 51 | 325 |
| 11723 | Common Item - Artisan's Sword*Crimson Sword | D | lrhand | 817 | 107 | 51 | 325 |
| 13034 | Sprite's Sword | D | lrhand | 817 | 107 | 72 | 325 |
| 13035 | Enhanced Sprite's Sword | D | lrhand | 817 | 127 | 82 | 325 |
| 13036 | Sword of Ice and Fire | D | lrhand | 817 | 147 | 92 | 325 |
| 13163 | Player Commendation - Bastard*Crimson Sword - Player Commendation Weapon | D | lrhand | 2470 | 107 | 51 | 325 |
| 15063 | Bastard Sword*Elven Sword of Fortune - 30-day limited period | D | lrhand | 2460 | 107 | 51 | 325 |
| 15177 | Bastard Sword*Elven Sword of Fortune - 10-day limited period | D | lrhand | 2460 | 107 | 51 | 325 |
| 16951 | Bastard Sword*Elven Sword of Fortune - 90-day limited period | D | lrhand | 2460 | 107 | 51 | 325 |
| 20119 | Artisan's Sword*Artisan's Sword (Event) - 4-hour limited period | D | lrhand | 827 | 96 | 47 | 325 |
| 20641 | Common Item - Knight's Sword*Elven Sword | D | lrhand | 100 | 107 | 51 | 325 |
| 21742 | Bastard Sword*Bastard Sword - Event | D | lrhand | 2470 | 96 | 47 | 325 |
| 2523 | Saber*Sword of Revolution | C | lrhand | 2420 | 118 | 56 | 325 |
| 2524 | Saber*Elven Long Sword | C | lrhand | 2420 | 130 | 61 | 325 |
| 2531 | Bastard Sword*Sword of Revolution | C | lrhand | 2450 | 124 | 58 | 325 |
| 2532 | Bastard Sword*Elven Long Sword | C | lrhand | 2430 | 136 | 63 | 325 |
| 2538 | Spinebone Sword*Sword of Revolution | C | lrhand | 2460 | 124 | 58 | 325 |
| 2539 | Spinebone Sword*Elven Long Sword | C | lrhand | 2390 | 136 | 63 | 325 |
| 2544 | Artisan's Sword*Sword of Revolution | C | lrhand | 2420 | 124 | 58 | 325 |
| 2545 | Artisan's Sword*Elven Long Sword | C | lrhand | 2410 | 136 | 63 | 325 |
| 2549 | Knight's Sword*Sword of Revolution | C | lrhand | 2430 | 124 | 58 | 325 |
| 2550 | Knight's Sword*Elven Long Sword | C | lrhand | 2370 | 136 | 63 | 325 |
| 2551 | Crimson Sword*Crimson Sword | C | lrhand | 2440 | 118 | 56 | 325 |
| 2552 | Crimson Sword*Elven Sword | C | lrhand | 2450 | 118 | 56 | 325 |
| 2553 | Crimson Sword*Sword of Revolution | C | lrhand | 2390 | 136 | 63 | 325 |
| 2554 | Crimson Sword*Elven Long Sword | C | lrhand | 2360 | 148 | 68 | 325 |
| 2555 | Elven Sword*Elven Sword | C | lrhand | 2440 | 118 | 56 | 325 |
| 2556 | Elven Sword*Sword of Revolution | C | lrhand | 2410 | 136 | 63 | 325 |
| 2557 | Elven Sword*Elven Long Sword | C | lrhand | 2410 | 148 | 68 | 325 |
| 2558 | Sword of Revolution*Sword of Revolution | C | lrhand | 2360 | 148 | 68 | 325 |
| 2559 | Sword of Revolution*Elven Long Sword | C | lrhand | 2340 | 155 | 70 | 325 |
| 2560 | Elven Long Sword*Elven Long Sword | C | lrhand | 2340 | 162 | 73 | 325 |
| 2561 | Stormbringer*Stormbringer | C | lrhand | 2330 | 175 | 78 | 325 |
| 2562 | Stormbringer*Shamshir | C | lrhand | 2300 | 183 | 81 | 325 |
| 2563 | Stormbringer*Katana | C | lrhand | 2320 | 183 | 81 | 325 |
| 2564 | Stormbringer*Spirit Sword | C | lrhand | 2310 | 183 | 81 | 325 |
| 2565 | Stormbringer*Raid Sword | C | lrhand | 2340 | 183 | 81 | 325 |
| 2572 | Shamshir*Shamshir | C | lrhand | 2330 | 190 | 83 | 325 |
| 2573 | Shamshir*Katana | C | lrhand | 2310 | 190 | 83 | 325 |
| 2574 | Shamshir*Spirit Sword | C | lrhand | 2280 | 190 | 83 | 325 |
| 2575 | Shamshir*Raid Sword | C | lrhand | 2280 | 190 | 83 | 325 |
| 2582 | Katana*Katana | C | lrhand | 2270 | 190 | 83 | 325 |
| 2583 | Katana*Spirit Sword | C | lrhand | 2250 | 190 | 83 | 325 |
| 2584 | Katana*Raid Sword | C | lrhand | 2270 | 190 | 83 | 325 |
| 2591 | Spirit Sword*Spirit Sword | C | lrhand | 2240 | 190 | 83 | 325 |
| 2592 | Spirit Sword*Raid Sword | C | lrhand | 2260 | 190 | 83 | 325 |
| 2599 | Raid Sword*Raid Sword | C | lrhand | 2250 | 190 | 83 | 325 |
| 8837 | Shadow Item: Sword of Revolution | C | lrhand | 790 | 148 | 68 | 325 |
| 8848 | Shadow Item: Stormbringer | C | lrhand | 780 | 175 | 78 | 325 |
| 8937 | Shadow Item: Stormbringer | C | lrhand | 780 | 175 | 78 | 325 |
| 9000 | Shadow Item: Stormbringer*Stormbringer | C | lrhand | 780 | 175 | 78 | 325 |
| 11738 | Common Item - Saber*Sword of Revolution | C | lrhand | 807 | 118 | 56 | 325 |
| 11739 | Common Item - Elven Sword*Elven Sword | C | lrhand | 813 | 118 | 56 | 325 |
| 11740 | Common Item - Crimson Sword*Elven Sword | C | lrhand | 817 | 118 | 56 | 325 |
| 11741 | Common Item - Crimson Sword*Crimson Sword | C | lrhand | 813 | 118 | 56 | 325 |
| 11742 | Common Item - Knight's Sword*Sword of Revolution | C | lrhand | 810 | 124 | 58 | 325 |
| 11743 | Common Item - Bastard Sword*Sword of Revolution | C | lrhand | 817 | 124 | 58 | 325 |
| 11744 | Common Item - Spinebone Sword*Sword of Revolution | C | lrhand | 820 | 124 | 58 | 325 |
| 11745 | Common Item - Artisan's Sword*Sword of Revolution | C | lrhand | 807 | 124 | 58 | 325 |
| 11752 | Common Item - Saber*Elven Long Sword | C | lrhand | 807 | 130 | 61 | 325 |
| 11769 | Common Item - Knight's Sword*Elven Long Sword | C | lrhand | 790 | 136 | 63 | 325 |
| 11770 | Common Item - Bastard Sword*Elven Long Sword | C | lrhand | 810 | 136 | 63 | 325 |
| 11771 | Common Item - Spinebone Sword*Elven Long Sword | C | lrhand | 797 | 136 | 63 | 325 |
| 11772 | Common Item - Elven Sword*Sword of Revolution | C | lrhand | 803 | 136 | 63 | 325 |
| 11773 | Common Item - Artisan's Sword*Elven Long Sword | C | lrhand | 803 | 136 | 63 | 325 |
| 11774 | Common Item - Crimson Sword*Sword of Revolution | C | lrhand | 797 | 136 | 63 | 325 |
| 11791 | Common Item - Elven Sword*Elven Long Sword | C | lrhand | 803 | 148 | 68 | 325 |
| 11795 | Common Item - Crimson Sword*Elven Long Sword | C | lrhand | 787 | 148 | 68 | 325 |
| 11796 | Common Item - Sword of Revolution*Sword of Revolution | C | lrhand | 787 | 148 | 68 | 325 |
| 11797 | Common Item - Sword of Revolution*Elven Long Sword | C | lrhand | 780 | 155 | 70 | 325 |
| 11798 | Common Item - Elven Long Sword*Elven Long Sword | C | lrhand | 780 | 162 | 73 | 325 |
| 11831 | Common Item - Stormbringer*Stormbringer | C | lrhand | 777 | 175 | 78 | 325 |
| 11834 | Common Item - Stormbringer*Raid Sword | C | lrhand | 780 | 183 | 81 | 325 |
| 11835 | Common Item - Stormbringer*Shamshir | C | lrhand | 767 | 183 | 81 | 325 |
| 11836 | Common Item - Stormbringer*Spirit Sword | C | lrhand | 770 | 183 | 81 | 325 |
| 11837 | Common Item - Stormbringer*Katana | C | lrhand | 773 | 183 | 81 | 325 |
| 11841 | Common Item - Raid Sword*Raid Sword | C | lrhand | 750 | 190 | 83 | 325 |
| 11845 | Common Item - Shamshir*Raid Sword | C | lrhand | 760 | 190 | 83 | 325 |
| 11846 | Common Item - Shamshir*Shamshir | C | lrhand | 777 | 190 | 83 | 325 |
| 11847 | Common Item - Shamshir*Spirit Sword | C | lrhand | 760 | 190 | 83 | 325 |
| 11848 | Common Item - Shamshir*Katana | C | lrhand | 770 | 190 | 83 | 325 |
| 11851 | Common Item - Spirit Sword*Raid Sword | C | lrhand | 753 | 190 | 83 | 325 |
| 11852 | Common Item - Spirit Sword*Spirit Sword | C | lrhand | 747 | 190 | 83 | 325 |
| 11860 | Common Item - Katana*Raid Sword | C | lrhand | 757 | 190 | 83 | 325 |
| 11861 | Common Item - Katana*Spirit Sword | C | lrhand | 750 | 190 | 83 | 325 |
| 11862 | Common Item - Katana*Katana | C | lrhand | 757 | 190 | 83 | 325 |
| 13187 | Player Commendation - Shamshir*Shamshir - Player Commendation Weapon | C | lrhand | 2330 | 190 | 83 | 325 |
| 15062 | Spirit Sword*Raid Sword of Fortune - 30-day limited period | C | lrhand | 2260 | 190 | 83 | 325 |
| 15176 | Spirit Sword*Raid Sword of Fortune - 10-day limited period | C | lrhand | 2260 | 190 | 83 | 325 |
| 16950 | Spirit Sword*Raid Sword of Fortune - 90-day limited period | C | lrhand | 2260 | 190 | 83 | 325 |
| 20133 | Katana*Katana (Event) - 4-hour limited period | C | lrhand | 757 | 190 | 83 | 325 |
| 2566 | Stormbringer*Caliburs | B | lrhand | 2260 | 197 | 86 | 325 |
| 2567 | Stormbringer*Sword of Limit | B | lrhand | 2240 | 197 | 86 | 325 |
| 2568 | Stormbringer*Sword of Delusion | B | lrhand | 2230 | 197 | 86 | 325 |
| 2569 | Stormbringer*Sword of Nightmare | B | lrhand | 2250 | 197 | 86 | 325 |
| 2570 | Stormbringer*Tsurugi | B | lrhand | 2220 | 197 | 86 | 325 |
| 2571 | Stormbringer*Samurai Long sword | B | lrhand | 2150 | 213 | 91 | 325 |
| 2576 | Shamshir*Caliburs | B | lrhand | 2230 | 204 | 89 | 325 |
| 2577 | Shamshir*Sword of Limit | B | lrhand | 2240 | 204 | 89 | 325 |
| 2578 | Shamshir*Sword of Delusion | B | lrhand | 2200 | 204 | 89 | 325 |
| 2579 | Shamshir*Sword of Nightmare | B | lrhand | 2210 | 204 | 89 | 325 |
| 2580 | Shamshir*Tsurugi | B | lrhand | 2220 | 204 | 89 | 325 |
| 2581 | Shamshir*Samurai Long Sword | B | lrhand | 2110 | 220 | 94 | 325 |
| 2585 | Katana*Caliburs | B | lrhand | 2220 | 204 | 89 | 325 |
| 2586 | Katana*Sword of Limit | B | lrhand | 2180 | 204 | 89 | 325 |
| 2587 | Katana*Sword of Delusion | B | lrhand | 2190 | 204 | 89 | 325 |
| 2588 | Katana*Sword of Nightmare | B | lrhand | 2170 | 204 | 89 | 325 |
| 2589 | Katana*Tsurugi | B | lrhand | 2210 | 204 | 89 | 325 |
| 2590 | Katana*Samurai Long Sword | B | lrhand | 2130 | 220 | 94 | 325 |
| 2593 | Spirit Sword*Caliburs | B | lrhand | 2240 | 204 | 89 | 325 |
| 2594 | Spirit Sword*Sword of Limit | B | lrhand | 2240 | 204 | 89 | 325 |
| 2595 | Spirit Sword*Sword of Delusion | B | lrhand | 2250 | 204 | 89 | 325 |
| 2596 | Spirit Sword*Sword of Nightmare | B | lrhand | 2250 | 204 | 89 | 325 |
| 2597 | Spirit Sword*Tsurugi | B | lrhand | 2220 | 204 | 89 | 325 |
| 2598 | Spirit Sword*Samurai Long Sword | B | lrhand | 2110 | 220 | 94 | 325 |
| 2600 | Raid Sword*Caliburs | B | lrhand | 2190 | 204 | 89 | 325 |
| 2601 | Raid Sword*Sword of Limit | B | lrhand | 2170 | 204 | 89 | 325 |
| 2602 | Raid Sword*Sword of Delusion | B | lrhand | 2180 | 204 | 89 | 325 |
| 2603 | Raid Sword*Sword of Nightmare | B | lrhand | 2170 | 204 | 89 | 325 |
| 2604 | Raid Sword*Tsurugi | B | lrhand | 2170 | 204 | 89 | 325 |
| 2605 | Raid Sword*Samurai Long Sword | B | lrhand | 2130 | 220 | 94 | 325 |
| 2606 | Caliburs*Caliburs | B | lrhand | 2140 | 213 | 91 | 325 |
| 2607 | Caliburs*Sword of Limit | B | lrhand | 2150 | 213 | 91 | 325 |
| 2608 | Caliburs*Sword of Delusion | B | lrhand | 2140 | 213 | 91 | 325 |
| 2609 | Caliburs*Sword of Nightmare | B | lrhand | 2170 | 213 | 91 | 325 |
| 2610 | Caliburs*Tsurugi | B | lrhand | 2150 | 213 | 91 | 325 |
| 2611 | Caliburs*Samurai Long Sword | B | lrhand | 2120 | 228 | 97 | 325 |
| 2612 | Sword of Limit*Sword of Limit | B | lrhand | 2140 | 213 | 91 | 325 |
| 2613 | Sword of Limit*Sword of Delusion | B | lrhand | 2140 | 213 | 91 | 325 |
| 2614 | Sword of Limit*Sword of Nightmare | B | lrhand | 2130 | 213 | 91 | 325 |
| 2615 | Sword of Limit*Tsurugi | B | lrhand | 2120 | 213 | 91 | 325 |
| 2616 | Sword of Limit*Samurai Long Sword | B | lrhand | 2100 | 228 | 97 | 325 |
| 2617 | Sword of Delusion*Sword of Delusion | B | lrhand | 2150 | 213 | 91 | 325 |
| 2618 | Sword of Delusion*Sword of Nightmare | B | lrhand | 2130 | 213 | 91 | 325 |
| 2619 | Sword of Delusion*Tsurugi | B | lrhand | 2140 | 213 | 91 | 325 |
| 2620 | Sword of Delusion*Samurai Long Sword | B | lrhand | 2110 | 228 | 97 | 325 |
| 2621 | Sword of Nightmare*Sword of Nightmare | B | lrhand | 2130 | 213 | 91 | 325 |
| 2622 | Sword of Nightmare*Tsurugi | B | lrhand | 2140 | 213 | 91 | 325 |
| 2623 | Sword of Nightmare*Samurai Long Sword | B | lrhand | 2080 | 228 | 97 | 325 |
| 2624 | Tsurugi*Tsurugi | B | lrhand | 2120 | 213 | 91 | 325 |
| 2625 | Tsurugi*Samurai Long Sword | B | lrhand | 2090 | 228 | 97 | 325 |
| 2626 | Samurai Long Sword*Samurai Long Sword | B | lrhand | 2080 | 236 | 99 | 325 |
| 6722 | Monster Only(Ahrimanes) | B | lrhand | 2080 | 236 | 99 | 325 |
| 8857 | Shadow Item: Sword of Delusion*Sword of Delusion | B | lrhand | 720 | 213 | 91 | 325 |
| 9009 | Shadow Item: Sword of Delusion*Sword of Delusion | B | lrhand | 720 | 213 | 91 | 325 |
| 9813 | Orc Officer | B | lrhand | 2150 | 213 | 91 | 325 |
| 10878 | Sword of Limit*Sword of Limit - Destruction | B | lrhand | 2140 | 213 | 91 | 325 |
| 10879 | Sword of Limit*Sword of Delusion - Destruction | B | lrhand | 2140 | 213 | 91 | 325 |
| 10880 | Sword of Limit*Sword of Nightmare - Destruction | B | lrhand | 2130 | 213 | 91 | 325 |
| 10881 | Sword of Limit*Tsurugi - Destruction | B | lrhand | 2120 | 213 | 91 | 325 |
| 10890 | Sword of Delusion*Sword of Delusion - Destruction | B | lrhand | 2150 | 213 | 91 | 325 |
| 10891 | Sword of Delusion*Sword of Nightmare - Destruction | B | lrhand | 2130 | 213 | 91 | 325 |
| 10892 | Sword of Delusion*Tsurugi - Destruction | B | lrhand | 2140 | 213 | 91 | 325 |
| 10897 | Stormbringer*Samurai Long Sword - Destruction | B | lrhand | 2150 | 213 | 91 | 325 |
| 10910 | Sword of Nightmare*Sword of Nightmare - Destruction | B | lrhand | 2130 | 213 | 91 | 325 |
| 10911 | Sword of Nightmare*Tsurugi - Destruction | B | lrhand | 2140 | 213 | 91 | 325 |
| 10920 | Tsurugi*Tsurugi - Destruction | B | lrhand | 2120 | 213 | 91 | 325 |
| 10921 | Caliburs*Sword of Limit - Destruction | B | lrhand | 2150 | 213 | 91 | 325 |
| 10922 | Caliburs*Sword of Delusion - Destruction | B | lrhand | 2140 | 213 | 91 | 325 |
| 10923 | Caliburs*Sword of Nightmare - Destruction | B | lrhand | 2170 | 213 | 91 | 325 |
| 10924 | Caliburs*Tsurugi - Destruction | B | lrhand | 2150 | 213 | 91 | 325 |
| 10925 | Caliburs*Caliburs - Destruction | B | lrhand | 2140 | 213 | 91 | 325 |
| 10946 | Raid Sword*Samurai Long Sword - Destruction | B | lrhand | 2130 | 220 | 94 | 325 |
| 10947 | Shamshir*Samurai Long Sword - Destruction | B | lrhand | 2110 | 220 | 94 | 325 |
| 10948 | Spirit Sword*Samurai Long Sword - Destruction | B | lrhand | 2110 | 220 | 94 | 325 |
| 10949 | Katana*Samurai Long Sword - Destruction | B | lrhand | 2130 | 220 | 94 | 325 |
| 10950 | Sword of Limit*Samurai Long Sword - Destruction | B | lrhand | 2100 | 228 | 97 | 325 |
| 10951 | Sword of Delusion*Samurai Long Sword - Destruction | B | lrhand | 2110 | 228 | 97 | 325 |
| 10952 | Sword of Nightmare*Samurai Long Sword - Destruction | B | lrhand | 2080 | 228 | 97 | 325 |
| 10953 | Tsurugi*Samurai Long Sword - Destruction | B | lrhand | 2090 | 228 | 97 | 325 |
| 10954 | Caliburs*Samurai Long Sword - Destruction | B | lrhand | 2120 | 228 | 97 | 325 |
| 10987 | Samurai Long Sword*Samurai Long Sword - Landslide | B | lrhand | 2080 | 236 | 99 | 325 |
| 11864 | Common Item - Stormbringer*Sword of Limit | B | lrhand | 747 | 197 | 86 | 325 |
| 11865 | Common Item - Stormbringer*Sword of Delusion | B | lrhand | 743 | 197 | 86 | 325 |
| 11866 | Common Item - Stormbringer*Sword of Nightmare | B | lrhand | 750 | 197 | 86 | 325 |
| 11867 | Common Item - Stormbringer*Tsurugi | B | lrhand | 740 | 197 | 86 | 325 |
| 11868 | Common Item - Stormbringer*Caliburs | B | lrhand | 753 | 197 | 86 | 325 |
| 11869 | Common Item - Raid Sword*Sword of Limit | B | lrhand | 723 | 204 | 89 | 325 |
| 11870 | Common Item - Raid Sword*Sword of Delusion | B | lrhand | 727 | 204 | 89 | 325 |
| 11871 | Common Item - Raid Sword*Sword of Nightmare | B | lrhand | 723 | 204 | 89 | 325 |
| 11872 | Common Item - Raid Sword*Tsurugi | B | lrhand | 723 | 204 | 89 | 325 |
| 11873 | Common Item - Raid Sword*Caliburs | B | lrhand | 730 | 204 | 89 | 325 |
| 11874 | Common Item - Shamshir*Sword of Limit | B | lrhand | 747 | 204 | 89 | 325 |
| 11875 | Common Item - Shamshir*Sword of Delusion | B | lrhand | 733 | 204 | 89 | 325 |
| 11876 | Common Item - Shamshir*Sword of Nightmare | B | lrhand | 737 | 204 | 89 | 325 |
| 11877 | Common Item - Shamshir*Tsurugi | B | lrhand | 740 | 204 | 89 | 325 |
| 11878 | Common Item - Shamshir*Caliburs | B | lrhand | 743 | 204 | 89 | 325 |
| 11879 | Common Item - Spirit Sword*Sword of Limit | B | lrhand | 747 | 204 | 89 | 325 |
| 11880 | Common Item - Spirit Sword*Sword of Delusion | B | lrhand | 750 | 204 | 89 | 325 |
| 11881 | Common Item - Spirit Sword*Sword of Nightmare | B | lrhand | 750 | 204 | 89 | 325 |
| 11882 | Common Item - Spirit Sword*Tsurugi | B | lrhand | 740 | 204 | 89 | 325 |
| 11883 | Common Item - Spirit Sword*Caliburs | B | lrhand | 747 | 204 | 89 | 325 |
| 11884 | Common Item - Katana*Sword of Limit | B | lrhand | 727 | 204 | 89 | 325 |
| 11885 | Common Item - Katana*Sword of Delusion | B | lrhand | 730 | 204 | 89 | 325 |
| 11886 | Common Item - Katana*Sword of Nightmare | B | lrhand | 723 | 204 | 89 | 325 |
| 11887 | Common Item - Katana*Tsurugi | B | lrhand | 737 | 204 | 89 | 325 |
| 11888 | Common Item - Katana*Caliburs | B | lrhand | 740 | 204 | 89 | 325 |
| 11891 | Common Item - Sword of Limit*Sword of Limit | B | lrhand | 713 | 213 | 91 | 325 |
| 11892 | Common Item - Sword of Limit*Sword of Delusion | B | lrhand | 713 | 213 | 91 | 325 |
| 11893 | Common Item - Sword of Limit*Sword of Nightmare | B | lrhand | 710 | 213 | 91 | 325 |
| 11894 | Common Item - Sword of Limit*Tsurugi | B | lrhand | 707 | 213 | 91 | 325 |
| 11897 | Common Item - Sword of Delusion*Sword of Delusion | B | lrhand | 717 | 213 | 91 | 325 |
| 11898 | Common Item - Sword of Delusion*Sword of Nightmare | B | lrhand | 710 | 213 | 91 | 325 |
| 11899 | Common Item - Sword of Delusion*Tsurugi | B | lrhand | 713 | 213 | 91 | 325 |
| 11901 | Common Item - Stormbringer*Samurai Long Sword | B | lrhand | 717 | 213 | 91 | 325 |
| 11905 | Common Item - Sword of Nightmare*Sword of Nightmare | B | lrhand | 710 | 213 | 91 | 325 |
| 11906 | Common Item - Sword of Nightmare*Tsurugi | B | lrhand | 713 | 213 | 91 | 325 |
| 11909 | Common Item - Tsurugi*Tsurugi | B | lrhand | 707 | 213 | 91 | 325 |
| 11910 | Common Item - Caliburs*Sword of Limit | B | lrhand | 717 | 213 | 91 | 325 |
| 11911 | Common Item - Caliburs*Sword of Delusion | B | lrhand | 713 | 213 | 91 | 325 |
| 11912 | Common Item - Caliburs*Sword of Nightmare | B | lrhand | 723 | 213 | 91 | 325 |
| 11913 | Common Item - Caliburs*Tsurugi | B | lrhand | 717 | 213 | 91 | 325 |
| 11914 | Common Item - Caliburs*Caliburs | B | lrhand | 713 | 213 | 91 | 325 |
| 11920 | Common Item - Raid Sword*Samurai Long Sword | B | lrhand | 710 | 220 | 94 | 325 |
| 11921 | Common Item - Shamshir*Samurai Long Sword | B | lrhand | 703 | 220 | 94 | 325 |
| 11922 | Common Item - Spirit Sword*Samurai Long Sword | B | lrhand | 703 | 220 | 94 | 325 |
| 11923 | Common Item - Katana*Samurai Long Sword | B | lrhand | 710 | 220 | 94 | 325 |
| 11924 | Common Item - Sword of Limit*Samurai Long Sword | B | lrhand | 700 | 228 | 97 | 325 |
| 11925 | Common Item - Sword of Delusion*Samurai Long Sword | B | lrhand | 703 | 228 | 97 | 325 |
| 11926 | Common Item - Sword of Nightmare*Samurai Long Sword | B | lrhand | 693 | 228 | 97 | 325 |
| 11927 | Common Item - Tsurugi*Samurai Long Sword | B | lrhand | 697 | 228 | 97 | 325 |
| 11928 | Common Item - Caliburs*Samurai Long Sword | B | lrhand | 707 | 228 | 97 | 325 |
| 11937 | Common Item - Samurai Long Sword*Samurai Long Sword | B | lrhand | 693 | 236 | 99 | 325 |
| 13202 | Player Commendation - Samurai*Samurai - Player Commendation Weapon | B | lrhand | 2080 | 236 | 99 | 325 |
| 13985 | Exclusive to Monsters (Death Slayer_r) | B | lrhand | 2150 | 213 | 91 | 325 |
| 13986 | Exclusive to Monsters (Death Slayer_l) | B | lrhand | 2150 | 213 | 91 | 325 |
| 15061 | Samurai Long Sword*Samurai Long Sword of Fortune - 30-day limited period | B | lrhand | 2080 | 236 | 99 | 325 |
| 15175 | Samurai Long Sword*Samurai Long Sword of Fortune - 10-day limited period | B | lrhand | 2080 | 236 | 99 | 325 |
| 16949 | Samurai Long Sword*Samurai Long Sword of Fortune - 90-day limited period | B | lrhand | 2080 | 236 | 99 | 325 |
| 20147 | Samurai Long Sword*Samurai Long Sword (Event) - 4-hour limited period | B | lrhand | 693 | 236 | 99 | 325 |
| 5233 | Keshanberk*Keshanberk | A | lrhand | 2080 | 259 | 107 | 325 |
| 5704 | Keshanberk*Keshanberk | A | lrhand | 2080 | 259 | 107 | 325 |
| 5705 | Keshanberk*Damascus | A | lrhand | 2080 | 275 | 112 | 325 |
| 5706 | Damascus*Damascus | A | lrhand | 2080 | 282 | 114 | 325 |
| 8865 | Shadow Item: Keshanberk*Keshanberk | A | lrhand | 700 | 259 | 107 | 325 |
| 8938 | Damascus * Tallum Blade | A | lrhand | 1890 | 305 | 121 | 325 |
| 9017 | Shadow Item: Keshanberk*Keshanberk | A | lrhand | 700 | 259 | 107 | 325 |
| 9020 | Shadow Item: Keshanberk*Damascus | A | lrhand | 693 | 275 | 112 | 325 |
| 10709 | Tallum Blade*Damascus {PvP} | A | lrhand | 1890 | 305 | 121 | 325 |
| 11057 | Keshanberk*Keshanberk - Destruction | A | lrhand | 2080 | 259 | 107 | 325 |
| 11074 | Keshanberk*Damascus - Destruction | A | lrhand | 2080 | 275 | 112 | 325 |
| 11079 | Damascus*Damascus - Thunder | A | lrhand | 2080 | 282 | 114 | 325 |
| 11181 | Tallum Blade*Damascus - Landslide | A | lrhand | 1890 | 305 | 121 | 325 |
| 11956 | Common Item - Keshanberk*Keshanberk | A | lrhand | 693 | 259 | 107 | 325 |
| 11961 | Common Item - Keshanberk*Damascus | A | lrhand | 693 | 275 | 112 | 325 |
| 11963 | Common Item - Damascus*Damascus | A | lrhand | 693 | 282 | 114 | 325 |
| 11989 | Common Item - Tallum Blade*Damascus | A | lrhand | 630 | 305 | 121 | 325 |
| 12888 | Tallum Blade*Damascus - Landslide {PvP} | A | lrhand | 1890 | 305 | 121 | 325 |
| 13221 | Player Commendation - Tallum Blade*Damascus - Player Commendation Weapon | A | lrhand | 1890 | 305 | 121 | 325 |
| 15060 | Tallum Blade*Damascus of Fortune - 30-day limited period | A | lrhand | 1890 | 305 | 121 | 325 |
| 15174 | Tallum Blade*Damascus of Fortune - 10-day limited period | A | lrhand | 1890 | 305 | 121 | 325 |
| 16948 | Tallum Blade*Damascus of Fortune - 90-day limited period | A | lrhand | 1890 | 305 | 121 | 325 |
| 20161 | Damascus*Damascus (Event) - 4-hour limited period | A | lrhand | 693 | 282 | 114 | 325 |
| 6580 | Tallum Blade*Dark Legion's Edge | S | lrhand | 2080 | 342 | 132 | 325 |
| 6620 | Infinity Wing | S | lrhand | 1300 | 638 | 230 | 325 |
| 10004 | Dynasty Dual Sword | S | lrhand | 1520 | 405 | 151 | 325 |
| 10749 | Tallum Blade*Dark Legion's Edge {PvP} | S | lrhand | 2080 | 342 | 132 | 325 |
| 10792 | Dynasty Dual Sword {PvP} | S | lrhand | 1520 | 405 | 151 | 325 |
| 11234 | Tallum Blade*Dark Legion's Edge - Lightning | S | lrhand | 2080 | 342 | 132 | 325 |
| 11251 | Dynasty Dual Sword - Earth | S | lrhand | 1520 | 405 | 151 | 325 |
| 12003 | Common Item - Tallum Blade*Dark Legion's Edge | S | lrhand | 693 | 342 | 132 | 325 |
| 12928 | Tallum Blade*Dark Legion's Edge - Lightning {PvP} | S | lrhand | 2080 | 342 | 132 | 325 |
| 12941 | Dynasty Dual Sword - Earth {PvP} | S | lrhand | 1520 | 405 | 151 | 325 |
| 14570 | Dual Sword of Hunter Family | S | lrhand | 1560 | 376 | 119 | 325 |
| 15326 | Player Commendation - Tallum Blade *Dark Legion's Edge - Player Recommendation Weapon | S | lrhand | 2080 | 342 | 132 | 325 |
| 20175 | Tallum Blade*Dark Legion's Edge (Event) - 4-hour limited period | S | lrhand | 693 | 342 | 132 | 325 |
| 21828 | Tallum Blade*Dark Legion's Edge of Fortune - 90-day limited period | S | lrhand | 2080 | 342 | 132 | 325 |
| 21840 | Dynasty Dualsword of Fortune - 90-day limited period | S | lrhand | 1520 | 405 | 151 | 325 |
| 21955 | Blades of Delusion | S | lrhand | 1520 | 405 | 151 | 325 |
| 21956 | Blades of Delusion {PvP} | S | lrhand | 1520 | 405 | 151 | 325 |
| 21957 | Blades of Delusion - Earth | S | lrhand | 1520 | 405 | 151 | 325 |
| 21958 | Blades of Delusion - Earth {PvP} | S | lrhand | 1520 | 405 | 151 | 325 |
| 10415 | Icarus Dual Sword | S80 | lrhand | 1520 | 442 | 163 | 325 |
| 11300 | Icarus Dual Sword - Destruction | S80 | lrhand | 1520 | 442 | 163 | 325 |
| 14375 | Icarus Dual Sword {PvP} | S80 | lrhand | 1520 | 442 | 163 | 325 |
| 14412 | Icarus Dual Sword - Destruction {PvP} | S80 | lrhand | 1520 | 442 | 163 | 325 |
| 15300 | Transparent Dual (for NPC) | S80 | lrhand | 2080 | 282 | 114 | 325 |
| 52 | Vesper Dual Sword | S84 | lrhand | 1520 | 482 | 176 | 325 |
| 14462 | Vesper Dual Sword {PvP} | S84 | lrhand | 1520 | 482 | 176 | 325 |
| 16150 | Vesper Dual Sword - Destruction | S84 | lrhand | 1520 | 482 | 176 | 325 |
| 16151 | Vesper Dual Sword - Destruction {PvP} | S84 | lrhand | 1520 | 482 | 176 | 325 |
| 16154 | Periel Dual Sword | S84 | lrhand | 1520 | 505 | 183 | 325 |
| 16155 | Periel Dual Sword {PvP} | S84 | lrhand | 1520 | 505 | 183 | 325 |
| 16158 | Eternal Core Dual Sword | S84 | lrhand | 1520 | 532 | 192 | 325 |
| 16159 | Eternal Core Dual Sword {PvP} | S84 | lrhand | 1520 | 532 | 192 | 325 |

### FIST (11)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 244 | Elven Fighter Fist | NONE | rhand | 0 |  |  | 325 |
| 245 | Dark Fighter Fist | NONE | rhand | 0 |  |  | 325 |
| 246 | Human Fighter Fist | NONE | rhand | 0 |  |  | 325 |
| 247 | Dwarven Fighter Fist | NONE | rhand | 0 |  |  | 325 |
| 248 | Orc Fighter Fist | NONE | rhand | 0 |  |  | 325 |
| 249 | Elven Mystic Fist | NONE | rhand | 0 |  |  | 325 |
| 250 | Dark Mystic Fist | NONE | rhand | 0 |  |  | 325 |
| 251 | Human Mystic Fist | NONE | rhand | 0 |  |  | 325 |
| 252 | Orc Shaman Fist | NONE | rhand | 0 |  |  | 379 |
| 8190 | Demonic Sword Zariche | NONE | lrhand | 1840 | 361 | 137 | 325 |
| 8689 | Blood Sword Akamanah | NONE | lrhand | 1840 | 361 | 137 | 325 |

### DUALFIST (226)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 253 | Spiked Gloves | NONE | lrhand | 1590 | 10 | 6 | 325 |
| 254 | Iron Gloves | NONE | lrhand | 1580 | 13 | 9 | 325 |
| 255 | Fox Claw Gloves | NONE | lrhand | 1560 | 21 | 12 | 325 |
| 256 | Cestus | NONE | lrhand | 1570 | 29 | 17 | 325 |
| 257 | Viper Fang | NONE | lrhand | 1560 | 38 | 21 | 325 |
| 2368 | Training Gloves | NONE | lrhand | 1580 | 7 | 5 | 325 |
| 2371 | Fist of Butcher | NONE | lrhand | 1400 | 16 | 10 | 325 |
| 5133 | Chrono Unitus | NONE | lrhand | 0 | 1 | 1 | 325 |
| 7819 | Apprentice Adventurer's Cestus | NONE | lrhand | 1570 | 29 | 17 | 325 |
| 8216 | Monster Only (Zombie Enlisted Man Claw) | NONE | lrhand | 1350 |  |  | 325 |
| 8579 | Cestus (Event) | NONE | lrhand | 1570 | 29 | 17 | 325 |
| 8979 | Shadow Item: Viper Fang | NONE | lrhand | 520 | 38 | 21 | 325 |
| 9905 | Improved Viper Fang | NONE | lrhand | 1560 | 38 | 21 | 325 |
| 10477 | Shadow Item - Cestus | NONE | lrhand | 1570 | 29 | 17 | 325 |
| 13160 | Player Commendation - Viper Fang - Player Commendation Weapon | NONE | lrhand | 1560 | 38 | 21 | 325 |
| 14628 | Santa Claus' Sobekk Hurricane | NONE | lrhand | 1330 | 41 | 38 | 325 |
| 14787 | Baguette's Fist | NONE | lrhand | 1520 |  |  |  |
| 20262 | Baguette Fist - 7-day limited period | NONE | lrhand | 500 | 1 | 2 | 325 |
| 21110 | Warm Bear Paws | NONE | lrhand | 450 | 5 | 5 | 325 |
| 21111 | Warm Bear Paws - 7-day limited period | NONE | lrhand | 450 | 5 | 5 | 325 |
| 21990 | Warm Bear Paws | NONE | lrhand | 450 | 5 | 5 | 325 |
| 258 | Bagh-Nakh | D | lrhand | 1540 | 49 | 26 | 325 |
| 259 | Single-Edged Jamadhr | D | lrhand | 1550 | 62 | 32 | 325 |
| 260 | Triple-Edged Jamadhr | D | lrhand | 1540 | 78 | 39 | 325 |
| 261 | Bich'Hwa | D | lrhand | 1510 | 96 | 47 | 325 |
| 262 | Scallop Jamadhr | D | lrhand | 1520 | 112 | 54 | 325 |
| 7828 | Traveler's Jamadhr | D | lrhand | 1550 | 62 | 32 | 325 |
| 8588 | Single-Edged Jamadhr (Event) | D | lrhand | 1550 | 62 | 32 | 325 |
| 8827 | Shadow Item: Triple-Edged Jamadhr | D | lrhand | 520 | 78 | 39 | 325 |
| 8988 | Shadow Item: Triple-Edged Jamadhr | D | lrhand | 520 | 78 | 39 | 325 |
| 11608 | Common Item - Bagh-Nakh | D | lrhand | 513 | 49 | 26 | 325 |
| 11642 | Common Item - Single-Edged Jamadhr | D | lrhand | 517 | 62 | 32 | 325 |
| 11665 | Common Item - Triple-Edged Jamadhr | D | lrhand | 513 | 78 | 39 | 325 |
| 11691 | Common Item - Bich'Hwa | D | lrhand | 503 | 96 | 47 | 325 |
| 11730 | Common Item - Scallop Jamadhr | D | lrhand | 507 | 112 | 54 | 325 |
| 13171 | Player Commendation - Scallop Jamadhr - Player Commendation Weapon | D | lrhand | 1520 | 112 | 54 | 325 |
| 15059 | Scallop Jamadhr of Fortune - 30-day limited period | D | lrhand | 1520 | 112 | 54 | 325 |
| 15173 | Scallop Jamadhr of Fortune - 10-day limited period | D | lrhand | 1520 | 112 | 54 | 325 |
| 16947 | Scallop Jamadhr of Fortune - 90-day limited period | D | lrhand | 1520 | 112 | 54 | 325 |
| 20116 | Bich'Hwa (Event) - 4-hour limited period | D | lrhand | 503 | 96 | 47 | 325 |
| 21743 | Bich'Hwa - Event | D | lrhand | 1510 | 96 | 47 | 325 |
| 263 | Chakram | C | lrhand | 1490 | 130 | 61 | 325 |
| 265 | Fisted Blade | C | lrhand | 1480 | 169 | 76 | 325 |
| 266 | Great Pata | C | lrhand | 1460 | 190 | 83 | 325 |
| 4233 | Knuckle Duster | C | lrhand | 1490 | 148 | 68 | 325 |
| 4789 | Chakram - Critical Drain | C | lrhand | 1490 | 130 | 61 | 325 |
| 4790 | Chakram - Critical Poison | C | lrhand | 1490 | 130 | 61 | 325 |
| 4791 | Chakram - Rsk. Haste | C | lrhand | 1490 | 130 | 61 | 325 |
| 4792 | Fisted Blade - Rsk. Evasion | C | lrhand | 1480 | 169 | 76 | 325 |
| 4793 | Fisted Blade - Rsk. Haste | C | lrhand | 1480 | 169 | 76 | 325 |
| 4794 | Fisted Blade - Haste | C | lrhand | 1480 | 169 | 76 | 325 |
| 4795 | Great Pata - Critical Drain | C | lrhand | 1460 | 190 | 83 | 325 |
| 4796 | Great Pata - Critical Poison | C | lrhand | 1460 | 190 | 83 | 325 |
| 4797 | Great Pata - Rsk. Haste | C | lrhand | 1460 | 190 | 83 | 325 |
| 4798 | Knuckle Duster - Rsk. Evasion | C | lrhand | 1490 | 148 | 68 | 325 |
| 4799 | Knuckle Duster - Rsk. Haste | C | lrhand | 1490 | 148 | 68 | 325 |
| 4800 | Knuckle Duster - Haste | C | lrhand | 1490 | 148 | 68 | 325 |
| 8838 | Shadow Item: Knuckle Duster | C | lrhand | 500 | 148 | 68 | 325 |
| 8847 | Shadow Item: Fisted Blade | C | lrhand | 500 | 169 | 76 | 325 |
| 8934 | Shadow Item: Fisted Blade | C | lrhand | 500 | 169 | 76 | 325 |
| 8999 | Shadow Item: Fisted Blade | C | lrhand | 500 | 169 | 76 | 325 |
| 11763 | Common Item - Chakram | C | lrhand | 497 | 130 | 61 | 325 |
| 11776 | Common Item - Knuckle Duster | C | lrhand | 497 | 148 | 68 | 325 |
| 11827 | Common Item - Fisted Blade | C | lrhand | 493 | 169 | 76 | 325 |
| 11839 | Common Item - Great Pata | C | lrhand | 487 | 190 | 83 | 325 |
| 13183 | Player Commendation - Great Pata - Player Commendation Weapon | C | lrhand | 1460 | 190 | 83 | 325 |
| 15058 | Great Pata of Fortune - 30-day limited period | C | lrhand | 1460 | 190 | 83 | 325 |
| 15172 | Great Pata of Fortune - 10-day limited period | C | lrhand | 1460 | 190 | 83 | 325 |
| 16946 | Great Pata of Fortune - 90-day limited period | C | lrhand | 1460 | 190 | 83 | 325 |
| 20130 | Great Pata (Event) - 4-hour limited period | C | lrhand | 487 | 190 | 83 | 325 |
| 264 | Pata | B | lrhand | 1440 | 204 | 89 | 325 |
| 267 | Arthro Nail | B | lrhand | 1420 | 213 | 91 | 325 |
| 268 | Bellion Cestus | B | lrhand | 1390 | 236 | 99 | 325 |
| 4801 | Arthro Nail - Critical Poison | B | lrhand | 1420 | 213 | 91 | 325 |
| 4802 | Arthro Nail - Rsk. Evasion | B | lrhand | 1420 | 213 | 91 | 325 |
| 4803 | Arthro Nail - Rsk. Haste | B | lrhand | 1420 | 213 | 91 | 325 |
| 4804 | Bellion Cestus - Critical Drain | B | lrhand | 1390 | 236 | 99 | 325 |
| 4805 | Bellion Cestus - Critical Poison | B | lrhand | 1390 | 236 | 99 | 325 |
| 4806 | Bellion Cestus - Rsk. Haste | B | lrhand | 1390 | 236 | 99 | 325 |
| 8855 | Shadow Item: Arthro Nail | B | lrhand | 480 | 213 | 91 | 325 |
| 9007 | Shadow Item: Arthro Nail | B | lrhand | 480 | 213 | 91 | 325 |
| 10902 | Arthro Nail - Destruction | B | lrhand | 1420 | 213 | 91 | 325 |
| 10903 | Arthro Nail - Destruction - Critical Poison | B | lrhand | 1420 | 213 | 91 | 325 |
| 10904 | Arthro Nail - Destruction - Rsk. Evasion | B | lrhand | 1420 | 213 | 91 | 325 |
| 10905 | Arthro Nail - Destruction - Rsk. Haste | B | lrhand | 1420 | 213 | 91 | 325 |
| 10971 | Bellion Cestus - Great Gale | B | lrhand | 1390 | 236 | 99 | 325 |
| 10972 | Bellion Cestus - Great Gale - Critical Drain | B | lrhand | 1390 | 236 | 99 | 325 |
| 10973 | Bellion Cestus - Great Gale - Critical Poison | B | lrhand | 1390 | 236 | 99 | 325 |
| 10974 | Bellion Cestus - Great Gale - Rsk. Haste | B | lrhand | 1390 | 236 | 99 | 325 |
| 11903 | Common Item - Arthro Nail | B | lrhand | 473 | 213 | 91 | 325 |
| 11933 | Common Item - Bellion Cestus | B | lrhand | 463 | 236 | 99 | 325 |
| 13200 | Player Commendation - Bellion Cestus - Player Commendation Weapon | B | lrhand | 1390 | 236 | 99 | 325 |
| 15057 | Bellion Cestus of Fortune - 30-day limited period | B | lrhand | 1390 | 236 | 99 | 325 |
| 15171 | Bellion Cestus of Fortune - 10-day limited period | B | lrhand | 1390 | 236 | 99 | 325 |
| 16945 | Bellion Cestus of Fortune - 90-day limited period | B | lrhand | 1390 | 236 | 99 | 325 |
| 20144 | Bellion Cestus (Event) - 4-hour limited period | B | lrhand | 463 | 236 | 99 | 325 |
| 269 | Blood Tornado | A | lrhand | 1370 | 259 | 107 | 325 |
| 270 | Dragon Grinder | A | lrhand | 1350 | 282 | 114 | 325 |
| 4807 | Blood Tornado - Critical Drain | A | lrhand | 1370 | 259 | 107 | 325 |
| 4808 | Blood Tornado - Rsk. Evasion | A | lrhand | 1370 | 259 | 107 | 325 |
| 4809 | Blood Tornado - Haste | A | lrhand | 1370 | 259 | 107 | 325 |
| 5620 | Blood Tornado - Haste | A | lrhand | 1370 | 259 | 107 | 325 |
| 5621 | Blood Tornado - Focus | A | lrhand | 1370 | 259 | 107 | 325 |
| 5622 | Blood Tornado - Anger | A | lrhand | 1370 | 259 | 107 | 325 |
| 5623 | Dragon Grinder - Rsk. Evasion | A | lrhand | 1350 | 282 | 114 | 325 |
| 5624 | Dragon Grinder - Guidance | A | lrhand | 1350 | 282 | 114 | 325 |
| 5625 | Dragon Grinder - Health | A | lrhand | 1350 | 282 | 114 | 325 |
| 8685 | Sobekk's Hurricane | A | lrhand | 1330 | 305 | 121 | 325 |
| 8809 | Sobekk's Hurricane - Rsk. Haste | A | lrhand | 1330 | 305 | 121 | 325 |
| 8810 | Sobekk's Hurricane - Haste | A | lrhand | 1330 | 305 | 121 | 325 |
| 8811 | Sobekk's Hurricane - Critical Drain | A | lrhand | 1330 | 305 | 121 | 325 |
| 8863 | Shadow Item: Blood Tornado | A | lrhand | 460 | 259 | 107 | 325 |
| 9015 | Shadow Item: Blood Tornado | A | lrhand | 460 | 259 | 107 | 325 |
| 9026 | Shadow Item: Dragon Grinder | A | lrhand | 450 | 282 | 114 | 325 |
| 10688 | Sobekk's Hurricane {PvP} - Rsk. Haste | A | lrhand | 1330 | 305 | 121 | 325 |
| 10689 | Sobekk's Hurricane {PvP} - Haste | A | lrhand | 1330 | 305 | 121 | 325 |
| 10690 | Sobekk's Hurricane {PvP} - Critical Drain | A | lrhand | 1330 | 305 | 121 | 325 |
| 11033 | Blood Tornado - Destruction | A | lrhand | 1370 | 259 | 107 | 325 |
| 11034 | Blood Tornado - Destruction - Haste | A | lrhand | 1370 | 259 | 107 | 325 |
| 11035 | Blood Tornado - Destruction - Focus | A | lrhand | 1370 | 259 | 107 | 325 |
| 11036 | Blood Tornado - Destruction - Anger | A | lrhand | 1370 | 259 | 107 | 325 |
| 11092 | Dragon Grinder - Earth | A | lrhand | 1350 | 282 | 114 | 325 |
| 11093 | Dragon Grinder - Earth - Rsk. Evasion | A | lrhand | 1350 | 282 | 114 | 325 |
| 11094 | Dragon Grinder - Earth - Guidance | A | lrhand | 1350 | 282 | 114 | 325 |
| 11095 | Dragon Grinder - Earth - Health | A | lrhand | 1350 | 282 | 114 | 325 |
| 11165 | Sobekk's Hurricane - Landslide | A | lrhand | 1330 | 305 | 121 | 325 |
| 11166 | Sobekk's Hurricane - Landslide - Rsk. Haste | A | lrhand | 1330 | 305 | 121 | 325 |
| 11167 | Sobekk's Hurricane - Landslide - Haste | A | lrhand | 1330 | 305 | 121 | 325 |
| 11168 | Sobekk's Hurricane - Landslide - Critical Drain | A | lrhand | 1330 | 305 | 121 | 325 |
| 11950 | Common Item - Blood Tornado | A | lrhand | 457 | 259 | 107 | 325 |
| 11967 | Common Item - Dragon Grinder | A | lrhand | 450 | 282 | 114 | 325 |
| 11985 | Common Item - Sobekk's Hurricane | A | lrhand | 443 | 305 | 121 | 325 |
| 12876 | Sobekk's Hurricane - Landslide {PvP} - Rsk. Haste | A | lrhand | 1330 | 305 | 121 | 325 |
| 12877 | Sobekk's Hurricane - Landslide {PvP} - Haste | A | lrhand | 1330 | 305 | 121 | 325 |
| 12878 | Sobekk's Hurricane - Landslide {PvP} - Critical Drain | A | lrhand | 1330 | 305 | 121 | 325 |
| 13217 | Player Commendation - Sobekk's Hurricane - Player Commendation Weapon | A | lrhand | 1330 | 305 | 121 | 325 |
| 15056 | Sobekk's Hurricane of Fortune - 30-day limited period | A | lrhand | 1330 | 305 | 121 | 325 |
| 15170 | Sobekk's Hurricane of Fortune - 10-day limited period | A | lrhand | 1330 | 305 | 121 | 325 |
| 16944 | Sobekk's Hurricane of Fortune - 90-day limited period | A | lrhand | 1330 | 305 | 121 | 325 |
| 20158 | Dragon Grinder (Event) - 4-hour limited period | A | lrhand | 450 | 282 | 114 | 325 |
| 6371 | Demon Splinter | S | lrhand | 1350 | 342 | 132 | 325 |
| 6602 | Demon Splinter - Focus | S | lrhand | 1350 | 342 | 132 | 325 |
| 6603 | Demon Splinter - Health | S | lrhand | 1350 | 342 | 132 | 325 |
| 6604 | Demon Splinter - Critical Stun | S | lrhand | 1350 | 342 | 132 | 325 |
| 6618 | Infinity Fang | S | lrhand | 1300 | 638 | 230 | 325 |
| 9450 | Dynasty Bagh-Nakh | S | lrhand | 1550 | 405 | 151 | 325 |
| 9878 | Dynasty Bagh-Nakh - Rsk. Evasion | S | lrhand | 1550 | 405 | 151 | 325 |
| 9879 | Dynasty Bagh-Nakh - Focus | S | lrhand | 1550 | 405 | 151 | 325 |
| 9880 | Dynasty Bagh-Nakh - Haste | S | lrhand | 1550 | 405 | 151 | 325 |
| 10728 | Demon Splinter {PvP} - Focus | S | lrhand | 1350 | 342 | 132 | 325 |
| 10729 | Demon Splinter {PvP} - Health | S | lrhand | 1350 | 342 | 132 | 325 |
| 10730 | Demon Splinter {PvP} - Critical Stun | S | lrhand | 1350 | 342 | 132 | 325 |
| 10768 | Dynasty Bagh-Nakh {PvP} - Rsk. Evasion | S | lrhand | 1550 | 405 | 151 | 325 |
| 10769 | Dynasty Bagh-Nakh {PvP} - Focus | S | lrhand | 1550 | 405 | 151 | 325 |
| 10770 | Dynasty Bagh-Nakh {PvP} - Haste | S | lrhand | 1550 | 405 | 151 | 325 |
| 11194 | Demon Splinter - Thunder | S | lrhand | 1350 | 342 | 132 | 325 |
| 11195 | Demon Splinter - Thunder - Focus | S | lrhand | 1350 | 342 | 132 | 325 |
| 11196 | Demon Splinter - Thunder - Health | S | lrhand | 1350 | 342 | 132 | 325 |
| 11197 | Demon Splinter - Thunder - Critical Stun | S | lrhand | 1350 | 342 | 132 | 325 |
| 11260 | Dynasty Bagh-Nakh - Great Gale | S | lrhand | 1550 | 405 | 151 | 325 |
| 11261 | Dynasty Bagh-Nakh - Great Gale - Rsk. Evasion | S | lrhand | 1550 | 405 | 151 | 325 |
| 11262 | Dynasty Bagh-Nakh - Great Gale - Focus | S | lrhand | 1550 | 405 | 151 | 325 |
| 11263 | Dynasty Bagh-Nakh - Great Gale - Haste | S | lrhand | 1550 | 405 | 151 | 325 |
| 11993 | Common Item - Demon Splinter | S | lrhand | 450 | 342 | 132 | 325 |
| 12898 | Demon Splinter - Thunder {PvP} - Focus | S | lrhand | 1350 | 342 | 132 | 325 |
| 12899 | Demon Splinter - Thunder {PvP} - Health | S | lrhand | 1350 | 342 | 132 | 325 |
| 12900 | Demon Splinter - Thunder {PvP} - Critical Stun | S | lrhand | 1350 | 342 | 132 | 325 |
| 12948 | Dynasty Bagh-Nakh - Great Gale {PvP} - Rsk. Evasion | S | lrhand | 1550 | 405 | 151 | 325 |
| 12949 | Dynasty Bagh-Nakh - Great Gale {PvP} - Focus | S | lrhand | 1550 | 405 | 151 | 325 |
| 12950 | Dynasty Bagh-Nakh - Great Gale {PvP} - Haste | S | lrhand | 1550 | 405 | 151 | 325 |
| 14563 | Claw of Ashton Family | S | lrhand | 1013 | 376 | 119 | 325 |
| 14577 | Claw of Orwen Family | S | lrhand | 1013 | 376 | 119 | 325 |
| 15319 | Player Commendation - Demon Splinter - Player Recommendation Weapon | S | lrhand | 1350 | 342 | 132 | 325 |
| 20172 | Demon Splinter (Event) - 4-hour limited period | S | lrhand | 450 | 342 | 132 | 325 |
| 21827 | Demon Splinter of Fortune - 90-day limited period | S | lrhand | 1350 | 342 | 132 | 325 |
| 21839 | Dynasty Bagh-Nakh of Fortune - 90-day limited period | S | lrhand | 1550 | 405 | 151 | 325 |
| 10221 | Icarus Hand | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 10458 | Icarus Hand - Rsk. Evasion | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 10459 | Icarus Hand - Focus | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 10460 | Icarus Hand - Haste | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 11337 | Icarus Hand - Destruction | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 11338 | Icarus Hand - Destruction - Rsk. Evasion | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 11339 | Icarus Hand - Destruction - Focus | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 11340 | Icarus Hand - Destruction - Haste | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 14369 | Icarus Hand {PvP} | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 14400 | Icarus Hand {PvP} - Rsk. Evasion | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 14401 | Icarus Hand {PvP} - Focus | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 14402 | Icarus Hand {PvP} - Haste | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 14449 | Icarus Hand - Destruction {PvP} | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 14450 | Icarus Hand - Destruction {PvP} - Rsk. Evasion | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 14451 | Icarus Hand - Destruction {PvP} - Focus | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 14452 | Icarus Hand - Destruction {PvP} - Haste | S80 | lrhand | 1550 | 442 | 163 | 325 |
| 15303 | Transparent Claw (for NPC) | S80 | lrhand | 1013 | 376 | 119 | 325 |
| 13461 | Vesper Fighter | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 14130 | Vesper Fighter - Focus | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 14131 | Vesper Fighter - Health | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 14132 | Vesper Fighter - Critical Stun | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 14467 | Vesper Fighter {PvP} | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 14490 | Vesper Fighter {PvP} - Focus | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 14491 | Vesper Fighter {PvP} - Health | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 14492 | Vesper Fighter {PvP} - Critical Stun | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 15549 | Jade Claw | S84 | lrhand | 1550 | 532 | 192 | 325 |
| 15563 | Octo Claw | S84 | lrhand | 1550 | 505 | 183 | 325 |
| 15681 | Triumph Jamadhr | S84 | lrhand | 1550 | 482 | 183 | 325 |
| 15844 | Octo Claw - Health | S84 | lrhand | 1550 | 505 | 183 | 325 |
| 15845 | Octo Claw - Critical Stun | S84 | lrhand | 1550 | 505 | 183 | 325 |
| 15846 | Octo Claw - Focus | S84 | lrhand | 1550 | 505 | 183 | 325 |
| 15886 | Jade Claw - Critical Stun | S84 | lrhand | 1550 | 532 | 192 | 325 |
| 15887 | Jade Claw - Focus | S84 | lrhand | 1550 | 532 | 192 | 325 |
| 15888 | Jade Claw - Health | S84 | lrhand | 1550 | 532 | 192 | 325 |
| 15918 | Jade Claw {PvP} | S84 | lrhand | 1550 | 532 | 192 | 325 |
| 15932 | Octo Claw {PvP} | S84 | lrhand | 1550 | 505 | 183 | 325 |
| 15956 | Octo Claw {PvP} - Health | S84 | lrhand | 1550 | 505 | 183 | 325 |
| 15957 | Octo Claw {PvP} - Critical Stun | S84 | lrhand | 1550 | 505 | 183 | 325 |
| 15958 | Octo Claw {PvP} - Focus | S84 | lrhand | 1550 | 505 | 183 | 325 |
| 15998 | Jade Claw {PvP} - Critical Stun | S84 | lrhand | 1550 | 532 | 192 | 325 |
| 15999 | Jade Claw {PvP} - Focus | S84 | lrhand | 1550 | 532 | 192 | 325 |
| 16000 | Jade Claw {PvP} - Health | S84 | lrhand | 1550 | 532 | 192 | 325 |
| 16046 | Vesper Fighter - Gale | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 16068 | Vesper Fighter - Gale - Focus | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 16069 | Vesper Fighter - Gale - Health | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 16070 | Vesper Fighter - Gale - Critical Stun | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 16138 | Vesper Fighter - Gale {PvP} | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 16191 | Vesper Fighter - Gale {PvP} - Focus | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 16192 | Vesper Fighter - Gale {PvP} - Health | S84 | lrhand | 1550 | 482 | 176 | 325 |
| 16193 | Vesper Fighter - Gale {PvP} - Critical Stun | S84 | lrhand | 1550 | 482 | 176 | 325 |

### POLE (266)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 15 | Short Spear | NONE | lrhand | 2140 | 24 | 17 | 325 |
| 16 | Great Spear | NONE | lrhand | 2120 | 31 | 21 | 325 |
| 1302 | Bec de Corbin | NONE | lrhand | 750 | 22 | 6 | 325 |
| 1303 | Lance | NONE | lrhand | 750 | 30000 | 6 | 325 |
| 3026 | Talins Spear | NONE | lrhand | 800 | 24 | 17 | 325 |
| 5817 | Chrono Campana | NONE | lrhand | 0 | 1 | 1 | 325 |
| 8205 | Monster Only (Heretic Priest Sigil) | NONE | lrhand | 1920 |  |  | 325 |
| 8208 | Monster Only (Heretic Private Staff) | NONE | lrhand | 1560 |  |  | 325 |
| 8214 | Monster Only (Solina Priest Pole) | NONE | lrhand | 1920 |  |  | 325 |
| 8221 | Monster Only (Grail Apostle Spear) | NONE | lrhand | 1920 |  |  | 325 |
| 8972 | Shadow Item: Great Spear | NONE | lrhand | 707 | 31 | 21 | 325 |
| 9902 | Improved Great Spear | NONE | lrhand | 2120 | 31 | 21 | 325 |
| 10277 | Monster Only (Behamah Pole) | NONE | lrhand | 2140 | 24 | 17 | 325 |
| 13153 | Player Commendation - Great Spear - Player Commendation Weapon | NONE | lrhand | 2120 | 31 | 21 | 325 |
| 13978 | Exclusive to Monsters (Mounted Troops High Level Leader) | NONE | lrhand | 2120 | 31 | 21 | 325 |
| 13982 | Exclusive to Monsters (Death Knight_pole) | NONE | lrhand | 2140 | 24 | 17 | 325 |
| 14626 | Santa Claus' Tiphon Spear | NONE | lrhand | 1820 | 51 | 38 | 325 |
| 14784 | Baguette's Two-handed Hammer | NONE | lrhand | 2080 |  |  |  |
| 14785 | Baguette's Spear | NONE | lrhand | 2120 |  |  |  |
| 20260 | Baguette Spear - 7-day limited period | NONE | lrhand | 500 | 1 | 2 | 325 |
| 20867 | Kadomas Transformation Stick - 7-day limited period | NONE | lrhand | 150 | 1 | 1 | 379 |
| 21754 | Server Ziggi's Magic Pencil | NONE | lrhand | 100 | 1 | 1 | 325 |
| 93 | Winged Spear | D | lrhand | 2060 | 79 | 47 | 325 |
| 291 | Trident | D | lrhand | 2100 | 40 | 26 | 325 |
| 292 | Pike | D | lrhand | 2090 | 51 | 32 | 325 |
| 293 | War Hammer | D | lrhand | 2080 | 64 | 39 | 325 |
| 294 | War Pick | D | lrhand | 2050 | 79 | 47 | 325 |
| 295 | Dwarven Trident | D | lrhand | 2090 | 51 | 32 | 325 |
| 296 | Dwarven Pike | D | lrhand | 2070 | 64 | 39 | 325 |
| 297 | Glaive | D | lrhand | 2050 | 92 | 54 | 325 |
| 1376 | Guard Spear | D | lrhand | 300 | 50 | 26 | 325 |
| 1472 | Dreadbane | D | lrhand | 300 | 50 | 26 | 325 |
| 3937 | Giant Bar | D | lrhand | 300 | 50 | 26 | 325 |
| 3938 | Giant Rod | D | lrhand | 300 | 50 | 26 | 325 |
| 3939 | Lady's Fan | D | lrhand | 300 | 50 | 26 | 325 |
| 7831 | Traveler's Pike | D | lrhand | 2090 | 51 | 32 | 325 |
| 8591 | Pike (Event) | D | lrhand | 2090 | 51 | 32 | 325 |
| 8829 | Shadow Item: War Hammer | D | lrhand | 700 | 64 | 39 | 325 |
| 8990 | Shadow Item: War Hammer | D | lrhand | 700 | 64 | 39 | 325 |
| 11622 | Common Item - Trident | D | lrhand | 700 | 40 | 26 | 325 |
| 11631 | Common Item - Dwarven Trident | D | lrhand | 697 | 51 | 32 | 325 |
| 11647 | Common Item - Pike | D | lrhand | 697 | 51 | 32 | 325 |
| 11661 | Common Item - Dwarven Pike | D | lrhand | 690 | 64 | 39 | 325 |
| 11671 | Common Item - War Hammer | D | lrhand | 693 | 64 | 39 | 325 |
| 11703 | Common Item - Winged Spear | D | lrhand | 687 | 79 | 47 | 325 |
| 11712 | Common Item - War Pick | D | lrhand | 683 | 79 | 47 | 325 |
| 11725 | Common Item - Glaive | D | lrhand | 683 | 92 | 54 | 325 |
| 13173 | Player Commendation - Glaive - Player Commendation Weapon | D | lrhand | 2050 | 92 | 54 | 325 |
| 15067 | Glaive of Fortune - 30-day limited period | D | lrhand | 2050 | 92 | 54 | 325 |
| 15181 | Glaive of Fortune - 10-day limited period | D | lrhand | 2050 | 92 | 54 | 325 |
| 16955 | Glaive of Fortune - 90-day limited period | D | lrhand | 2050 | 92 | 54 | 325 |
| 20118 | Winged Spear (Event) - 4-hour limited period | D | lrhand | 687 | 79 | 47 | 325 |
| 21738 | Winged Spear - Event | D | lrhand | 2060 | 79 | 47 | 325 |
| 94 | Bec de Corbin | C | lrhand | 2020 | 122 | 68 | 325 |
| 95 | Poleaxe | C | lrhand | 2010 | 139 | 76 | 325 |
| 96 | Scythe | C | lrhand | 2040 | 107 | 61 | 325 |
| 298 | Orcish Glaive | C | lrhand | 2030 | 107 | 61 | 325 |
| 299 | Orcish Poleaxe | C | lrhand | 1950 | 156 | 83 | 325 |
| 301 | Scorpion | C | lrhand | 1990 | 144 | 78 | 325 |
| 302 | Body Slasher | C | lrhand | 2030 | 107 | 61 | 325 |
| 303 | Widow Maker | C | lrhand | 1980 | 144 | 78 | 325 |
| 4834 | Scythe - Anger | C | lrhand | 2040 | 107 | 61 | 325 |
| 4835 | Scythe - Critical Stun | C | lrhand | 2040 | 107 | 61 | 325 |
| 4836 | Scythe - Light | C | lrhand | 2040 | 107 | 61 | 325 |
| 4837 | Orcish Glaive - Anger | C | lrhand | 2030 | 107 | 61 | 325 |
| 4838 | Orcish Glaive - Critical Stun | C | lrhand | 2030 | 107 | 61 | 325 |
| 4839 | Orcish Glaive - Towering Blow | C | lrhand | 2030 | 107 | 61 | 325 |
| 4840 | Body Slasher - Critical Stun | C | lrhand | 2030 | 107 | 61 | 325 |
| 4841 | Body Slasher - Towering Blow | C | lrhand | 2030 | 107 | 61 | 325 |
| 4842 | Body Slasher - Wide Blow | C | lrhand | 2030 | 107 | 61 | 325 |
| 4843 | Bec de Corbin - Critical Stun | C | lrhand | 2020 | 122 | 68 | 325 |
| 4844 | Bec de Corbin - Towering Blow | C | lrhand | 2020 | 122 | 68 | 325 |
| 4845 | Bec de Corbin - Light | C | lrhand | 2020 | 122 | 68 | 325 |
| 4846 | Scorpion - Anger | C | lrhand | 1990 | 144 | 78 | 325 |
| 4847 | Scorpion - Critical Stun | C | lrhand | 1990 | 144 | 78 | 325 |
| 4848 | Scorpion - Towering Blow | C | lrhand | 1990 | 144 | 78 | 325 |
| 4849 | Widow Maker - Critical Stun | C | lrhand | 1980 | 144 | 78 | 325 |
| 4850 | Widow Maker - Towering Blow | C | lrhand | 1980 | 144 | 78 | 325 |
| 4851 | Widow Maker - Wide Blow | C | lrhand | 1980 | 144 | 78 | 325 |
| 4852 | Orcish Poleaxe - Critical Stun | C | lrhand | 1950 | 156 | 83 | 325 |
| 4853 | Orcish Poleaxe - Towering Blow | C | lrhand | 1950 | 156 | 83 | 325 |
| 4854 | Orcish Poleaxe - Wide Blow | C | lrhand | 1950 | 156 | 83 | 325 |
| 7719 | Poleaxe - Critical Stun | C | lrhand | 2010 | 139 | 76 | 325 |
| 7720 | Poleaxe - Towering Blow | C | lrhand | 2010 | 139 | 76 | 325 |
| 7721 | Poleaxe - Wide Blow | C | lrhand | 2010 | 139 | 76 | 325 |
| 8831 | Shadow Item: Bec de Corbin | C | lrhand | 680 | 122 | 68 | 325 |
| 8840 | Shadow Item: Poleaxe | C | lrhand | 670 | 139 | 76 | 325 |
| 8927 | Shadow Item: Poleaxe | C | lrhand | 670 | 139 | 76 | 325 |
| 8992 | Shadow Item: Poleaxe | C | lrhand | 670 | 139 | 76 | 325 |
| 11749 | Common Item - Body Slasher | C | lrhand | 677 | 107 | 61 | 325 |
| 11751 | Common Item - Scythe | C | lrhand | 680 | 107 | 61 | 325 |
| 11760 | Common Item - Orcish Glaive | C | lrhand | 677 | 107 | 61 | 325 |
| 11782 | Common Item - Bec de Corbin | C | lrhand | 673 | 122 | 68 | 325 |
| 11826 | Common Item - Poleaxe | C | lrhand | 670 | 139 | 76 | 325 |
| 11830 | Common Item - Scorpion | C | lrhand | 663 | 144 | 78 | 325 |
| 11832 | Common Item - Widow Maker | C | lrhand | 660 | 144 | 78 | 325 |
| 11858 | Common Item - Orcish Poleaxe | C | lrhand | 650 | 156 | 83 | 325 |
| 13185 | Player Commendation - Orcish Poleaxe - Player Commendation Weapon | C | lrhand | 1950 | 156 | 83 | 325 |
| 15066 | Orcish Poleaxe of Fortune - 30-day limited period | C | lrhand | 1950 | 156 | 83 | 325 |
| 15180 | Orcish Poleaxe of Fortune - 10-day limited period | C | lrhand | 1950 | 156 | 83 | 325 |
| 16954 | Orcish Poleaxe of Fortune - 90-day limited period | C | lrhand | 1950 | 156 | 83 | 325 |
| 20132 | Orcish Poleaxe (Event) - 4-hour limited period | C | lrhand | 650 | 156 | 83 | 325 |
| 97 | Lance | B | lrhand | 1920 | 194 | 99 | 325 |
| 300 | Great Axe | B | lrhand | 1940 | 175 | 91 | 325 |
| 4855 | Great Axe - Anger | B | lrhand | 1940 | 175 | 91 | 325 |
| 4856 | Great Axe - Critical Stun | B | lrhand | 1940 | 175 | 91 | 325 |
| 4857 | Great Axe - Light | B | lrhand | 1940 | 175 | 91 | 325 |
| 4858 | Lance - Anger | B | lrhand | 1920 | 194 | 99 | 325 |
| 4859 | Lance - Critical Stun | B | lrhand | 1920 | 194 | 99 | 325 |
| 4860 | Lance - Towering Blow | B | lrhand | 1920 | 194 | 99 | 325 |
| 8858 | Shadow Item: Great Axe | B | lrhand | 650 | 175 | 91 | 325 |
| 9010 | Shadow Item: Great Axe | B | lrhand | 650 | 175 | 91 | 325 |
| 10874 | Great Axe - Thunder | B | lrhand | 1940 | 175 | 91 | 325 |
| 10875 | Great Axe - Thunder - Anger | B | lrhand | 1940 | 175 | 91 | 325 |
| 10876 | Great Axe - Thunder - Critical Stun | B | lrhand | 1940 | 175 | 91 | 325 |
| 10877 | Great Axe - Thunder - Light | B | lrhand | 1940 | 175 | 91 | 325 |
| 10967 | Lance - Earth | B | lrhand | 1920 | 194 | 99 | 325 |
| 10968 | Lance - Earth - Anger | B | lrhand | 1920 | 194 | 99 | 325 |
| 10969 | Lance - Earth - Critical Stun | B | lrhand | 1920 | 194 | 99 | 325 |
| 10970 | Lance - Earth - Towering Blow | B | lrhand | 1920 | 194 | 99 | 325 |
| 11890 | Common Item - Great Axe | B | lrhand | 647 | 175 | 91 | 325 |
| 11932 | Common Item - Lance | B | lrhand | 640 | 194 | 99 | 325 |
| 13195 | Player Commendation - Lance - Player Commendation Weapon | B | lrhand | 1920 | 194 | 99 | 325 |
| 15065 | Lance of Fortune - 30-day limited period | B | lrhand | 1920 | 194 | 99 | 325 |
| 15179 | Lance of Fortune - 10-day limited period | B | lrhand | 1920 | 194 | 99 | 325 |
| 16953 | Lance of Fortune - 90-day limited period | B | lrhand | 1920 | 194 | 99 | 325 |
| 20146 | Lance (Event) - 4-hour limited period | B | lrhand | 640 | 194 | 99 | 325 |
| 98 | Halberd | A | lrhand | 1900 | 213 | 107 | 325 |
| 304 | Orcish Halberd | A | lrhand | 1880 | 219 | 109 | 325 |
| 305 | Tallum Glaive | A | lrhand | 1840 | 232 | 114 | 325 |
| 4861 | Halberd - Critical Stun | A | lrhand | 1900 | 213 | 107 | 325 |
| 4862 | Halberd - Towering Blow | A | lrhand | 1900 | 213 | 107 | 325 |
| 4863 | Halberd - Wide Blow | A | lrhand | 1900 | 213 | 107 | 325 |
| 5626 | Halberd - Haste | A | lrhand | 1900 | 213 | 107 | 325 |
| 5627 | Halberd - Critical Stun | A | lrhand | 1900 | 213 | 107 | 325 |
| 5628 | Halberd - Wide Blow | A | lrhand | 1900 | 213 | 107 | 325 |
| 5629 | Orcish Halberd | A | lrhand | 1880 | 219 | 109 | 325 |
| 5630 | Orcish Halberd | A | lrhand | 1880 | 219 | 109 | 325 |
| 5631 | Orcish Halberd | A | lrhand | 1880 | 219 | 109 | 325 |
| 5632 | Tallum Glaive - Guidance | A | lrhand | 1840 | 232 | 114 | 325 |
| 5633 | Tallum Glaive - Health | A | lrhand | 1840 | 232 | 114 | 325 |
| 5634 | Tallum Glaive - Wide Blow | A | lrhand | 1840 | 232 | 114 | 325 |
| 8683 | Tiphon's Spear | A | lrhand | 1820 | 251 | 121 | 325 |
| 8803 | Tiphon's Spear - Critical Stun | A | lrhand | 1820 | 251 | 121 | 325 |
| 8804 | Tiphon's Spear - Towering Blow | A | lrhand | 1820 | 251 | 121 | 325 |
| 8805 | Tiphon's Spear - Wild Blow | A | lrhand | 1820 | 251 | 121 | 325 |
| 8860 | Shadow Item: Halberd | A | lrhand | 640 | 213 | 107 | 325 |
| 9012 | Shadow Item: Halberd | A | lrhand | 640 | 213 | 107 | 325 |
| 9028 | Shadow Item: Tallum Glaive | A | lrhand | 613 | 232 | 114 | 325 |
| 10682 | Tiphon's Spear {PvP} - Critical Stun | A | lrhand | 1820 | 251 | 121 | 325 |
| 10683 | Tiphon's Spear {PvP} - Towering Blow | A | lrhand | 1820 | 251 | 121 | 325 |
| 10684 | Tiphon's Spear {PvP} - Wild Blow | A | lrhand | 1820 | 251 | 121 | 325 |
| 11070 | Halberd - Lightning | A | lrhand | 1900 | 213 | 107 | 325 |
| 11071 | Halberd - Lightning - Haste | A | lrhand | 1900 | 213 | 107 | 325 |
| 11072 | Halberd - Lightning - Critical Stun | A | lrhand | 1900 | 213 | 107 | 325 |
| 11073 | Halberd - Lightning - Wide Blow | A | lrhand | 1900 | 213 | 107 | 325 |
| 11128 | Tallum Glaive - On Fire | A | lrhand | 1840 | 232 | 114 | 325 |
| 11129 | Tallum Glaive - On Fire - Guidance | A | lrhand | 1840 | 232 | 114 | 325 |
| 11130 | Tallum Glaive - On Fire - Health | A | lrhand | 1840 | 232 | 114 | 325 |
| 11131 | Tallum Glaive - On Fire - Wide Blow | A | lrhand | 1840 | 232 | 114 | 325 |
| 11177 | Tiphon's Spear - Landslide | A | lrhand | 1820 | 251 | 121 | 325 |
| 11178 | Tiphon's Spear - Landslide - Critical Stun | A | lrhand | 1820 | 251 | 121 | 325 |
| 11179 | Tiphon's Spear - Landslide - Towering Blow | A | lrhand | 1820 | 251 | 121 | 325 |
| 11180 | Tiphon's Spear - Landslide - Wild Blow | A | lrhand | 1820 | 251 | 121 | 325 |
| 11960 | Common Item - Halberd | A | lrhand | 633 | 213 | 107 | 325 |
| 11976 | Common Item - Tallum Glaive | A | lrhand | 613 | 232 | 114 | 325 |
| 11988 | Common Item - Tiphon's Spear | A | lrhand | 607 | 251 | 121 | 325 |
| 12885 | Tiphon's Spear - Landslide {PvP} - Critical Stun | A | lrhand | 1820 | 251 | 121 | 325 |
| 12886 | Tiphon's Spear - Landslide {PvP} - Towering Blow | A | lrhand | 1820 | 251 | 121 | 325 |
| 12887 | Tiphon's Spear - Landslide {PvP} - Wild Blow | A | lrhand | 1820 | 251 | 121 | 325 |
| 13052 | Spear of Silenos | A | lrhand | 607 | 251 | 161 | 325 |
| 13053 | Enhanced Spear of Silenos | A | lrhand | 607 | 271 | 171 | 325 |
| 13054 | Complete Spear of Silenos | A | lrhand | 607 | 291 | 181 | 325 |
| 13215 | Player Commendation - Tiphon's Spear - Player Commendation Weapon | A | lrhand | 1820 | 251 | 121 | 325 |
| 15064 | Tiphon's Spear of Fortune - 30-day limited period | A | lrhand | 1820 | 251 | 121 | 325 |
| 15178 | Tiphon's Spear of Fortune - 10-day limited period | A | lrhand | 1820 | 251 | 121 | 325 |
| 16952 | Tiphon's Spear of Fortune - 90-day limited period | A | lrhand | 1820 | 251 | 121 | 325 |
| 20160 | Tallum Glaive (Event) - 4-hour limited period | A | lrhand | 613 | 232 | 114 | 325 |
| 306 | Dragon Claw Axe | S | lrhand | 1820 | 251 | 121 | 325 |
| 307 | Aurakyria Lance | S | lrhand | 1800 | 269 | 128 | 325 |
| 6370 | Saint Spear | S | lrhand | 1800 | 281 | 132 | 325 |
| 6599 | Saint Spear - Health | S | lrhand | 1800 | 281 | 132 | 325 |
| 6600 | Saint Spear - Guidance | S | lrhand | 1800 | 281 | 132 | 325 |
| 6601 | Saint Spear - Haste | S | lrhand | 1800 | 281 | 132 | 325 |
| 6621 | Infinity Spear | S | lrhand | 1300 | 524 | 230 | 325 |
| 9447 | Dynasty Halberd | S | lrhand | 2010 | 333 | 151 | 325 |
| 9869 | Dynasty Halberd - Anger | S | lrhand | 2010 | 333 | 151 | 325 |
| 9870 | Dynasty Halberd - Critical Stun | S | lrhand | 2010 | 333 | 151 | 325 |
| 9871 | Dynasty Halberd - Light | S | lrhand | 2010 | 333 | 151 | 325 |
| 10725 | Saint Spear {PvP} - Health | S | lrhand | 1800 | 281 | 132 | 325 |
| 10726 | Saint Spear {PvP} - Guidance | S | lrhand | 1800 | 281 | 132 | 325 |
| 10727 | Saint Spear {PvP} - Haste | S | lrhand | 1800 | 281 | 132 | 325 |
| 10765 | Dynasty Halberd {PvP} - Anger | S | lrhand | 2010 | 333 | 151 | 325 |
| 10766 | Dynasty Halberd {PvP} - Critical Stun | S | lrhand | 2010 | 333 | 151 | 325 |
| 10767 | Dynasty Halberd {PvP} - Light | S | lrhand | 2010 | 333 | 151 | 325 |
| 11218 | Saint Spear - Destruction | S | lrhand | 1800 | 281 | 132 | 325 |
| 11219 | Saint Spear - Destruction - Health | S | lrhand | 1800 | 281 | 132 | 325 |
| 11220 | Saint Spear - Destruction - Guidance | S | lrhand | 1800 | 281 | 132 | 325 |
| 11221 | Saint Spear - Destruction - Haste | S | lrhand | 1800 | 281 | 132 | 325 |
| 11296 | Dynasty Halberd - Earth | S | lrhand | 2010 | 333 | 151 | 325 |
| 11297 | Dynasty Halberd - Earth - Anger | S | lrhand | 2010 | 333 | 151 | 325 |
| 11298 | Dynasty Halberd - Earth - Critical Stun | S | lrhand | 2010 | 333 | 151 | 325 |
| 11299 | Dynasty Halberd - Earth - Light | S | lrhand | 2010 | 333 | 151 | 325 |
| 11999 | Common Item - Saint Spear | S | lrhand | 600 | 281 | 132 | 325 |
| 12916 | Saint Spear - Destruction {PvP} - Health | S | lrhand | 1800 | 281 | 132 | 325 |
| 12917 | Saint Spear - Destruction {PvP} - Guidance | S | lrhand | 1800 | 281 | 132 | 325 |
| 12918 | Saint Spear - Destruction {PvP} - Haste | S | lrhand | 1800 | 281 | 132 | 325 |
| 12975 | Dynasty Halberd - Earth {PvP} - Anger | S | lrhand | 2010 | 333 | 151 | 325 |
| 12976 | Dynasty Halberd - Earth {PvP} - Critical Stun | S | lrhand | 2010 | 333 | 151 | 325 |
| 12977 | Dynasty Halberd - Earth {PvP} - Light | S | lrhand | 2010 | 333 | 151 | 325 |
| 14571 | Spear of Hunter Family | S | lrhand | 1350 | 310 | 119 | 325 |
| 14574 | Spear of Halter Family | S | lrhand | 1350 | 310 | 119 | 325 |
| 15318 | Player Commendation - Saint Spear - Player Recommendation Weapon | S | lrhand | 1800 | 281 | 132 | 325 |
| 20174 | Saint Spear (Event) - 4-hour limited period | S | lrhand | 600 | 281 | 132 | 325 |
| 21829 | Saint Spear of Fortune - 90-day limited period | S | lrhand | 1800 | 281 | 132 | 325 |
| 21841 | Dynasty Halberd of Fortune - 90-day limited period | S | lrhand | 2010 | 333 | 151 | 325 |
| 10219 | Icarus Trident | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 10449 | Icarus Trident - Anger | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 10450 | Icarus Trident - Critical Stun | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 10451 | Icarus Trident - Light | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 11329 | Icarus Trident - Thunder | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 11330 | Icarus Trident - Thunder - Anger | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 11331 | Icarus Trident - Thunder - Critical Stun | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 11332 | Icarus Trident - Thunder - Light | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 14367 | Icarus Trident {PvP} | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 14391 | Icarus Trident {PvP} - Anger | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 14392 | Icarus Trident {PvP} - Critical Stun | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 14393 | Icarus Trident {PvP} - Light | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 14441 | Icarus Trident - Thunder {PvP} | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 14442 | Icarus Trident - Thunder {PvP} - Anger | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 14443 | Icarus Trident - Thunder {PvP} - Critical Stun | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 14444 | Icarus Trident - Thunder {PvP} - Light | S80 | lrhand | 2010 | 363 | 163 | 325 |
| 15301 | Transparent Pole (for NPC) | S80 | lrhand | 1950 | 156 | 83 | 325 |
| 13462 | Vesper Stormer | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 14133 | Vesper Stormer - Health | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 14134 | Vesper Stormer - Guidance | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 14135 | Vesper Stormer - Haste | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 14468 | Vesper Stormer {PvP} | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 14493 | Vesper Stormer {PvP} - Health | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 14494 | Vesper Stormer {PvP} - Guidance | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 14495 | Vesper Stormer {PvP} - Haste | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 15550 | Demitelum | S84 | lrhand | 2010 | 437 | 192 | 325 |
| 15564 | Doubletop Spear | S84 | lrhand | 2010 | 415 | 183 | 325 |
| 15682 | Triumph Spear | S84 | lrhand | 2010 | 396 | 183 | 325 |
| 15847 | Doubletop Spear - Guidance | S84 | lrhand | 2010 | 415 | 183 | 325 |
| 15848 | Doubletop Spear - Haste | S84 | lrhand | 2010 | 415 | 183 | 325 |
| 15849 | Doubletop Spear - Health | S84 | lrhand | 2010 | 415 | 183 | 325 |
| 15889 | Demitelum - Haste | S84 | lrhand | 2010 | 437 | 192 | 325 |
| 15890 | Demitelum - Health | S84 | lrhand | 2010 | 437 | 192 | 325 |
| 15891 | Demitelum - Guidance | S84 | lrhand | 2010 | 437 | 192 | 325 |
| 15919 | Demitelum {PvP} | S84 | lrhand | 2010 | 437 | 192 | 325 |
| 15933 | Doubletop Spear {PvP} | S84 | lrhand | 2010 | 415 | 183 | 325 |
| 15959 | Doubletop Spear {PvP} - Guidance | S84 | lrhand | 2010 | 415 | 183 | 325 |
| 15960 | Doubletop Spear {PvP} - Haste | S84 | lrhand | 2010 | 415 | 183 | 325 |
| 15961 | Doubletop Spear {PvP} - Health | S84 | lrhand | 2010 | 415 | 183 | 325 |
| 16001 | Demitelum {PvP} - Haste | S84 | lrhand | 2010 | 437 | 192 | 325 |
| 16002 | Demitelum {PvP} - Health | S84 | lrhand | 2010 | 437 | 192 | 325 |
| 16003 | Demitelum {PvP} - Guidance | S84 | lrhand | 2010 | 437 | 192 | 325 |
| 16047 | Vesper Stormer - Thunder | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 16071 | Vesper Stormer - Thunder - Health | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 16072 | Vesper Stormer - Thunder - Guidance | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 16073 | Vesper Stormer - Thunder - Haste | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 16139 | Vesper Stormer - Thunder {PvP} | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 16194 | Vesper Stormer - Thunder {PvP} - Health | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 16195 | Vesper Stormer - Thunder {PvP} - Guidance | S84 | lrhand | 2010 | 396 | 176 | 325 |
| 16196 | Vesper Stormer - Thunder {PvP} - Haste | S84 | lrhand | 2010 | 396 | 176 | 325 |

### BOW (245)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 13 | Short Bow | NONE | lrhand | 1950 | 16 | 6 | 293 |
| 14 | Bow | NONE | lrhand | 1930 | 23 | 9 | 293 |
| 271 | Hunting Bow | NONE | lrhand | 1910 | 34 | 12 | 293 |
| 272 | Forest Bow | NONE | lrhand | 1900 | 49 | 17 | 293 |
| 273 | Composite Bow | NONE | lrhand | 1880 | 64 | 21 | 293 |
| 1181 | Neti's Bow | NONE | lrhand | 1850 | 45 | 16 | 293 |
| 1213 | Guard's Bow | NONE | lrhand | 1800 | 49 | 17 | 293 |
| 1307 | Bow | NONE | lrhand | 150 | 120 | 6 | 293 |
| 3028 | Crescent Moon Bow | NONE | lrhand | 600 | 34 | 12 | 293 |
| 6715 | Monster Only(Silenos Archer) | NONE | lrhand | 1950 | 16 | 6 | 293 |
| 6720 | Monster Only(Shadow of Halisha) | NONE | lrhand | 1950 | 16 | 6 | 293 |
| 7820 | Apprentice Adventurer's Bow | NONE | lrhand | 1900 | 49 | 17 | 293 |
| 8220 | Monster Only (Grail Apostle Bow) | NONE | lrhand | 1950 |  |  | 293 |
| 8580 | Forest Bow (Event) | NONE | lrhand | 1900 | 49 | 17 | 293 |
| 8980 | Shadow Item: Composite Bow | NONE | lrhand | 627 | 64 | 21 | 293 |
| 9140 | Salvation Bow | NONE | lrhand | 900 | 1 | 1 | 293 |
| 9141 | Redemption Bow | NONE | lrhand | 300 | 1 | 1 | 293 |
| 9906 | Improved Composite Bow | NONE | lrhand | 1880 | 64 | 21 | 293 |
| 10212 | For NPC (Bow) | NONE | rhand | 1530 | 31 | 21 | 379 |
| 10478 | Shadow Item - Forest Bow | NONE | lrhand | 1900 | 49 | 17 | 293 |
| 13161 | Player Commendation - Compound Bow - Player Commendation Weapon | NONE | lrhand | 1880 | 64 | 21 | 293 |
| 14627 | Santa Claus' Shyeed Bow | NONE | lrhand | 1640 | 116 | 42 | 227 |
| 14786 | Baguette's Bow | NONE | lrhand | 1790 |  |  |  |
| 20261 | Baguette Bow - 7-day limited period | NONE | lrhand | 500 | 1 | 3 | 227 |
| 274 | Reinforced Bow | D | lrhand | 1870 | 82 | 26 | 293 |
| 275 | Long Bow | D | lrhand | 1830 | 114 | 35 | 227 |
| 276 | Elven Bow | D | lrhand | 1850 | 105 | 32 | 293 |
| 277 | Dark Elven Bow | D | lrhand | 1830 | 105 | 32 | 293 |
| 278 | Gastraphetes | D | lrhand | 1840 | 132 | 39 | 293 |
| 279 | Reinforced Long Bow | D | lrhand | 1820 | 179 | 51 | 227 |
| 280 | Light Crossbow | D | lrhand | 1810 | 191 | 54 | 293 |
| 7823 | Traveler's Dark Elven Bow | D | lrhand | 1830 | 105 | 32 | 293 |
| 7824 | Traveler's Long Bow | D | lrhand | 1830 | 105 | 32 | 293 |
| 8527 | For Monsters Only (Reinforced Bow) | D | lrhand | 1870 | 82 | 26 | 293 |
| 8583 | Dark Elven Bow (Event) | D | lrhand | 1830 | 105 | 32 | 293 |
| 8584 | Long Bow (Event) | D | lrhand | 1830 | 114 | 35 | 227 |
| 8828 | Shadow Item: Gastraphetes | D | lrhand | 620 | 132 | 39 | 293 |
| 8989 | Shadow Item: Gastraphetes | D | lrhand | 620 | 132 | 39 | 293 |
| 11606 | Common Item - Reinforced Bow | D | lrhand | 623 | 82 | 26 | 293 |
| 11629 | Common Item - Dark Elven Bow | D | lrhand | 610 | 105 | 32 | 293 |
| 11632 | Common Item - Long Bow | D | lrhand | 610 | 114 | 35 | 227 |
| 11640 | Common Item - Elven Bow | D | lrhand | 617 | 105 | 32 | 293 |
| 11659 | Common Item - Gastraphetes | D | lrhand | 613 | 132 | 39 | 293 |
| 11683 | Common Item - Reinforced Long Bow | D | lrhand | 607 | 179 | 51 | 227 |
| 11728 | Common Item - Light Crossbow | D | lrhand | 603 | 191 | 54 | 293 |
| 13172 | Player Commendation - Crossbow - Player Commendation Weapon | D | lrhand | 1810 | 191 | 54 | 293 |
| 15043 | Light Crossbow of Fortune - 30-day limited period | D | lrhand | 1810 | 191 | 54 | 293 |
| 15157 | Light Crossbow of Fortune - 10-day limited period | D | lrhand | 1810 | 191 | 54 | 293 |
| 16931 | Light Crossbow of Fortune - 90-day limited period | D | lrhand | 1810 | 191 | 54 | 293 |
| 20117 | Strengthened Long Bow (Event) - 4-hour limited period | D | lrhand | 607 | 179 | 51 | 227 |
| 20640 | Common Item - Light Crossbow | D | lrhand | 100 | 191 | 54 | 293 |
| 21739 | Reinforced Long Bow - Event | D | lrhand | 1820 | 179 | 51 | 227 |
| 281 | Crystallized Ice Bow | C | lrhand | 1790 | 220 | 61 | 293 |
| 282 | Elemental Bow | C | lrhand | 1770 | 277 | 75 | 227 |
| 283 | Akat Long Bow | C | lrhand | 1740 | 316 | 84 | 227 |
| 285 | Noble Elven Bow | C | lrhand | 1760 | 252 | 68 | 293 |
| 286 | Eminence Bow | C | lrhand | 1720 | 323 | 83 | 293 |
| 4810 | Crystallized Ice Bow - Guidance | C | lrhand | 1790 | 220 | 61 | 293 |
| 4811 | Crystallized Ice Bow - Evasion | C | lrhand | 1790 | 220 | 61 | 293 |
| 4812 | Crystallized Ice Bow - Quick Recovery | C | lrhand | 1790 | 220 | 61 | 293 |
| 4813 | Elemental Bow - Guidance | C | lrhand | 1770 | 277 | 75 | 227 |
| 4814 | Elemental Bow - Miser | C | lrhand | 1770 | 277 | 75 | 227 |
| 4815 | Elemental Bow - Quick Recovery | C | lrhand | 1770 | 277 | 75 | 227 |
| 4816 | Noble Elven Bow - Evasion | C | lrhand | 1760 | 252 | 68 | 293 |
| 4817 | Noble Elven Bow - Miser | C | lrhand | 1760 | 252 | 68 | 293 |
| 4818 | Noble Elven Bow - Cheap Shot | C | lrhand | 1760 | 252 | 68 | 293 |
| 4819 | Akat Long Bow - Guidance | C | lrhand | 1740 | 316 | 84 | 227 |
| 4820 | Akat Long Bow - Evasion | C | lrhand | 1740 | 316 | 84 | 227 |
| 4821 | Akat Long Bow - Miser | C | lrhand | 1740 | 316 | 84 | 227 |
| 4822 | Eminence Bow - Guidance | C | lrhand | 1720 | 323 | 83 | 293 |
| 4823 | Eminence Bow - Miser | C | lrhand | 1720 | 323 | 83 | 293 |
| 4824 | Eminence Bow - Cheap Shot | C | lrhand | 1720 | 323 | 83 | 293 |
| 8835 | Shadow Item: Elemental Bow | C | lrhand | 590 | 277 | 75 | 227 |
| 8845 | Shadow Item: Akat Long Bow | C | lrhand | 580 | 316 | 84 | 227 |
| 8932 | Shadow Item: Akat Long Bow | C | lrhand | 580 | 316 | 84 | 227 |
| 8997 | Shadow Item: Akat Long Bow | C | lrhand | 580 | 316 | 84 | 227 |
| 11759 | Common Item - Crystallized Ice Bow | C | lrhand | 597 | 220 | 61 | 293 |
| 11775 | Common Item - Noble Elven Bow | C | lrhand | 587 | 252 | 68 | 293 |
| 11790 | Common Item - Elemental Bow | C | lrhand | 590 | 277 | 75 | 227 |
| 11814 | Common Item - Akat Long Bow | C | lrhand | 580 | 316 | 84 | 227 |
| 11857 | Common Item - Eminence Bow | C | lrhand | 573 | 323 | 83 | 293 |
| 13184 | Player Commendation - Eminence Bow - Player Commendation Weapon | C | lrhand | 1720 | 323 | 83 | 293 |
| 15042 | Eminence Bow of Fortune - 30-day limited period | C | lrhand | 1720 | 323 | 83 | 293 |
| 15156 | Eminence Bow of Fortune - 10-day limited period | C | lrhand | 1720 | 323 | 83 | 293 |
| 16930 | Eminence Bow of Fortune - 90-day limited period | C | lrhand | 1720 | 323 | 83 | 293 |
| 20131 | Eminence Bow (Event) - 4-hour limited period | C | lrhand | 573 | 323 | 83 | 293 |
| 284 | Dark Elven Long Bow | B | lrhand | 1720 | 397 | 100 | 227 |
| 287 | Bow of Peril | B | lrhand | 1700 | 400 | 99 | 293 |
| 4825 | Dark Elven Long Bow - Evasion | B | lrhand | 1720 | 397 | 100 | 227 |
| 4826 | Dark Elven Long Bow - Critical Bleed | B | lrhand | 1720 | 397 | 100 | 227 |
| 4827 | Dark Elven Long Bow - Miser | B | lrhand | 1720 | 397 | 100 | 227 |
| 4828 | Bow of Peril - Guidance | B | lrhand | 1700 | 400 | 99 | 293 |
| 4829 | Bow of Peril - Quick Recovery | B | lrhand | 1700 | 400 | 99 | 293 |
| 4830 | Bow of Peril - Cheap Shot | B | lrhand | 1700 | 400 | 99 | 293 |
| 8856 | Shadow Item: Dark Elven Long Bow | B | lrhand | 580 | 397 | 100 | 227 |
| 9008 | Shadow Item: Dark Elven Long Bow | B | lrhand | 580 | 397 | 100 | 227 |
| 10886 | Dark Elven Long Bow - Concentration | B | lrhand | 1720 | 397 | 100 | 227 |
| 10887 | Dark Elven Long Bow - Concentration - Evasion | B | lrhand | 1720 | 397 | 100 | 227 |
| 10888 | Dark Elven Long Bow - Concentration - Critical Bleed | B | lrhand | 1720 | 397 | 100 | 227 |
| 10889 | Dark Elven Long Bow - Concentration - Miser | B | lrhand | 1720 | 397 | 100 | 227 |
| 11009 | Bow of Peril - Earth | B | lrhand | 1700 | 400 | 99 | 293 |
| 11010 | Bow of Peril - Earth - Guidance | B | lrhand | 1700 | 400 | 99 | 293 |
| 11011 | Bow of Peril - Earth - Quick Recovery | B | lrhand | 1700 | 400 | 99 | 293 |
| 11012 | Bow of Peril - Earth - Cheap Shot | B | lrhand | 1700 | 400 | 99 | 293 |
| 11896 | Common Item - Dark Elven Long Bow | B | lrhand | 573 | 397 | 100 | 227 |
| 11944 | Common Item - Bow of Peril | B | lrhand | 567 | 400 | 99 | 293 |
| 13201 | Player Commendation - Bow of Peril - Player Commendation Weapon | B | lrhand | 1700 | 400 | 99 | 293 |
| 15041 | Fortune Bow of Peril - 30-day limited period | B | lrhand | 1700 | 400 | 99 | 293 |
| 15155 | Fortune Bow of Peril - 10-day limited period | B | lrhand | 1700 | 400 | 99 | 293 |
| 16929 | Fortune Bow of Peril - 90-day limited period | B | lrhand | 1700 | 400 | 99 | 293 |
| 20145 | Bow of Peril (Event) - 4-hour limited period | B | lrhand | 567 | 400 | 99 | 293 |
| 288 | Carnage Bow | A | lrhand | 1670 | 440 | 107 | 293 |
| 289 | Soul Bow | A | lrhand | 1660 | 528 | 125 | 227 |
| 4831 | Carnage Bow - Critical Bleed | A | lrhand | 1670 | 440 | 107 | 293 |
| 4832 | Carnage Bow - Mana Up | A | lrhand | 1670 | 440 | 107 | 293 |
| 4833 | Carnage Bow - Quick Recovery | A | lrhand | 1670 | 440 | 107 | 293 |
| 5608 | Carnage Bow - Light | A | lrhand | 900 | 440 | 107 | 293 |
| 5609 | Carnage Bow - Critical Bleed | A | lrhand | 1670 | 440 | 107 | 293 |
| 5610 | Carnage Bow - Mana Up | A | lrhand | 1670 | 440 | 107 | 293 |
| 5611 | Soul Bow - Cheap Shot | A | lrhand | 1660 | 528 | 125 | 227 |
| 5612 | Soul Bow - Quick Recovery | A | lrhand | 1660 | 528 | 125 | 227 |
| 5613 | Soul Bow - Critical Poison | A | lrhand | 1660 | 528 | 125 | 227 |
| 8684 | Shyeed's Bow | A | lrhand | 1640 | 570 | 133 | 227 |
| 8806 | Shyeed's Bow - Cheap Shot | A | lrhand | 1640 | 570 | 133 | 227 |
| 8807 | Shyeed's Bow - Focus | A | lrhand | 1640 | 570 | 133 | 227 |
| 8808 | Shyeed's Bow - Quick Recovery | A | lrhand | 1640 | 570 | 133 | 227 |
| 8864 | Shadow Item: Carnage Bow | A | lrhand | 560 | 440 | 107 | 293 |
| 9016 | Shadow Item: Carnage Bow | A | lrhand | 560 | 440 | 107 | 293 |
| 9027 | Shadow Item: Soul Bow | A | lrhand | 553 | 528 | 125 | 227 |
| 10685 | Shyeed's Bow {PvP} - Cheap Shot | A | lrhand | 1640 | 571 | 133 | 227 |
| 10686 | Shyeed's Bow {PvP} - Focus | A | lrhand | 1640 | 571 | 133 | 227 |
| 10687 | Shyeed's Bow {PvP} - Quick Recovery | A | lrhand | 1640 | 571 | 133 | 227 |
| 11053 | Carnage Bow - Concentration | A | lrhand | 1670 | 440 | 107 | 293 |
| 11054 | Carnage Bow - Concentration - Light | A | lrhand | 900 | 440 | 107 | 293 |
| 11055 | Carnage Bow - Concentration - Critical Bleed | A | lrhand | 1670 | 440 | 107 | 293 |
| 11056 | Carnage Bow - Concentration - Mana Up | A | lrhand | 1670 | 440 | 107 | 293 |
| 11124 | Soul Bow - Clairvoyance | A | lrhand | 1660 | 528 | 125 | 227 |
| 11125 | Soul Bow - Clairvoyance - Cheap Shot | A | lrhand | 1660 | 528 | 125 | 227 |
| 11126 | Soul Bow - Clairvoyance - Quick Recovery | A | lrhand | 1660 | 528 | 125 | 227 |
| 11127 | Soul Bow - Clairvoyance - Critical Poison | A | lrhand | 1660 | 528 | 125 | 227 |
| 11157 | Shyeed's Bow - Concentration | A | lrhand | 1640 | 570 | 133 | 227 |
| 11158 | Shyeed's Bow - Concentration - Cheap Shot | A | lrhand | 1640 | 570 | 133 | 227 |
| 11159 | Shyeed's Bow - Concentration - Focus | A | lrhand | 1640 | 570 | 133 | 227 |
| 11160 | Shyeed's Bow - Concentration - Quick Recovery | A | lrhand | 1640 | 570 | 133 | 227 |
| 11955 | Common Item - Carnage Bow | A | lrhand | 557 | 440 | 107 | 293 |
| 11975 | Common Item - Soul Bow | A | lrhand | 553 | 528 | 125 | 227 |
| 11983 | Common Item - Shyeed's Bow | A | lrhand | 547 | 570 | 133 | 227 |
| 12870 | Shyeed's Bow - Concentration {PvP} - Cheap Shot | A | lrhand | 1640 | 571 | 133 | 227 |
| 12871 | Shyeed's Bow - Concentration {PvP} - Focus | A | lrhand | 1640 | 571 | 133 | 227 |
| 12872 | Shyeed's Bow - Concentration {PvP} - Quick Recovery | A | lrhand | 1640 | 571 | 133 | 227 |
| 13216 | Player Commendation - Shyeed's Bow - Player Commendation Weapon | A | lrhand | 1640 | 570 | 133 | 227 |
| 15040 | Shyeed's Bow of Fortune - 30-day limited period | A | lrhand | 1640 | 570 | 133 | 227 |
| 15154 | Shyeed's Bow of Fortune - 10-day limited period | A | lrhand | 1640 | 570 | 133 | 227 |
| 16928 | Shyeed's Bow of Fortune - 90-day limited period | A | lrhand | 1640 | 570 | 133 | 227 |
| 20159 | Soul Bow (Event) - 4-hour limited period | A | lrhand | 553 | 528 | 125 | 227 |
| 290 | The Bow | S | lrhand | 1650 | 519 | 121 | 293 |
| 6368 | Shining Bow | S | lrhand | 1650 | 581 | 132 | 293 |
| 6593 | Shining Bow - Cheap Shot | S | lrhand | 1650 | 581 | 132 | 293 |
| 6594 | Shining Bow - Focus | S | lrhand | 1650 | 581 | 132 | 293 |
| 6595 | Shining Bow - Critical Slow | S | lrhand | 1650 | 581 | 132 | 293 |
| 6619 | Infinity Bow | S | lrhand | 1300 | 952 | 230 | 293 |
| 7575 | Draconic Bow | S | lrhand | 1650 | 581 | 132 | 293 |
| 7576 | Draconic Bow - Cheap Shot | S | lrhand | 1650 | 581 | 132 | 293 |
| 7577 | Draconic Bow - Focus | S | lrhand | 1650 | 581 | 132 | 293 |
| 7578 | Draconic Bow - Critical Slow | S | lrhand | 1650 | 581 | 132 | 293 |
| 9445 | Dynasty Bow | S | lrhand | 1520 | 654 | 151 | 293 |
| 9863 | Dynasty Bow - Cheap Shot | S | lrhand | 1520 | 654 | 151 | 293 |
| 9864 | Dynasty Bow - Guidance | S | lrhand | 1520 | 654 | 151 | 293 |
| 9865 | Dynasty Bow - Focus | S | lrhand | 1520 | 654 | 151 | 293 |
| 10737 | Draconic Bow {PvP} - Cheap Shot | S | lrhand | 1650 | 581 | 132 | 293 |
| 10738 | Draconic Bow {PvP} - Focus | S | lrhand | 1650 | 581 | 132 | 293 |
| 10739 | Draconic Bow {PvP} - Critical Slow | S | lrhand | 1650 | 581 | 132 | 293 |
| 10780 | Dynasty Bow {PvP} - Cheap Shot | S | lrhand | 1520 | 654 | 151 | 293 |
| 10781 | Dynasty Bow {PvP} - Guidance | S | lrhand | 1520 | 654 | 151 | 293 |
| 10782 | Dynasty Bow {PvP} - Focus | S | lrhand | 1520 | 654 | 151 | 293 |
| 11198 | Draconic Bow - Earth | S | lrhand | 1650 | 581 | 132 | 293 |
| 11199 | Draconic Bow - Earth - Cheap Shot | S | lrhand | 1650 | 581 | 132 | 293 |
| 11200 | Draconic Bow - Earth - Focus | S | lrhand | 1650 | 581 | 132 | 293 |
| 11201 | Draconic Bow - Earth - Critical Slow | S | lrhand | 1650 | 581 | 132 | 293 |
| 11264 | Dynasty Bow - Great Gale | S | lrhand | 1520 | 654 | 151 | 293 |
| 11265 | Dynasty Bow - Great Gale - Cheap Shot | S | lrhand | 1520 | 654 | 151 | 293 |
| 11266 | Dynasty Bow - Great Gale - Guidance | S | lrhand | 1520 | 654 | 151 | 293 |
| 11267 | Dynasty Bow - Great Gale - Focus | S | lrhand | 1520 | 654 | 151 | 293 |
| 11994 | Common Item - Draconic Bow | S | lrhand | 550 | 581 | 132 | 293 |
| 12901 | Draconic Bow - Earth {PvP} - Cheap Shot | S | lrhand | 1650 | 581 | 132 | 293 |
| 12902 | Draconic Bow - Earth {PvP} - Focus | S | lrhand | 1650 | 581 | 132 | 293 |
| 12903 | Draconic Bow - Earth {PvP} - Critical Slow | S | lrhand | 1650 | 581 | 132 | 293 |
| 12951 | Dynasty Bow - Great Gale {PvP} - Cheap Shot | S | lrhand | 1520 | 654 | 151 | 293 |
| 12952 | Dynasty Bow - Great Gale {PvP} - Guidance | S | lrhand | 1520 | 654 | 151 | 293 |
| 12953 | Dynasty Bow - Great Gale {PvP} - Focus | S | lrhand | 1520 | 654 | 151 | 293 |
| 14568 | Bow of Cadmus Family | S | lrhand | 1238 | 640 | 119 | 293 |
| 15322 | Player Commendation - Draconic Bow - Player Recommendation Weapon | S | lrhand | 1650 | 581 | 132 | 293 |
| 20173 | Draconic Bow (Event) - 4-hour limited period | S | lrhand | 550 | 581 | 132 | 293 |
| 21823 | Draconic Bow of Fortune - 90-day limited period | S | lrhand | 1650 | 581 | 132 | 293 |
| 21835 | Dynasty Bow of Fortune - 90-day limited period | S | lrhand | 1520 | 654 | 151 | 293 |
| 10223 | Icarus Spitter | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 10443 | Icarus Spitter - Cheap Shot | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 10444 | Icarus Spitter - Guidance | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 10445 | Icarus Spitter - Focus | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 11321 | Icarus Spitter - Concentration | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 11322 | Icarus Spitter - Concentration - Cheap Shot | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 11323 | Icarus Spitter - Concentration - Guidance | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 11324 | Icarus Spitter - Concentration - Focus | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 14371 | Icarus Spitter {PvP} | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 14385 | Icarus Spitter {PvP} - Cheap Shot | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 14386 | Icarus Spitter {PvP} - Guidance | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 14387 | Icarus Spitter {PvP} - Focus | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 14433 | Icarus Spitter - Concentration {PvP} | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 14434 | Icarus Spitter - Concentration {PvP} - Cheap Shot | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 14435 | Icarus Spitter - Concentration {PvP} - Guidance | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 14436 | Icarus Spitter - Concentration {PvP} - Focus | S80 | lrhand | 1520 | 689 | 163 | 293 |
| 15302 | Transparent Bow (for NPC) | S80 | lrhand | 1830 | 114 | 35 | 227 |
| 13467 | Vesper Thrower | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 14148 | Vesper Thrower - Cheap Shot | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 14149 | Vesper Thrower - Focus | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 14150 | Vesper Thrower - Critical Slow | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 14473 | Vesper Thrower {PvP} | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 14508 | Vesper Thrower {PvP} - Cheap Shot | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 14509 | Vesper Thrower {PvP} - Focus | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 14510 | Vesper Thrower {PvP} - Critical Slow | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 15554 | Recurve Thorne Bow | S84 | lrhand | 1520 | 794 | 192 | 293 |
| 15568 | Skull Carnium Bow | S84 | lrhand | 1520 | 768 | 183 | 293 |
| 15686 | Triumph Bow | S84 | lrhand | 1520 | 724 | 183 | 293 |
| 15859 | Skull Carnium Bow - Focus | S84 | lrhand | 1520 | 768 | 183 | 293 |
| 15860 | Skull Carnium Bow - Critical Slow | S84 | lrhand | 1520 | 768 | 183 | 293 |
| 15861 | Skull Carnium Bow - Cheap Shot | S84 | lrhand | 1520 | 768 | 183 | 293 |
| 15901 | Recurve Thorne Bow - Critical Slow | S84 | lrhand | 1520 | 794 | 192 | 293 |
| 15902 | Recurve Thorne Bow - Cheap Shot | S84 | lrhand | 1520 | 794 | 192 | 293 |
| 15903 | Recurve Thorne Bow - Focus | S84 | lrhand | 1520 | 794 | 192 | 293 |
| 15923 | Recurve Thorne Bow {PvP} | S84 | lrhand | 1520 | 794 | 192 | 293 |
| 15937 | Skull Carnium Bow {PvP} | S84 | lrhand | 1520 | 768 | 183 | 293 |
| 15971 | Skull Carnium Bow {PvP} - Focus | S84 | lrhand | 1520 | 768 | 183 | 293 |
| 15972 | Skull Carnium Bow {PvP} - Critical Slow | S84 | lrhand | 1520 | 768 | 183 | 293 |
| 15973 | Skull Carnium Bow {PvP} - Cheap Shot | S84 | lrhand | 1520 | 768 | 183 | 293 |
| 16013 | Recurve Thorne Bow {PvP} - Critical Slow | S84 | lrhand | 1520 | 794 | 192 | 293 |
| 16014 | Recurve Thorne Bow {PvP} - Cheap Shot | S84 | lrhand | 1520 | 794 | 192 | 293 |
| 16015 | Recurve Thorne Bow {PvP} - Focus | S84 | lrhand | 1520 | 794 | 192 | 293 |
| 16052 | Vesper Thrower - Clairvoyance | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 16086 | Vesper Thrower - Clairvoyance - Cheap Shot | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 16087 | Vesper Thrower - Clairvoyance - Focus | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 16088 | Vesper Thrower - Clairvoyance - Critical Slow | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 16144 | Vesper Thrower - Clairvoyance {PvP} | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 16209 | Vesper Thrower - Clairvoyance {PvP} - Cheap Shot | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 16210 | Vesper Thrower - Clairvoyance {PvP} - Focus | S84 | lrhand | 1520 | 724 | 176 | 293 |
| 16211 | Vesper Thrower - Clairvoyance {PvP} - Critical Slow | S84 | lrhand | 1520 | 724 | 176 | 293 |

### CROSSBOW (204)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 14633 | Santa Claus' Screaming Vengeance | NONE | lrhand | 1640 | 56 | 38 | 303 |
| 14794 | Baguette's Crossbow | NONE | lrhand | 1580 |  |  |  |
| 20269 | Baguette Crossbow - 7-day limited period | NONE | lrhand | 500 | 1 | 3 | 303 |
| 9212 | Field Gun | D | lrhand | 1870 | 51 | 26 | 303 |
| 9217 | Hand Crossbow | D | lrhand | 1850 | 64 | 32 | 303 |
| 9221 | Crossbow | D | lrhand | 1840 | 81 | 39 | 303 |
| 9224 | Arm Breaker | D | lrhand | 1820 | 100 | 47 | 303 |
| 9227 | Cranequin | D | lrhand | 1810 | 117 | 54 | 303 |
| 9995 | Hand Crossbow | D | lrhand | 1850 | 64 | 32 | 303 |
| 9996 | Hand Crossbow | D | lrhand | 1850 | 64 | 32 | 303 |
| 10007 | Shadow Item: Hand Crossbow | D | lrhand | 693 | 64 | 32 | 303 |
| 11624 | Common Item - Field Gun | D | lrhand | 623 | 51 | 26 | 303 |
| 11652 | Common Item - Hand Crossbow | D | lrhand | 617 | 64 | 32 | 303 |
| 11653 | Common Item - Hand Crossbow | D | lrhand | 617 | 64 | 32 | 303 |
| 11654 | Common Item - Hand Crossbow | D | lrhand | 617 | 64 | 32 | 303 |
| 11674 | Common Item - Crossbow | D | lrhand | 613 | 81 | 39 | 303 |
| 11701 | Common Item - Arm Breaker | D | lrhand | 607 | 100 | 47 | 303 |
| 11735 | Common Item - Cranequin | D | lrhand | 603 | 117 | 54 | 303 |
| 13177 | Player Commendation - Cranequin - Player Commendation Weapon | D | lrhand | 1810 | 117 | 54 | 303 |
| 15079 | Cranequin of Fortune - 30-day limited period | D | lrhand | 1810 | 117 | 54 | 303 |
| 15193 | Cranequin of Fortune - 10-day limited period | D | lrhand | 1810 | 117 | 54 | 303 |
| 16967 | Cranequin of Fortune - 90-day limited period | D | lrhand | 1810 | 117 | 54 | 303 |
| 20122 | Arm Breaker (Event) - 4-hour limited period | D | lrhand | 607 | 100 | 47 | 303 |
| 21745 | Arm Breaker - Event | D | lrhand | 1820 | 100 | 47 | 303 |
| 9236 | Arbalest | C | lrhand | 1790 | 135 | 61 | 303 |
| 9237 | Arbalest - Guidance | C | lrhand | 1790 | 135 | 61 | 303 |
| 9238 | Arbalest - Evasion | C | lrhand | 1790 | 135 | 61 | 303 |
| 9239 | Arbalest - Quick Recovery | C | lrhand | 1790 | 135 | 61 | 303 |
| 9256 | Ballista | C | lrhand | 1770 | 155 | 68 | 303 |
| 9257 | Ballista - Guidance | C | lrhand | 1770 | 155 | 68 | 303 |
| 9258 | Ballista - Miser | C | lrhand | 1770 | 155 | 68 | 303 |
| 9259 | Ballista - Quick Recovery | C | lrhand | 1770 | 155 | 68 | 303 |
| 9260 | Ballista | C | lrhand | 1770 | 155 | 68 | 303 |
| 9261 | Ballista - Evasion | C | lrhand | 1770 | 155 | 68 | 303 |
| 9262 | Ballista - Miser | C | lrhand | 1770 | 155 | 68 | 303 |
| 9263 | Ballista - Cheap Shot | C | lrhand | 1770 | 155 | 68 | 303 |
| 9288 | Tathlum | C | lrhand | 1760 | 176 | 76 | 303 |
| 9289 | Tathlum - Guidance | C | lrhand | 1760 | 176 | 76 | 303 |
| 9290 | Tathlum - Evasion | C | lrhand | 1760 | 176 | 76 | 303 |
| 9291 | Tathlum - Miser | C | lrhand | 1760 | 176 | 76 | 303 |
| 9300 | Sharpshooter | C | lrhand | 1740 | 198 | 83 | 303 |
| 9301 | Sharpshooter - Guidance | C | lrhand | 1740 | 198 | 83 | 303 |
| 9302 | Sharpshooter - Miser | C | lrhand | 1740 | 198 | 83 | 303 |
| 9303 | Sharpshooter - Cheap Shot | C | lrhand | 1740 | 198 | 83 | 303 |
| 9842 | Shadow Item: Ballista | C | lrhand | 590 | 155 | 68 | 303 |
| 9845 | Shadow Item: Tathlum | C | lrhand | 587 | 176 | 76 | 303 |
| 10010 | Shadow Item: Tathlum | C | lrhand | 587 | 176 | 76 | 303 |
| 11758 | Common Item - Arbalest | C | lrhand | 597 | 135 | 61 | 303 |
| 11780 | Common Item - Ballista | C | lrhand | 590 | 155 | 68 | 303 |
| 11781 | Common Item - Ballista | C | lrhand | 590 | 155 | 68 | 303 |
| 11823 | Common Item - Tathlum | C | lrhand | 587 | 176 | 76 | 303 |
| 11844 | Common Item - Sharpshooter | C | lrhand | 580 | 198 | 83 | 303 |
| 13190 | Player Commendation - Sharpshooter - Player Commendation Weapon | C | lrhand | 1740 | 198 | 83 | 303 |
| 15078 | Sharpshooter of Fortune - 30-day limited period | C | lrhand | 1740 | 198 | 83 | 303 |
| 15192 | Sharpshooter of Fortune - 10-day limited period | C | lrhand | 1740 | 198 | 83 | 303 |
| 16966 | Sharpshooter of Fortune - 90-day limited period | C | lrhand | 1740 | 198 | 83 | 303 |
| 20136 | Sharpshooter (Event) - 4-hour limited period | C | lrhand | 580 | 198 | 83 | 303 |
| 9312 | Peacemaker | B | lrhand | 1720 | 221 | 91 | 303 |
| 9313 | Peacemaker - Evasion | B | lrhand | 1720 | 221 | 91 | 303 |
| 9314 | Peacemaker - Critical Bleed | B | lrhand | 1720 | 221 | 91 | 303 |
| 9315 | Peacemaker - Miser | B | lrhand | 1720 | 221 | 91 | 303 |
| 9324 | Hell Hound | B | lrhand | 1700 | 245 | 99 | 303 |
| 9325 | Hell Hound - Guidance | B | lrhand | 1700 | 245 | 99 | 303 |
| 9326 | Hell Hound - Quick Recovery | B | lrhand | 1700 | 245 | 99 | 303 |
| 9327 | Hell Hound - Cheap Shot | B | lrhand | 1700 | 245 | 99 | 303 |
| 9848 | Shadow Item: Peacemaker | B | lrhand | 573 | 221 | 91 | 303 |
| 10934 | Peacemaker - Concentration | B | lrhand | 1720 | 221 | 91 | 303 |
| 10935 | Peacemaker - Concentration - Evasion | B | lrhand | 1720 | 221 | 91 | 303 |
| 10936 | Peacemaker - Concentration - Critical Bleed | B | lrhand | 1720 | 221 | 91 | 303 |
| 10937 | Peacemaker - Concentration - Miser | B | lrhand | 1720 | 221 | 91 | 303 |
| 11013 | Hell Hound - Earth | B | lrhand | 1700 | 245 | 99 | 303 |
| 11014 | Hell Hound - Earth - Guidance | B | lrhand | 1700 | 245 | 99 | 303 |
| 11015 | Hell Hound - Earth - Quick Recovery | B | lrhand | 1700 | 245 | 99 | 303 |
| 11016 | Hell Hound - Earth - Cheap Shot | B | lrhand | 1700 | 245 | 99 | 303 |
| 11917 | Common Item - Peacemaker | B | lrhand | 573 | 221 | 91 | 303 |
| 11945 | Common Item - Hell Hound | B | lrhand | 567 | 245 | 99 | 303 |
| 13209 | Player Commendation - Hell Hound - Player Commendation Weapon | B | lrhand | 1700 | 245 | 99 | 303 |
| 15077 | Hell Hound of Fortune - 30-day limited period | B | lrhand | 1700 | 245 | 99 | 303 |
| 15191 | Hell Hound of Fortune - 10-day limited period | B | lrhand | 1700 | 245 | 99 | 303 |
| 16965 | Hell Hound of Fortune - 90-day limited period | B | lrhand | 1700 | 245 | 99 | 303 |
| 20150 | Hell Hound (Event) - 4-hour limited period | B | lrhand | 567 | 245 | 99 | 303 |
| 9336 | Doomchanter | A | lrhand | 1670 | 270 | 107 | 303 |
| 9337 | Doomchanter - Light | A | lrhand | 1670 | 270 | 107 | 303 |
| 9338 | Doomchanter - Critical Bleed | A | lrhand | 1670 | 270 | 107 | 303 |
| 9339 | Doomchanter - Mana Up | A | lrhand | 1670 | 270 | 107 | 303 |
| 9348 | Reaper | A | lrhand | 1660 | 294 | 114 | 303 |
| 9349 | Reaper - Cheap Shot | A | lrhand | 1660 | 294 | 114 | 303 |
| 9350 | Reaper - Quick Recovery | A | lrhand | 1660 | 294 | 114 | 303 |
| 9351 | Reaper - Critical Poison | A | lrhand | 1660 | 294 | 114 | 303 |
| 9360 | Screaming Vengeance | A | lrhand | 1640 | 318 | 121 | 303 |
| 9361 | Screaming Vengeance - Cheap Shot | A | lrhand | 1640 | 318 | 121 | 303 |
| 9362 | Screaming Vengeance - Focus | A | lrhand | 1640 | 318 | 121 | 303 |
| 9363 | Screaming Vengeance - Quick Recovery | A | lrhand | 1640 | 318 | 121 | 303 |
| 10706 | Screaming Vengeance {PvP} - Cheap Shot | A | lrhand | 1640 | 318 | 121 | 303 |
| 10707 | Screaming Vengeance {PvP} - Focus | A | lrhand | 1640 | 318 | 121 | 303 |
| 10708 | Screaming Vengeance {PvP} - Quick Recovery | A | lrhand | 1640 | 318 | 121 | 303 |
| 11021 | Doomchanter - Concentration | A | lrhand | 1670 | 270 | 107 | 303 |
| 11022 | Doomchanter - Concentration - Light | A | lrhand | 1670 | 270 | 107 | 303 |
| 11023 | Doomchanter - Concentration - Critical Bleed | A | lrhand | 1670 | 270 | 107 | 303 |
| 11024 | Doomchanter - Concentration - Mana Up | A | lrhand | 1670 | 270 | 107 | 303 |
| 11112 | Reaper - Clairvoyance | A | lrhand | 1660 | 294 | 114 | 303 |
| 11113 | Reaper - Clairvoyance - Cheap Shot | A | lrhand | 1660 | 294 | 114 | 303 |
| 11114 | Reaper - Clairvoyance - Quick Recovery | A | lrhand | 1660 | 294 | 114 | 303 |
| 11115 | Reaper - Clairvoyance - Critical Poison | A | lrhand | 1660 | 294 | 114 | 303 |
| 11145 | Screaming Vengeance - Concentration | A | lrhand | 1640 | 318 | 121 | 303 |
| 11146 | Screaming Vengeance - Concentration - Cheap Shot | A | lrhand | 1640 | 318 | 121 | 303 |
| 11147 | Screaming Vengeance - Concentration - Focus | A | lrhand | 1640 | 318 | 121 | 303 |
| 11148 | Screaming Vengeance - Concentration - Quick Recovery | A | lrhand | 1640 | 318 | 121 | 303 |
| 11947 | Common Item - Doomchanter | A | lrhand | 557 | 270 | 107 | 303 |
| 11972 | Common Item - Reaper | A | lrhand | 553 | 294 | 114 | 303 |
| 11980 | Common Item - Screaming Vengeance | A | lrhand | 547 | 318 | 121 | 303 |
| 12861 | Screaming Vengeance - Concentration {PvP} - Cheap Shot | A | lrhand | 1640 | 318 | 121 | 303 |
| 12862 | Screaming Vengeance - Concentration {PvP} - Focus | A | lrhand | 1640 | 318 | 121 | 303 |
| 12863 | Screaming Vengeance - Concentration {PvP} - Quick Recovery | A | lrhand | 1640 | 318 | 121 | 303 |
| 13224 | Player Commendation - Screaming Vengeance - Player Commendation Weapon | A | lrhand | 1640 | 318 | 121 | 303 |
| 15076 | Screaming Vengeance of Fortune - 30-day limited period | A | lrhand | 1640 | 318 | 121 | 303 |
| 15190 | Screaming Vengeance of Fortune - 10-day limited period | A | lrhand | 1640 | 318 | 121 | 303 |
| 16964 | Screaming Vengeance of Fortune - 90-day limited period | A | lrhand | 1640 | 318 | 121 | 303 |
| 20164 | Reaper (Event) - 4-hour limited period | A | lrhand | 553 | 294 | 114 | 303 |
| 9372 | Sarunga | S | lrhand | 1600 | 356 | 132 | 303 |
| 9373 | Sarunga - Cheap Shot | S | lrhand | 1600 | 356 | 132 | 303 |
| 9374 | Sarunga - Focus | S | lrhand | 1600 | 356 | 132 | 303 |
| 9375 | Sarunga - Critical Slow | S | lrhand | 1600 | 356 | 132 | 303 |
| 9384 | Dynasty Crossbow | S | lrhand | 1580 | 401 | 151 | 303 |
| 9385 | Dynasty Crossbow - Cheap Shot | S | lrhand | 1580 | 401 | 151 | 303 |
| 9386 | Dynasty Crossbow - Guidance | S | lrhand | 1580 | 401 | 151 | 303 |
| 9387 | Dynasty Crossbow - Focus | S | lrhand | 1580 | 401 | 151 | 303 |
| 9390 | Infinity Shooter | S | lrhand | 1580 | 584 | 230 | 303 |
| 10746 | Sarunga {PvP} - Cheap Shot | S | lrhand | 1600 | 356 | 132 | 303 |
| 10747 | Sarunga {PvP} - Focus | S | lrhand | 1600 | 356 | 132 | 303 |
| 10748 | Sarunga {PvP} - Critical Slow | S | lrhand | 1600 | 356 | 132 | 303 |
| 10789 | Dynasty Crossbow {PvP} - Cheap Shot | S | lrhand | 1580 | 401 | 151 | 303 |
| 10790 | Dynasty Crossbow {PvP} - Guidance | S | lrhand | 1580 | 401 | 151 | 303 |
| 10791 | Dynasty Crossbow {PvP} - Focus | S | lrhand | 1580 | 401 | 151 | 303 |
| 11214 | Sarunga - Earth | S | lrhand | 1600 | 356 | 132 | 303 |
| 11215 | Sarunga - Earth - Cheap Shot | S | lrhand | 1600 | 356 | 132 | 303 |
| 11216 | Sarunga - Earth - Focus | S | lrhand | 1600 | 356 | 132 | 303 |
| 11217 | Sarunga - Earth - Critical Slow | S | lrhand | 1600 | 356 | 132 | 303 |
| 11288 | Dynasty Crossbow - Great Gale | S | lrhand | 1580 | 401 | 151 | 303 |
| 11289 | Dynasty Crossbow - Great Gale - Cheap Shot | S | lrhand | 1580 | 401 | 151 | 303 |
| 11290 | Dynasty Crossbow - Great Gale - Guidance | S | lrhand | 1580 | 401 | 151 | 303 |
| 11291 | Dynasty Crossbow - Great Gale - Focus | S | lrhand | 1580 | 401 | 151 | 303 |
| 11998 | Common Item - Sarunga | S | lrhand | 533 | 356 | 132 | 303 |
| 12913 | Sarunga - Earth {PvP} - Cheap Shot | S | lrhand | 1600 | 356 | 132 | 303 |
| 12914 | Sarunga - Earth {PvP} - Focus | S | lrhand | 1600 | 356 | 132 | 303 |
| 12915 | Sarunga - Earth {PvP} - Critical Slow | S | lrhand | 1600 | 356 | 132 | 303 |
| 12969 | Dynasty Crossbow - Great Gale {PvP} - Cheap Shot | S | lrhand | 1580 | 401 | 151 | 303 |
| 12970 | Dynasty Crossbow - Great Gale {PvP} - Guidance | S | lrhand | 1580 | 401 | 151 | 303 |
| 12971 | Dynasty Crossbow - Great Gale {PvP} - Focus | S | lrhand | 1580 | 401 | 151 | 303 |
| 14581 | Estoc of Cadmus Family | S | lrhand | 1200 | 392 | 119 | 303 |
| 15325 | Player Commendation - Sarunga - Player Recommendation Weapon | S | lrhand | 1600 | 356 | 132 | 303 |
| 20178 | Sarunga (Event) - 4-hour limited period | S | lrhand | 533 | 356 | 132 | 303 |
| 21832 | Sarunga of Fortune - 90-day limited period | S | lrhand | 1600 | 356 | 132 | 303 |
| 21844 | Dynasty Crossbow of Fortune - 90-day limited period | S | lrhand | 1580 | 401 | 151 | 303 |
| 10226 | Icarus Shooter | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 10467 | Icarus Shooter - Cheap Shot | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 10468 | Icarus Shooter - Guidance | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 10469 | Icarus Shooter - Focus | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 11309 | Icarus Shooter - Concentration | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 11310 | Icarus Shooter - Concentration - Cheap Shot | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 11311 | Icarus Shooter - Concentration - Guidance | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 11312 | Icarus Shooter - Concentration - Focus | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 14374 | Icarus Shooter {PvP} | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 14409 | Icarus Shooter {PvP} - Cheap Shot | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 14410 | Icarus Shooter {PvP} - Guidance | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 14411 | Icarus Shooter {PvP} - Focus | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 14421 | Icarus Shooter - Concentration {PvP} | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 14422 | Icarus Shooter - Concentration {PvP} - Cheap Shot | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 14423 | Icarus Shooter - Concentration {PvP} - Guidance | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 14424 | Icarus Shooter - Concentration {PvP} - Focus | S80 | lrhand | 1580 | 422 | 163 | 303 |
| 15304 | Transparent Bowgun (for NPC) | S80 | lrhand | 1850 | 64 | 32 | 303 |
| 13469 | Vesper Shooter | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 14154 | Vesper Shooter - Cheap Shot | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 14155 | Vesper Shooter - Focus | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 14156 | Vesper Shooter - Critical Slow | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 14475 | Vesper Shooter {PvP} | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 14514 | Vesper Shooter {PvP} - Cheap Shot | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 14515 | Vesper Shooter {PvP} - Focus | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 14516 | Vesper Shooter {PvP} - Critical Slow | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 15557 | Thorne Crossbow | S84 | lrhand | 1580 | 487 | 192 | 303 |
| 15571 | Dominion Crossbow | S84 | lrhand | 1580 | 471 | 183 | 303 |
| 15689 | Triumph Crossbow | S84 | lrhand | 1580 | 444 | 183 | 303 |
| 15868 | Dominion Crossbow - Focus | S84 | lrhand | 1580 | 471 | 183 | 303 |
| 15869 | Dominion Crossbow - Critical Slow | S84 | lrhand | 1580 | 471 | 183 | 303 |
| 15870 | Dominion Crossbow - Cheap Shot | S84 | lrhand | 1580 | 471 | 183 | 303 |
| 15910 | Thorne Crossbow - Critical Slow | S84 | lrhand | 1580 | 487 | 192 | 303 |
| 15911 | Thorne Crossbow - Cheap Shot | S84 | lrhand | 1580 | 487 | 192 | 303 |
| 15912 | Thorne Crossbow - Focus | S84 | lrhand | 1580 | 487 | 192 | 303 |
| 15926 | Thorne Crossbow {PvP} | S84 | lrhand | 1580 | 487 | 192 | 303 |
| 15940 | Dominion Crossbow {PvP} | S84 | lrhand | 1580 | 471 | 183 | 303 |
| 15980 | Dominion Crossbow {PvP} - Focus | S84 | lrhand | 1580 | 471 | 183 | 303 |
| 15981 | Dominion Crossbow {PvP} - Critical Slow | S84 | lrhand | 1580 | 471 | 183 | 303 |
| 15982 | Dominion Crossbow {PvP} - Cheap Shot | S84 | lrhand | 1580 | 471 | 183 | 303 |
| 16022 | Thorne Crossbow {PvP} - Critical Slow | S84 | lrhand | 1580 | 487 | 192 | 303 |
| 16023 | Thorne Crossbow {PvP} - Cheap Shot | S84 | lrhand | 1580 | 487 | 192 | 303 |
| 16024 | Thorne Crossbow {PvP} - Focus | S84 | lrhand | 1580 | 487 | 192 | 303 |
| 16054 | Vesper Shooter - Clairvoyance | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 16092 | Vesper Shooter - Clairvoyance - Cheap Shot | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 16093 | Vesper Shooter - Clairvoyance - Focus | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 16094 | Vesper Shooter - Clairvoyance - Critical Slow | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 16146 | Vesper Shooter - Clairvoyance {PvP} | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 16215 | Vesper Shooter - Clairvoyance {PvP} - Cheap Shot | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 16216 | Vesper Shooter - Clairvoyance {PvP} - Focus | S84 | lrhand | 1580 | 444 | 176 | 303 |
| 16217 | Vesper Shooter - Clairvoyance {PvP} - Critical Slow | S84 | lrhand | 1580 | 444 | 176 | 303 |

### RAPIER (239)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 9720 | Warrior's Sword | NONE | rhand | 1300 | 12 | 10 | 406 |
| 14632 | Santa Claus' Éclair Bijou | NONE | rhand | 1300 | 46 | 38 | 406 |
| 14792 | Baguette's Rapier | NONE | rhand | 1520 |  |  |  |
| 20267 | Baguette Rapier - 7-day limited period | NONE | rhand | 500 | 1 | 3 | 406 |
| 9209 | Rapier | D | rhand | 1520 | 36 | 26 | 406 |
| 9213 | Fleuret | D | rhand | 1500 | 46 | 32 | 406 |
| 9214 | Fleuret | D | rhand | 1500 | 46 | 32 | 406 |
| 9215 | Fleuret | D | rhand | 1500 | 46 | 32 | 406 |
| 9218 | Estoc | D | rhand | 1470 | 58 | 39 | 406 |
| 9219 | Estoc | D | rhand | 1470 | 58 | 39 | 406 |
| 9222 | Epee | D | rhand | 1450 | 72 | 47 | 406 |
| 9225 | Grand Epee | D | rhand | 1440 | 83 | 54 | 406 |
| 10003 | Fleuret | D | rhand | 1500 | 46 | 32 | 406 |
| 10005 | Shadow Item: Fleuret | D | rhand | 500 | 46 | 32 | 406 |
| 11607 | Common Item - Rapier | D | rhand | 507 | 36 | 26 | 406 |
| 11648 | Common Item - Fleuret | D | rhand | 500 | 46 | 32 | 406 |
| 11649 | Common Item - Fleuret | D | rhand | 500 | 46 | 32 | 406 |
| 11650 | Common Item - Fleuret | D | rhand | 500 | 46 | 32 | 406 |
| 11651 | Common Item - Fleuret | D | rhand | 500 | 46 | 32 | 406 |
| 11668 | Common Item - Estoc | D | rhand | 490 | 58 | 39 | 406 |
| 11669 | Common Item - Estoc | D | rhand | 490 | 58 | 39 | 406 |
| 11702 | Common Item - Epee | D | rhand | 483 | 72 | 47 | 406 |
| 11724 | Common Item - Grand Epee | D | rhand | 480 | 83 | 54 | 406 |
| 13175 | Player Commendation - Grand Epee - Player Commendation Weapon | D | rhand | 1440 | 83 | 54 | 406 |
| 15075 | Grand Epee of Fortune - 30-day limited period | D | rhand | 1440 | 83 | 54 | 406 |
| 15189 | Grand Epee of Fortune - 10-day limited period | D | rhand | 1440 | 83 | 54 | 406 |
| 16963 | Grand Epee of Fortune - 90-day limited period | D | rhand | 1440 | 83 | 54 | 406 |
| 20120 | Epee (Event) - 4-hour limited period | D | rhand | 483 | 72 | 47 | 406 |
| 21740 | Epee - Event | D | rhand | 1450 | 72 | 47 | 406 |
| 9228 | Soldat Estoc | C | rhand | 1430 | 97 | 61 | 406 |
| 9229 | Soldat Estoc - Critical Anger | C | rhand | 1430 | 97 | 61 | 406 |
| 9230 | Soldat Estoc - Focus | C | rhand | 1430 | 97 | 61 | 406 |
| 9231 | Soldat Estoc - Light | C | rhand | 1430 | 97 | 61 | 406 |
| 9240 | Chevalier Rapier | C | rhand | 1420 | 111 | 68 | 406 |
| 9241 | Chevalier Rapier - Guidance | C | rhand | 1420 | 111 | 68 | 406 |
| 9242 | Chevalier Rapier - Back Blow | C | rhand | 1420 | 111 | 68 | 406 |
| 9243 | Chevalier Rapier - Rsk. Evasion | C | rhand | 1420 | 111 | 68 | 406 |
| 9244 | Chevalier Rapier | C | rhand | 1420 | 111 | 68 | 406 |
| 9245 | Chevalier Rapier - Focus | C | rhand | 1420 | 111 | 68 | 406 |
| 9246 | Chevalier Rapier - Critical Damage | C | rhand | 1420 | 111 | 68 | 406 |
| 9247 | Chevalier Rapier - Haste | C | rhand | 1420 | 111 | 68 | 406 |
| 9248 | Chevalier Rapier | C | rhand | 1420 | 111 | 68 | 406 |
| 9249 | Chevalier Rapier - Critical Damage | C | rhand | 1420 | 111 | 68 | 406 |
| 9250 | Chevalier Rapier - Critical Poison | C | rhand | 1420 | 111 | 68 | 406 |
| 9251 | Chevalier Rapier - Haste | C | rhand | 1420 | 111 | 68 | 406 |
| 9252 | Chevalier Rapier | C | rhand | 1420 | 111 | 68 | 406 |
| 9253 | Chevalier Rapier - Focus | C | rhand | 1420 | 111 | 68 | 406 |
| 9254 | Chevalier Rapier - Critical Drain | C | rhand | 1420 | 111 | 68 | 406 |
| 9255 | Chevalier Rapier - Critical Poison | C | rhand | 1420 | 111 | 68 | 406 |
| 9264 | Blinzlasher | C | rhand | 1400 | 126 | 76 | 406 |
| 9265 | Blinzlasher - Guidance | C | rhand | 1400 | 126 | 76 | 406 |
| 9266 | Blinzlasher - Focus | C | rhand | 1400 | 126 | 76 | 406 |
| 9267 | Blinzlasher - Critical Damage | C | rhand | 1400 | 126 | 76 | 406 |
| 9268 | Blinzlasher | C | rhand | 1400 | 126 | 76 | 406 |
| 9269 | Blinzlasher - Focus | C | rhand | 1400 | 126 | 76 | 406 |
| 9270 | Blinzlasher - Health | C | rhand | 1400 | 126 | 76 | 406 |
| 9271 | Blinzlasher - Rsk. Haste | C | rhand | 1400 | 126 | 76 | 406 |
| 9272 | Blinzlasher | C | rhand | 1400 | 126 | 76 | 406 |
| 9273 | Blinzlasher - Focus | C | rhand | 1400 | 126 | 76 | 406 |
| 9274 | Blinzlasher - Critical Damage | C | rhand | 1400 | 126 | 76 | 406 |
| 9275 | Blinzlasher - Haste | C | rhand | 1400 | 126 | 76 | 406 |
| 9276 | Blinzlasher | C | rhand | 1400 | 126 | 76 | 406 |
| 9277 | Blinzlasher - Health | C | rhand | 1400 | 126 | 76 | 406 |
| 9278 | Blinzlasher - Focus | C | rhand | 1400 | 126 | 76 | 406 |
| 9279 | Blinzlasher - Light | C | rhand | 1400 | 126 | 76 | 406 |
| 9280 | Blinzlasher | C | rhand | 1400 | 126 | 76 | 406 |
| 9281 | Blinzlasher - Guidance | C | rhand | 1400 | 126 | 76 | 406 |
| 9282 | Blinzlasher - Critical Drain | C | rhand | 1400 | 126 | 76 | 406 |
| 9283 | Blinzlasher - Health | C | rhand | 1400 | 126 | 76 | 406 |
| 9292 | Admiral's Estoc | C | rhand | 1380 | 141 | 83 | 406 |
| 9293 | Admiral's Estoc - Focus | C | rhand | 1380 | 141 | 83 | 406 |
| 9294 | Admiral's Estoc - Critical Damage | C | rhand | 1380 | 141 | 83 | 406 |
| 9295 | Admiral's Estoc - Haste | C | rhand | 1380 | 141 | 83 | 406 |
| 9840 | Shadow Item: Chevalier Rapier | C | rhand | 473 | 111 | 68 | 406 |
| 9843 | Shadow Item: Blinzlasher | C | rhand | 467 | 126 | 76 | 406 |
| 10008 | Shadow Item: Blinzlasher | C | rhand | 467 | 126 | 76 | 406 |
| 11753 | Common Item - Soldat Estoc | C | rhand | 477 | 97 | 61 | 406 |
| 11784 | Common Item - Chevalier Rapier | C | rhand | 473 | 111 | 68 | 406 |
| 11785 | Common Item - Chevalier Rapier | C | rhand | 473 | 111 | 68 | 406 |
| 11786 | Common Item - Chevalier Rapier | C | rhand | 473 | 111 | 68 | 406 |
| 11787 | Common Item - Chevalier Rapier | C | rhand | 473 | 111 | 68 | 406 |
| 11808 | Common Item - Blinzlasher | C | rhand | 467 | 126 | 76 | 406 |
| 11809 | Common Item - Blinzlasher | C | rhand | 467 | 126 | 76 | 406 |
| 11810 | Common Item - Blinzlasher | C | rhand | 467 | 126 | 76 | 406 |
| 11811 | Common Item - Blinzlasher | C | rhand | 467 | 126 | 76 | 406 |
| 11812 | Common Item - Blinzlasher | C | rhand | 467 | 126 | 76 | 406 |
| 11854 | Common Item - Admiral's Estoc | C | rhand | 460 | 141 | 83 | 406 |
| 13188 | Player Commendation - Admiral's Estoc - Player Commendation Weapon | C | rhand | 1380 | 141 | 83 | 406 |
| 15074 | Admiral's Estoc of Fortune - 30-day limited period | C | rhand | 1380 | 141 | 83 | 406 |
| 15188 | Admiral's Estoc of Fortune - 10-day limited period | C | rhand | 1380 | 141 | 83 | 406 |
| 16962 | Admiral's Estoc of Fortune - 90-day limited period | C | rhand | 1380 | 141 | 83 | 406 |
| 20134 | Admiral's Estoc (Event) - 4-hour limited period | C | rhand | 460 | 141 | 83 | 406 |
| 9304 | Military Fleuret | B | rhand | 1370 | 159 | 91 | 406 |
| 9305 | Military Fleuret - Guidance | B | rhand | 1370 | 159 | 91 | 406 |
| 9306 | Military Fleuret - Focus | B | rhand | 1370 | 159 | 91 | 406 |
| 9307 | Military Fleuret - Back Blow | B | rhand | 1370 | 159 | 91 | 406 |
| 9316 | Colichemarde | B | rhand | 1350 | 176 | 99 | 406 |
| 9317 | Colichemarde - Focus | B | rhand | 1350 | 176 | 99 | 406 |
| 9318 | Colichemarde - Critical Damage | B | rhand | 1350 | 176 | 99 | 406 |
| 9319 | Colichemarde - Haste | B | rhand | 1350 | 176 | 99 | 406 |
| 9846 | Shadow Item: Military Fleuret | B | rhand | 457 | 159 | 91 | 406 |
| 10912 | Military Fleuret - Destruction | B | rhand | 1370 | 159 | 91 | 406 |
| 10913 | Military Fleuret - Destruction - Guidance | B | rhand | 1370 | 159 | 91 | 406 |
| 10914 | Military Fleuret - Destruction - Focus | B | rhand | 1370 | 159 | 91 | 406 |
| 10915 | Military Fleuret - Destruction - Back Blow | B | rhand | 1370 | 159 | 91 | 406 |
| 11001 | Colichemarde - Earth | B | rhand | 1350 | 176 | 99 | 406 |
| 11002 | Colichemarde - Earth - Focus | B | rhand | 1350 | 176 | 99 | 406 |
| 11003 | Colichemarde - Earth - Critical Damage | B | rhand | 1350 | 176 | 99 | 406 |
| 11004 | Colichemarde - Earth - Haste | B | rhand | 1350 | 176 | 99 | 406 |
| 11907 | Common Item - Military Fleuret | B | rhand | 457 | 159 | 91 | 406 |
| 11942 | Common Item - Colichemarde | B | rhand | 450 | 176 | 99 | 406 |
| 13207 | Player Commendation - Colichemarde - Player Commendation Weapon | B | rhand | 1350 | 176 | 99 | 406 |
| 15073 | Colichemarde of Fortune - 30-day limited period | B | rhand | 1350 | 176 | 99 | 406 |
| 15187 | Colichemarde of Fortune - 10-day limited period | B | rhand | 1350 | 176 | 99 | 406 |
| 16961 | Colichemarde of Fortune - 90-day limited period | B | rhand | 1350 | 176 | 99 | 406 |
| 20148 | Colichemarde (Event) - 4-hour limited period | B | rhand | 450 | 176 | 99 | 406 |
| 9328 | White Lightning | A | rhand | 1330 | 193 | 107 | 406 |
| 9329 | White Lightning - Critical Poison | A | rhand | 1330 | 193 | 107 | 406 |
| 9330 | White Lightning - Haste | A | rhand | 1330 | 193 | 107 | 406 |
| 9331 | White Lightning - Anger | A | rhand | 1330 | 193 | 107 | 406 |
| 9340 | Lacerator | A | rhand | 1320 | 210 | 114 | 406 |
| 9341 | Lacerator - Critical Damage | A | rhand | 1320 | 210 | 114 | 406 |
| 9342 | Lacerator - Health | A | rhand | 1320 | 210 | 114 | 406 |
| 9343 | Lacerator - Rsk. Focus | A | rhand | 1320 | 210 | 114 | 406 |
| 9352 | Éclair Bijou | A | rhand | 1300 | 228 | 121 | 406 |
| 9353 | Éclair Bijou - Haste | A | rhand | 1300 | 228 | 121 | 406 |
| 9354 | Éclair Bijou - Health | A | rhand | 1300 | 228 | 121 | 406 |
| 9355 | Éclair Bijou - Critical Poison | A | rhand | 1300 | 228 | 121 | 406 |
| 10700 | Éclair Bijou {PvP} - Haste | A | rhand | 1300 | 228 | 121 | 406 |
| 10701 | Éclair Bijou {PvP} - Health | A | rhand | 1300 | 228 | 121 | 406 |
| 10702 | Éclair Bijou {PvP} - Critical Poison | A | rhand | 1300 | 228 | 121 | 406 |
| 11025 | White Lightning - Destruction | A | rhand | 1330 | 193 | 107 | 406 |
| 11026 | White Lightning - Destruction - Critical Poison | A | rhand | 1330 | 193 | 107 | 406 |
| 11027 | White Lightning - Destruction - Haste | A | rhand | 1330 | 193 | 107 | 406 |
| 11028 | White Lightning - Destruction - Anger | A | rhand | 1330 | 193 | 107 | 406 |
| 11075 | Lacerator - Thunder | A | rhand | 1320 | 210 | 114 | 406 |
| 11076 | Lacerator - Thunder - Critical Damage | A | rhand | 1320 | 210 | 114 | 406 |
| 11077 | Lacerator - Thunder - Health | A | rhand | 1320 | 210 | 114 | 406 |
| 11078 | Lacerator - Thunder - Rsk. Focus | A | rhand | 1320 | 210 | 114 | 406 |
| 11173 | Éclair Bijou - Landslide | A | rhand | 1300 | 228 | 121 | 406 |
| 11174 | Éclair Bijou - Landslide - Haste | A | rhand | 1300 | 228 | 121 | 406 |
| 11175 | Éclair Bijou - Landslide - Health | A | rhand | 1300 | 228 | 121 | 406 |
| 11176 | Éclair Bijou - Landslide - Critical Poison | A | rhand | 1300 | 228 | 121 | 406 |
| 11948 | Common Item - White Lightning | A | rhand | 443 | 193 | 107 | 406 |
| 11962 | Common Item - Lacerator | A | rhand | 440 | 210 | 114 | 406 |
| 11987 | Common Item - Éclair Bijou | A | rhand | 433 | 228 | 121 | 406 |
| 12882 | Éclair Bijou - Landslide {PvP} - Haste | A | rhand | 1300 | 228 | 121 | 406 |
| 12883 | Éclair Bijou - Landslide {PvP} - Health | A | rhand | 1300 | 228 | 121 | 406 |
| 12884 | Éclair Bijou - Landslide {PvP} - Critical Poison | A | rhand | 1300 | 228 | 121 | 406 |
| 13222 | Player Commendation - Éclair Bijou - Player Commendation Weapon | A | rhand | 1300 | 228 | 121 | 406 |
| 15072 | Éclair Bijou of Fortune - 30-day limited period | A | rhand | 1300 | 228 | 121 | 406 |
| 15186 | Éclair Bijou of Fortune - 10-day limited period | A | rhand | 1300 | 228 | 121 | 406 |
| 16960 | Éclair Bijou of Fortune - 90-day limited period | A | rhand | 1300 | 228 | 121 | 406 |
| 20162 | Lacerator (Event) - 4-hour limited period | A | rhand | 440 | 210 | 114 | 406 |
| 9364 | Laevateinn | S | rhand | 1300 | 255 | 132 | 406 |
| 9365 | Laevateinn - Haste | S | rhand | 1300 | 255 | 132 | 406 |
| 9366 | Laevateinn - Health | S | rhand | 1300 | 255 | 132 | 406 |
| 9367 | Laevateinn - Focus | S | rhand | 1300 | 255 | 132 | 406 |
| 9376 | Dynasty Rapier | S | rhand | 1280 | 302 | 151 | 406 |
| 9377 | Dynasty Rapier - Focus | S | rhand | 1280 | 302 | 151 | 406 |
| 9378 | Dynasty Rapier - Health | S | rhand | 1280 | 302 | 151 | 406 |
| 9379 | Dynasty Rapier - Light | S | rhand | 1280 | 302 | 151 | 406 |
| 9388 | Infinity Rapier | S | rhand | 1280 | 475 | 230 | 406 |
| 10740 | Laevateinn {PvP} - Haste | S | rhand | 1300 | 255 | 132 | 406 |
| 10741 | Laevateinn {PvP} - Health | S | rhand | 1300 | 255 | 132 | 406 |
| 10742 | Laevateinn {PvP} - Focus | S | rhand | 1300 | 255 | 132 | 406 |
| 10783 | Dynasty Rapier {PvP} - Focus | S | rhand | 1280 | 302 | 151 | 406 |
| 10784 | Dynasty Rapier {PvP} - Health | S | rhand | 1280 | 302 | 151 | 406 |
| 10785 | Dynasty Rapier {PvP} - Light | S | rhand | 1280 | 302 | 151 | 406 |
| 11206 | Laevateinn - Lightning | S | rhand | 1300 | 255 | 132 | 406 |
| 11207 | Laevateinn - Lightning - Haste | S | rhand | 1300 | 255 | 132 | 406 |
| 11208 | Laevateinn - Lightning - Health | S | rhand | 1300 | 255 | 132 | 406 |
| 11209 | Laevateinn - Lightning - Focus | S | rhand | 1300 | 255 | 132 | 406 |
| 11252 | Dynasty Rapier - Earth | S | rhand | 1280 | 302 | 151 | 406 |
| 11253 | Dynasty Rapier - Earth - Focus | S | rhand | 1280 | 302 | 151 | 406 |
| 11254 | Dynasty Rapier - Earth - Health | S | rhand | 1280 | 302 | 151 | 406 |
| 11255 | Dynasty Rapier - Earth - Light | S | rhand | 1280 | 302 | 151 | 406 |
| 11996 | Common Item - Laevateinn | S | rhand | 433 | 255 | 132 | 406 |
| 12907 | Laevateinn - Lightning {PvP} - Haste | S | rhand | 1300 | 255 | 132 | 406 |
| 12908 | Laevateinn - Lightning {PvP} - Health | S | rhand | 1300 | 255 | 132 | 406 |
| 12909 | Laevateinn - Lightning {PvP} - Focus | S | rhand | 1300 | 255 | 132 | 406 |
| 12942 | Dynasty Rapier - Earth {PvP} - Focus | S | rhand | 1280 | 302 | 151 | 406 |
| 12943 | Dynasty Rapier - Earth {PvP} - Health | S | rhand | 1280 | 302 | 151 | 406 |
| 12944 | Dynasty Rapier - Earth {PvP} - Light | S | rhand | 1280 | 302 | 151 | 406 |
| 14579 | Epee of Ashton Family | S | rhand | 975 | 281 | 119 | 406 |
| 15323 | Player Commendation - Laevateinn - Player Recommendation Weapon | S | rhand | 1300 | 255 | 132 | 406 |
| 15687 | Triumph Rapier | S | rhand | 1280 | 344 | 183 | 406 |
| 20176 | Laevateinn (Event) - 4-hour limited period | S | rhand | 433 | 255 | 132 | 406 |
| 21831 | Laevateinn of Fortune - 90-day limited period | S | rhand | 1300 | 255 | 132 | 406 |
| 21843 | Dynasty Rapier of Fortune - 90-day limited period | S | rhand | 1280 | 302 | 151 | 406 |
| 10224 | Icarus Stinger | S80 | rhand | 1280 | 329 | 163 | 406 |
| 10461 | Icarus Stinger - Focus | S80 | rhand | 1280 | 329 | 163 | 406 |
| 10462 | Icarus Stinger - Health | S80 | rhand | 1280 | 329 | 163 | 406 |
| 10463 | Icarus Stinger - Light | S80 | rhand | 1280 | 329 | 163 | 406 |
| 11313 | Icarus Stinger - Destruction | S80 | rhand | 1280 | 329 | 163 | 406 |
| 11314 | Icarus Stinger - Destruction - Focus | S80 | rhand | 1280 | 329 | 163 | 406 |
| 11315 | Icarus Stinger - Destruction - Health | S80 | rhand | 1280 | 329 | 163 | 406 |
| 11316 | Icarus Stinger - Destruction - Light | S80 | rhand | 1280 | 329 | 163 | 406 |
| 14372 | Icarus Stinger {PvP} | S80 | rhand | 1280 | 329 | 163 | 406 |
| 14403 | Icarus Stinger {PvP} - Focus | S80 | rhand | 1280 | 329 | 163 | 406 |
| 14404 | Icarus Stinger {PvP} - Health | S80 | rhand | 1280 | 329 | 163 | 406 |
| 14405 | Icarus Stinger {PvP} - Light | S80 | rhand | 1280 | 329 | 163 | 406 |
| 14425 | Icarus Stinger - Destruction {PvP} | S80 | rhand | 1280 | 329 | 163 | 406 |
| 14426 | Icarus Stinger - Destruction {PvP} - Focus | S80 | rhand | 1280 | 329 | 163 | 406 |
| 14427 | Icarus Stinger - Destruction {PvP} - Health | S80 | rhand | 1280 | 329 | 163 | 406 |
| 14428 | Icarus Stinger - Destruction {PvP} - Light | S80 | rhand | 1280 | 329 | 163 | 406 |
| 15305 | Transparent Rapier (for NPC) | S80 | rhand | 1520 | 36 | 26 | 406 |
| 13468 | Vesper Pincer | S84 | rhand | 1280 | 359 | 176 | 406 |
| 14151 | Vesper Pincer - Haste | S84 | rhand | 1280 | 359 | 176 | 406 |
| 14152 | Vesper Pincer - Health | S84 | rhand | 1280 | 359 | 176 | 406 |
| 14153 | Vesper Pincer - Focus | S84 | rhand | 1280 | 359 | 176 | 406 |
| 14474 | Vesper Pincer {PvP} | S84 | rhand | 1280 | 359 | 176 | 406 |
| 14511 | Vesper Pincer {PvP} - Haste | S84 | rhand | 1280 | 359 | 176 | 406 |
| 14512 | Vesper Pincer {PvP} - Health | S84 | rhand | 1280 | 359 | 176 | 406 |
| 14513 | Vesper Pincer {PvP} - Focus | S84 | rhand | 1280 | 359 | 176 | 406 |
| 15555 | Heavenstare Rapier | S84 | rhand | 1280 | 396 | 192 | 406 |
| 15569 | Gemtail Rapier | S84 | rhand | 1280 | 376 | 183 | 406 |
| 15862 | Gemtail Rapier - Health | S84 | rhand | 1280 | 376 | 183 | 406 |
| 15863 | Gemtail Rapier - Focus | S84 | rhand | 1280 | 376 | 183 | 406 |
| 15864 | Gemtail Rapier - Haste | S84 | rhand | 1280 | 376 | 183 | 406 |
| 15904 | Heavenstare Rapier - Focus | S84 | rhand | 1280 | 396 | 192 | 406 |
| 15905 | Heavenstare Rapier - Haste | S84 | rhand | 1280 | 396 | 192 | 406 |
| 15906 | Heavenstare Rapier - Health | S84 | rhand | 1280 | 396 | 192 | 406 |
| 15924 | Heavenstare Rapier {PvP} | S84 | rhand | 1280 | 396 | 192 | 406 |
| 15938 | Gemtail Rapier {PvP} | S84 | rhand | 1280 | 376 | 183 | 406 |
| 15974 | Gemtail Rapier {PvP} - Health | S84 | rhand | 1280 | 376 | 183 | 406 |
| 15975 | Gemtail Rapier {PvP} - Focus | S84 | rhand | 1280 | 376 | 183 | 406 |
| 15976 | Gemtail Rapier {PvP} - Haste | S84 | rhand | 1280 | 376 | 183 | 406 |
| 16016 | Heavenstare Rapier {PvP} - Focus | S84 | rhand | 1280 | 396 | 192 | 406 |
| 16017 | Heavenstare Rapier {PvP} - Haste | S84 | rhand | 1280 | 396 | 192 | 406 |
| 16018 | Heavenstare Rapier {PvP} - Health | S84 | rhand | 1280 | 396 | 192 | 406 |
| 16053 | Vesper Pincer - Thunder | S84 | rhand | 1280 | 359 | 176 | 406 |
| 16089 | Vesper Pincer - Thunder - Haste | S84 | rhand | 1280 | 359 | 176 | 406 |
| 16090 | Vesper Pincer - Thunder - Health | S84 | rhand | 1280 | 359 | 176 | 406 |
| 16091 | Vesper Pincer - Thunder - Focus | S84 | rhand | 1280 | 359 | 176 | 406 |
| 16145 | Vesper Pincer- Thunder {PvP} | S84 | rhand | 1280 | 359 | 176 | 406 |
| 16212 | Vesper Pincer- Thunder {PvP} - Haste | S84 | rhand | 1280 | 359 | 176 | 406 |
| 16213 | Vesper Pincer- Thunder {PvP} - Health | S84 | rhand | 1280 | 359 | 176 | 406 |
| 16214 | Vesper Pincer- Thunder {PvP} - Focus | S84 | rhand | 1280 | 359 | 176 | 406 |

### ANCIENTSWORD (192)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 14634 | Santa Claus' Durendal | NONE | lrhand | 1820 | 65 | 38 | 350 |
| 14793 | Baguette's Ancient Sword | NONE | lrhand | 1800 |  |  |  |
| 20268 | Baguette Ancient Sword - 7-day limited period | NONE | lrhand | 500 | 1 | 3 | 350 |
| 9210 | Talwar | D | lrhand | 2100 | 43 | 26 | 350 |
| 9211 | Talwar | D | lrhand | 2100 | 43 | 26 | 350 |
| 9216 | Military Talwar | D | lrhand | 2080 | 55 | 32 | 350 |
| 9220 | Field Sword | D | lrhand | 2060 | 69 | 39 | 350 |
| 9223 | Katzbalger | D | lrhand | 2020 | 86 | 47 | 350 |
| 9226 | General's Katzbalger | D | lrhand | 2010 | 100 | 54 | 350 |
| 10006 | Shadow Item: Military Talwar | D | lrhand | 693 | 55 | 32 | 350 |
| 11620 | Common Item - Talwar | D | lrhand | 700 | 43 | 26 | 350 |
| 11621 | Common Item - Talwar | D | lrhand | 700 | 43 | 26 | 350 |
| 11639 | Common Item - Military Talwar | D | lrhand | 693 | 55 | 32 | 350 |
| 11677 | Common Item - Field Sword | D | lrhand | 687 | 69 | 39 | 350 |
| 11707 | Common Item - Katzbalger | D | lrhand | 673 | 86 | 47 | 350 |
| 11734 | Common Item - General's Katzbalger | D | lrhand | 670 | 100 | 54 | 350 |
| 13176 | Player Commendation - General Katzbalger - Player Commendation Weapon | D | lrhand | 2010 | 100 | 54 | 350 |
| 15071 | General's Katzbalger of Fortune - 30-day limited period | D | lrhand | 2010 | 100 | 54 | 350 |
| 15185 | General's Katzbalger of Fortune - 10-day limited period | D | lrhand | 2010 | 100 | 54 | 350 |
| 16959 | General's Katzbalger of Fortune - 90-day limited period | D | lrhand | 2010 | 100 | 54 | 350 |
| 20121 | Katzbalger (Event) - 4-hour limited period | D | lrhand | 673 | 86 | 47 | 350 |
| 21744 | Katzbalger - Event | D | lrhand | 2020 | 86 | 47 | 350 |
| 9232 | Schlager | C | lrhand | 1980 | 116 | 61 | 350 |
| 9233 | Schlager - Critical Damage | C | lrhand | 1980 | 116 | 61 | 350 |
| 9234 | Schlager - Focus | C | lrhand | 1980 | 116 | 61 | 350 |
| 9235 | Schlager - Light | C | lrhand | 1980 | 116 | 61 | 350 |
| 9284 | Immortal Edge | C | lrhand | 1980 | 151 | 76 | 350 |
| 9285 | Immortal Edge - Focus | C | lrhand | 1980 | 151 | 76 | 350 |
| 9286 | Immortal Edge - Health | C | lrhand | 1980 | 151 | 76 | 350 |
| 9287 | Immortal Edge - Critical Drain | C | lrhand | 1980 | 151 | 76 | 350 |
| 9296 | Saber Tooth | C | lrhand | 1950 | 169 | 83 | 350 |
| 9297 | Saber Tooth - Focus | C | lrhand | 1950 | 169 | 83 | 350 |
| 9298 | Saber Tooth - Critical Damage | C | lrhand | 1950 | 169 | 83 | 350 |
| 9299 | Saber Tooth - Haste | C | lrhand | 1950 | 169 | 83 | 350 |
| 9841 | Shadow Item: Riter Schlager | C | lrhand | 667 | 132 | 68 | 350 |
| 9844 | Shadow Item: Immortal Edge | C | lrhand | 660 | 151 | 76 | 350 |
| 10009 | Shadow Item: Immortal Edge | C | lrhand | 660 | 151 | 76 | 350 |
| 11754 | Common Item - Schlager | C | lrhand | 660 | 116 | 61 | 350 |
| 11818 | Common Item - Immortal Edge | C | lrhand | 660 | 151 | 76 | 350 |
| 11849 | Common Item - Saber Tooth | C | lrhand | 650 | 169 | 83 | 350 |
| 13189 | Player Commendation - Saber Tooth - Player Commendation Weapon | C | lrhand | 1950 | 169 | 83 | 350 |
| 15070 | Saber Tooth of Fortune - 30-day limited period | C | lrhand | 1950 | 169 | 83 | 350 |
| 15184 | Saber Tooth of Fortune - 10-day limited period | C | lrhand | 1950 | 169 | 83 | 350 |
| 16958 | Saber Tooth of Fortune - 90-day limited period | C | lrhand | 1950 | 169 | 83 | 350 |
| 20135 | Saber Tooth (Event) - 4-hour limited period | C | lrhand | 650 | 169 | 83 | 350 |
| 9308 | Innominate Victory | B | lrhand | 1930 | 190 | 91 | 350 |
| 9309 | Innominate Victory - Health | B | lrhand | 1930 | 190 | 91 | 350 |
| 9310 | Innominate Victory - Critical Damage | B | lrhand | 1930 | 190 | 91 | 350 |
| 9311 | Innominate Victory - Focus | B | lrhand | 1930 | 190 | 91 | 350 |
| 9320 | Dismantler | B | lrhand | 1930 | 210 | 99 | 350 |
| 9321 | Dismantler - Critical Drain | B | lrhand | 1930 | 210 | 99 | 350 |
| 9322 | Dismantler - Health | B | lrhand | 1930 | 210 | 99 | 350 |
| 9323 | Dismantler - Critical Bleed | B | lrhand | 1930 | 210 | 99 | 350 |
| 9847 | Shadow Item: Innominate Victory | B | lrhand | 643 | 190 | 91 | 350 |
| 10882 | Innominate Victory - Lightning | B | lrhand | 1930 | 190 | 91 | 350 |
| 10883 | Innominate Victory - Lightning - Health | B | lrhand | 1930 | 190 | 91 | 350 |
| 10884 | Innominate Victory - Lightning - Critical Damage | B | lrhand | 1930 | 190 | 91 | 350 |
| 10885 | Innominate Victory - Lightning - Focus | B | lrhand | 1930 | 190 | 91 | 350 |
| 10963 | Dismantler - Great Gale | B | lrhand | 1930 | 210 | 99 | 350 |
| 10964 | Dismantler - Great Gale - Critical Drain | B | lrhand | 1930 | 210 | 99 | 350 |
| 10965 | Dismantler - Great Gale - Health | B | lrhand | 1930 | 210 | 99 | 350 |
| 10966 | Dismantler - Great Gale - Critical Bleed | B | lrhand | 1930 | 210 | 99 | 350 |
| 11895 | Common Item - Innominate Victory | B | lrhand | 643 | 190 | 91 | 350 |
| 11931 | Common Item - Dismantler | B | lrhand | 643 | 210 | 99 | 350 |
| 13208 | Player Commendation - Dismantler - Player Commendation Weapon | B | lrhand | 1930 | 210 | 99 | 350 |
| 15069 | Dismantler of Fortune - 30-day limited period | B | lrhand | 1930 | 210 | 99 | 350 |
| 15183 | Dismantler of Fortune - 10-day limited period | B | lrhand | 1930 | 210 | 99 | 350 |
| 16957 | Dismantler of Fortune - 90-day limited period | B | lrhand | 1930 | 210 | 99 | 350 |
| 20149 | Dismantler (Event) - 4-hour limited period | B | lrhand | 643 | 210 | 99 | 350 |
| 9332 | Divine Pain | A | lrhand | 1900 | 231 | 107 | 350 |
| 9333 | Divine Pain - Haste | A | lrhand | 1900 | 231 | 107 | 350 |
| 9334 | Divine Pain - Critical Damage | A | lrhand | 1900 | 231 | 107 | 350 |
| 9335 | Divine Pain - Focus | A | lrhand | 1900 | 231 | 107 | 350 |
| 9344 | Undertaker | A | lrhand | 1840 | 251 | 114 | 350 |
| 9345 | Undertaker - Health | A | lrhand | 1840 | 251 | 114 | 350 |
| 9346 | Undertaker - Critical Bleed | A | lrhand | 1840 | 251 | 114 | 350 |
| 9347 | Undertaker - Critical Drain | A | lrhand | 1840 | 251 | 114 | 350 |
| 9356 | Durendal | A | lrhand | 1820 | 272 | 121 | 350 |
| 9357 | Durendal - Focus | A | lrhand | 1820 | 272 | 121 | 350 |
| 9358 | Durendal - Haste | A | lrhand | 1820 | 272 | 121 | 350 |
| 9359 | Durendal - Health | A | lrhand | 1820 | 272 | 121 | 350 |
| 10703 | Durendal {PvP} - Focus | A | lrhand | 1820 | 272 | 121 | 350 |
| 10704 | Durendal {PvP} - Haste | A | lrhand | 1820 | 272 | 121 | 350 |
| 10705 | Durendal {PvP} - Health | A | lrhand | 1820 | 272 | 121 | 350 |
| 11066 | Divine Pain - Concentration | A | lrhand | 1900 | 231 | 107 | 350 |
| 11067 | Divine Pain - Concentration - Haste | A | lrhand | 1900 | 231 | 107 | 350 |
| 11068 | Divine Pain - Concentration - Critical Damage | A | lrhand | 1900 | 231 | 107 | 350 |
| 11069 | Divine Pain - Concentration - Focus | A | lrhand | 1900 | 231 | 107 | 350 |
| 11084 | Undertaker - Evil Spirit | A | lrhand | 1840 | 251 | 114 | 350 |
| 11085 | Undertaker - Evil Spirit - Health | A | lrhand | 1840 | 251 | 114 | 350 |
| 11086 | Undertaker - Evil Spirit - Critical Bleed | A | lrhand | 1840 | 251 | 114 | 350 |
| 11087 | Undertaker - Evil Spirit - Critical Drain | A | lrhand | 1840 | 251 | 114 | 350 |
| 11153 | Bultgang - Earth | A | lrhand | 1820 | 272 | 121 | 350 |
| 11154 | Bultgang - Earth - Focus | A | lrhand | 1820 | 272 | 121 | 350 |
| 11155 | Bultgang - Earth - Haste | A | lrhand | 1820 | 272 | 121 | 350 |
| 11156 | Bultgang - Earth - Health | A | lrhand | 1820 | 272 | 121 | 350 |
| 11959 | Common Item - Divine Pain | A | lrhand | 633 | 231 | 107 | 350 |
| 11965 | Common Item - Undertaker | A | lrhand | 613 | 251 | 114 | 350 |
| 11982 | Common Item - Durendal | A | lrhand | 607 | 272 | 121 | 350 |
| 12867 | Durendal - Earth {PvP} - Focus | A | lrhand | 1820 | 272 | 121 | 350 |
| 12868 | Durendal - Earth {PvP} - Haste | A | lrhand | 1820 | 272 | 121 | 350 |
| 12869 | Durendal - Earth {PvP} - Health | A | lrhand | 1820 | 272 | 121 | 350 |
| 13223 | Player Commendation - Durendal - Player Commendation Weapon | A | lrhand | 1820 | 272 | 121 | 350 |
| 15068 | Durendal of Fortune - 30-day limited period | A | lrhand | 1820 | 272 | 121 | 350 |
| 15182 | Durendal of Fortune - 10-day limited period | A | lrhand | 1820 | 272 | 121 | 350 |
| 16956 | Durendal of Fortune - 90-day limited period | A | lrhand | 1820 | 272 | 121 | 350 |
| 20163 | Undertaker (Event) - 4-hour limited period | A | lrhand | 613 | 251 | 114 | 350 |
| 9368 | Gram | S | lrhand | 1800 | 304 | 132 | 350 |
| 9369 | Gram - Haste | S | lrhand | 1800 | 304 | 132 | 350 |
| 9370 | Gram - Health | S | lrhand | 1800 | 304 | 132 | 350 |
| 9371 | Gram - Focus | S | lrhand | 1800 | 304 | 132 | 350 |
| 9380 | Dynasty Ancient Sword | S | lrhand | 1800 | 361 | 151 | 350 |
| 9381 | Dynasty Ancient Sword - Focus | S | lrhand | 1800 | 361 | 151 | 350 |
| 9382 | Dynasty Ancient Sword - Health | S | lrhand | 1800 | 361 | 151 | 350 |
| 9383 | Dynasty Ancient Sword - Light | S | lrhand | 1800 | 361 | 151 | 350 |
| 9389 | Infinity Sword | S | lrhand | 1800 | 568 | 230 | 350 |
| 10743 | Gram {PvP} - Haste | S | lrhand | 1800 | 304 | 132 | 350 |
| 10744 | Gram {PvP} - Health | S | lrhand | 1800 | 304 | 132 | 350 |
| 10745 | Gram {PvP} - Focus | S | lrhand | 1800 | 304 | 132 | 350 |
| 10786 | Dynasty Ancient Sword {PvP} - Focus | S | lrhand | 1800 | 361 | 151 | 350 |
| 10787 | Dynasty Ancient Sword {PvP} - Health | S | lrhand | 1800 | 361 | 151 | 350 |
| 10788 | Dynasty Ancient Sword {PvP} - Light | S | lrhand | 1800 | 361 | 151 | 350 |
| 11190 | Gram - Thunder | S | lrhand | 1800 | 304 | 132 | 350 |
| 11191 | Gram - Thunder - Haste | S | lrhand | 1800 | 304 | 132 | 350 |
| 11192 | Gram - Thunder - Health | S | lrhand | 1800 | 304 | 132 | 350 |
| 11193 | Gram - Thunder - Focus | S | lrhand | 1800 | 304 | 132 | 350 |
| 11243 | Dynasty Ancient Sword - Great Gale | S | lrhand | 1800 | 361 | 151 | 350 |
| 11244 | Dynasty Ancient Sword - Great Gale - Focus | S | lrhand | 1800 | 361 | 151 | 350 |
| 11245 | Dynasty Ancient Sword - Great Gale - Health | S | lrhand | 1800 | 361 | 151 | 350 |
| 11246 | Dynasty Ancient Sword - Great Gale - Light | S | lrhand | 1800 | 361 | 151 | 350 |
| 11992 | Common Item - Gram | S | lrhand | 600 | 304 | 132 | 350 |
| 12895 | Gram - Thunder {PvP} - Haste | S | lrhand | 1800 | 304 | 132 | 350 |
| 12896 | Gram - Thunder {PvP} - Health | S | lrhand | 1800 | 304 | 132 | 350 |
| 12897 | Gram - Thunder {PvP} - Focus | S | lrhand | 1800 | 304 | 132 | 350 |
| 12935 | Dynasty Ancient Sword - Great Gale {PvP} - Focus | S | lrhand | 1800 | 361 | 151 | 350 |
| 12936 | Dynasty Ancient Sword - Great Gale {PvP} - Health | S | lrhand | 1800 | 361 | 151 | 350 |
| 12937 | Dynasty Ancient Sword - Great Gale {PvP} - Light | S | lrhand | 1800 | 361 | 151 | 350 |
| 14578 | Slicer of Val Turner Family | S | lrhand | 1350 | 334 | 119 | 350 |
| 14580 | Slicer of Esthus Family | S | lrhand | 1350 | 334 | 119 | 350 |
| 15324 | Player Commendation - Gram - Player Recommendation Weapon | S | lrhand | 1800 | 304 | 132 | 350 |
| 20177 | Gram (Event) - 4-hour limited period | S | lrhand | 600 | 304 | 132 | 350 |
| 21830 | Gram of Fortune - 90-day limited period | S | lrhand | 1800 | 304 | 132 | 350 |
| 21842 | Dynasty Ancient Sword of Fortune - 90-day limited period | S | lrhand | 1800 | 361 | 151 | 350 |
| 10225 | Icarus Wingblade | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 10464 | Icarus Wingblade - Focus | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 10465 | Icarus Wingblade - Health | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 10466 | Icarus Wingblade - Light | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 11325 | Icarus Wingblade - Lightning | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 11326 | Icarus Wingblade - Lightning - Focus | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 11327 | Icarus Wingblade - Lightning - Health | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 11328 | Icarus Wingblade - Lightning - Light | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 14373 | Icarus Wingblade {PvP} | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 14406 | Icarus Wingblade {PvP} - Focus | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 14407 | Icarus Wingblade {PvP} - Health | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 14408 | Icarus Wingblade {PvP} - Light | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 14437 | Icarus Wingblade - Lightning {PvP} | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 14438 | Icarus Wingblade - Lightning {PvP} - Focus | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 14439 | Icarus Wingblade - Lightning {PvP} - Health | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 14440 | Icarus Wingblade - Lightning {PvP} - Light | S80 | lrhand | 1800 | 393 | 163 | 350 |
| 13470 | Vesper Nagan | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 14157 | Vesper Nagan - Haste | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 14158 | Vesper Nagan - Health | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 14159 | Vesper Nagan - Focus | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 14476 | Vesper Nagan {PvP} | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 14517 | Vesper Nagan {PvP} - Haste | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 14518 | Vesper Nagan {PvP} - Health | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 14519 | Vesper Nagan {PvP} - Focus | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 15556 | Pyseal Blade | S84 | lrhand | 1800 | 473 | 192 | 350 |
| 15570 | Finale Blade | S84 | lrhand | 1800 | 449 | 183 | 350 |
| 15688 | Triumph Ancientsword | S84 | lrhand | 1800 | 429 | 183 | 350 |
| 15865 | Finale Blade - Health | S84 | lrhand | 1800 | 449 | 183 | 350 |
| 15866 | Finale Blade - Focus | S84 | lrhand | 1800 | 449 | 183 | 350 |
| 15867 | Finale Blade - Haste | S84 | lrhand | 1800 | 449 | 183 | 350 |
| 15907 | Pyseal Blade - Focus | S84 | lrhand | 1800 | 473 | 192 | 350 |
| 15908 | Pyseal Blade - Haste | S84 | lrhand | 1800 | 473 | 192 | 350 |
| 15909 | Pyseal Blade - Health | S84 | lrhand | 1800 | 473 | 192 | 350 |
| 15925 | Pyseal Blade {PvP} | S84 | lrhand | 1800 | 473 | 192 | 350 |
| 15939 | Finale Blade {PvP} | S84 | lrhand | 1800 | 449 | 183 | 350 |
| 15977 | Finale Blade {PvP} - Health | S84 | lrhand | 1800 | 449 | 183 | 350 |
| 15978 | Finale Blade {PvP} - Focus | S84 | lrhand | 1800 | 449 | 183 | 350 |
| 15979 | Finale Blade {PvP} - Haste | S84 | lrhand | 1800 | 449 | 183 | 350 |
| 16019 | Pyseal Blade {PvP} - Focus | S84 | lrhand | 1800 | 473 | 192 | 350 |
| 16020 | Pyseal Blade {PvP} - Haste | S84 | lrhand | 1800 | 473 | 192 | 350 |
| 16021 | Pyseal Blade {PvP} - Health | S84 | lrhand | 1800 | 473 | 192 | 350 |
| 16055 | Vesper Nagan - Gale | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 16095 | Vesper Nagan - Gale - Haste | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 16096 | Vesper Nagan - Gale - Health | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 16097 | Vesper Nagan - Gale - Focus | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 16147 | Vesper Nagan - Gale {PvP} | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 16218 | Vesper Nagan - Gale {PvP} - Haste | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 16219 | Vesper Nagan - Gale {PvP} - Health | S84 | lrhand | 1800 | 429 | 176 | 350 |
| 16220 | Vesper Nagan - Gale {PvP} - Focus | S84 | lrhand | 1800 | 429 | 176 | 350 |

### FISHINGROD (7)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 6529 | Baby Duck Rod | NONE | lrhand | 1000 | 1 | 1 | 325 |
| 7560 | Monster Only (Fishing Rod) | NONE | lrhand | 1000 | 1 | 1 | 325 |
| 6530 | Albatross Rod | D | lrhand | 1000 | 1 | 1 | 325 |
| 6531 | Pelican Rod | C | lrhand | 1000 | 1 | 1 | 325 |
| 6532 | KingFisher Rod | B | lrhand | 1000 | 1 | 1 | 325 |
| 6533 | Cygnus Pole | A | lrhand | 1000 | 1 | 1 | 325 |
| 6534 | Triton Pole | S | lrhand | 1000 | 1 | 1 | 325 |

### ETC (60)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 99 | Apprentice's Spellbook | NONE | rhand | 650 | 9 | 12 | 379 |
| 100 | Voodoo Doll | NONE | rhand | 630 | 25 | 28 | 379 |
| 308 | Buffalo's Horn | NONE | rhand | 660 | 6 | 8 | 379 |
| 309 | Tears of Eva | NONE | rhand | 630 | 19 | 22 | 379 |
| 310 | Relic of the Saints | NONE | rhand | 610 | 19 | 22 | 379 |
| 311 | Crucifix of Blessing | NONE | rhand | 620 | 25 | 28 | 379 |
| 8975 | Shadow Item: Voodoo Doll | NONE | rhand | 210 | 25 | 28 | 379 |
| 8981 | Shadow Item: Crucifix of Blessing | NONE | rhand | 207 | 25 | 28 | 379 |
| 13156 | Player Commendation - Voodoo Doll - Player Commendation Weapon | NONE | rhand | 630 | 25 | 28 | 379 |
| 13162 | Player Commendation - Crucifix of Blessing - Player Commendation Weapon | NONE | rhand | 620 | 25 | 28 | 379 |
| 21163 | Wedding Bouquet | NONE | rhand | 1600 | 1 | 1 | 379 |
| 101 | Scroll of Wisdom | D | rhand | 610 | 32 | 35 | 379 |
| 312 | Branch of Life | D | rhand | 620 | 32 | 35 | 379 |
| 313 | Temptation of Abyss | D | rhand | 610 | 32 | 35 | 379 |
| 314 | Proof of Revenge | D | rhand | 600 | 32 | 35 | 379 |
| 315 | Divine Tome | D | rhand | 570 | 41 | 43 | 379 |
| 316 | Sage's Blood | D | rhand | 580 | 51 | 52 | 379 |
| 317 | Tome of Blood | D | rhand | 570 | 51 | 52 | 379 |
| 318 | Crucifix of Blood | D | rhand | 540 | 63 | 63 | 379 |
| 319 | Eye of Infinity | D | rhand | 1600 | 63 | 63 | 379 |
| 320 | Blue Crystal Skull | D | rhand | 1600 | 67 | 66 | 379 |
| 321 | Demon Fangs | D | rhand | 1600 | 67 | 66 | 379 |
| 322 | Vajra Wands | D | rhand | 1600 | 74 | 72 | 379 |
| 323 | Ancient Reagent | D | rhand | 1600 | 74 | 72 | 379 |
| 7827 | Traveler's Wand | D | rhand | 570 | 41 | 43 | 379 |
| 8587 | Divine Tomb (Event) | D | rhand | 570 | 41 | 43 | 379 |
| 11609 | Common Item - Proof of Revenge | D | rhand | 200 | 32 | 35 | 379 |
| 11612 | Common Item - Branch of Life | D | rhand | 207 | 32 | 35 | 379 |
| 11616 | Common Item - Temptation of Abyss | D | rhand | 203 | 32 | 35 | 379 |
| 11619 | Common Item - Scroll of Wisdom | D | rhand | 203 | 32 | 35 | 379 |
| 11637 | Common Item - Divine Tome | D | rhand | 190 | 41 | 43 | 379 |
| 11676 | Common Item - Tome of Blood | D | rhand | 190 | 51 | 52 | 379 |
| 11678 | Common Item - Sage's Blood | D | rhand | 193 | 51 | 52 | 379 |
| 11709 | Common Item - Crucifix of Blood | D | rhand | 180 | 63 | 63 | 379 |
| 11715 | Common Item - Demon Fangs | D | rhand | 533 | 67 | 66 | 379 |
| 324 | Tears of Fairy | C | rhand | 1600 | 98 | 91 | 379 |
| 325 | Horn of Glory | C | rhand | 540 | 98 | 91 | 379 |
| 326 | Heathen's Book | C | rhand | 560 | 111 | 101 | 379 |
| 327 | Hex Doll | C | rhand | 1600 | 111 | 101 | 379 |
| 328 | Candle of Wisdom | C | rhand | 1600 | 125 | 111 | 379 |
| 329 | Blessed Branch | C | rhand | 800 | 125 | 111 | 379 |
| 330 | Phoenix Feather | C | rhand | 800 | 125 | 111 | 379 |
| 331 | Cerberus Eye | C | rhand | 1600 | 125 | 111 | 379 |
| 332 | Scroll of Destruction | C | rhand | 1600 | 125 | 111 | 379 |
| 333 | Claws of Black Dragon | C | rhand | 1600 | 125 | 111 | 379 |
| 334 | Three Eyed Crow's Feather | C | rhand | 1600 | 125 | 111 | 379 |
| 11792 | Common Item - Horn of Glory | C | rhand | 180 | 98 | 91 | 379 |
| 11817 | Common Item - Heathen's Book | C | rhand | 187 | 111 | 101 | 379 |
| 335 | Soul Crystal | B | rhand | 1600 | 155 | 132 | 379 |
| 336 | Scroll of Mana | B | rhand | 1600 | 170 | 143 | 379 |
| 337 | Scroll of Massacre | B | rhand | 1600 | 170 | 143 | 379 |
| 338 | Wyvern's Skull | B | rhand | 4800 | 170 | 143 | 379 |
| 339 | Blood Crystal | B | rhand | 1600 | 170 | 143 | 379 |
| 340 | Unicorn's Horn | B | rhand | 1600 | 170 | 143 | 379 |
| 341 | Forgotten Tome | A | rhand | 1600 | 186 | 152 | 379 |
| 342 | Enchanted Flute | A | rhand | 1600 | 186 | 152 | 379 |
| 343 | Headless Arrow | A | rhand | 1600 | 186 | 152 | 379 |
| 344 | Proof of Overlord | A | rhand | 1600 | 186 | 152 | 379 |
| 345 | Deathbringer Sword | A | rhand | 4800 | 186 | 152 | 379 |
| 346 | Tears of Fallen Angel | S | rhand | 1600 | 201 | 162 | 379 |

### FLAG (10)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 9819 | Combat flag | NONE | lrhand | 500 |  |  | 325 |
| 13530 | Flag of Gludio | NONE | lrhand | 500 |  |  | 325 |
| 13531 | Flag of Dion | NONE | lrhand | 500 |  |  | 325 |
| 13532 | Flag of Giran | NONE | lrhand | 500 |  |  | 325 |
| 13533 | Flag of Oren | NONE | lrhand | 500 |  |  | 325 |
| 13534 | Flag of Aden | NONE | lrhand | 500 |  |  | 325 |
| 13535 | Flag of Innadril | NONE | lrhand | 500 |  |  | 325 |
| 13536 | Goddard Flag | NONE | lrhand | 500 |  |  | 325 |
| 13537 | Flag of Rune | NONE | lrhand | 500 |  |  | 325 |
| 13538 | Flag of Schuttgart | NONE | lrhand | 500 |  |  | 325 |

### OWNTHING (9)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 13560 | Gludio Ward | NONE | lrhand | 500 |  |  | 325 |
| 13561 | Dion Ward | NONE | lrhand | 500 |  |  | 325 |
| 13562 | Giran Ward | NONE | lrhand | 500 |  |  | 325 |
| 13563 | Oren Ward | NONE | lrhand | 500 |  |  | 325 |
| 13564 | Aden Ward | NONE | lrhand | 500 |  |  | 325 |
| 13565 | Innadril Ward | NONE | lrhand | 500 |  |  | 325 |
| 13566 | Goddard Ward | NONE | lrhand | 500 |  |  | 325 |
| 13567 | Rune Ward | NONE | lrhand | 500 |  |  | 325 |
| 13568 | Schuttgart Ward | NONE | lrhand | 500 |  |  | 325 |

### NONE (5)

| Id | Name | Grade | Body | Weight | pAtk | mAtk | Atk.Spd |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 6721 | Monster Only(Shield of Imperial Warlord Zombie) | NONE | lhand | 1430 |  |  |  |
| 6917 | Monster Only (Poison Sting) | NONE | rhand | 6 |  |  |  |
| 6918 | Monster Only (Shield of Silenos) | NONE | lhand | 1380 |  |  |  |
| 6919 | Monster Only (Shield of Ketra Orc) | NONE | lhand | 1320 |  |  |  |
| 10548 | Monster Only (Transparent Shield) | NONE | lhand | 1430 |  |  |  |

## Armor (1961)

Grouped by body slot and split by `armor_type`. Kamael cannot equip `HEAVY` or `MAGIC`; non-Kamael cannot equip Kamael-exclusive templates — this is enforced server-side in `UseItem`.

### Chest — `bodypart=chest` (419)

#### HEAVY (115)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 25 | Piece Bone Breastplate | NONE | 8970 |  |  |
| 26 | Bronze Breastplate | NONE | 8920 |  |  |
| 1308 | Compound Scale Mail | NONE | 1400 |  |  |
| 1309 | Mithril Breastplate | NONE | 1000 |  |  |
| 4224 | Dream Armor | NONE | 8920 |  |  |
| 4228 | Ubiquitous Armor | NONE | 8920 |  |  |
| 9030 | Shadow Item: Bronze Breastplate | NONE | 2973 |  |  |
| 58 | Mithril Breastplate | D | 8670 |  |  |
| 347 | Ring Mail Breastplate | D | 8820 |  |  |
| 348 | Scale Mail | D | 8720 |  |  |
| 349 | Compound Scale Mail | D | 8620 |  |  |
| 350 | Dwarven Scale Mail | D | 8540 |  |  |
| 351 | Blast Plate | D | 8420 |  |  |
| 352 | Brigandine Tunic | D | 8320 |  |  |
| 353 | Half Plate Armor | D | 8220 |  |  |
| 9040 | Shadow Item: Mithril Breastplate | D | 2890 |  |  |
| 10019 | Ring Mail Breastplate | D | 8820 |  |  |
| 12008 | Common Item - Ring Mail Breastplate | D | 2940 |  |  |
| 12024 | Common Item - Scale Mail | D | 2907 |  |  |
| 12030 | Common Item - Dwarven Scale Mail | D | 2847 |  |  |
| 12031 | Common Item - Mithril Breastplate | D | 2890 |  |  |
| 12032 | Common Item - Compound Scale Mail | D | 2873 |  |  |
| 12044 | Common Item - Blast Plate | D | 2807 |  |  |
| 12059 | Common Item - Brigandine | D | 2773 |  |  |
| 12081 | Common Item - Half Plate Armor | D | 2740 |  |  |
| 15021 | Brigandine of Fortune - 30-day limited period | D | 8320 |  |  |
| 15135 | Brigandine of Fortune - 10-day limited period | D | 8320 |  |  |
| 16909 | Brigandine of Fortune - 90-day limited period | D | 8320 |  |  |
| 20647 | Common Item - Half Plate Armor | D | 100 |  |  |
| 354 | Chain Mail Shirt | C | 8120 |  |  |
| 355 | Dwarven Chain Mail Shirt | C | 8070 |  |  |
| 12095 | Common Item - Chain Mail Shirt | C | 2707 |  |  |
| 12110 | Common Item - Dwarven Chain Mail Shirt | C | 2690 |  |  |
| 357 | Zubei's Breastplate | B | 7970 |  |  |
| 358 | Blue Wolf Breastplate | B | 7820 |  |  |
| 360 | Armor of Victory | B | 3360 |  |  |
| 361 | Breastplate of Valor | B | 3360 |  |  |
| 364 | Elven Crystal Breastplate | B | 2400 |  |  |
| 2376 | Avadon Breastplate | B | 7920 |  |  |
| 9067 | Shadow Item: Zubei's Breastplate | B | 2657 |  |  |
| 11364 | Zubei's Breastplate | B | 7970 |  |  |
| 11376 | Avadon Breastplate | B | 7920 |  |  |
| 11405 | Blue Wolf Breastplate | B | 7820 |  |  |
| 12161 | Common Item - Zubei's Breastplate | B | 2657 |  |  |
| 12173 | Common Item - Avadon Breastplate | B | 2640 |  |  |
| 12204 | Common Item - Blue Wolf Breastplate | B | 2607 |  |  |
| 365 | Dark Crystal Breastplate | A | 7700 |  |  |
| 5287 | Sealed Dark Crystal breastplate | A | 7700 |  |  |
| 9081 | Shadow Item: Dark Crystal Breastplate | A | 2567 |  |  |
| 11418 | Dark Crystal Breastplate | A | 7700 |  |  |
| 11427 | Sealed Dark Crystal breastplate | A | 7700 |  |  |
| 12217 | Common Item - Dark Crystal Breastplate | A | 2567 |  |  |
| 12227 | Common Item - Sealed Dark Crystal Breastplate | A | 2567 |  |  |
| 375 | Dragon Scale Mail | S | 7620 |  |  |
| 6373 | Imperial Crusader Breastplate | S | 7620 |  |  |
| 6674 | Sealed Imperial Crusader Breastplate | S | 7620 |  |  |
| 9416 | Dynasty Breast Plate | S | 7570 |  |  |
| 9417 | Dynasty Breast Plate - Shield Master | S | 7570 |  |  |
| 9418 | Dynasty Breast Plate - Weapon Master | S | 7570 |  |  |
| 9419 | Dynasty Breast Plate - Force Master | S | 7570 |  |  |
| 9420 | Dynasty Breast Plate - Bard | S | 7570 |  |  |
| 9514 | Sealed Dynasty Breast Plate | S | 7570 |  |  |
| 10227 | Dynasty Platinum Plate | S | 7570 |  |  |
| 10228 | Dynasty Platinum Plate - Shield Master | S | 7570 |  |  |
| 10229 | Dynasty Platinum Plate - Weapon Master | S | 7570 |  |  |
| 10230 | Dynasty Platinum Plate - Force Master | S | 7570 |  |  |
| 10231 | Dynasty Platinum Plate - Bard | S | 7570 |  |  |
| 10799 | Imperial Crusader Breastplate {PvP} | S | 7620 |  |  |
| 10802 | Dynasty Breastplate {PvP} | S | 7570 |  |  |
| 10803 | Dynasty Breastplate {PvP} - Shield Master | S | 7570 |  |  |
| 10804 | Dynasty Breastplate {PvP} - Weapon Master | S | 7570 |  |  |
| 10805 | Dynasty Breastplate {PvP} - Force Master | S | 7570 |  |  |
| 10806 | Dynasty Breastplate {PvP} - Bard | S | 7570 |  |  |
| 10819 | Dynasty Platinum Breastplate {PvP} | S | 7570 |  |  |
| 10820 | Dynasty Platinum Breastplate {PvP} - Shield Master | S | 7570 |  |  |
| 10821 | Dynasty Platinum Breastplate {PvP} - Weapon Master | S | 7570 |  |  |
| 10822 | Dynasty Platinum Breastplate {PvP} - Force Master | S | 7570 |  |  |
| 10823 | Dynasty Platinum Breastplate {PvP} - Bard | S | 7570 |  |  |
| 11504 | Sealed Imperial Crusader Breastplate | S | 7620 |  |  |
| 11510 | Imperial Crusader Breastplate | S | 7620 |  |  |
| 11527 | Dynasty Breastplate | S | 7570 |  |  |
| 11528 | Dynasty Breastplate | S | 7570 |  |  |
| 11529 | Dynasty Breastplate | S | 7570 |  |  |
| 11530 | Dynasty Breastplate | S | 7570 |  |  |
| 11531 | Dynasty Breastplate | S | 7570 |  |  |
| 11552 | Dynasty Platinum Plate | S | 7570 |  |  |
| 11553 | Dynasty Platinum Plate | S | 7570 |  |  |
| 11554 | Dynasty Platinum Plate | S | 7570 |  |  |
| 11555 | Dynasty Platinum Plate | S | 7570 |  |  |
| 11556 | Dynasty Platinum Plate | S | 7570 |  |  |
| 11568 | Sealed Dynasty Breastplate | S | 7570 |  |  |
| 12304 | Common Item - Sealed Imperial Crusader Breastplate | S | 2540 |  |  |
| 12310 | Common Item - Imperial Crusader Breastplate | S | 2540 |  |  |
| 21775 | Imperial Crusader Breastplate of Fortune - 90-day limited period | S | 7620 |  |  |
| 21793 | Dynasty Breastplate of Fortune - 90-day limited period | S | 7570 |  |  |
| 15609 | Moirai Breastplate | S80 | 7520 |  |  |
| 15697 | Sealed Moirai Breastplate | S80 | 7520 |  |  |
| 16174 | Moirai Breastplate {PvP} | S80 | 7520 |  |  |
| 16292 | Moirai Breastplate | S80 | 7520 |  |  |
| 16326 | Sealed Moirai Breastplate | S80 | 7520 |  |  |
| 13432 | Vesper Breastplate | S84 | 7520 |  |  |
| 13435 | Vesper Noble Breastplate | S84 | 7520 |  |  |
| 14105 | Sealed Vesper Breastplate | S84 | 7520 |  |  |
| 14520 | Vesper Breastplate {PvP} | S84 | 7520 |  |  |
| 14523 | Vesper Noble Breastplate {PvP} | S84 | 7520 |  |  |
| 15575 | Elegia Breastplate | S84 | 7520 |  |  |
| 15592 | Vorpal Breastplate | S84 | 7520 |  |  |
| 15729 | Sealed Elegia Breastplate | S84 | 7520 |  |  |
| 15746 | Sealed Vorpal Breastplate | S84 | 7520 |  |  |
| 16168 | Elegia Breastplate {PvP} | S84 | 7520 |  |  |
| 16171 | Vorpal Breastplate {PvP} | S84 | 7520 |  |  |
| 16309 | Vesper Breastplate | S84 | 7520 |  |  |
| 16343 | Sealed Vesper Breastplate | S84 | 7520 |  |  |
| 16840 | Vesper Noble Breastplate | S84 | 7520 |  |  |
| 17006 | Sealed Vesper Noble Breastplate | S84 | 7520 |  |  |

#### LIGHT (185)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 21 | Shirt | NONE | 4830 |  |  |
| 22 | Leather Shirt | NONE | 4830 |  |  |
| 23 | Wooden Breastplate | NONE | 4820 |  |  |
| 24 | Bone Breastplate | NONE | 4770 |  |  |
| 27 | Hard Leather Shirt | NONE | 4720 |  |  |
| 390 | Cotton Shirt | NONE | 4770 |  |  |
| 485 | Tattoo of Power | NONE | 4200 |  |  |
| 1146 | Squire's Shirt | NONE | 3301 |  |  |
| 1311 | Puma Skin Shirt | NONE | 300 |  |  |
| 2506 | Wolf's Leather Armor | NONE | 160 |  |  |
| 3891 | Wolf's Hide Armor | NONE | 160 |  |  |
| 3892 | Wolf's Hard Leather Armor | NONE | 160 |  |  |
| 3893 | Wolf's Wooden Armor | NONE | 160 |  |  |
| 3894 | Wolf's Ring Mail | NONE | 160 |  |  |
| 3895 | Wolf's Bone Armor | NONE | 160 |  |  |
| 3896 | Wolf's Scale Mail | NONE | 160 |  |  |
| 3897 | Wolf's Bronze Armor | NONE | 160 |  |  |
| 3898 | Wolf's Plate Mail | NONE | 160 |  |  |
| 3899 | Wolf's Steel Armor | NONE | 160 |  |  |
| 3900 | Wolf's Luxury Plate | NONE | 160 |  |  |
| 3901 | Wolf's Mithril Armor | NONE | 160 |  |  |
| 3912 | Hatchling's Soft Leather | NONE | 160 |  |  |
| 3913 | Hatchling's Scale Mail | NONE | 160 |  |  |
| 3914 | Hatchling's Brigandine | NONE | 160 |  |  |
| 3915 | Hatchling's Bronze Coat | NONE | 160 |  |  |
| 3916 | Hatchling's Steel Coat | NONE | 160 |  |  |
| 3917 | Hatchling's Shadowplate | NONE | 160 |  |  |
| 3918 | Hatchling's Mithril Coat | NONE | 160 |  |  |
| 4234 | Hatchling's Level 65 Armor | NONE | 160 |  |  |
| 4235 | Hatchling's Level 75 Armor | NONE | 160 |  |  |
| 4236 | Gara Item | NONE | 160 |  |  |
| 5170 | Mithril Panzer Coat | NONE | 160 |  |  |
| 5171 | Brigadine Panzer Coat | NONE | 160 |  |  |
| 5172 | Draconic Panzer Coat | NONE | 160 |  |  |
| 5173 | Blood Panzer Coat | NONE | 160 |  |  |
| 5174 | Ophidian Panzer Coat | NONE | 160 |  |  |
| 5175 | Inferno Panzer Coat | NONE | 160 |  |  |
| 5182 | Hatchling's Gorgon Coat | NONE | 160 |  |  |
| 5183 | Hatchling's Ophidian Plate | NONE | 160 |  |  |
| 5184 | Hatchling's Crimson Plate | NONE | 160 |  |  |
| 5185 | Hatchling's Draconic Plate | NONE | 160 |  |  |
| 5186 | Hatchling's Inferno Plate | NONE | 160 |  |  |
| 5216 | Wolf's Level 75 Armor | NONE | 160 |  |  |
| 8541 | Little Harness | NONE | 160 |  |  |
| 9032 | Shadow Item: Hard Leather Shirt | NONE | 1573 |  |  |
| 9662 | Great Wolf Scale Armor | NONE | 160 |  |  |
| 9663 | Great Wolf Bronze Armor | NONE | 160 |  |  |
| 9664 | Great Wolf Plate Armor | NONE | 160 |  |  |
| 9665 | Great Wolf Mithril Armor | NONE | 160 |  |  |
| 9666 | Great Wolf Oriharukon Armor | NONE | 160 |  |  |
| 9667 | Great Wolf Orichalcum Armor | NONE | 160 |  |  |
| 9670 | Native Tunic | NONE | 4720 |  |  |
| 11482 | Great Wolf Oriharukon Armor | NONE | 160 |  |  |
| 11511 | Great Wolf Orichalcum Armor | NONE | 160 |  |  |
| 12740 | Baby Pet Scale Armor | NONE | 160 |  |  |
| 12741 | Baby Pet Bronze Armor | NONE | 160 |  |  |
| 12742 | Baby Pet Plate Armor | NONE | 160 |  |  |
| 12743 | Baby Pet Mithril Armor | NONE | 160 |  |  |
| 12744 | Baby Pet Oriharukon Armor | NONE | 160 |  |  |
| 12745 | Baby Pet Orichalcum Armor | NONE | 160 |  |  |
| 13050 | Tigress exclusive armor | NONE | 160 |  |  |
| 13803 | Native's Tunic | NONE | 4720 |  |  |
| 13806 | Guards of the Dawn Tunic | NONE | 4720 |  |  |
| 391 | Puma Skin Shirt | D | 4700 |  |  |
| 392 | Lion Skin Shirt | D | 4580 |  |  |
| 393 | Mithril Banded Mail | D | 4570 |  |  |
| 394 | Reinforced Leather Shirt | D | 4570 |  |  |
| 395 | Manticore Skin Shirt | D | 4520 |  |  |
| 486 | Tattoo of Fire | D | 4050 |  |  |
| 487 | Tattoo of Resolve | D | 4000 |  |  |
| 492 | Tattoo of Soul | D | 4150 |  |  |
| 9045 | Shadow Item: Reinforced Leather Shirt | D | 1523 |  |  |
| 10021 | Puma Skin Shirt | D | 4700 |  |  |
| 12015 | Common Item - Puma Skin Shirt | D | 1567 |  |  |
| 12021 | Common Item - Lion Skin Shirt | D | 1527 |  |  |
| 12036 | Common Item - Reinforced Leather Shirt | D | 1523 |  |  |
| 12043 | Common Item - Mithril Banded Mail | D | 1523 |  |  |
| 12054 | Common Item - Manticore Skin Shirt | D | 1507 |  |  |
| 15017 | Manticore Skin Shirt of Fortune - 30-day limited period | D | 4520 |  |  |
| 15131 | Manticore Skin Shirt of Fortune - 10-day limited period | D | 4520 |  |  |
| 16905 | Manticore Skin Shirt of Fortune - 90-day limited period | D | 4520 |  |  |
| 397 | Mithril Shirt | C | 4470 |  |  |
| 398 | Plated Leather | C | 4450 |  |  |
| 399 | Rind Leather Armor | C | 4420 |  |  |
| 400 | Theca Leather Armor | C | 4370 |  |  |
| 489 | Tattoo of Bravery | C | 4100 |  |  |
| 9058 | Shadow Item: Theca Leather Armor | C | 1457 |  |  |
| 12086 | Common Item - Reinforced Mithril Shirt | C | 1490 |  |  |
| 12105 | Common Item - Plate Leather Armor | C | 1483 |  |  |
| 12113 | Common Item - Rind Leather Armor | C | 1473 |  |  |
| 12133 | Common Item - Theca Leather Armor | C | 1457 |  |  |
| 15008 | Plate Leather Armor of Fortune - 30-day limited period | C | 4450 |  |  |
| 15122 | Plate Leather Armor of Fortune - 10-day limited period | C | 4450 |  |  |
| 16896 | Plate Leather Armor of Fortune - 90-day limited period | C | 4450 |  |  |
| 404 | Prairie Leather Armor | B | 8000 |  |  |
| 405 | Leather Armor of Underworld | B | 8000 |  |  |
| 408 | Guardian's Leather Armor | B | 8000 |  |  |
| 409 | Marksman's Leather Armor | B | 4300 |  |  |
| 488 | Tattoo of Flame | B | 800 |  |  |
| 493 | Tattoo of Avadon | B | 4000 |  |  |
| 494 | Tattoo of Doom | B | 4100 |  |  |
| 495 | Tattoo of Pledge | B | 4000 |  |  |
| 496 | Tattoo of Divine | B | 4100 |  |  |
| 2384 | Zubei's Leather Shirt | B | 4330 |  |  |
| 9073 | Shadow Item: Zubei's Leather Shirt | B | 1443 |  |  |
| 11354 | Zubei's Leather Shirt | B | 4330 |  |  |
| 12151 | Common Item - Zubei's Leather Shirt | B | 1443 |  |  |
| 490 | Tattoo of Blood | A | 3800 |  |  |
| 491 | Tattoo of Absolute | A | 800 |  |  |
| 2385 | Dark Crystal Leather Armor | A | 4300 |  |  |
| 2410 | Nightmarish Tattoo | A | 3600 |  |  |
| 5297 | Sealed Dark Crystal Leather Armor | A | 4300 |  |  |
| 9087 | Shadow Item: Dark Crystal Leather Armor | A | 1433 |  |  |
| 11411 | Dark Crystal Leather Armor | A | 4300 |  |  |
| 11422 | Sealed Dark Crystal Leather Armor | A | 4300 |  |  |
| 12210 | Common Item - Dark Crystal Leather Armor | A | 1433 |  |  |
| 12222 | Common Item - Sealed Dark Crystal Leather Armor | A | 1433 |  |  |
| 14996 | Dark Crystal Leather Armor of Fortune - 30-day limited period | A | 4300 |  |  |
| 15110 | Dark Crystal Leather Armor of Fortune - 10-day limited period | A | 4300 |  |  |
| 16884 | Dark Crystal Leather Armor of Fortune - 90-day limited period | A | 4300 |  |  |
| 9425 | Dynasty Leather Armor | S | 4180 |  |  |
| 9426 | Dynasty Leather Armor - Dagger Master | S | 4180 |  |  |
| 9427 | Dynasty Leather Armor - Bow Master | S | 4180 |  |  |
| 9519 | Sealed Dynasty Leather Armor | S | 4180 |  |  |
| 10126 | Dynasty Leather Armor - Force Master | S | 4180 |  |  |
| 10127 | Dynasty Leather Armor - Weapon Master | S | 4180 |  |  |
| 10168 | Dynasty Leather Armor - Enchanter | S | 4180 |  |  |
| 10214 | Dynasty Leather Armor - Summoner | S | 4180 |  |  |
| 10232 | Dynasty Jewel Leather Armor | S | 4180 |  |  |
| 10233 | Dynasty Jewel Leather Armor - Dagger Master | S | 4180 |  |  |
| 10234 | Dynasty Jewel Leather Armor - Bow Master | S | 4180 |  |  |
| 10487 | Dynasty Jeweled Leather Armor - Force Master | S | 4180 |  |  |
| 10488 | Dynasty Jeweled Leather Armor - Weapon Master | S | 4180 |  |  |
| 10489 | Dynasty Jeweled Leather Armor - Enchanter | S | 4180 |  |  |
| 10490 | Dynasty Jeweled Leather Armor - Summoner | S | 4180 |  |  |
| 10807 | Dynasty Leather Armor {PvP} | S | 4180 |  |  |
| 10808 | Dynasty Leather Armor {PvP} - Dagger Master | S | 4180 |  |  |
| 10809 | Dynasty Leather Armor {PvP} - Bow Master | S | 4180 |  |  |
| 10815 | Dynasty Leather Armor {PvP} - Force Master | S | 4180 |  |  |
| 10816 | Dynasty Leather Armor {PvP} - Weapon Master | S | 4180 |  |  |
| 10817 | Dynasty Leather Armor {PvP} - Enchanter | S | 4180 |  |  |
| 10818 | Dynasty Leather Armor {PvP} - Summoner | S | 4180 |  |  |
| 10824 | Dynasty Jewel Leather Armor {PvP} | S | 4180 |  |  |
| 10825 | Dynasty Jewel Leather Armor {PvP} - Dagger Master | S | 4180 |  |  |
| 10826 | Dynasty Jewel Leather Armor {PvP} - Bow Master | S | 4180 |  |  |
| 10832 | Dynasty Jewel Leather Armor {PvP} - Force Master | S | 4180 |  |  |
| 10833 | Dynasty Jewel Leather Armor {PvP} - Weapon Master | S | 4180 |  |  |
| 10834 | Dynasty Jewel Leather Armor {PvP} - Enchanter | S | 4180 |  |  |
| 10835 | Dynasty Jewel Leather Armor {PvP} - Summoner | S | 4180 |  |  |
| 11517 | Dynasty Leather Armor | S | 4180 |  |  |
| 11518 | Dynasty Leather Armor | S | 4180 |  |  |
| 11519 | Dynasty Leather Armor | S | 4180 |  |  |
| 11520 | Dynasty Leather Armor | S | 4180 |  |  |
| 11521 | Dynasty Leather Armor | S | 4180 |  |  |
| 11522 | Dynasty Leather Armor | S | 4180 |  |  |
| 11523 | Dynasty Leather Armor | S | 4180 |  |  |
| 11540 | Dynasty Jewel Leather Armor | S | 4180 |  |  |
| 11541 | Dynasty Jewel Leather Armor | S | 4180 |  |  |
| 11542 | Dynasty Jewel Leather Armor | S | 4180 |  |  |
| 11543 | Dynasty Jewel Leather Armor | S | 4180 |  |  |
| 11544 | Dynasty Jewel Leather Armor | S | 4180 |  |  |
| 11545 | Dynasty Jewel Leather Armor | S | 4180 |  |  |
| 11546 | Dynasty Jewel Leather Armor | S | 4180 |  |  |
| 11564 | Sealed Dynasty Leather Armor | S | 4180 |  |  |
| 21800 | Dynasty Leather Armor of Fortune - 90-day limited period | S | 4180 |  |  |
| 15610 | Moirai Leather Breastplate | S80 | 4140 |  |  |
| 15698 | Sealed Moirai Leather Breastplate | S80 | 4140 |  |  |
| 16175 | Moirai Leather Breastplate {PvP} | S80 | 4140 |  |  |
| 16293 | Moirai Leather Breastplate | S80 | 4140 |  |  |
| 16327 | Sealed Moirai Leather Breastplate | S80 | 4140 |  |  |
| 13433 | Vesper Leather Breastplate | S84 | 4140 |  |  |
| 13436 | Vesper Noble Leather Breastplate | S84 | 4140 |  |  |
| 14106 | Sealed Vesper Leather Breastplate | S84 | 4140 |  |  |
| 14521 | Vesper Leather Breastplate {PvP} | S84 | 4140 |  |  |
| 14524 | Vesper Noble Leather Breastplate {PvP} | S84 | 4140 |  |  |
| 15576 | Elegia Leather Breastplate | S84 | 4140 |  |  |
| 15593 | Vorpal Leather Breastplate | S84 | 4140 |  |  |
| 15730 | Sealed Elegia Leather Breastplate | S84 | 4140 |  |  |
| 15747 | Sealed Vorpal Leather Breastplate | S84 | 4140 |  |  |
| 16169 | Elegia Leather Breastplate {PvP} | S84 | 4140 |  |  |
| 16172 | Vorpal Leather Breastplate {PvP} | S84 | 4140 |  |  |
| 16310 | Vesper Leather Breastplate | S84 | 4140 |  |  |
| 16344 | Sealed Vesper Leather Leather Breastplate | S84 | 4140 |  |  |
| 16841 | Vesper Noble Houberk | S84 | 4140 |  |  |
| 17007 | Sealed Vesper Noble Leather Breastplate | S84 | 4140 |  |  |

#### MAGIC (119)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 425 | Apprentice's Tunic | NONE | 2150 |  |  |
| 426 | Tunic | NONE | 2150 |  |  |
| 428 | Feriotic Tunic | NONE | 2140 |  |  |
| 429 | Leather Tunic | NONE | 2110 |  |  |
| 1100 | Cotton Tunic | NONE | 2120 |  |  |
| 1101 | Tunic of Devotion | NONE | 2090 |  |  |
| 1102 | Tunic of Magic | NONE | 2080 |  |  |
| 1310 | Tunic of Magic | NONE | 150 |  |  |
| 1312 | White Tunic | NONE | 150 |  |  |
| 9034 | Shadow Item: Tunic of Magic | NONE | 693 |  |  |
| 432 | Cursed Tunic | D | 2090 |  |  |
| 433 | Elven Tunic | D | 2080 |  |  |
| 434 | White Tunic | D | 2040 |  |  |
| 435 | Mystic's Tunic | D | 2030 |  |  |
| 436 | Tunic of Knowledge | D | 2020 |  |  |
| 437 | Mithril Tunic | D | 2010 |  |  |
| 2396 | Elven Mithril Tunic | D | 720 |  |  |
| 9049 | Shadow Item: Tunic of Knowledge | D | 673 |  |  |
| 10023 | Cursed Tunic | D | 2090 |  |  |
| 12010 | Common Item - Cursed Tunic | D | 697 |  |  |
| 12018 | Common Item - Mystic's Tunic | D | 677 |  |  |
| 12022 | Common Item - White Tunic | D | 680 |  |  |
| 12026 | Common Item - Elven Tunic | D | 693 |  |  |
| 12047 | Common Item - Tunic of Knowledge | D | 673 |  |  |
| 12057 | Common Item - Mithril Tunic | D | 670 |  |  |
| 14992 | Mithril Tunic of Fortune - 30-day limited period | D | 2010 |  |  |
| 15106 | Mithril Tunic of Fortune - 10-day limited period | D | 2010 |  |  |
| 16880 | Mithril Tunic of Fortune - 90-day limited period | D | 2010 |  |  |
| 20650 | Common Item - Mithril Tunic | D | 100 |  |  |
| 439 | Karmian Tunic | C | 1980 |  |  |
| 441 | Demon's Tunic | C | 1990 |  |  |
| 442 | Divine Tunic | C | 1980 |  |  |
| 9062 | Shadow Item: Demon's Tunic | C | 663 |  |  |
| 12099 | Common Item - Karmian Tunic | C | 660 |  |  |
| 12123 | Common Item - Demon's Tunic | C | 663 |  |  |
| 12138 | Common Item - Divine Tunic | C | 660 |  |  |
| 14988 | Karmian Tunic of Fortune - 30-day limited period | C | 1980 |  |  |
| 15102 | Karmian Tunic of Fortune - 10-day limited period | C | 1980 |  |  |
| 16876 | Karmian Tunic of Fortune - 90-day limited period | C | 1980 |  |  |
| 443 | Tunic of Mana | B | 2000 |  |  |
| 445 | Paradia Tunic | B | 1990 |  |  |
| 446 | Inferno Tunic | B | 1880 |  |  |
| 447 | Tunic of Solar Eclipse | B | 1960 |  |  |
| 449 | Tunic of Summoning | B | 1950 |  |  |
| 451 | Elemental Tunic | B | 1970 |  |  |
| 452 | Tunic of Phantom | B | 1890 |  |  |
| 453 | Tunic of Grace | B | 1930 |  |  |
| 455 | Phoenix Tunic | B | 1950 |  |  |
| 456 | Cerberus Tunic | B | 1870 |  |  |
| 457 | Tunic of Aid | B | 1910 |  |  |
| 2397 | Tunic of Zubei | B | 1960 |  |  |
| 2398 | Blue Wolf Tunic | B | 1920 |  |  |
| 2399 | Tunic of Doom | B | 1900 |  |  |
| 9077 | Shadow Item: Tunic of Zubei | B | 653 |  |  |
| 11377 | Tunic of Zubei | B | 1960 |  |  |
| 11393 | Tunic of Doom | B | 1900 |  |  |
| 11402 | Blue Wolf Tunic | B | 1920 |  |  |
| 12175 | Common Item - Tunic of Zubei | B | 653 |  |  |
| 12192 | Common Item - Tunic of Doom | B | 633 |  |  |
| 12201 | Common Item - Blue Wolf Tunic | B | 640 |  |  |
| 2400 | Tallum Tunic | A | 1860 |  |  |
| 5304 | Sealed Tallum Tunic | A | 1860 |  |  |
| 11432 | Sealed Tallum Tunic | A | 1860 |  |  |
| 11444 | Tallum Tunic | A | 1860 |  |  |
| 12232 | Common Item - Sealed Tallum Tunic | A | 620 |  |  |
| 12243 | Common Item - Tallum Tunic | A | 620 |  |  |
| 9432 | Dynasty Tunic | S | 1780 |  |  |
| 9433 | Dynasty Tunic - Healer | S | 1780 |  |  |
| 9434 | Dynasty Tunic - Enchanter | S | 1780 |  |  |
| 9435 | Dynasty Tunic - Summoner | S | 1780 |  |  |
| 9436 | Dynasty Tunic - Wizard | S | 1780 |  |  |
| 9524 | Sealed Dynasty Tunic | S | 1780 |  |  |
| 10235 | Dynasty Silver Satin Tunic | S | 1780 |  |  |
| 10236 | Dynasty Silver Satin Tunic - Healer | S | 1780 |  |  |
| 10237 | Dynasty Silver Satin Tunic - Enchanter | S | 1780 |  |  |
| 10238 | Dynasty Silver Satin Tunic - Summoner | S | 1780 |  |  |
| 10239 | Dynasty Silver Satin Tunic - Wizard | S | 1780 |  |  |
| 10810 | Dynasty Tunic {PvP} | S | 1780 |  |  |
| 10811 | Dynasty Tunic {PvP} - Healer | S | 1780 |  |  |
| 10812 | Dynasty Tunic {PvP} - Enchanter | S | 1780 |  |  |
| 10813 | Dynasty Tunic {PvP} - Summoner | S | 1780 |  |  |
| 10814 | Dynasty Tunic {PvP} - Wizard | S | 1780 |  |  |
| 10827 | Dynasty Silver Satin Tunic {PvP} | S | 1780 |  |  |
| 10828 | Dynasty Silver Satin Tunic {PvP} - Healer | S | 1780 |  |  |
| 10829 | Dynasty Silver Satin Tunic {PvP} - Enchanter | S | 1780 |  |  |
| 10830 | Dynasty Silver Satin Tunic {PvP} - Summoner | S | 1780 |  |  |
| 10831 | Dynasty Silver Satin Tunic {PvP} - Wizard | S | 1780 |  |  |
| 11534 | Dynasty Silver Satin Tunic | S | 1780 |  |  |
| 11535 | Dynasty Silver Satin Tunic | S | 1780 |  |  |
| 11536 | Dynasty Silver Satin Tunic | S | 1780 |  |  |
| 11537 | Dynasty Silver Satin Tunic | S | 1780 |  |  |
| 11538 | Dynasty Silver Satin Tunic | S | 1780 |  |  |
| 11547 | Dynasty Tunic | S | 1780 |  |  |
| 11548 | Dynasty Tunic | S | 1780 |  |  |
| 11549 | Dynasty Tunic | S | 1780 |  |  |
| 11550 | Dynasty Tunic | S | 1780 |  |  |
| 11551 | Dynasty Tunic | S | 1780 |  |  |
| 11572 | Sealed Dynasty Tunic | S | 1780 |  |  |
| 21806 | Dynasty Tunic of Fortune - 90-day limited period | S | 1780 |  |  |
| 15611 | Moirai Tunic | S80 | 1750 |  |  |
| 15699 | Sealed Moirai Tunic | S80 | 1750 |  |  |
| 16176 | Moirai Tunic {PvP} | S80 | 1750 |  |  |
| 16294 | Moirai Tunic | S80 | 1750 |  |  |
| 16328 | Sealed Moirai Tunic | S80 | 1750 |  |  |
| 13434 | Vesper Tunic | S84 | 1750 |  |  |
| 13437 | Vesper Noble Tunic | S84 | 1750 |  |  |
| 14107 | Sealed Vesper Tunic | S84 | 1750 |  |  |
| 14522 | Vesper Tunic {PvP} | S84 | 1750 |  |  |
| 14525 | Vesper Noble Tunic {PvP} | S84 | 1750 |  |  |
| 15577 | Elegia Tunic | S84 | 1750 |  |  |
| 15594 | Vorpal Tunic | S84 | 1750 |  |  |
| 15731 | Sealed Elegia Tunic | S84 | 1750 |  |  |
| 15748 | Sealed Vorpal Tunic | S84 | 1750 |  |  |
| 16170 | Elegia Tunic {PvP} | S84 | 1750 |  |  |
| 16173 | Vorpal Tunic {PvP} | S84 | 1750 |  |  |
| 16311 | Vesper Tunic | S84 | 1750 |  |  |
| 16345 | Sealed Vesper Tunic | S84 | 1750 |  |  |
| 16842 | Vesper Noble Tunic | S84 | 1750 |  |  |
| 17008 | Sealed Vesper Noble Tunic | S84 | 1750 |  |  |

### Legs — `bodypart=legs` (246)

#### HEAVY (82)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 32 | Piece Bone Gaiters | NONE | 4020 |  |  |
| 34 | Bronze Gaiters | NONE | 3960 |  |  |
| 1313 | Compound Scale Gaiters | NONE | 1000 |  |  |
| 1314 | Mithril Gaiters | NONE | 600 |  |  |
| 4225 | Dream Stockings | NONE | 3960 |  |  |
| 4229 | Ubiquitous Stockings | NONE | 3960 |  |  |
| 9031 | Shadow Item: Bronze Gaiters | NONE | 1320 |  |  |
| 59 | Mithril Gaiters | D | 3830 |  |  |
| 376 | Iron Plate Gaiters | D | 3820 |  |  |
| 377 | Scale Gaiters | D | 3860 |  |  |
| 378 | Compound Scale Gaiters | D | 3770 |  |  |
| 379 | Dwarven Scale Gaiters | D | 3840 |  |  |
| 380 | Plate Gaiters | D | 3770 |  |  |
| 2377 | Mithril Scale Gaiters | D | 3870 |  |  |
| 2378 | Brigandine Gaiters | D | 3820 |  |  |
| 9041 | Shadow Item: Mithril Gaiters | D | 1277 |  |  |
| 10020 | Iron Plate Gaiters | D | 3820 |  |  |
| 12012 | Common Item - Iron Plate Gaiters | D | 1273 |  |  |
| 12023 | Common Item - Scale Gaiters | D | 1287 |  |  |
| 12039 | Common Item - Dwarven Scale Gaiters | D | 1280 |  |  |
| 12041 | Common Item - Mithril Gaiters | D | 1277 |  |  |
| 12049 | Common Item - Compound Scale Gaiters | D | 1257 |  |  |
| 12056 | Common Item - Mithril Scale Gaiters | D | 1290 |  |  |
| 12060 | Common Item - Brigandine Gaiters | D | 1273 |  |  |
| 12080 | Common Item - Plate Gaiters | D | 1257 |  |  |
| 15022 | Brigandine Gaiters of Fortune - 30-day limited period | D | 3820 |  |  |
| 15136 | Brigandine Gaiters of Fortune - 10-day limited period | D | 3820 |  |  |
| 16910 | Brigandine Gaiters of Fortune - 90-day limited period | D | 3820 |  |  |
| 20646 | Common Item - Plate Gaiters | D | 100 |  |  |
| 381 | Chain Gaiters | C | 3680 |  |  |
| 382 | Dwarven Chain Gaiters | C | 3620 |  |  |
| 12094 | Common Item - Chain Gaiters | C | 1227 |  |  |
| 12109 | Common Item - Dwarven Chain Gaiters | C | 1207 |  |  |
| 383 | Zubei's Gaiters | B | 3570 |  |  |
| 384 | Wolf Gaiters | B | 2560 |  |  |
| 385 | Gaiters of Victory | B | 2240 |  |  |
| 386 | Gaiters of Valor | B | 2240 |  |  |
| 387 | Elven Crystal Gaiters | B | 2240 |  |  |
| 2379 | Avadon Gaiters | B | 3520 |  |  |
| 2380 | Blue Wolf Gaiters | B | 3370 |  |  |
| 9068 | Shadow Item: Zubei's Gaiters | B | 1190 |  |  |
| 11355 | Zubei's Gaiters | B | 3570 |  |  |
| 11375 | Avadon Gaiters | B | 3520 |  |  |
| 11394 | Blue Wolf Gaiters | B | 3370 |  |  |
| 12152 | Common Item - Zubei's Gaiters | B | 1190 |  |  |
| 12172 | Common Item - Avadon Plate Gaiters | B | 1173 |  |  |
| 12193 | Common Item - Blue Wolf Gaiters | B | 1123 |  |  |
| 388 | Dark Crystal Gaiters | A | 3320 |  |  |
| 5288 | Sealed Dark Crystal Gaiters | A | 3320 |  |  |
| 9082 | Shadow Item: Dark Crystal Gaiters | A | 1107 |  |  |
| 11407 | Dark Crystal Gaiters | A | 3320 |  |  |
| 11420 | Sealed Dark Crystal Gaiters | A | 3320 |  |  |
| 12206 | Common Item - Dark Crystal Gaiters | A | 1107 |  |  |
| 12220 | Common Item - Sealed Dark Crystal Gaiters | A | 1107 |  |  |
| 389 | Dragon Scale Gaiters | S | 3260 |  |  |
| 6374 | Imperial Crusader Gaiters | S | 3260 |  |  |
| 6675 | Sealed Imperial Crusader Gaiters | S | 3260 |  |  |
| 9421 | Dynasty Gaiters | S | 3210 |  |  |
| 9515 | Sealed Dynasty Gaiter | S | 3210 |  |  |
| 11499 | Sealed Imperial Crusader Gaiters | S | 3260 |  |  |
| 11505 | Imperial Crusader Gaiters | S | 3260 |  |  |
| 11512 | Dynasty Gaiters | S | 3210 |  |  |
| 11559 | Sealed Dynasty Gaiters | S | 3210 |  |  |
| 12299 | Common Item - Sealed Imperial Crusader Gaiters | S | 1087 |  |  |
| 12305 | Common Item - Imperial Crusader Gaiters | S | 1087 |  |  |
| 21776 | Imperial Crusader Gaiters of Fortune - 90-day limited period | S | 3260 |  |  |
| 21794 | Dynasty Gaiters of Fortune - 90-day limited period | S | 3210 |  |  |
| 15612 | Moirai Gaiter | S80 | 3170 |  |  |
| 15700 | Sealed Moirai Gaiter | S80 | 3170 |  |  |
| 16295 | Moirai Gaiter | S80 | 3170 |  |  |
| 16329 | Sealed Moirai Gaiter | S80 | 3170 |  |  |
| 13438 | Vesper Gaiters | S84 | 3170 |  |  |
| 13448 | Vesper Noble Gaiters | S84 | 3170 |  |  |
| 14108 | Sealed Vesper Gaiters | S84 | 3170 |  |  |
| 15578 | Elegia Gaiter | S84 | 3170 |  |  |
| 15595 | Vorpal Gaiter | S84 | 3170 |  |  |
| 15732 | Sealed Elegia Gaiter | S84 | 3170 |  |  |
| 15749 | Sealed Vorpal Gaiter | S84 | 3170 |  |  |
| 16312 | Vesper Gaiter | S84 | 3170 |  |  |
| 16346 | Sealed Vesper Gaiter | S84 | 3170 |  |  |
| 16843 | Vesper Noble Gaiter | S84 | 3170 |  |  |
| 17009 | Sealed Vesper Noble Gaiters | S84 | 3170 |  |  |

#### LIGHT (78)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 28 | Pants | NONE | 1740 |  |  |
| 29 | Leather Pants | NONE | 1730 |  |  |
| 30 | Hard Leather Pants | NONE | 1700 |  |  |
| 31 | Bone Gaiters | NONE | 1680 |  |  |
| 33 | Hard Leather Gaiters | NONE | 1610 |  |  |
| 412 | Cotton Pants | NONE | 1630 |  |  |
| 1147 | Squire's Pants | NONE | 1750 |  |  |
| 1316 | Puma Skin Gaiters | NONE | 400 |  |  |
| 2386 | Wooden Gaiters | NONE | 1670 |  |  |
| 9033 | Shadow Item: Hard Leather Gaiters | NONE | 537 |  |  |
| 9671 | Native Pants | NONE | 1700 |  |  |
| 13804 | Native's Trousers | NONE | 1700 |  |  |
| 13807 | Guards of the Dawn Trousers | NONE | 1700 |  |  |
| 413 | Puma Skin Gaiters | D | 1600 |  |  |
| 414 | Lion Skin Gaiters | D | 1570 |  |  |
| 415 | Mithril Banded Gaiters | D | 1580 |  |  |
| 416 | Reinforced Leather Gaiters | D | 1570 |  |  |
| 417 | Manticore Skin Gaiters | D | 1550 |  |  |
| 9046 | Shadow Item: Reinforced Leather Gaiters | D | 523 |  |  |
| 10022 | Puma Skin Gaiters | D | 1600 |  |  |
| 12014 | Common Item - Puma Skin Gaiters | D | 533 |  |  |
| 12020 | Common Item - Lion Skin Gaiters | D | 523 |  |  |
| 12034 | Common Item - Reinforced Leather Gaiters | D | 523 |  |  |
| 12042 | Common Item - Mithril Banded Gaiters | D | 527 |  |  |
| 12052 | Common Item - Manticore Skin Gaiters | D | 517 |  |  |
| 15018 | Manticore Skin Gaiters of Fortune - 30-day limited period | D | 1550 |  |  |
| 15132 | Manticore Skin Gaiters of Fortune - 10-day limited period | D | 1550 |  |  |
| 16906 | Manticore Skin Gaiters of Fortune - 90-day limited period | D | 1550 |  |  |
| 418 | Plated Leather Gaiters | C | 1560 |  |  |
| 419 | Rind Leather Gaiters | C | 1550 |  |  |
| 420 | Theca Leather Gaiters | C | 1530 |  |  |
| 2387 | Reinforced Mithril Gaiters | C | 1530 |  |  |
| 9059 | Shadow Item: Theca Leather Gaiters | C | 510 |  |  |
| 12084 | Common Item - Reinforced Mithril Gaiters | C | 510 |  |  |
| 12103 | Common Item - Plate Leather Gaiters | C | 520 |  |  |
| 12111 | Common Item - Rind Leather Gaiters | C | 517 |  |  |
| 12130 | Common Item - Theca Leather Gaiters | C | 510 |  |  |
| 15009 | Plate Leather Gaiters of Fortune - 30-day limited period | C | 1560 |  |  |
| 15123 | Plate Leather Gaiters of Fortune - 10-day limited period | C | 1560 |  |  |
| 16897 | Plate Leather Gaiters of Fortune - 90-day limited period | C | 1560 |  |  |
| 421 | Prairie Leather Gaiters | B | 4800 |  |  |
| 422 | Gaiters of Underworld | B | 4800 |  |  |
| 423 | Guardian's Leather Gaiters | B | 4800 |  |  |
| 424 | Marksman's Leather Gaiters | B | 1490 |  |  |
| 2388 | Zubei's Leather Gaiters | B | 1480 |  |  |
| 9074 | Shadow Item: Zubei's Leather Gaiters | B | 493 |  |  |
| 11353 | Zubei's Leather Gaiters | B | 1480 |  |  |
| 12150 | Common Item - Zubei's Leather Gaiters | B | 493 |  |  |
| 2389 | Dark Crystal Leggings | A | 1480 |  |  |
| 5298 | Sealed Dark Crystal Leggings | A | 1480 |  |  |
| 9088 | Shadow Item: Dark Crystal Leggings | A | 493 |  |  |
| 11419 | Dark Crystal Leggings | A | 1480 |  |  |
| 11428 | Sealed Dark Crystal Leggings | A | 1480 |  |  |
| 12218 | Common Item - Dark Crystal Leggings | A | 493 |  |  |
| 12228 | Common Item - Sealed Dark Crystal Leggings | A | 493 |  |  |
| 14997 | Dark Crystal Leggings of Fortune - 30-day limited period | A | 1480 |  |  |
| 15111 | Dark Crystal Leggings of Fortune - 10-day limited period | A | 1480 |  |  |
| 16885 | Dark Crystal Leggings of Fortune - 90-day limited period | A | 1480 |  |  |
| 9428 | Dynasty Leather Leggings | S | 1370 |  |  |
| 9520 | Sealed Dynasty Leather Leggings | S | 1370 |  |  |
| 11516 | Dynasty Leather Leggings | S | 1370 |  |  |
| 11563 | Sealed Dynasty Leather Leggings | S | 1370 |  |  |
| 21801 | Dynasty Leather Leggings of Fortune - 90-day limited period | S | 1370 |  |  |
| 15613 | Moirai Leather Legging | S80 | 1320 |  |  |
| 15701 | Sealed Moirai Leather Legging | S80 | 1320 |  |  |
| 16296 | Moirai Leather Legging | S80 | 1320 |  |  |
| 16330 | Sealed Moirai Leather Legging | S80 | 1320 |  |  |
| 13441 | Vesper Leather Leggings | S84 | 1320 |  |  |
| 13451 | Vesper Noble Leather Leggings | S84 | 1320 |  |  |
| 14112 | Sealed Vesper Leather Leggings | S84 | 1320 |  |  |
| 15579 | Elegia Leather Legging | S84 | 1320 |  |  |
| 15596 | Vorpal Leather Legging | S84 | 1320 |  |  |
| 15733 | Sealed Elegia Leather Legging | S84 | 1320 |  |  |
| 15750 | Sealed Vorpal Leather Legging | S84 | 1320 |  |  |
| 16313 | Vesper Leather Legging | S84 | 1320 |  |  |
| 16347 | Sealed Vesper Leather Legging | S84 | 1320 |  |  |
| 16844 | Vesper Noble Leather Legging | S84 | 1320 |  |  |
| 17012 | Sealed Vesper Noble Leather Leggings | S84 | 1320 |  |  |

#### MAGIC (86)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 461 | Apprentice's Stockings | NONE | 1100 |  |  |
| 462 | Stockings | NONE | 1080 |  |  |
| 463 | Feriotic Stockings | NONE | 1070 |  |  |
| 464 | Leather Stockings | NONE | 1020 |  |  |
| 1103 | Cotton Stockings | NONE | 1060 |  |  |
| 1104 | Stockings of Devotion | NONE | 1040 |  |  |
| 1105 | Stockings of Magic | NONE | 1030 |  |  |
| 1315 | Stockings of Magic | NONE | 150 |  |  |
| 1317 | Dark Stockings | NONE | 150 |  |  |
| 9035 | Shadow Item: Stockings of Magic | NONE | 343 |  |  |
| 465 | Cursed Stockings | D | 1020 |  |  |
| 466 | Elven Stockings | D | 1010 |  |  |
| 467 | Dark Stockings | D | 1000 |  |  |
| 468 | Mystic's Stockings | D | 990 |  |  |
| 469 | Stockings of Knowledge | D | 1000 |  |  |
| 470 | Mithril Stockings | D | 980 |  |  |
| 2401 | Elven Mithril Stockings | D | 2400 |  |  |
| 9050 | Shadow Item: Stockings of Knowledge | D | 333 |  |  |
| 10024 | Cursed Stockings | D | 1020 |  |  |
| 12011 | Common Item - Cursed Stockings | D | 340 |  |  |
| 12017 | Common Item - Dark Stockings | D | 333 |  |  |
| 12019 | Common Item - Mystic's Stockings | D | 330 |  |  |
| 12027 | Common Item - Elven Stockings | D | 337 |  |  |
| 12048 | Common Item - Stockings of Knowledge | D | 333 |  |  |
| 12058 | Common Item - Mithril Stockings | D | 327 |  |  |
| 14993 | Mithril Stockings of Fortune - 30-day limited period | D | 980 |  |  |
| 15107 | Mithril Stockings of Fortune - 10-day limited period | D | 980 |  |  |
| 16881 | Mithril Stockings of Fortune - 90-day limited period | D | 980 |  |  |
| 20651 | Common Item - Mithril Stockings | D | 100 |  |  |
| 471 | Karmian Stockings | C | 970 |  |  |
| 472 | Demon's Stockings | C | 980 |  |  |
| 473 | Divine Stockings | C | 960 |  |  |
| 9063 | Shadow Item: Demon's Stockings | C | 327 |  |  |
| 12100 | Common Item - Karmian Stockings | C | 323 |  |  |
| 12124 | Common Item - Demon's Stockings | C | 327 |  |  |
| 12139 | Common Item - Divine Stockings | C | 320 |  |  |
| 14989 | Karmian Stockings of Fortune - 30-day limited period | C | 970 |  |  |
| 15103 | Karmian Stockings of Fortune - 10-day limited period | C | 970 |  |  |
| 16877 | Karmian Stockings of Fortune - 90-day limited period | C | 970 |  |  |
| 474 | Stockings of Mana | B | 2400 |  |  |
| 475 | Paradia Stockings | B | 1600 |  |  |
| 476 | Inferno Stockings | B | 1600 |  |  |
| 477 | Stockings of Solar Eclipse | B | 2400 |  |  |
| 478 | Stockings of Summoning | B | 2400 |  |  |
| 479 | Elemental Stockings | B | 1600 |  |  |
| 480 | Stockings of Phantom | B | 1600 |  |  |
| 481 | Stockings of Grace | B | 2400 |  |  |
| 482 | Phoenix Stockings | B | 2400 |  |  |
| 483 | Cerberus Stockings | B | 6400 |  |  |
| 484 | Stockings of Aid | B | 2400 |  |  |
| 2402 | Stockings of Zubei | B | 940 |  |  |
| 2403 | Blue Wolf Stockings | B | 920 |  |  |
| 2404 | Stockings of Doom | B | 910 |  |  |
| 9078 | Shadow Item: Stockings of Zubei | B | 313 |  |  |
| 11378 | Stockings of Zubei | B | 940 |  |  |
| 11404 | Blue Wolf Stockings | B | 920 |  |  |
| 11406 | Stockings of Doom | B | 910 |  |  |
| 12176 | Common Item - Stockings of Zubei | B | 313 |  |  |
| 12203 | Common Item - Blue Wolf Stockings | B | 307 |  |  |
| 12205 | Common Item - Stockings of Doom | B | 303 |  |  |
| 2405 | Tallum Stockings | A | 920 |  |  |
| 5305 | Sealed Tallum Stockings | A | 920 |  |  |
| 11435 | Sealed Tallum Stockings | A | 920 |  |  |
| 11447 | Tallum Stockings | A | 920 |  |  |
| 12235 | Common Item - Sealed Tallum Stockings | A | 307 |  |  |
| 12246 | Common Item - Tallum Stockings | A | 307 |  |  |
| 9437 | Dynasty Stockings | S | 860 |  |  |
| 9525 | Sealed Dynasty Stockings | S | 860 |  |  |
| 11558 | Dynasty Stockings | S | 860 |  |  |
| 11574 | Sealed Dynasty Stockings | S | 860 |  |  |
| 21807 | Dynasty Stockings of Fortune - 90-day limited period | S | 860 |  |  |
| 15614 | Moirai Stockings | S80 | 850 |  |  |
| 15702 | Sealed Moirai Stockings | S80 | 850 |  |  |
| 16297 | Moirai Stockings | S80 | 850 |  |  |
| 16331 | Sealed Moirai Stockings | S80 | 850 |  |  |
| 13444 | Vesper Stockings | S84 | 850 |  |  |
| 13454 | Vesper Noble Stockings | S84 | 850 |  |  |
| 14115 | Sealed Vesper Stockings | S84 | 850 |  |  |
| 15580 | Elegia Stockings | S84 | 850 |  |  |
| 15597 | Vorpal Stockings | S84 | 850 |  |  |
| 15734 | Sealed Elegia Stockings | S84 | 850 |  |  |
| 15751 | Sealed Vorpal Stockings | S84 | 850 |  |  |
| 16314 | Vesper Stockings | S84 | 850 |  |  |
| 16348 | Sealed Vesper Stockings | S84 | 850 |  |  |
| 16845 | Vesper Noble Stockings | S84 | 850 |  |  |
| 17015 | Sealed Vesper Noble Stockings | S84 | 850 |  |  |

### Full armor (chest+legs) — `bodypart=onepiece` (172)

#### HEAVY (55)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 7851 | Clan Oath Armor | D | 9870 |  |  |
| 9821 | Shadow Item: Clan Oath Armor | D | 3290 |  |  |
| 60 | Composite Armor | C | 10980 |  |  |
| 356 | Full Plate Armor | C | 10480 |  |  |
| 9054 | Shadow Item: Composite Armor | C | 3660 |  |  |
| 12128 | Common Item - Composite Armor | C | 3660 |  |  |
| 12144 | Common Item - Full Plate Armor | C | 3493 |  |  |
| 15013 | Full Plate Armor of Fortune - 30-day limited period | C | 10480 |  |  |
| 15127 | Full Plate Armor of Fortune - 10-day limited period | C | 10480 |  |  |
| 16901 | Full Plate Armor of Fortune - 90-day limited period | C | 10480 |  |  |
| 359 | Shining Dragon Armor | B | 6400 |  |  |
| 362 | Glorious Armor | B | 6720 |  |  |
| 363 | Red Flame Armor | B | 6400 |  |  |
| 366 | Implosion Armor | B | 6080 |  |  |
| 367 | Dark Dragon Armor | B | 5760 |  |  |
| 368 | Elven Vagian Armor | B | 2400 |  |  |
| 369 | Dark Vagian Armor | B | 2400 |  |  |
| 370 | Complete Set of Plate Armor | B | 6400 |  |  |
| 371 | Hell Plate | B | 6400 |  |  |
| 372 | Art of Plate | B | 6720 |  |  |
| 373 | Masterpiece Armor | B | 5600 |  |  |
| 2381 | Doom Plate Armor | B | 9980 |  |  |
| 11386 | Doom Plate Armor | B | 9980 |  |  |
| 12184 | Common Item - Doom Plate Armor | B | 3327 |  |  |
| 15006 | Doom Plate Armor of Fortune - 30-day limited period | B | 9980 |  |  |
| 15120 | Doom Plate Armor of Fortune - 10-day limited period | B | 9980 |  |  |
| 16894 | Doom Plate Armor of Fortune - 90-day limited period | B | 9980 |  |  |
| 374 | Armor of Nightmare | A | 9580 |  |  |
| 2382 | Tallum Plate Armor | A | 9780 |  |  |
| 2383 | Majestic Plate Armor | A | 9200 |  |  |
| 5293 | Sealed Tallum Plate Armor | A | 9780 |  |  |
| 5311 | Sealed Armor of Nightmare | A | 9580 |  |  |
| 5316 | Sealed Majestic Plate Armor | A | 9200 |  |  |
| 7861 | Apella Plate Armor | A | 9780 |  |  |
| 7871 | Sealed Apella Plate Armor | A | 9780 |  |  |
| 9094 | Shadow Item: Majestic Plate Armor | A | 3067 |  |  |
| 9831 | Improved Apella Plate Armor | A | 9780 |  |  |
| 10793 | Armor of Nightmare {PvP} | A | 9580 |  |  |
| 10794 | Majestic Plate Armor {PvP} | A | 9200 |  |  |
| 11433 | Sealed Tallum Plate Armor | A | 9780 |  |  |
| 11445 | Tallum Plate Armor | A | 9780 |  |  |
| 11457 | Majestic Plate Armor | A | 9200 |  |  |
| 11463 | Sealed Majestic Plate Armor | A | 9200 |  |  |
| 11464 | Sealed Armor of Nightmare | A | 9580 |  |  |
| 11471 | Armor of Nightmare | A | 9580 |  |  |
| 12233 | Common Item - Sealed Tallum Plate Armor | A | 3260 |  |  |
| 12244 | Common Item - Tallum Plate Armor | A | 3260 |  |  |
| 12256 | Common Item - Majestic Plate Armor | A | 3067 |  |  |
| 12262 | Common Item - Sealed Majestic Plate Armor | A | 3067 |  |  |
| 12263 | Common Item - Sealed Armor of Nightmare | A | 3193 |  |  |
| 12270 | Common Item - Armor of Nightmare | A | 3193 |  |  |
| 14583 | Apella Combat Armor | A | 9780 |  |  |
| 15027 | Fortune Armor of Nightmare - 30-day limited period | A | 9580 |  |  |
| 15141 | Fortune Armor of Nightmare - 10-day limited period | A | 9580 |  |  |
| 16915 | Fortune Armor of Nightmare - 90-day limited period | A | 9580 |  |  |

#### LIGHT (58)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 396 | Salamander Skin Mail | D | 6100 |  |  |
| 7854 | Clan Oath Brigandine | D | 5400 |  |  |
| 9824 | Shadow Item: Clan Oath Brigandine | D | 1800 |  |  |
| 12074 | Common Item - Salamander Skin Mail | D | 2033 |  |  |
| 20648 | Common Item - Salamander Skin Mail | D | 100 |  |  |
| 401 | Drake Leather Armor | C | 5800 |  |  |
| 12135 | Common Item - Drake Leather Armor | C | 1933 |  |  |
| 402 | Chain Mail of Silence | B | 3200 |  |  |
| 403 | Gust Chain Mail | B | 2720 |  |  |
| 406 | Leather Armor of Concentration | B | 2400 |  |  |
| 407 | Ace's Leather Armor | B | 2400 |  |  |
| 2390 | Avadon Leather Armor | B | 5600 |  |  |
| 2391 | Blue Wolf Leather Armor | B | 5500 |  |  |
| 2392 | Leather Armor of Doom | B | 5500 |  |  |
| 11368 | Avadon Leather Armor | B | 5600 |  |  |
| 11388 | Leather Armor of Doom | B | 5500 |  |  |
| 11395 | Blue Wolf Leather Armor | B | 5500 |  |  |
| 12165 | Common Item - Avadon Leather Armor | B | 1867 |  |  |
| 12186 | Common Item - Leather Armor of Doom | B | 1833 |  |  |
| 12194 | Common Item - Blue Wolf Leather Armor | B | 1833 |  |  |
| 15000 | Leather Armor of Doom of Fortune - 30-day limited period | B | 5500 |  |  |
| 15114 | Leather Armor of Doom of Fortune - 10-day limited period | B | 5500 |  |  |
| 16888 | Leather Armor of Doom of Fortune - 90-day limited period | B | 5500 |  |  |
| 410 | Unicorn Leather Armor | A | 1280 |  |  |
| 2393 | Tallum Leather Armor | A | 5400 |  |  |
| 2394 | Leather Armor of Nightmare | A | 5300 |  |  |
| 2395 | Majestic Leather Armor | A | 5350 |  |  |
| 5301 | Sealed Tallum Leather Armor | A | 5400 |  |  |
| 5320 | Sealed Leather Armor of Nightmare | A | 5300 |  |  |
| 5323 | Sealed Majestic Leather Armor | A | 5350 |  |  |
| 7864 | Apella Brigandine | A | 5400 |  |  |
| 7874 | Sealed Apella Brigandine | A | 5400 |  |  |
| 9098 | Shadow Item: Majestic Leather Armor | A | 1783 |  |  |
| 9834 | Improved Apella Brigandine | A | 5400 |  |  |
| 10795 | Leather Armor of Nightmare {PvP} | A | 5300 |  |  |
| 10796 | Majestic Leather Armor {PvP} | A | 5350 |  |  |
| 11430 | Sealed Tallum Leather Armor | A | 5400 |  |  |
| 11440 | Tallum Leather Armor | A | 5400 |  |  |
| 11451 | Majestic Leather Armor | A | 5350 |  |  |
| 11459 | Sealed Majestic Leather Armor | A | 5350 |  |  |
| 11466 | Sealed Leather Armor of Nightmare | A | 5300 |  |  |
| 11475 | Leather Armor of Nightmare | A | 5300 |  |  |
| 12230 | Common Item - Sealed Tallum Leather Armor | A | 1800 |  |  |
| 12239 | Common Item - Tallum Leather Armor | A | 1800 |  |  |
| 12250 | Common Item - Majestic Leather Armor | A | 1783 |  |  |
| 12258 | Common Item - Sealed Majestic Leather Armor | A | 1783 |  |  |
| 12265 | Common Item - Sealed Leather Armor of Nightmare | A | 1767 |  |  |
| 12274 | Common Item - Leather Armor of Nightmare | A | 1767 |  |  |
| 14586 | Apella Combat Clothes | A | 5400 |  |  |
| 411 | Dragon Leather Armor | S | 4950 |  |  |
| 6379 | Draconic Leather Armor | S | 4950 |  |  |
| 6680 | Sealed Draconic Leather Armor | S | 4950 |  |  |
| 10800 | Draconic Leather Armor {PvP} | S | 4950 |  |  |
| 11485 | Draconic Leather Armor | S | 4950 |  |  |
| 11493 | Sealed Draconic Leather Armor | S | 4950 |  |  |
| 12284 | Common Item - Draconic Leather Armor | S | 1650 |  |  |
| 12293 | Common Item - Sealed Draconic Leather Armor | S | 1650 |  |  |
| 21782 | Draconic Leather Armor of Fortune - 90-day limited period | S | 4950 |  |  |

#### MAGIC (59)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 427 | Cotton Robe | NONE | 2750 |  |  |
| 430 | Robe of Devotion | NONE | 2650 |  |  |
| 431 | Robe of Magic | NONE | 2600 |  |  |
| 438 | Sage's Rag | D | 2580 |  |  |
| 7857 | Clan Oath Aketon | D | 2450 |  |  |
| 9827 | Shadow Item: Clan Oath Aketon | D | 820 |  |  |
| 12083 | Common Item - Sage's Rag | D | 860 |  |  |
| 440 | Robe of Seal | C | 2500 |  |  |
| 12115 | Common Item - Robe of Seal | C | 833 |  |  |
| 444 | Sage's Robe | B | 1600 |  |  |
| 448 | Robe of Black Ore | B | 1600 |  |  |
| 450 | Otherworldly Robe | B | 1600 |  |  |
| 454 | Robe of Holy Spirit | B | 1600 |  |  |
| 458 | Robe of Blessing | B | 1600 |  |  |
| 2406 | Avadon Robe | B | 2540 |  |  |
| 11369 | Avadon Robe | B | 2540 |  |  |
| 12166 | Common Item - Avadon Robe | B | 847 |  |  |
| 14983 | Avadon Robe of Fortune - 30-day limited period | B | 2540 |  |  |
| 15097 | Avadon Robe of Fortune - 10-day limited period | B | 2540 |  |  |
| 16871 | Avadon Robe of Fortune - 90-day limited period | B | 2540 |  |  |
| 459 | Dasparion's Robe | A | 1200 |  |  |
| 2407 | Dark Crystal Robe | A | 2450 |  |  |
| 2408 | Robe of Nightmare | A | 2300 |  |  |
| 2409 | Majestic Robe | A | 2330 |  |  |
| 5308 | Sealed Dark Crystal Robe | A | 2450 |  |  |
| 5326 | Sealed Robe of Nightmare | A | 2300 |  |  |
| 5329 | Sealed Majestic Robe | A | 2330 |  |  |
| 7867 | Apella Doublet | A | 2450 |  |  |
| 7877 | Sealed Apella Doublet | A | 2450 |  |  |
| 9091 | Shadow Item: Dark Crystal Robe | A | 817 |  |  |
| 9101 | Shadow Item: Majestic Robe | A | 777 |  |  |
| 9837 | Improved Apella Doublet | A | 2450 |  |  |
| 10797 | Robe of Nightmare {PvP} | A | 2300 |  |  |
| 10798 | Majestic Robe {PvP} | A | 2330 |  |  |
| 11412 | Dark Crystal Robe | A | 2450 |  |  |
| 11423 | Sealed Dark Crystal Robe | A | 2450 |  |  |
| 11452 | Majestic Robe | A | 2330 |  |  |
| 11460 | Sealed Majestic Robe | A | 2330 |  |  |
| 11467 | Sealed Robe of Nightmare | A | 2300 |  |  |
| 11476 | Robe of Nightmare | A | 2300 |  |  |
| 12211 | Common Item - Dark Crystal Robe | A | 817 |  |  |
| 12223 | Common Item - Sealed Dark Crystal Robe | A | 817 |  |  |
| 12251 | Common Item - Majestic Robe | A | 777 |  |  |
| 12259 | Common Item - Sealed Majestic Robe | A | 777 |  |  |
| 12266 | Common Item - Sealed Robe of Nightmare | A | 767 |  |  |
| 12275 | Common Item - Robe of Nightmare | A | 767 |  |  |
| 14589 | Apella Combat Overcoat | A | 2450 |  |  |
| 14978 | Dark Crystal Robe of Fortune - 30-day limited period | A | 2450 |  |  |
| 15092 | Dark Crystal Robe of Fortune - 10-day limited period | A | 2450 |  |  |
| 16866 | Dark Crystal Robe of Fortune - 90-day limited period | A | 2450 |  |  |
| 460 | The Robe | S | 2300 |  |  |
| 6383 | Major Arcana Robe | S | 2300 |  |  |
| 6684 | Sealed Major Arcana Robe | S | 2300 |  |  |
| 10801 | Major Arcana Robe {PvP} | S | 2300 |  |  |
| 11488 | Major Arcana Robe | S | 2300 |  |  |
| 11496 | Sealed Major Arcana Robe | S | 2300 |  |  |
| 12287 | Common Item - Major Arcana Robe | S | 767 |  |  |
| 12296 | Common Item - Sealed Major Arcana Robe | S | 767 |  |  |
| 21787 | Major Arcana Robe of Fortune - 90-day limited period | S | 2300 |  |  |

### Formal all-dress — `bodypart=alldress` (4)

#### HEAVY (1)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 6408 | Formal Wear | NONE | 1000 |  |  |

#### MAGIC (3)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 14773 | Suit - 14-day limited period | NONE | 0 |  |  |
| 20098 | Formal Dress (Event) - 1 hour Shadow time | NONE | 1000 |  |  |
| 20099 | Formal Dress (Event) - 7-day limited period | NONE | 1000 |  |  |

### Gloves — `bodypart=gloves` (362)

#### NONE (362)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 48 | Short Gloves | NONE | 660 |  |  |
| 49 | Gloves | NONE | 660 |  |  |
| 50 | Leather Gloves | NONE | 650 |  |  |
| 51 | Bracer | NONE | 650 |  |  |
| 990 | Mandragora Essence | NONE | 60 |  |  |
| 991 | Royen's Key | NONE | 60 |  |  |
| 992 | Shilen's 1st Mark | NONE | 60 |  |  |
| 993 | Shilen's 2nd Mark | NONE | 60 |  |  |
| 994 | Eye of Abyss | NONE | 60 |  |  |
| 995 | Wanted Poster | NONE | 60 |  |  |
| 996 | Alex's Dagger | NONE | 60 |  |  |
| 997 | Pinter's Bill | NONE | 60 |  |  |
| 998 | Book of Aklantoth - Part 1 | NONE | 60 |  |  |
| 999 | Book of Aklantoth - Part 2 | NONE | 60 |  |  |
| 1000 | Book of Aklantoth - Part 3 | NONE | 60 |  |  |
| 1119 | Short Leather Gloves | NONE | 660 |  |  |
| 1318 | Gloves | NONE | 80 |  |  |
| 1319 | Leather Gloves | NONE | 100 |  |  |
| 1320 | Crafted Leather Gloves | NONE | 100 |  |  |
| 1321 | Rip Gauntlets | NONE | 150 |  |  |
| 1322 | Bracer | NONE | 80 |  |  |
| 4226 | Dream Gloves | NONE | 650 |  |  |
| 4230 | Ubiquitous Gloves | NONE | 650 |  |  |
| 9039 | Shadow Item: Bracer | NONE | 217 |  |  |
| 61 | Mithril Plate Gloves | D | 630 |  |  |
| 63 | Gauntlets | D | 640 |  |  |
| 604 | Crafted Leather Gloves | D | 650 |  |  |
| 605 | Leather Gauntlets | D | 640 |  |  |
| 606 | Rip Gauntlets | D | 630 |  |  |
| 607 | Ogre Power Gauntlets | D | 620 |  |  |
| 2446 | Reinforced Leather Gloves | D | 640 |  |  |
| 2447 | Gloves of Knowledge | D | 640 |  |  |
| 2448 | Manticore Skin Gloves | D | 630 |  |  |
| 2449 | Brigandine Gauntlets | D | 630 |  |  |
| 2450 | Mithril Gloves | D | 640 |  |  |
| 2451 | Sage's Worn Gloves | D | 630 |  |  |
| 7852 | Clan Oath Gauntlets - Heavy Armor | D | 640 |  |  |
| 7855 | Clan Oath Leather Gloves - Light Armor | D | 640 |  |  |
| 7858 | Clan Oath Padded Gloves - Robe | D | 640 |  |  |
| 9042 | Shadow Item: Gauntlet | D | 213 |  |  |
| 9047 | Shadow Item: Reinforced Leather Gloves | D | 213 |  |  |
| 9051 | Shadow Item: Gloves of Knowledge | D | 213 |  |  |
| 9822 | Shadow Item: Clan Oath Gauntlets - Heavy Armor | D | 210 |  |  |
| 9825 | Shadow Item: Clan Oath Leather Gloves - Light Armor | D | 210 |  |  |
| 9828 | Shadow Item: Clan Oath Padded Gloves - Robe | D | 210 |  |  |
| 12007 | Common Item - Crafted Leather Gloves | D | 217 |  |  |
| 12016 | Common Item - Leather Gauntlet | D | 213 |  |  |
| 12037 | Common Item - Reinforced Leather Gloves | D | 213 |  |  |
| 12038 | Common Item - Gauntlet | D | 213 |  |  |
| 12046 | Common Item - Gloves of Knowledge | D | 213 |  |  |
| 12055 | Common Item - Manticore Skin Gloves | D | 210 |  |  |
| 12061 | Common Item - Brigandine Gauntlet | D | 210 |  |  |
| 12065 | Common Item - Elven Mithril Gloves | D | 213 |  |  |
| 12068 | Common Item - Rip Gauntlet | D | 210 |  |  |
| 12072 | Common Item - Mithril Gloves | D | 210 |  |  |
| 12076 | Common Item - Ogre Power Gauntlet | D | 207 |  |  |
| 12082 | Common Item - Sage's Worn Gloves | D | 210 |  |  |
| 14994 | Elven Mithril Gloves of Fortune - 30-day limited period | D | 640 |  |  |
| 15020 | Manticore Skin Gloves of Fortune - 30-day limited period | D | 630 |  |  |
| 15025 | Brigandine Gauntlet of Fortune - 30-day limited period | D | 630 |  |  |
| 15108 | Elven Mithril Gloves of Fortune - 10-day limited period | D | 640 |  |  |
| 15134 | Manticore Skin Gloves of Fortune - 10-day limited period | D | 630 |  |  |
| 15139 | Brigandine Gauntlet of Fortune - 10-day limited period | D | 630 |  |  |
| 16882 | Elven Mithril Gloves of Fortune - 90-day limited period | D | 640 |  |  |
| 16908 | Manticore Skin Gloves of Fortune - 90-day limited period | D | 630 |  |  |
| 16913 | Brigandine Gauntlet of Fortune - 90-day limited period | D | 630 |  |  |
| 20642 | Common Item - Mithril Gloves | D | 100 |  |  |
| 20653 | Common Item - Ogre Power Gauntlet | D | 100 |  |  |
| 608 | Mithril Gauntlets | C | 600 |  |  |
| 609 | Gauntlets of Ghost | C | 1920 |  |  |
| 1120 | Pa'agrian Hand | C | 1600 |  |  |
| 2452 | Reinforced Mithril Gloves | C | 620 |  |  |
| 2453 | Chain Gloves | C | 620 |  |  |
| 2454 | Karmian Gloves | C | 620 |  |  |
| 2455 | Plated Leather Gloves | C | 610 |  |  |
| 2456 | Dwarven Chain Gloves | C | 600 |  |  |
| 2457 | Gloves of Seal | C | 620 |  |  |
| 2458 | Rind Leather Gloves | C | 600 |  |  |
| 2459 | Demon's Gloves | C | 610 |  |  |
| 2460 | Theca Leather Gloves | C | 600 |  |  |
| 2461 | Drake Leather Gloves | C | 600 |  |  |
| 2462 | Full Plate Gauntlets | C | 600 |  |  |
| 2463 | Divine Gloves | C | 610 |  |  |
| 2468 | Blessed Gloves | C | 600 |  |  |
| 9061 | Shadow Item: Theca Leather Gloves | C | 200 |  |  |
| 9065 | Shadow Item: Demon's Gloves | C | 203 |  |  |
| 9128 | Shadow Item: Mithril Gauntlet | C | 200 |  |  |
| 12087 | Common Item - Reinforced Mithril Gloves | C | 207 |  |  |
| 12092 | Common Item - Chain Gloves | C | 207 |  |  |
| 12097 | Common Item - Karmian Gloves | C | 207 |  |  |
| 12104 | Common Item - Plate Leather Gloves | C | 203 |  |  |
| 12108 | Common Item - Dwarven Chain Gloves | C | 200 |  |  |
| 12112 | Common Item - Rind Leather Gloves | C | 200 |  |  |
| 12116 | Common Item - Gloves of Seal | C | 207 |  |  |
| 12119 | Common Item - Mithril Gauntlet | C | 200 |  |  |
| 12122 | Common Item - Demon's Gloves | C | 203 |  |  |
| 12131 | Common Item - Theca Leather Gloves | C | 200 |  |  |
| 12134 | Common Item - Drake Leather Gloves | C | 200 |  |  |
| 12137 | Common Item - Divine Gloves | C | 203 |  |  |
| 12141 | Common Item - Full Plate Gauntlet | C | 200 |  |  |
| 14990 | Karmian Gloves of Fortune - 30-day limited period | C | 620 |  |  |
| 15011 | Plate Leather Gloves of Fortune - 30-day limited period | C | 610 |  |  |
| 15015 | Full Plate Gauntlet of Fortune - 30-day limited period | C | 600 |  |  |
| 15104 | Karmian Gloves of Fortune - 10-day limited period | C | 620 |  |  |
| 15125 | Plate Leather Gloves of Fortune - 10-day limited period | C | 610 |  |  |
| 15129 | Full Plate Gauntlet of Fortune - 10-day limited period | C | 600 |  |  |
| 16878 | Karmian Gloves of Fortune - 90-day limited period | C | 620 |  |  |
| 16899 | Plate Leather Gloves of Fortune - 90-day limited period | C | 610 |  |  |
| 16903 | Full Plate Gauntlet of Fortune - 90-day limited period | C | 600 |  |  |
| 610 | Saint Knight's Gauntlets | B | 6400 |  |  |
| 611 | Soul Leech Gauntlets | B | 4800 |  |  |
| 612 | Sealed Zubei's Gauntlets | B | 590 |  |  |
| 2464 | Sealed Avadon Gloves | B | 590 |  |  |
| 2465 | Chain Gloves of Silence | B | 590 |  |  |
| 2466 | Guardian's Gloves | B | 590 |  |  |
| 2467 | Gloves of Blessing | B | 590 |  |  |
| 2475 | Sealed Doom Gloves | B | 580 |  |  |
| 2480 | Elemental Gloves | B | 580 |  |  |
| 2481 | Gloves of Grace | B | 580 |  |  |
| 2485 | Implosion Gauntlets | B | 580 |  |  |
| 2486 | Paradia Gloves | B | 580 |  |  |
| 2487 | Sealed Blue Wolf Gloves | B | 590 |  |  |
| 5709 | Sealed Zubei's Gauntlets | B | 590 |  |  |
| 5710 | Zubei's Gauntlets - Heavy Armor | B | 590 |  |  |
| 5711 | Zubei's Gauntlets - Light Armor | B | 590 |  |  |
| 5712 | Zubei's Gauntlets - Robe | B | 590 |  |  |
| 5713 | Sealed Avadon Gloves | B | 590 |  |  |
| 5714 | Avadon Gloves - Heavy Armor | B | 590 |  |  |
| 5715 | Avadon Gloves - Light Armor | B | 590 |  |  |
| 5716 | Avadon Gloves - Robe | B | 590 |  |  |
| 5717 | Sealed Blue Wolf Gloves | B | 590 |  |  |
| 5718 | Blue Wolf Gloves - Heavy Armor | B | 590 |  |  |
| 5719 | Blue Wolf Gloves - Light Armor | B | 590 |  |  |
| 5720 | Blue Wolf Gloves - Robe | B | 590 |  |  |
| 5721 | Sealed Doom Gloves | B | 580 |  |  |
| 5722 | Doom Gloves - Heavy Armor | B | 580 |  |  |
| 5723 | Doom Gloves - Light Armor | B | 580 |  |  |
| 5724 | Doom Gloves - Robe | B | 580 |  |  |
| 9071 | Shadow Item: Zubei's Gauntlet | B | 197 |  |  |
| 9075 | Shadow Item: Zubei's Gauntlet | B | 197 |  |  |
| 9079 | Shadow Item: Zubei's Gauntlet | B | 197 |  |  |
| 11349 | Sealed Zubei's Gauntlet | B | 590 |  |  |
| 11351 | Sealed Avadon Gloves | B | 590 |  |  |
| 11356 | Zubei's Gauntlet - Heavy Armor | B | 590 |  |  |
| 11357 | Zubei's Gauntlet - Light Armor Use | B | 590 |  |  |
| 11358 | Zubei's Gauntlet - Robe | B | 590 |  |  |
| 11365 | Avadon Gloves - Heavy Armor | B | 590 |  |  |
| 11366 | Avadon Gloves - Light Armor Use | B | 590 |  |  |
| 11367 | Avadon Gloves - Robe | B | 590 |  |  |
| 11379 | Doom Gloves - Heavy Armor | B | 580 |  |  |
| 11380 | Doom Gloves - Light Armor Use | B | 580 |  |  |
| 11381 | Doom Gloves - Robe | B | 580 |  |  |
| 11389 | Sealed Doom Gloves | B | 580 |  |  |
| 11392 | Sealed Blue Wolf Gloves | B | 590 |  |  |
| 11399 | Blue Wolf Gloves - Heavy Armor | B | 590 |  |  |
| 11400 | Blue Wolf Gloves - Light Armor Use | B | 590 |  |  |
| 11401 | Blue Wolf Gloves - Robe | B | 590 |  |  |
| 12146 | Common Item - Sealed Zubei's Gauntlet | B | 197 |  |  |
| 12148 | Common Item - Sealed Avadon Gloves | B | 197 |  |  |
| 12153 | Common Item - Zubei's Gauntlet - Heavy Armor | B | 197 |  |  |
| 12154 | Common Item - Zubei's Gauntlet - Tans Armor Use | B | 197 |  |  |
| 12155 | Common Item - Zubei's Gauntlet - Robe | B | 197 |  |  |
| 12162 | Common Item - Avadon Gloves - Heavy Armor | B | 197 |  |  |
| 12163 | Common Item - Avadon Gloves - Tans Armor Use | B | 197 |  |  |
| 12164 | Common Item - Avadon Gloves - Robe | B | 197 |  |  |
| 12177 | Common Item - Doom Gloves - Heavy Armor | B | 193 |  |  |
| 12178 | Common Item - Doom Gloves - Tans Armor Use | B | 193 |  |  |
| 12179 | Common Item - Doom Gloves - Robe | B | 193 |  |  |
| 12187 | Common Item - Sealed Doom Gloves | B | 193 |  |  |
| 12190 | Common Item - Sealed Blue Wolf Gloves | B | 197 |  |  |
| 12198 | Common Item - Blue Wolf Gloves - Heavy Armor | B | 197 |  |  |
| 12199 | Common Item - Blue Wolf Gloves - Tans Armor Use | B | 197 |  |  |
| 12200 | Common Item - Blue Wolf Gloves - Robe | B | 197 |  |  |
| 14985 | Avadon Gloves of Fortune - Robe - 30-day limited period | B | 590 |  |  |
| 15002 | Doom Gloves of Fortune - Heavy Armor - 30-day limited period | B | 580 |  |  |
| 15003 | Doom Gloves of Fortune - Light Armor - 30-day limited period | B | 580 |  |  |
| 15099 | Avadon Gloves of Fortune - Robe - 10-day limited period | B | 590 |  |  |
| 15116 | Doom Gloves of Fortune - Heavy Armor - 10-day limited period | B | 580 |  |  |
| 15117 | Doom Gloves of Fortune - Light Armor - 10-day limited period | B | 580 |  |  |
| 16873 | Avadon Gloves of Fortune - Robe - 90-day limited period | B | 590 |  |  |
| 16890 | Doom Gloves of Fortune - Heavy Armor - 90-day limited period | B | 580 |  |  |
| 16891 | Doom Gloves of Fortune - Light Armor - 90-day limited period | B | 580 |  |  |
| 613 | Sand Dragon Gloves | A | 3200 |  |  |
| 2469 | Gloves of Underworld | A | 580 |  |  |
| 2470 | Gloves of Phantom | A | 560 |  |  |
| 2471 | Dark Legion Gloves | A | 560 |  |  |
| 2472 | Dark Crystal Gloves | A | 580 |  |  |
| 2474 | Dasparion's Gloves | A | 550 |  |  |
| 2478 | Tallum Gloves | A | 580 |  |  |
| 2479 | Gauntlets of Nightmare | A | 550 |  |  |
| 2482 | Majestic Gauntlets | A | 540 |  |  |
| 2483 | Gust Bracer | A | 580 |  |  |
| 2484 | Cerberus Gloves | A | 540 |  |  |
| 2488 | Phoenix Gloves | A | 570 |  |  |
| 2489 | Gloves of Black Ore | A | 570 |  |  |
| 5290 | Sealed Dark Crystal Gloves | A | 580 |  |  |
| 5295 | Sealed Tallum Gloves | A | 580 |  |  |
| 5299 | Sealed Gloves of Underworld | A | 580 |  |  |
| 5302 | Sealed Gust Bracer | A | 580 |  |  |
| 5306 | Sealed Gloves of Black Ore | A | 570 |  |  |
| 5309 | Sealed Phoenix Gloves | A | 570 |  |  |
| 5313 | Sealed Gauntlets of Nightmare | A | 550 |  |  |
| 5318 | Sealed Majestic Gauntlets | A | 540 |  |  |
| 5321 | Sealed Dark Legion Gloves | A | 560 |  |  |
| 5324 | Sealed Gloves of Phantom | A | 560 |  |  |
| 5327 | Sealed Cerberus Gloves | A | 540 |  |  |
| 5330 | Sealed Dasparion's Gloves | A | 550 |  |  |
| 5765 | Dark Crystal Gloves - Heavy Armor | A | 580 |  |  |
| 5766 | Dark Crystal Gloves - Light Armor | A | 580 |  |  |
| 5767 | Dark Crystal Gloves - Robe | A | 580 |  |  |
| 5768 | Tallum Gloves - Heavy Armor | A | 580 |  |  |
| 5769 | Tallum Gloves - Light Armor | A | 580 |  |  |
| 5770 | Tallum Gloves - Robe | A | 580 |  |  |
| 5771 | Gauntlets of Nightmare - Heavy Armor | A | 550 |  |  |
| 5772 | Gauntlets of Nightmare - Light Armor | A | 550 |  |  |
| 5773 | Gauntlets of Nightmare - Robe | A | 550 |  |  |
| 5774 | Majestic Gauntlets - Heavy Armor | A | 540 |  |  |
| 5775 | Majestic Gauntlets - Light Armor | A | 540 |  |  |
| 5776 | Majestic Gauntlets - Robe | A | 540 |  |  |
| 7862 | Apella Gauntlet - Heavy Armor | A | 580 |  |  |
| 7865 | Apella Leather Gloves - Light Armor | A | 580 |  |  |
| 7868 | Apella Silk Gloves - Robe | A | 580 |  |  |
| 7872 | Sealed Apella Gauntlet | A | 580 |  |  |
| 7875 | Sealed Apella Leather Gloves | A | 580 |  |  |
| 7878 | Sealed Apella Silk Gloves | A | 580 |  |  |
| 9085 | Shadow Item: Dark Crystal Gloves | A | 193 |  |  |
| 9089 | Shadow Item: Dark Crystal Gloves | A | 193 |  |  |
| 9092 | Shadow Item: Dark Crystal Gloves | A | 193 |  |  |
| 9096 | Shadow Item: Majestic Gauntlet | A | 180 |  |  |
| 9099 | Shadow Item: Majestic Gauntlet | A | 180 |  |  |
| 9102 | Shadow Item: Majestic Gauntlet | A | 180 |  |  |
| 9832 | Improved Apella Gauntlet - Heavy Armor | A | 580 |  |  |
| 9835 | Improved Apella Leather Gloves - Light Armor | A | 580 |  |  |
| 9838 | Improved Apella Silk Gloves - Robe | A | 580 |  |  |
| 11408 | Dark Crystal Gloves - Heavy Armor | A | 580 |  |  |
| 11409 | Dark Crystal Gloves - Light Armor Use | A | 580 |  |  |
| 11410 | Dark Crystal Gloves - Robe | A | 580 |  |  |
| 11421 | Sealed Dark Crystal Gloves | A | 580 |  |  |
| 11429 | Sealed Tallum Gloves | A | 580 |  |  |
| 11437 | Tallum Gloves - Heavy Armor | A | 580 |  |  |
| 11438 | Tallum Gloves - Light Armor Use | A | 580 |  |  |
| 11439 | Tallum Gloves - Robe | A | 580 |  |  |
| 11448 | Majestic Gauntlet - Heavy Armor | A | 540 |  |  |
| 11449 | Majestic Gauntlet - Light Armor Use | A | 540 |  |  |
| 11450 | Majestic Gauntlet - Robe | A | 540 |  |  |
| 11458 | Sealed Majestic Gauntlet | A | 540 |  |  |
| 11465 | Sealed Gauntlet of Nightmare | A | 550 |  |  |
| 11472 | Gauntlet of Nightmare - Heavy Armor | A | 550 |  |  |
| 11473 | Gauntlet of Nightmare - Light Armor Use | A | 550 |  |  |
| 11474 | Gauntlet of Nightmare - Robe | A | 550 |  |  |
| 12207 | Common Item - Dark Crystal Gloves - Heavy Armor | A | 193 |  |  |
| 12208 | Common Item - Dark Crystal Gloves - Tans Armor Use | A | 193 |  |  |
| 12209 | Common Item - Dark Crystal Gloves - Robe | A | 193 |  |  |
| 12221 | Common Item - Sealed Dark Crystal Gloves | A | 193 |  |  |
| 12229 | Common Item - Sealed Tallum Gloves | A | 193 |  |  |
| 12236 | Common Item - Tallum Gloves - Heavy Armor | A | 193 |  |  |
| 12237 | Common Item - Tallum Gloves - Tans Armor Use | A | 193 |  |  |
| 12238 | Common Item - Tallum Gloves - Robe | A | 193 |  |  |
| 12247 | Common Item - Majestic Gauntlet - Heavy Armor | A | 180 |  |  |
| 12248 | Common Item - Majestic Gauntlet - Tans Armor Use | A | 180 |  |  |
| 12249 | Common Item - Majestic Gauntlet - Robe | A | 180 |  |  |
| 12257 | Common Item - Sealed Majestic Gauntlet | A | 180 |  |  |
| 12264 | Common Item - Sealed Gauntlet of Nightmare | A | 183 |  |  |
| 12271 | Common Item - Gauntlet of Nightmare - Heavy Armor | A | 183 |  |  |
| 12272 | Common Item - Gauntlet of Nightmare - Tans Armor Use | A | 183 |  |  |
| 12273 | Common Item - Gauntlet of Nightmare - Robe | A | 183 |  |  |
| 14584 | Apella Combat Gauntlet - Heavy Armor | A | 580 |  |  |
| 14587 | Apella Combat Leather Gloves - Tans Armor Use | A | 580 |  |  |
| 14590 | Apella Combat Silk Gloves - Robe | A | 580 |  |  |
| 14980 | Dark Crystal Gloves of Fortune - Robe - 30-day limited period | A | 580 |  |  |
| 14998 | Dark Crystal Gloves of Fortune - Light Armor - 30-day limited period | A | 580 |  |  |
| 15029 | Fortune Gauntlet of Nightmare - Heavy Armor - 30-day limited period | A | 550 |  |  |
| 15094 | Dark Crystal Gloves of Fortune - Robe - 10-day limited period | A | 580 |  |  |
| 15112 | Dark Crystal Gloves of Fortune - Light Armor - 10-day limited period | A | 580 |  |  |
| 15143 | Fortune Gauntlet of Nightmare - Heavy Armor - 10-day limited period | A | 550 |  |  |
| 16868 | Dark Crystal Gloves of Fortune - Robe - 90-day limited period | A | 580 |  |  |
| 16886 | Dark Crystal Gloves of Fortune - Light Armor - 90-day limited period | A | 580 |  |  |
| 16917 | Fortune Gauntlet of Nightmare - Heavy Armor - 90-day limited period | A | 550 |  |  |
| 2473 | The Gloves | S | 540 |  |  |
| 2476 | Dragon Gauntlets | S | 540 |  |  |
| 2477 | Dragon Leather Gloves | S | 540 |  |  |
| 6375 | Imperial Crusader Gauntlets | S | 540 |  |  |
| 6380 | Draconic Leather Gloves | S | 540 |  |  |
| 6384 | Major Arcana Gloves | S | 540 |  |  |
| 6676 | Sealed Imperial Crusader Gauntlet | S | 540 |  |  |
| 6681 | Sealed Draconic Leather Glove | S | 540 |  |  |
| 6685 | Sealed Major Arcana Glove | S | 540 |  |  |
| 9423 | Dynasty Gauntlet - Heavy Armor | S | 520 |  |  |
| 9430 | Dynasty Leather Gloves - Light Armor | S | 520 |  |  |
| 9439 | Dynasty Gloves - Robe | S | 520 |  |  |
| 9517 | Sealed Dynasty Gauntlets | S | 520 |  |  |
| 9522 | Sealed Dynasty Leather Gloves | S | 520 |  |  |
| 9527 | Sealed Dynasty Gloves | S | 520 |  |  |
| 11483 | Draconic Leather Gloves | S | 540 |  |  |
| 11487 | Major Arcana Gloves | S | 540 |  |  |
| 11491 | Sealed Draconic Leather Gloves | S | 540 |  |  |
| 11495 | Sealed Major Arcana Gloves | S | 540 |  |  |
| 11500 | Sealed Imperial Crusader Gauntlet | S | 540 |  |  |
| 11506 | Imperial Crusader Gauntlet | S | 540 |  |  |
| 11513 | Dynasty Gauntlet | S | 520 |  |  |
| 11514 | Dynasty Gloves | S | 520 |  |  |
| 11515 | Dynasty Leather Gloves | S | 520 |  |  |
| 11560 | Sealed Dynasty Gauntlet | S | 520 |  |  |
| 11561 | Sealed Dynasty Gloves | S | 520 |  |  |
| 11562 | Sealed Dynasty Leather Gloves | S | 520 |  |  |
| 12282 | Common Item - Draconic Leather Gloves | S | 180 |  |  |
| 12286 | Common Item - Major Arcana Gloves | S | 180 |  |  |
| 12291 | Common Item - Sealed Draconic Leather Gloves | S | 180 |  |  |
| 12295 | Common Item - Sealed Major Arcana Gloves | S | 180 |  |  |
| 12300 | Common Item - Sealed Imperial Crusader Gauntlet | S | 180 |  |  |
| 12306 | Common Item - Imperial Crusader Gauntlet | S | 180 |  |  |
| 21777 | Imperial Crusader Gauntlet of Fortune - 90-day limited period | S | 540 |  |  |
| 21783 | Draconic Leather Gloves of Fortune - 90-day limited period | S | 540 |  |  |
| 21788 | Major Arcana Gloves of Fortune - 90-day limited period | S | 540 |  |  |
| 21795 | Dynasty Gauntlet of Fortune - 90-day limited period | S | 520 |  |  |
| 21803 | Dynasty Leather Gloves of Fortune - 90-day limited period | S | 520 |  |  |
| 21809 | Dynasty Gloves of Fortune - 90-day limited period | S | 520 |  |  |
| 15615 | Moirai Gauntlet | S80 | 510 |  |  |
| 15616 | Moirai Leather Gloves | S80 | 510 |  |  |
| 15617 | Moirai Gloves | S80 | 510 |  |  |
| 15703 | Sealed Moirai Gauntlet | S80 | 510 |  |  |
| 15704 | Sealed Moirai Leather Gloves | S80 | 510 |  |  |
| 15705 | Sealed Moirai Gloves | S80 | 510 |  |  |
| 16298 | Moirai Gauntlet | S80 | 510 |  |  |
| 16299 | Moirai Leather Gloves | S80 | 510 |  |  |
| 16300 | Moirai Gloves | S80 | 510 |  |  |
| 16332 | Sealed Moirai Gauntlet | S80 | 510 |  |  |
| 16333 | Sealed Moirai Leather Gloves | S80 | 510 |  |  |
| 16334 | Sealed Moirai Gloves | S80 | 510 |  |  |
| 13439 | Vesper Gauntlet | S84 | 510 |  |  |
| 13442 | Vesper Leather Gloves | S84 | 510 |  |  |
| 13445 | Vesper Gloves | S84 | 510 |  |  |
| 13449 | Vesper Noble Gauntlet | S84 | 510 |  |  |
| 13452 | Vesper Noble Leather Gloves | S84 | 510 |  |  |
| 13455 | Vesper Noble Gloves | S84 | 510 |  |  |
| 14109 | Sealed Vesper Gauntlet | S84 | 510 |  |  |
| 14113 | Sealed Vesper Leather Gloves | S84 | 510 |  |  |
| 14116 | Sealed Vesper Gloves | S84 | 510 |  |  |
| 15581 | Elegia Gauntlet | S84 | 510 |  |  |
| 15582 | Elegia Leather Gloves | S84 | 510 |  |  |
| 15583 | Elegia Gloves | S84 | 510 |  |  |
| 15598 | Vorpal Gauntlet | S84 | 510 |  |  |
| 15599 | Vorpal Leather Gloves | S84 | 510 |  |  |
| 15600 | Vorpal Gloves | S84 | 510 |  |  |
| 15735 | Sealed Elegia Gauntlet | S84 | 510 |  |  |
| 15736 | Sealed Elegia Leather Gloves | S84 | 510 |  |  |
| 15737 | Sealed Elegia Gloves | S84 | 510 |  |  |
| 15752 | Sealed Vorpal Gauntlet | S84 | 510 |  |  |
| 15753 | Sealed Vorpal Leather Gloves | S84 | 510 |  |  |
| 15754 | Sealed Vorpal Gloves | S84 | 510 |  |  |
| 16315 | Vesper Gauntlet | S84 | 510 |  |  |
| 16316 | Vesper Leather Gloves | S84 | 510 |  |  |
| 16317 | Vesper Gloves | S84 | 510 |  |  |
| 16349 | Sealed Vesper Gauntlet | S84 | 510 |  |  |
| 16350 | Sealed Vesper Leather Gloves | S84 | 510 |  |  |
| 16351 | Sealed Vesper Gloves | S84 | 510 |  |  |
| 16846 | Vesper Noble Gauntlet | S84 | 510 |  |  |
| 16847 | Vesper Noble Leather Gloves | S84 | 510 |  |  |
| 16848 | Vesper Noble Gloves | S84 | 510 |  |  |
| 17010 | Sealed Vesper Noble Gauntlet | S84 | 510 |  |  |
| 17013 | Sealed Vesper Noble Leather Gloves | S84 | 510 |  |  |
| 17016 | Sealed Vesper Noble Gloves | S84 | 510 |  |  |

### Boots — `bodypart=feet` (384)

#### NONE (384)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 35 | Cloth Shoes | NONE | 1320 |  |  |
| 36 | Leather Sandals | NONE | 1320 |  |  |
| 37 | Leather Shoes | NONE | 1320 |  |  |
| 38 | Low Boots | NONE | 1320 |  |  |
| 39 | Boots | NONE | 1310 |  |  |
| 1121 | Apprentice's Shoes | NONE | 1320 |  |  |
| 1122 | Cotton Shoes | NONE | 1320 |  |  |
| 1129 | Crude Leather Shoes | NONE | 1320 |  |  |
| 1323 | Leather Shoes | NONE | 120 |  |  |
| 1324 | Low Boots | NONE | 150 |  |  |
| 1325 | Leather Boots | NONE | 250 |  |  |
| 1326 | Iron Boots | NONE | 300 |  |  |
| 1327 | Boots | NONE | 200 |  |  |
| 4227 | Dream Boots | NONE | 1310 |  |  |
| 4231 | Ubiquitous Boots | NONE | 1310 |  |  |
| 5576 | Sound Test Boots | NONE | 50 |  |  |
| 5590 | Squeaking Shoes | NONE | 50 |  |  |
| 9038 | Shadow Item: Boots | NONE | 437 |  |  |
| 13260 | Gran Kain's Squeaking Shoes - 10-hour limited period | NONE | 50 |  |  |
| 40 | Leather Boots | D | 1300 |  |  |
| 553 | Iron Boots | D | 1280 |  |  |
| 1123 | Blue Buckskin Boots | D | 1300 |  |  |
| 1124 | Boots of Power | D | 1250 |  |  |
| 1125 | Assault Boots | D | 1240 |  |  |
| 2422 | Reinforced Leather Boots | D | 1280 |  |  |
| 2423 | Boots of Knowledge | D | 1270 |  |  |
| 2424 | Manticore Skin Boots | D | 1260 |  |  |
| 2425 | Brigandine Boots | D | 1250 |  |  |
| 2426 | Elven Mithril Boots | D | 1250 |  |  |
| 2427 | Salamander Skin Boots | D | 1230 |  |  |
| 2428 | Plate Boots | D | 1240 |  |  |
| 7853 | Clan Oath Sabaton - Heavy Armor | D | 1280 |  |  |
| 7856 | Clan Oath Boots - Light Armor | D | 1280 |  |  |
| 7859 | Clan Oath Sandals - Robe | D | 1280 |  |  |
| 9043 | Shadow Item: Iron Boots | D | 427 |  |  |
| 9048 | Shadow Item: Reinforced Leather Boots | D | 427 |  |  |
| 9052 | Shadow Item: Boots of Knowledge | D | 423 |  |  |
| 9823 | Shadow Item: Clan Oath Sabaton - Heavy Armor | D | 430 |  |  |
| 9826 | Shadow Item: Clan Oath Boots - Light Armor | D | 430 |  |  |
| 9829 | Shadow Item: Clan Oath Sandals - Robe | D | 430 |  |  |
| 12006 | Common Item - Leather Boots | D | 433 |  |  |
| 12029 | Common Item - Blue Buckskin Boots | D | 433 |  |  |
| 12033 | Common Item - Iron Boots | D | 427 |  |  |
| 12035 | Common Item - Reinforced Leather Boots | D | 427 |  |  |
| 12045 | Common Item - Boots of Knowledge | D | 423 |  |  |
| 12053 | Common Item - Manticore Skin Boots | D | 420 |  |  |
| 12062 | Common Item - Brigandine Boots | D | 417 |  |  |
| 12066 | Common Item - Elven Mithril Boots | D | 417 |  |  |
| 12070 | Common Item - Boots of Power | D | 417 |  |  |
| 12071 | Common Item - Assault Boots | D | 413 |  |  |
| 12075 | Common Item - Salamander Skin Boots | D | 410 |  |  |
| 12077 | Common Item - Plate Boots | D | 413 |  |  |
| 14995 | Elven Mithril Boots of Fortune - 30-day limited period | D | 1250 |  |  |
| 15019 | Manticore Skin Boots of Fortune - 30-day limited period | D | 1260 |  |  |
| 15024 | Brigandine Boots of Fortune - 30-day limited period | D | 1250 |  |  |
| 15109 | Elven Mithril Boots of Fortune - 10-day limited period | D | 1250 |  |  |
| 15133 | Manticore Skin Boots of Fortune - 10-day limited period | D | 1260 |  |  |
| 15138 | Brigandine Boots of Fortune - 10-day limited period | D | 1250 |  |  |
| 16883 | Elven Mithril Boots of Fortune - 90-day limited period | D | 1250 |  |  |
| 16907 | Manticore Skin Boots of Fortune - 90-day limited period | D | 1260 |  |  |
| 16912 | Brigandine Boots of Fortune - 90-day limited period | D | 1250 |  |  |
| 20643 | Common Item - Plate Boots | D | 100 |  |  |
| 20652 | Common Item - Salamander Skin Boots | D | 100 |  |  |
| 62 | Reinforced Mithril Boots | C | 1230 |  |  |
| 64 | Composite Boots | C | 1220 |  |  |
| 603 | Divine Boots | C | 1200 |  |  |
| 1126 | Crimson Boots | C | 1210 |  |  |
| 1127 | Forgotten Boots | C | 4000 |  |  |
| 1128 | Adamantite Boots | C | 4000 |  |  |
| 2429 | Chain Boots | C | 1220 |  |  |
| 2430 | Karmian Boots | C | 1230 |  |  |
| 2431 | Plated Leather Boots | C | 1220 |  |  |
| 2432 | Dwarven Chain Boots | C | 1210 |  |  |
| 2433 | Boots of Seal | C | 1220 |  |  |
| 2434 | Rind Leather Boots | C | 1220 |  |  |
| 2435 | Demon's Boots | C | 1220 |  |  |
| 2436 | Theca Leather Boots | C | 1210 |  |  |
| 2437 | Drake Leather Boots | C | 1210 |  |  |
| 2438 | Full Plate Boots | C | 1200 |  |  |
| 9055 | Shadow Item: Composite Boots | C | 407 |  |  |
| 9060 | Shadow Item: Theca Leather Boots | C | 403 |  |  |
| 9064 | Shadow Item: Demon's Boots | C | 407 |  |  |
| 12085 | Common Item - Reinforced Mithril Boots | C | 410 |  |  |
| 12088 | Common Item - Dwarven Chain Boots | C | 403 |  |  |
| 12089 | Common Item - Boots of Seal | C | 407 |  |  |
| 12093 | Common Item - Chain Boots | C | 407 |  |  |
| 12098 | Common Item - Karmian Boots | C | 410 |  |  |
| 12101 | Common Item - Plate Leather Boots | C | 407 |  |  |
| 12114 | Common Item - Rind Leather Boots | C | 407 |  |  |
| 12118 | Common Item - Crimson Boots | C | 403 |  |  |
| 12121 | Common Item - Demon's Boots | C | 407 |  |  |
| 12125 | Common Item - Composite Boots | C | 407 |  |  |
| 12132 | Common Item - Theca Leather Boots | C | 403 |  |  |
| 12136 | Common Item - Drake Leather Boots | C | 403 |  |  |
| 12142 | Common Item - Full Plate Boots | C | 400 |  |  |
| 14991 | Karmian Boots of Fortune - 30-day limited period | C | 1230 |  |  |
| 15010 | Plate Leather Boots of Fortune - 30-day limited period | C | 1220 |  |  |
| 15014 | Full Plate Boots of Fortune - 30-day limited period | C | 1200 |  |  |
| 15105 | Karmian Boots of Fortune - 10-day limited period | C | 1230 |  |  |
| 15124 | Plate Leather Boots of Fortune - 10-day limited period | C | 1220 |  |  |
| 15128 | Full Plate Boots of Fortune - 10-day limited period | C | 1200 |  |  |
| 16879 | Karmian Boots of Fortune - 90-day limited period | C | 1230 |  |  |
| 16898 | Plate Leather Boots of Fortune - 90-day limited period | C | 1220 |  |  |
| 16902 | Full Plate Boots of Fortune - 90-day limited period | C | 1200 |  |  |
| 554 | Sealed Zubei's Boots | B | 1180 |  |  |
| 556 | Wolf Boots | B | 1180 |  |  |
| 557 | Shining Dragon Boots | B | 1150 |  |  |
| 558 | Boots of Victory | B | 1180 |  |  |
| 559 | Boots of Valor | B | 1150 |  |  |
| 560 | Glorious Boots | B | 1180 |  |  |
| 562 | Elven Crystal Boots | B | 1180 |  |  |
| 564 | Implosion Boots | B | 1150 |  |  |
| 565 | Dark Dragon Boots | B | 1130 |  |  |
| 566 | Elven Vagian Boots | B | 1150 |  |  |
| 567 | Dark Vagian Boots | B | 1130 |  |  |
| 568 | _ | B | 200 |  |  |
| 569 | Hell Boots | B | 1130 |  |  |
| 570 | Art of Boots | B | 1150 |  |  |
| 571 | Masterpiece Boots | B | 1130 |  |  |
| 572 | Boots of Silence | B | 1190 |  |  |
| 574 | Prairie Boots | B | 1140 |  |  |
| 576 | Boots of Concentration | B | 1170 |  |  |
| 577 | Ace's Boots | B | 1150 |  |  |
| 578 | Guardian's Boots | B | 1180 |  |  |
| 579 | Marksman Boots | B | 1150 |  |  |
| 580 | Boots of Mana | B | 1180 |  |  |
| 581 | Sage's Boots | B | 1150 |  |  |
| 582 | Paradia Boots | B | 1140 |  |  |
| 584 | Boots of Solar Eclipse | B | 1180 |  |  |
| 585 | Boots of Black Ore | B | 1200 |  |  |
| 586 | Boots of Summoning | B | 1170 |  |  |
| 587 | Otherworldly Boots | B | 1200 |  |  |
| 588 | Elemental Boots | B | 1130 |  |  |
| 590 | Boots of Grace | B | 1130 |  |  |
| 591 | Boots of Holy Spirit | B | 1200 |  |  |
| 594 | Boots of Aid | B | 1200 |  |  |
| 595 | Boots of Blessing | B | 1160 |  |  |
| 596 | Flame Boots | B | 1020 |  |  |
| 597 | Boots of Bravery | B | 1050 |  |  |
| 599 | Absolute Boots | B | 1130 |  |  |
| 600 | Sealed Avadon Boots | B | 1170 |  |  |
| 601 | Sealed Doom Boots | B | 1130 |  |  |
| 602 | Boots of Pledge | B | 1130 |  |  |
| 2439 | Sealed Blue Wolf Boots | B | 1130 |  |  |
| 5725 | Sealed Zubei's Boots | B | 1180 |  |  |
| 5726 | Zubei's Boots - Heavy Armor | B | 1180 |  |  |
| 5727 | Zubei's Boots - Light Armor | B | 1180 |  |  |
| 5728 | Zubei's Boots - Robe | B | 1180 |  |  |
| 5729 | Sealed Avadon Boots | B | 1180 |  |  |
| 5730 | Avadon Boots - Heavy Armor | B | 1180 |  |  |
| 5731 | Avadon Boots - Light Armor | B | 1180 |  |  |
| 5732 | Avadon Boots - Robe | B | 1180 |  |  |
| 5733 | Sealed Blue Wolf Boots | B | 1130 |  |  |
| 5734 | Blue Wolf Boots - Heavy Armor | B | 1130 |  |  |
| 5735 | Blue Wolf Boots - Light Armor | B | 1130 |  |  |
| 5736 | Blue Wolf Boots - Robe | B | 1130 |  |  |
| 5737 | Sealed Doom Boots | B | 1130 |  |  |
| 5738 | Doom Boots - Heavy Armor | B | 1130 |  |  |
| 5739 | Doom Boots - Light Armor | B | 1130 |  |  |
| 5740 | Doom Boots - Robe | B | 1130 |  |  |
| 9072 | Shadow Item: Zubei's Boots | B | 393 |  |  |
| 9076 | Shadow Item: Zubei's Boots | B | 393 |  |  |
| 9080 | Shadow Item: Zubei's Boots | B | 393 |  |  |
| 11350 | Sealed Zubei's Boots | B | 1180 |  |  |
| 11352 | Sealed Avadon Boots | B | 1170 |  |  |
| 11359 | Zubei's Boots - Heavy Armor | B | 1180 |  |  |
| 11360 | Zubei's Boots - Light Armor Use | B | 1180 |  |  |
| 11361 | Zubei's Boots - Robe | B | 1180 |  |  |
| 11370 | Avadon Boots - Heavy Armor | B | 1180 |  |  |
| 11371 | Avadon Boots - Light Armor Use | B | 1180 |  |  |
| 11372 | Avadon Boots - Robe | B | 1180 |  |  |
| 11382 | Doom Boots - Heavy Armor | B | 1130 |  |  |
| 11383 | Doom Boots - Light Armor Use | B | 1130 |  |  |
| 11384 | Doom Boots - Robe | B | 1130 |  |  |
| 11390 | Sealed Doom Boots | B | 1130 |  |  |
| 11391 | Sealed Blue Wolf Boots | B | 1130 |  |  |
| 11396 | Blue Wolf Boots - Heavy Armor | B | 1130 |  |  |
| 11397 | Blue Wolf Boots - Light Armor Use | B | 1130 |  |  |
| 11398 | Blue Wolf Boots - Robe | B | 1130 |  |  |
| 12147 | Common Item - Sealed Zubei's Boots | B | 393 |  |  |
| 12149 | Common Item - Sealed Avadon Boots | B | 390 |  |  |
| 12156 | Common Item - Zubei's Boots - Heavy Armor | B | 393 |  |  |
| 12157 | Common Item - Zubei's Boots - Tans Armor Use | B | 393 |  |  |
| 12158 | Common Item - Zubei's Boots - Robe | B | 393 |  |  |
| 12167 | Common Item - Avadon Boots - Heavy Armor | B | 393 |  |  |
| 12168 | Common Item - Avadon Boots - Tans Armor Use | B | 393 |  |  |
| 12169 | Common Item - Avadon Boots - Robe | B | 393 |  |  |
| 12180 | Common Item - Doom Boots - Heavy Armor | B | 377 |  |  |
| 12181 | Common Item - Doom Boots - Tans Armor Use | B | 377 |  |  |
| 12182 | Common Item - Doom Boots - Robe | B | 377 |  |  |
| 12188 | Common Item - Sealed Doom Boots | B | 377 |  |  |
| 12189 | Common Item - Sealed Blue Wolf Boots | B | 377 |  |  |
| 12195 | Common Item - Blue Wolf Boots - Heavy Armor | B | 377 |  |  |
| 12196 | Common Item - Blue Wolf Boots - Tans Armor Use | B | 377 |  |  |
| 12197 | Common Item - Blue Wolf Boots - Robe | B | 377 |  |  |
| 14986 | Avadon Boots of Fortune - Robe - 30-day limited period | B | 1180 |  |  |
| 15004 | Doom Boots of Fortune - Heavy Armor - 30-day limited period | B | 1130 |  |  |
| 15005 | Doom Boots of Fortune - Light Armor - 30-day limited period | B | 1130 |  |  |
| 15100 | Avadon Boots of Fortune - Robe - 10-day limited period | B | 1180 |  |  |
| 15118 | Doom Boots of Fortune - Heavy Armor - 10-day limited period | B | 1130 |  |  |
| 15119 | Doom Boots of Fortune - Light Armor - 10-day limited period | B | 1130 |  |  |
| 16874 | Avadon Boots of Fortune - Robe - 90-day limited period | B | 1180 |  |  |
| 16892 | Doom Boots of Fortune - Heavy Armor - 90-day limited period | B | 1130 |  |  |
| 16893 | Doom Boots of Fortune - Light Armor - 90-day limited period | B | 1130 |  |  |
| 555 | Dragon Boots | A | 1110 |  |  |
| 561 | Red Flame Boots | A | 1120 |  |  |
| 563 | Dark Crystal Boots | A | 1110 |  |  |
| 573 | Gust Boots | A | 1120 |  |  |
| 575 | Boots of Underworld | A | 1110 |  |  |
| 583 | Majestic Boots | A | 1110 |  |  |
| 589 | Boots of Phantom | A | 1120 |  |  |
| 592 | Phoenix Boots | A | 1120 |  |  |
| 593 | Cerberus Boots | A | 1120 |  |  |
| 598 | Blood Boots | A | 1130 |  |  |
| 2440 | Boots of Nightmare | A | 1110 |  |  |
| 2441 | Dark Legion Boots | A | 1120 |  |  |
| 2442 | Dasparion's Boots | A | 1100 |  |  |
| 2445 | Dragon Scale Boots | A | 1100 |  |  |
| 5291 | Sealed Dark Crystal Boots | A | 1110 |  |  |
| 5296 | Sealed Tallum Boots | A | 1130 |  |  |
| 5300 | Sealed Boots of Underworld | A | 1110 |  |  |
| 5303 | Sealed Gust Boots | A | 1120 |  |  |
| 5307 | Sealed Red Flame Boots | A | 1120 |  |  |
| 5310 | Sealed Phoenix Boots | A | 1120 |  |  |
| 5314 | Sealed Boots of Nightmare | A | 1110 |  |  |
| 5319 | Sealed Majestic Boots | A | 1110 |  |  |
| 5322 | Sealed Dark Legion Boots | A | 1120 |  |  |
| 5325 | Sealed Boots of Phantom | A | 1120 |  |  |
| 5328 | Sealed Cerberus Boots | A | 1120 |  |  |
| 5331 | Sealed Dasparion's Boots | A | 1100 |  |  |
| 5777 | Dark Crystal Boots - Heavy Armor | A | 1110 |  |  |
| 5778 | Dark Crystal Boots - Light Armor | A | 1110 |  |  |
| 5779 | Dark Crystal Boots - Robe | A | 1110 |  |  |
| 5780 | Tallum Boots - Heavy Armor | A | 1130 |  |  |
| 5781 | Tallum Boots - Light Armor | A | 1130 |  |  |
| 5782 | Tallum Boots - Robe | A | 1130 |  |  |
| 5783 | Boots of Nightmare - Heavy Armor | A | 1110 |  |  |
| 5784 | Boots of Nightmare - Light Armor | A | 1110 |  |  |
| 5785 | Boots of Nightmare - Robe | A | 1110 |  |  |
| 5786 | Majestic Boots - Heavy Armor | A | 1110 |  |  |
| 5787 | Majestic Boots - Light Armor | A | 1110 |  |  |
| 5788 | Majestic Boots - Robe | A | 1110 |  |  |
| 7863 | Apella Solleret - Heavy Armor | A | 1130 |  |  |
| 7866 | Apella Boots - Light Armor | A | 1130 |  |  |
| 7869 | Apella Sandals - Robe | A | 1130 |  |  |
| 7873 | Sealed Apella Solleret | A | 1130 |  |  |
| 7876 | Sealed Apella Boots | A | 1130 |  |  |
| 7879 | Sealed Apella Sandals | A | 1130 |  |  |
| 9086 | Shadow Item: Dark Crystal Boots | A | 370 |  |  |
| 9090 | Shadow Item: Dark Crystal Boots | A | 370 |  |  |
| 9093 | Shadow Item: Dark Crystal Boots | A | 370 |  |  |
| 9097 | Shadow Item: Majestic Boots | A | 370 |  |  |
| 9100 | Shadow Item: Majestic Boots | A | 370 |  |  |
| 9103 | Shadow Item: Majestic Boots | A | 370 |  |  |
| 9833 | Improved Apella Solleret - Heavy Armor | A | 1130 |  |  |
| 9836 | Improved Apella Boots - Light Armor | A | 1130 |  |  |
| 9839 | Improved Apella Sandals - Robe | A | 1130 |  |  |
| 11413 | Dark Crystal Boots - Heavy Armor | A | 1110 |  |  |
| 11414 | Dark Crystal Boots - Light Armor Use | A | 1110 |  |  |
| 11415 | Dark Crystal Boots - Robe | A | 1110 |  |  |
| 11424 | Sealed Dark Crystal Boots | A | 1110 |  |  |
| 11431 | Sealed Tallum Boots | A | 1130 |  |  |
| 11441 | Tallum Boots - Heavy Armor | A | 1130 |  |  |
| 11442 | Tallum Boots - Light Armor Use | A | 1130 |  |  |
| 11443 | Tallum Boots - Robe | A | 1130 |  |  |
| 11453 | Majestic Boots - Heavy Armor | A | 1110 |  |  |
| 11454 | Majestic Boots - Light Armor Use | A | 1110 |  |  |
| 11455 | Majestic Boots - Robe | A | 1110 |  |  |
| 11461 | Sealed Majestic Boots | A | 1110 |  |  |
| 11468 | Sealed Boots of Nightmare | A | 1110 |  |  |
| 11477 | Boots of Nightmare - Heavy Armor | A | 1110 |  |  |
| 11478 | Boots of Nightmare - Light Armor Use | A | 1110 |  |  |
| 11479 | Boots of Nightmare - Robe | A | 1110 |  |  |
| 12212 | Common Item - Dark Crystal Boots - Heavy Armor | A | 370 |  |  |
| 12213 | Common Item - Dark Crystal Boots - Tans Armor Use | A | 370 |  |  |
| 12214 | Common Item - Dark Crystal Boots - Robe | A | 370 |  |  |
| 12224 | Common Item - Sealed Dark Crystal Boots | A | 370 |  |  |
| 12231 | Common Item - Sealed Tallum Boots | A | 377 |  |  |
| 12240 | Common Item - Tallum Boots - Heavy Armor | A | 377 |  |  |
| 12241 | Common Item - Tallum Boots - Tans Armor Use | A | 377 |  |  |
| 12242 | Common Item - Tallum Boots - Robe | A | 377 |  |  |
| 12252 | Common Item - Majestic Boots - Heavy Armor | A | 370 |  |  |
| 12253 | Common Item - Majestic Boots - Tans Armor Use | A | 370 |  |  |
| 12254 | Common Item - Majestic Boots - Robe | A | 370 |  |  |
| 12260 | Common Item - Sealed Majestic Boots | A | 370 |  |  |
| 12267 | Common Item - Sealed Boots of Nightmare | A | 370 |  |  |
| 12276 | Common Item - Boots of Nightmare - Heavy Armor | A | 370 |  |  |
| 12277 | Common Item - Boots of Nightmare - Tans Armor Use | A | 370 |  |  |
| 12278 | Common Item - Boots of Nightmare - Robe | A | 370 |  |  |
| 14585 | Apella Combat Boots - Heavy Armor | A | 1130 |  |  |
| 14588 | Apella Combat Shoes - Tans Armor Use | A | 1130 |  |  |
| 14591 | Apella Combat Sandals - Robe | A | 1130 |  |  |
| 14981 | Dark Crystal Boots of Fortune - Robe - 30-day limited period | A | 1110 |  |  |
| 14999 | Dark Crystal Boots of Fortune - Light Armor - 30-day limited period | A | 1110 |  |  |
| 15030 | Fortune Boots of Nightmare - Heavy Armor - 30-day limited period | A | 1110 |  |  |
| 15095 | Dark Crystal Boots of Fortune - Robe - 10-day limited period | A | 1110 |  |  |
| 15113 | Dark Crystal Boots of Fortune - Light Armor - 10-day limited period | A | 1110 |  |  |
| 15144 | Fortune Boots of Nightmare - Heavy Armor - 10-day limited period | A | 1110 |  |  |
| 16869 | Dark Crystal Boots of Fortune - Robe - 90-day limited period | A | 1110 |  |  |
| 16887 | Dark Crystal Boots of Fortune - Light Armor - 90-day limited period | A | 1110 |  |  |
| 16918 | Fortune Boots of Nightmare - Heavy Armor - 90-day limited period | A | 1110 |  |  |
| 2443 | Dragon Leather Boots | S | 1100 |  |  |
| 2444 | The Boots | S | 1100 |  |  |
| 6376 | Imperial Crusader Boots | S | 1110 |  |  |
| 6381 | Draconic Leather Boots | S | 1110 |  |  |
| 6385 | Major Arcana Boots | S | 1110 |  |  |
| 6677 | Sealed Imperial Crusader Boots | S | 1110 |  |  |
| 6682 | Sealed Draconic Leather Boots | S | 1110 |  |  |
| 6686 | Sealed Major Arcana Boots | S | 1110 |  |  |
| 9424 | Dynasty Boots - Heavy Armor | S | 1090 |  |  |
| 9431 | Dynasty Leather Boots - Light Armor | S | 1090 |  |  |
| 9440 | Dynasty Shoes - Robe | S | 1090 |  |  |
| 9518 | Sealed Dynasty Boots | S | 1090 |  |  |
| 9523 | Sealed Dynasty Leather Boots | S | 1090 |  |  |
| 9528 | Sealed Dynasty Shoes | S | 1090 |  |  |
| 11484 | Draconic Leather Boots | S | 1110 |  |  |
| 11489 | Major Arcana Boots | S | 1110 |  |  |
| 11492 | Sealed Draconic Leather Boots | S | 1110 |  |  |
| 11497 | Sealed Major Arcana Boots | S | 1110 |  |  |
| 11501 | Sealed Imperial Crusader Boots | S | 1110 |  |  |
| 11507 | Imperial Crusader Boots | S | 1110 |  |  |
| 11524 | Dynasty Leather Boots | S | 1090 |  |  |
| 11526 | Dynasty Boots | S | 1090 |  |  |
| 11533 | Dynasty Shoes | S | 1090 |  |  |
| 11565 | Sealed Dynasty Leather Boots | S | 1090 |  |  |
| 11567 | Sealed Dynasty Boots | S | 1090 |  |  |
| 11570 | Sealed Dynasty Shoes | S | 1090 |  |  |
| 12283 | Common Item - Draconic Leather Boots | S | 370 |  |  |
| 12288 | Common Item - Major Arcana Boots | S | 370 |  |  |
| 12292 | Common Item - Sealed Draconic Leather Boots | S | 370 |  |  |
| 12297 | Common Item - Sealed Major Arcana Boots | S | 370 |  |  |
| 12301 | Common Item - Sealed Imperial Crusader Boots | S | 370 |  |  |
| 12307 | Common Item - Imperial Crusader Boots | S | 370 |  |  |
| 21778 | Imperial Crusader Boots of Fortune - 90-day limited period | S | 1110 |  |  |
| 21784 | Draconic Leather Boots of Fortune - 90-day limited period | S | 1110 |  |  |
| 21789 | Major Arcana Boots of Fortune - 90-day limited period | S | 1110 |  |  |
| 21796 | Dynasty Boots of Fortune - 90-day limited period | S | 1090 |  |  |
| 21804 | Dynasty Leather Boots of Fortune - 90-day limited period | S | 1090 |  |  |
| 21810 | Dynasty Shoes of Fortune - 90-day limited period | S | 1090 |  |  |
| 15618 | Moirai Boots | S80 | 1070 |  |  |
| 15619 | Moirai Leather Boots | S80 | 1070 |  |  |
| 15620 | Moirai Shoes | S80 | 1070 |  |  |
| 15706 | Sealed Moirai Boots | S80 | 1070 |  |  |
| 15707 | Sealed Moirai Leather Boots | S80 | 1070 |  |  |
| 15708 | Sealed Moirai Shoes | S80 | 1070 |  |  |
| 16301 | Moirai Boots | S80 | 1070 |  |  |
| 16302 | Moirai Leather Boots | S80 | 1070 |  |  |
| 16303 | Moirai Shoes | S80 | 1070 |  |  |
| 16335 | Sealed Moirai Boots | S80 | 1070 |  |  |
| 16336 | Sealed Moirai Leather Boots | S80 | 1070 |  |  |
| 16337 | Sealed Moirai Shoes | S80 | 1070 |  |  |
| 13440 | Vesper Boots | S84 | 1070 |  |  |
| 13443 | Vesper Leather Boots | S84 | 1070 |  |  |
| 13446 | Vesper Shoes | S84 | 1070 |  |  |
| 13450 | Vesper Noble Boots | S84 | 1070 |  |  |
| 13453 | Vesper Noble Leather Boots | S84 | 1070 |  |  |
| 13456 | Vesper Noble Shoes | S84 | 1070 |  |  |
| 14110 | Sealed Vesper Boots | S84 | 1070 |  |  |
| 14114 | Sealed Vesper Leather Boots | S84 | 1070 |  |  |
| 14117 | Sealed Vesper Shoes | S84 | 1070 |  |  |
| 15584 | Elegia Boots | S84 | 1070 |  |  |
| 15585 | Elegia Leather Boots | S84 | 1070 |  |  |
| 15586 | Elegia Shoes | S84 | 1070 |  |  |
| 15601 | Vorpal Boots | S84 | 1070 |  |  |
| 15602 | Vorpal Leather Boots | S84 | 1070 |  |  |
| 15603 | Vorpal Shoes | S84 | 1070 |  |  |
| 15738 | Sealed Elegia Boots | S84 | 1070 |  |  |
| 15739 | Sealed Elegia Leather Boots | S84 | 1070 |  |  |
| 15740 | Sealed Elegia Shoes | S84 | 1070 |  |  |
| 15755 | Sealed Vorpal Boots | S84 | 1070 |  |  |
| 15756 | Sealed Vorpal Leather Boots | S84 | 1070 |  |  |
| 15757 | Sealed Vorpal Shoes | S84 | 1070 |  |  |
| 16318 | Vesper Boots | S84 | 1070 |  |  |
| 16319 | Vesper Leather Boots | S84 | 1070 |  |  |
| 16320 | Vesper Shoes | S84 | 1070 |  |  |
| 16352 | Sealed Vesper Boots | S84 | 1070 |  |  |
| 16353 | Sealed Vesper Leather Boots | S84 | 1070 |  |  |
| 16354 | Sealed Vesper Shoes | S84 | 1070 |  |  |
| 16849 | Vesper Noble Boots | S84 | 1070 |  |  |
| 16850 | Vesper Noble Leather Boots | S84 | 1070 |  |  |
| 16851 | Vesper Noble Shoes | S84 | 1070 |  |  |
| 17011 | Sealed Vesper Noble Boots | S84 | 1070 |  |  |
| 17014 | Sealed Vesper Noble Leather Boots | S84 | 1070 |  |  |
| 17017 | Sealed Vesper Noble Shoes | S84 | 1070 |  |  |

### Head — `bodypart=head` (254)

#### NONE (254)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 41 | Cloth Cap | NONE | 660 |  |  |
| 42 | Leather Cap | NONE | 660 |  |  |
| 43 | Wooden Helmet | NONE | 660 |  |  |
| 44 | Leather Helmet | NONE | 650 |  |  |
| 1148 | Hard Leather Helmet | NONE | 640 |  |  |
| 9037 | Shadow Item: Hard Leather Helmet | NONE | 213 |  |  |
| 9669 | Native Helmet | NONE | 70 |  |  |
| 13802 | Native's Hood | NONE | 70 |  |  |
| 13805 | Guards of the Dawn Helmet | NONE | 70 |  |  |
| 45 | Bone Helmet | D | 640 |  |  |
| 46 | Bronze Helmet | D | 630 |  |  |
| 47 | Helmet | D | 640 |  |  |
| 2411 | Brigandine Helmet | D | 630 |  |  |
| 2412 | Plate Helmet | D | 630 |  |  |
| 7850 | Clan Oath Helm | D | 640 |  |  |
| 9053 | Shadow Item: Helmet | D | 213 |  |  |
| 9820 | Shadow Item: Clan Oath Helm | D | 210 |  |  |
| 12009 | Common Item - Bone Helmet | D | 213 |  |  |
| 12028 | Common Item - Bronze Helmet | D | 210 |  |  |
| 12050 | Common Item - Helmet | D | 213 |  |  |
| 12064 | Common Item - Brigandine Helmet | D | 210 |  |  |
| 12079 | Common Item - Plate Helmet | D | 210 |  |  |
| 15023 | Brigandine Helmet of Fortune - 30-day limited period | D | 630 |  |  |
| 15137 | Brigandine Helmet of Fortune - 10-day limited period | D | 630 |  |  |
| 16911 | Brigandine Helmet of Fortune - 90-day limited period | D | 630 |  |  |
| 20645 | Common Item - Plate Helmet | D | 100 |  |  |
| 497 | Chain Helmet | C | 620 |  |  |
| 498 | Steel Plate Helmet | C | 610 |  |  |
| 499 | Mithril Helmet | C | 240 |  |  |
| 500 | Great Helmet | C | 610 |  |  |
| 517 | Composite Helmet | C | 610 |  |  |
| 529 | Cap of Mana | C | 320 |  |  |
| 531 | Paradia Hood | C | 320 |  |  |
| 533 | Hood of Solar Eclipse | C | 320 |  |  |
| 535 | Hood of Summoning | C | 320 |  |  |
| 537 | Elemental Hood | C | 320 |  |  |
| 539 | Hood of Grace | C | 320 |  |  |
| 541 | Phoenix Hood | C | 590 |  |  |
| 543 | Hood of Aid | C | 320 |  |  |
| 545 | Flame Helm | C | 400 |  |  |
| 549 | Helm of Avadon | C | 400 |  |  |
| 551 | Helmet of Pledge | C | 400 |  |  |
| 1149 | Shining Circlet | C | 600 |  |  |
| 2413 | Chain Hood | C | 620 |  |  |
| 2414 | Full Plate Helmet | C | 600 |  |  |
| 9057 | Shadow Item: Composite Helmet | C | 203 |  |  |
| 9066 | Shadow Item: Shining Circlet | C | 200 |  |  |
| 12090 | Common Item - Chain Hood | C | 207 |  |  |
| 12106 | Common Item - Great Helmet | C | 203 |  |  |
| 12120 | Common Item - Shining Circlet | C | 200 |  |  |
| 12127 | Common Item - Composite Helmet | C | 203 |  |  |
| 12145 | Common Item - Full Plate Helmet | C | 200 |  |  |
| 15012 | Full Plate Helmet of Fortune - 30-day limited period | C | 600 |  |  |
| 15126 | Full Plate Helmet of Fortune - 10-day limited period | C | 600 |  |  |
| 16900 | Full Plate Helmet of Fortune - 90-day limited period | C | 600 |  |  |
| 501 | Armet | B | 580 |  |  |
| 503 | Zubei's Helmet | B | 590 |  |  |
| 505 | Wolf Helmet | B | 580 |  |  |
| 506 | Shining Dragon Helmet | B | 880 |  |  |
| 507 | Helmet of Victory | B | 640 |  |  |
| 508 | Helmet of Valor | B | 720 |  |  |
| 511 | Elven Crystal Helmet | B | 580 |  |  |
| 513 | Implosion Helmet | B | 480 |  |  |
| 514 | Dark Dragon Helmet | B | 400 |  |  |
| 519 | Art of Helmet | B | 400 |  |  |
| 521 | Helmet of Silence | B | 320 |  |  |
| 522 | Gust Helmet | B | 570 |  |  |
| 523 | Prairie Helmet | B | 480 |  |  |
| 524 | Helm of Underworld | B | 320 |  |  |
| 525 | Helmet of Concentration | B | 320 |  |  |
| 526 | Ace's Helmet | B | 320 |  |  |
| 527 | Guardian's Helmet | B | 240 |  |  |
| 528 | Marksman Helmet | B | 240 |  |  |
| 530 | Sage's Cap | B | 320 |  |  |
| 532 | Inferno Hood | B | 320 |  |  |
| 534 | Hood of Black Ore | B | 320 |  |  |
| 536 | Otherworldly Hood | B | 320 |  |  |
| 538 | Hood of Phantom | B | 320 |  |  |
| 540 | Hood of Holy Spirit | B | 320 |  |  |
| 542 | Cerberus Hood | B | 320 |  |  |
| 544 | Hood of Blessing | B | 320 |  |  |
| 546 | Helm of Bravery | B | 400 |  |  |
| 548 | Absolute Helm | B | 400 |  |  |
| 550 | Helm of Doom | B | 400 |  |  |
| 552 | Divine Helm | B | 400 |  |  |
| 2415 | Avadon Circlet | B | 590 |  |  |
| 2416 | Blue Wolf Helmet | B | 580 |  |  |
| 2417 | Doom Helmet | B | 580 |  |  |
| 9069 | Shadow Item: Zubei's Helmet | B | 197 |  |  |
| 11363 | Zubei's Helmet - Heavy Armor | B | 590 |  |  |
| 11373 | Avadon Circlet - Heavy Armor | B | 590 |  |  |
| 11387 | Doom Helmet - Heavy Armor | B | 580 |  |  |
| 11403 | Blue Wolf Helmet - Heavy Armor | B | 580 |  |  |
| 12160 | Common Item - Zubei's Helmet | B | 197 |  |  |
| 12170 | Common Item - Avadon Circlet | B | 197 |  |  |
| 12185 | Common Item - Doom Helmet | B | 193 |  |  |
| 12202 | Common Item - Blue Wolf Helmet | B | 193 |  |  |
| 12978 | Zubei's Helmet - Light Armor Use | B | 590 |  |  |
| 12979 | Zubei's Helmet - Robe | B | 590 |  |  |
| 12980 | Avadon Circlet - Light Armor Use | B | 590 |  |  |
| 12981 | Avadon Circlet - Robe | B | 590 |  |  |
| 12982 | Doom Helmet - Light Armor Use | B | 580 |  |  |
| 12983 | Doom Helmet - Robe | B | 580 |  |  |
| 12984 | Blue Wolf Helmet - Light Armor Use | B | 580 |  |  |
| 12985 | Blue Wolf Helmet - Robe | B | 580 |  |  |
| 14984 | Avadon Circlet of Fortune - 30-day limited period | B | 590 |  |  |
| 15001 | Doom Helmet of Fortune - 30-day limited period | B | 580 |  |  |
| 15098 | Avadon Circlet of Fortune - 10-day limited period | B | 590 |  |  |
| 15115 | Doom Helmet of Fortune - 10-day limited period | B | 580 |  |  |
| 16872 | Avadon Circlet of Fortune - 90-day limited period | B | 590 |  |  |
| 16889 | Doom Helmet of Fortune - 90-day limited period | B | 580 |  |  |
| 502 | Close Helmet | A | 570 |  |  |
| 509 | Glorious Helmet | A | 800 |  |  |
| 510 | Red Flame Helmet | A | 960 |  |  |
| 512 | Dark Crystal Helmet | A | 570 |  |  |
| 515 | Elven Vagian Helm | A | 560 |  |  |
| 516 | Dark Vagian Helm | A | 560 |  |  |
| 518 | Hell Helm | A | 320 |  |  |
| 520 | Masterpiece Helm | A | 400 |  |  |
| 547 | Tallum Helm | A | 570 |  |  |
| 2418 | Helm of Nightmare | A | 560 |  |  |
| 2419 | Majestic Circlet | A | 550 |  |  |
| 5289 | Sealed Dark Crystal Helmet | A | 570 |  |  |
| 5294 | Sealed Tallum Helmet | A | 570 |  |  |
| 5312 | Sealed Helm of Nightmare | A | 560 |  |  |
| 5317 | Sealed Majestic Circlet | A | 550 |  |  |
| 7860 | Apella Helm | A | 570 |  |  |
| 7870 | Sealed Apella Helm | A | 570 |  |  |
| 9083 | Shadow Item: Dark Crystal Helmet | A | 190 |  |  |
| 9095 | Shadow Item: Majestic Circlet | A | 183 |  |  |
| 9830 | Improved Apella Helm | A | 570 |  |  |
| 11417 | Dark Crystal Helmet - Heavy Armor | A | 570 |  |  |
| 11426 | Sealed Dark Crystal Helmet - Heavy Armor | A | 570 |  |  |
| 11434 | Sealed Tallum Helmet - Heavy Armor | A | 570 |  |  |
| 11446 | Tallum Helmet - Heavy Armor | A | 570 |  |  |
| 11456 | Majestic Circlet - Heavy Armor | A | 550 |  |  |
| 11462 | Sealed Majestic Circlet - Heavy Armor | A | 550 |  |  |
| 11470 | Sealed Helm of Nightmare - Heavy Armor | A | 560 |  |  |
| 11481 | Helm of Nightmare - Heavy Armor | A | 560 |  |  |
| 12216 | Common Item - Dark Crystal Helmet | A | 190 |  |  |
| 12226 | Common Item - Sealed Dark Crystal Helmet | A | 190 |  |  |
| 12234 | Common Item - Sealed Tallum Helmet | A | 190 |  |  |
| 12245 | Common Item - Tallum Helmet | A | 190 |  |  |
| 12255 | Common Item - Majestic Circlet | A | 183 |  |  |
| 12261 | Common Item - Sealed Majestic Circlet | A | 183 |  |  |
| 12269 | Common Item - Sealed Helm of Nightmare | A | 187 |  |  |
| 12280 | Common Item - Helm of Nightmare | A | 187 |  |  |
| 12986 | Dark Crystal Helmet - Light Armor Use | A | 570 |  |  |
| 12987 | Dark Crystal Helmet - Robe | A | 570 |  |  |
| 12988 | Tallum Helmet - Light Armor Use | A | 570 |  |  |
| 12989 | Tallum Helmet - Robe | A | 570 |  |  |
| 12990 | Majestic Circlet - Light Armor Use | A | 550 |  |  |
| 12991 | Majestic Circlet - Robe | A | 550 |  |  |
| 12992 | Helm of Nightmare - Light Armor Use | A | 560 |  |  |
| 12993 | Helm of Nightmare - Robe | A | 560 |  |  |
| 12994 | Sealed Dark Crystal Helmet - Light Armor Use | A | 570 |  |  |
| 12995 | Sealed Dark Crystal Helmet - Robe | A | 570 |  |  |
| 12996 | Sealed Tallum Helmet - Light Armor Use | A | 570 |  |  |
| 12997 | Sealed Tallum Helmet - Robe | A | 570 |  |  |
| 12998 | Sealed Majestic Circlet - Light Armor Use | A | 550 |  |  |
| 12999 | Sealed Majestic Circlet - Robe | A | 550 |  |  |
| 13000 | Sealed Helm of Nightmare - Light Armor Use | A | 560 |  |  |
| 13001 | Sealed Helm of Nightmare - Robe | A | 560 |  |  |
| 14582 | Apella Combat Helmet | A | 570 |  |  |
| 14979 | Dark Crystal Helmet of Fortune - 30-day limited period | A | 570 |  |  |
| 15028 | Fortune Helm of Nightmare - 30-day limited period | A | 560 |  |  |
| 15093 | Dark Crystal Helmet of Fortune - 10-day limited period | A | 570 |  |  |
| 15142 | Fortune Helm of Nightmare - 10-day limited period | A | 560 |  |  |
| 16867 | Dark Crystal Helmet of Fortune - 90-day limited period | A | 570 |  |  |
| 16916 | Fortune Helm of Nightmare - 90-day limited period | A | 560 |  |  |
| 504 | Dragon Helmet | S | 550 |  |  |
| 2420 | Dragon Headgear | S | 540 |  |  |
| 2421 | The Hood | S | 540 |  |  |
| 6378 | Imperial Crusader Helmet | S | 550 |  |  |
| 6382 | Draconic Leather Helmet | S | 550 |  |  |
| 6386 | Major Arcana Circlet | S | 550 |  |  |
| 6679 | Sealed Imperial Crusader Helmet | S | 550 |  |  |
| 6683 | Sealed Draconic Leather Helmet | S | 550 |  |  |
| 6687 | Sealed Major Arcana Circlet | S | 550 |  |  |
| 9422 | Dynasty Helmet | S | 530 |  |  |
| 9429 | Dynasty Leather Helmet | S | 530 |  |  |
| 9438 | Dynasty Circlet | S | 530 |  |  |
| 9516 | Sealed Dynasty Helmet | S | 530 |  |  |
| 9521 | Sealed Dynasty Leather Helmet | S | 530 |  |  |
| 9526 | Sealed Dynasty Circlet | S | 530 |  |  |
| 11486 | Draconic Leather Helmet | S | 550 |  |  |
| 11490 | Major Arcana Circlet | S | 550 |  |  |
| 11494 | Sealed Draconic Leather Helmet | S | 550 |  |  |
| 11498 | Sealed Major Arcana Circlet | S | 550 |  |  |
| 11503 | Sealed Imperial Crusader Helmet | S | 550 |  |  |
| 11509 | Imperial Crusader Helmet | S | 550 |  |  |
| 11525 | Dynasty Leather Helmet | S | 530 |  |  |
| 11539 | Dynasty Circlet | S | 530 |  |  |
| 11557 | Dynasty Helmet | S | 530 |  |  |
| 11566 | Sealed Dynasty Leather Helmet | S | 530 |  |  |
| 11571 | Sealed Dynasty Circlet | S | 530 |  |  |
| 11573 | Sealed Dynasty Helmet | S | 530 |  |  |
| 12285 | Common Item - Draconic Leather Helmet | S | 183 |  |  |
| 12289 | Common Item - Major Arcana Circlet | S | 183 |  |  |
| 12294 | Common Item - Sealed Draconic Leather Helmet | S | 183 |  |  |
| 12298 | Common Item - Sealed Major Arcana Circlet | S | 183 |  |  |
| 12303 | Common Item - Sealed Imperial Crusader Helmet | S | 183 |  |  |
| 12309 | Common Item - Imperial Crusader Helmet | S | 183 |  |  |
| 21779 | Imperial Crusader Helmet of Fortune - 90-day limited period | S | 550 |  |  |
| 21785 | Draconic Leather Helmet of Fortune - 90-day limited period | S | 550 |  |  |
| 21790 | Major Arcana Circlet of Fortune - 90-day limited period | S | 550 |  |  |
| 21797 | Dynasty Helmet of Fortune - 90-day limited period | S | 530 |  |  |
| 21802 | Dynasty Leather Helmet of Fortune - 90-day limited period | S | 530 |  |  |
| 21808 | Dynasty Circlet of Fortune - 90-day limited period | S | 530 |  |  |
| 15606 | Moirai Helmet | S80 | 530 |  |  |
| 15607 | Moirai Leather Helmet | S80 | 530 |  |  |
| 15608 | Moirai Circlet | S80 | 530 |  |  |
| 15694 | Sealed Moirai Helmet | S80 | 530 |  |  |
| 15695 | Sealed Moirai Leather Helmet | S80 | 530 |  |  |
| 15696 | Sealed Moirai Circlet | S80 | 530 |  |  |
| 16289 | Moirai Helmet | S80 | 530 |  |  |
| 16290 | Moirai Leather Helmet | S80 | 530 |  |  |
| 16291 | Moirai Circlet | S80 | 530 |  |  |
| 16323 | Sealed Moirai Helmet | S80 | 530 |  |  |
| 16324 | Sealed Moirai Leather Helmet | S80 | 530 |  |  |
| 16325 | Sealed Moirai Circlet | S80 | 530 |  |  |
| 13137 | Vesper Helmet | S84 | 530 |  |  |
| 13138 | Vesper Leather Helmet | S84 | 530 |  |  |
| 13139 | Vesper Circlet | S84 | 530 |  |  |
| 13140 | Vesper Noble Helmet | S84 | 530 |  |  |
| 13141 | Vesper Noble Leather Helmet | S84 | 530 |  |  |
| 13142 | Vesper Noble Circlet | S84 | 530 |  |  |
| 13143 | Sealed Vesper Helmet | S84 | 530 |  |  |
| 13144 | Sealed Vesper Leather Helmet | S84 | 530 |  |  |
| 13145 | Sealed Vesper Circlet | S84 | 530 |  |  |
| 13146 | Sealed Vesper Noble Helmet | S84 | 530 |  |  |
| 13147 | Sealed Vesper Noble Leather Helmet | S84 | 530 |  |  |
| 13148 | Sealed Vesper Noble Circlet | S84 | 530 |  |  |
| 15572 | Elegia Helmet | S84 | 530 |  |  |
| 15573 | Elegia Leather Helmet | S84 | 530 |  |  |
| 15574 | Elegia Circlet | S84 | 530 |  |  |
| 15589 | Vorpal Helmet | S84 | 530 |  |  |
| 15590 | Vorpal Leather Helmet | S84 | 530 |  |  |
| 15591 | Vorpal Circlet | S84 | 530 |  |  |
| 15726 | Sealed Elegia Helmet | S84 | 530 |  |  |
| 15727 | Sealed Elegia Leather Helmet | S84 | 530 |  |  |
| 15728 | Sealed Elegia Circlet | S84 | 530 |  |  |
| 15743 | Sealed Vorpal Helmet | S84 | 530 |  |  |
| 15744 | Sealed Vorpal Leather Helmet | S84 | 530 |  |  |
| 15745 | Sealed Vorpal Circlet | S84 | 530 |  |  |
| 16306 | Vesper Helmet | S84 | 530 |  |  |
| 16307 | Vesper Leather Helmet | S84 | 530 |  |  |
| 16308 | Vesper Circlet | S84 | 530 |  |  |
| 16340 | Sealed Vesper Helmet | S84 | 530 |  |  |
| 16341 | Sealed Vesper Leather Helmet | S84 | 530 |  |  |
| 16342 | Sealed Vesper Circlet | S84 | 530 |  |  |
| 16837 | Vesper Noble Helmet | S84 | 530 |  |  |
| 16838 | Vesper Noble Leather Helmet | S84 | 530 |  |  |
| 16839 | Vesper Noble Circlet | S84 | 530 |  |  |

### Underwear / shirt — `bodypart=underwear` (82)

#### NONE (82)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 675 | Silk Yarn Undergarment Set | NONE | 170 |  |  |
| 676 | Pure White Undergarment Set | NONE | 160 |  |  |
| 9577 | Cotton Shirt | NONE | 130 |  |  |
| 9583 | Striped Cotton Shirt | NONE | 130 |  |  |
| 15383 | Weaver's Multi-colored Clothes - 7-day limited period | NONE | 0 |  |  |
| 15384 | Weaver's Multi-colored Clothes - 30-day limited period | NONE | 0 |  |  |
| 15385 | Weaver's Multi-colored Clothes - 60-day limited period | NONE | 0 |  |  |
| 15386 | Weaver's Multi-colored Clothes - 90-day limited period | NONE | 0 |  |  |
| 15387 | Weaver's Multi-colored Clothes - Permanent Use | NONE | 0 |  |  |
| 15388 | Weaver's Multi-colored Clothes (Event) - 7-day limited period | NONE | 0 |  |  |
| 15389 | Weaver's Multi-colored Clothes (Event) - 30-day limited period | NONE | 0 |  |  |
| 15390 | Weaver's Multi-colored Clothes (Event) - 60-day limited period | NONE | 0 |  |  |
| 15391 | Weaver's Multi-colored Clothes (Event) - 90-day limited period | NONE | 0 |  |  |
| 15392 | Weaver's Multi-colored Clothes (Event) - Permanent Use | NONE | 0 |  |  |
| 20759 | Christmas Shirt - 24-hour limited period | NONE | 0 |  |  |
| 21150 | Shiny Lit Platform Summon Bracelet | NONE | 30 |  |  |
| 21580 | Olf's T-shirt | NONE | 130 |  |  |
| 21706 | Olf's T-shirt - Event | NONE | 130 |  |  |
| 21988 | Shiny Lit Platform Summon Bracelet | NONE | 30 |  |  |
| 22254 | Mysterious Friend Summon Bracelet - 30-day limited period | NONE | 0 |  |  |
| 22326 | Blue Talisman - Buff Cancel | NONE | 150 |  |  |
| 22327 | Blue Talisman - Buff Steal | NONE | 150 |  |  |
| 677 | One-Piece Swimsuit | D | 150 |  |  |
| 678 | Bikini Set | D | 150 |  |  |
| 679 | Cursed Undergarment Set | D | 150 |  |  |
| 9578 | Linen Shirt | D | 130 |  |  |
| 9584 | Stripe Linen Shirt | D | 130 |  |  |
| 12040 | Common Item - Linen Shirt | D | 43 |  |  |
| 12067 | Common Item - Stripe Linen Shirt | D | 43 |  |  |
| 680 | Mithril Undergarment Set | C | 140 |  |  |
| 681 | Fascination Undergarment Set | C | 140 |  |  |
| 682 | Demon's Undergarment Set | C | 140 |  |  |
| 9579 | Silk Shirt | C | 130 |  |  |
| 9585 | Striped Silk Shirt | C | 130 |  |  |
| 10491 | Silk Shirt - HP | C | 130 |  |  |
| 10492 | Silk Shirt - MP | C | 130 |  |  |
| 10493 | Silk Shirt - CP | C | 130 |  |  |
| 10503 | Striped Silk Shirt - HP | C | 130 |  |  |
| 10504 | Striped Silk Shirt - MP | C | 130 |  |  |
| 10505 | Striped Silk Shirt - CP | C | 130 |  |  |
| 12117 | Common Item - Silk Shirt | C | 43 |  |  |
| 12140 | Common Item - Stripe Silk Shirt | C | 43 |  |  |
| 683 | Holy Undergarment Set | B | 140 |  |  |
| 9580 | Thin Leather Shirt | B | 130 |  |  |
| 9586 | Thin Striped Leather Shirt | B | 130 |  |  |
| 10494 | Thin Leather Shirt - HP | B | 130 |  |  |
| 10495 | Thin Leather Shirt - MP | B | 130 |  |  |
| 10496 | Thin Leather Shirt - CP | B | 130 |  |  |
| 10506 | Thin Striped Leather Shirt - HP | B | 130 |  |  |
| 10507 | Thin Striped Leather Shirt - MP | B | 130 |  |  |
| 10508 | Thin Striped Leather Shirt - CP | B | 130 |  |  |
| 12174 | Common Item - Thin Leather Shirt | B | 43 |  |  |
| 12191 | Common Item - Thin Stripe Leather Shirt | B | 43 |  |  |
| 684 | Underwear of Rule | A | 140 |  |  |
| 9581 | Scale Shirt | A | 130 |  |  |
| 9587 | Striped Scale Shirt | A | 130 |  |  |
| 10207 | Enhanced Striped Scale Shirt | A | 130 |  |  |
| 10497 | Scale Shirt - HP | A | 130 |  |  |
| 10498 | Scale Shirt - MP | A | 130 |  |  |
| 10499 | Scale Shirt - CP | A | 130 |  |  |
| 10509 | Striped Scale Shirt - HP | A | 130 |  |  |
| 10510 | Striped Scale Shirt - MP | A | 130 |  |  |
| 10511 | Striped Scale Shirt - CP | A | 130 |  |  |
| 12219 | Common Item - Barbed Shirt | A | 43 |  |  |
| 12281 | Common Item - Stripe Barbed Shirt | A | 43 |  |  |
| 13296 | Pailaka Shirt | A | 130 |  |  |
| 13389 | Kratei Barbed Shirt - CP | A | 130 |  |  |
| 13391 | Kratei Striped Barbed Shirt - CP | A | 130 |  |  |
| 13751 | Warrior's T-shirt | A | 130 |  |  |
| 685 | Crystal Swimsuit Set | S | 130 |  |  |
| 9582 | Mithril Shirt | S | 130 |  |  |
| 9588 | Striped Mithril Shirt | S | 130 |  |  |
| 10208 | Enhanced Striped Mithril Shirt | S | 130 |  |  |
| 10500 | Mithril Shirt - HP | S | 130 |  |  |
| 10501 | Mithril Shirt - MP | S | 130 |  |  |
| 10502 | Mithril Shirt - CP | S | 130 |  |  |
| 10512 | Striped Mithril Shirt - HP | S | 130 |  |  |
| 10513 | Striped Mithril Shirt - MP | S | 130 |  |  |
| 10514 | Striped Mithril Shirt - CP | S | 130 |  |  |
| 12290 | Common Item - Mithril Shirt | S | 43 |  |  |
| 13390 | Kratei Mithril Shirt - CP | S | 130 |  |  |
| 13392 | Kratei Striped Mithril Shirt - CP | S | 130 |  |  |

### Cloak — `bodypart=back` (38)

#### NONE (38)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 624 | Cloak of Invisibility | NONE | 260 |  |  |
| 2490 | Cloak of Silence | NONE | 250 |  |  |
| 2491 | Golden Yarn Cloak | NONE | 250 |  |  |
| 13527 | Test Cloak | NONE | 260 |  |  |
| 21583 | 7th Anniversary Cloak - Pitch Black | NONE | 220 |  |  |
| 21585 | Festival's Cloak - Pitch Black - Event | NONE | 220 |  |  |
| 21587 | 7th Anniversary Cloak - Blood Red | NONE | 220 |  |  |
| 21588 | 7th Anniversary Cloak - Pearl White | NONE | 220 |  |  |
| 21590 | Festival's Cloak - Pearl White - Event | NONE | 220 |  |  |
| 614 | Knight's Cloak | D | 240 |  |  |
| 615 | Cobweb Cloak | D | 240 |  |  |
| 616 | Cloak of Magic | D | 240 |  |  |
| 617 | Mithril Cloak | D | 240 |  |  |
| 618 | Cloak of Self Protection | C | 240 |  |  |
| 620 | Cloak of Protection | C | 230 |  |  |
| 2492 | Shadow Cloak | C | 240 |  |  |
| 621 | Cloak of Hell | B | 220 |  |  |
| 623 | Divine Cloak | A | 220 |  |  |
| 14601 | Ancient Cloak: Kamael exclusive - Kamael Use | S80 | 220 |  |  |
| 14602 | Ancient Cloak | S80 | 220 |  |  |
| 14608 | Ancient Cloak: Light Armor exclusive | S80 | 220 |  |  |
| 14609 | Ancient Cloak | S80 | 220 |  |  |
| 14610 | Ancient Cloak: Robe exclusive | S80 | 220 |  |  |
| 21716 | Cloak of Zaken | S80 | 220 |  |  |
| 21718 | Cloak of Frintezza | S80 | 220 |  |  |
| 21719 | Soul Cloak of Zaken | S80 | 110 |  |  |
| 21721 | Soul Cloak of Frintezza | S80 | 110 |  |  |
| 13687 | Knight's Cloak | S84 | 220 |  |  |
| 13688 | Knight's Cloak - Light Armor exclusive | S84 | 220 |  |  |
| 13689 | Knight's Cloak - Robe exclusive | S84 | 220 |  |  |
| 13690 | Knight's Cloak - Kamael exclusive | S84 | 220 |  |  |
| 13888 | Sealed Lord's Cloak | S84 | 220 |  |  |
| 13889 | Holy Spirit's Cloak - Kamael exclusive | S84 | 220 |  |  |
| 13890 | Holy Spirit's Cloak | S84 | 220 |  |  |
| 13891 | Holy Spirit's Cloak - Light Armor exclusive | S84 | 220 |  |  |
| 13892 | Holy Spirit's Cloak - Robe exclusive | S84 | 220 |  |  |
| 21717 | Cloak of Freya | S84 | 220 |  |  |
| 21720 | Soul Cloak of Freya | S84 | 110 |  |  |

## Off-hand — `bodypart=lhand` (190)

Shields (`SHIELD`) block physical damage; sigils (`SIGIL`) are magic off-hands for casters. Cannot coexist with a two-handed weapon.

### SIGIL (22)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 13529 | Test Sigil | NONE | 1430 |  |  |
| 14796 | Baguette's Sigil | NONE | 930 |  |  |
| 10119 | Dynasty Sigil | S | 930 |  |  |
| 10120 | Sealed Dynasty Sigil | S | 930 |  |  |
| 10121 | Sealed Arcana Sigil | S | 940 |  |  |
| 12811 | Arcana Sigil | S | 940 |  |  |
| 12812 | Dynasty Sigil | S | 930 |  |  |
| 13078 | Arcana Sigil | S | 940 |  |  |
| 13885 | Sealed Arcana Sigil | S | 940 |  |  |
| 13886 | Sealed Dynasty Sigil | S | 930 |  |  |
| 15622 | Moirai Sigil | S80 | 920 |  |  |
| 15709 | Sealed Moirai Sigil | S80 | 920 |  |  |
| 16305 | Moirai Sigil | S80 | 920 |  |  |
| 16339 | Sealed Moirai Sigil | S80 | 920 |  |  |
| 12813 | Vesper Sigil | S84 | 920 |  |  |
| 13887 | Sealed Vesper Sigil | S84 | 920 |  |  |
| 15588 | Elegia Sigil | S84 | 920 |  |  |
| 15605 | Vorpal Sigil | S84 | 920 |  |  |
| 15742 | Sealed Elegia Sigil | S84 | 920 |  |  |
| 15759 | Sealed Vorpal Sigil | S84 | 920 |  |  |
| 16322 | Vesper Sigil | S84 | 920 |  |  |
| 16356 | Sealed Vesper Sigil | S84 | 920 |  |  |

### NONE (168)

| Id | Name | Grade | Weight | pDef | mDef |
| ---: | --- | --- | ---: | ---: | ---: |
| 18 | Leather Shield | NONE | 1430 |  |  |
| 19 | Small Shield | NONE | 1420 |  |  |
| 20 | Buckler | NONE | 1410 |  |  |
| 102 | Round Shield | NONE | 1390 |  |  |
| 625 | Bone Shield | NONE | 1380 |  |  |
| 945 | Skeleton Buckler | NONE | 1400 |  |  |
| 1328 | Shield of Grace | NONE | 300 |  |  |
| 1329 | Shield of Victory | NONE | 350 |  |  |
| 1330 | Zubei's Shield | NONE | 500 |  |  |
| 1331 | Otherworldly Shield | NONE | 350 |  |  |
| 1332 | Knight's Shield | NONE | 500 |  |  |
| 4222 | Dream Shield | NONE | 1380 |  |  |
| 4223 | Ubiquitous Shield | NONE | 1380 |  |  |
| 6902 | Pledge Shield | NONE | 1380 |  |  |
| 7014 | Monster Only (Shield of Dark Dragon) | NONE | 4800 |  |  |
| 7015 | Shield of Castle Pledge | NONE | 1380 |  |  |
| 8210 | Monster Only (Monk Warrior Shield) | NONE | 4800 |  |  |
| 9036 | Shadow Item: Bone Shield | NONE | 460 |  |  |
| 13525 | Gracian Soldier Shield | NONE | 1300 |  |  |
| 13770 | Shadow Item - Shield of Yehan Miakesh | NONE | 1300 |  |  |
| 13980 | Exclusive to Monsters (Dragon Steed Troop Battle Infantry Shield) | NONE | 1430 |  |  |
| 14791 | Baguette's Shield | NONE | 460 |  |  |
| 20266 | Baguette Shield - 7-day limited period | NONE | 500 |  |  |
| 626 | Bronze Shield | D | 1370 |  |  |
| 627 | Aspis | D | 1350 |  |  |
| 628 | Hoplon | D | 1340 |  |  |
| 629 | Kite Shield | D | 1320 |  |  |
| 630 | Square Shield | D | 1310 |  |  |
| 2493 | Brigandine Shield | D | 1320 |  |  |
| 2494 | Plate Shield | D | 1310 |  |  |
| 5799 | Nephilim Lord | D | 1320 |  |  |
| 9044 | Shadow Item: Hoplon | D | 447 |  |  |
| 12013 | Common Item - Bronze Shield | D | 457 |  |  |
| 12025 | Common Item - Aspis | D | 450 |  |  |
| 12051 | Common Item - Hoplon | D | 447 |  |  |
| 12063 | Common Item - Brigandine Shield | D | 440 |  |  |
| 12069 | Common Item - Kite Shield | D | 440 |  |  |
| 12073 | Common Item - Square Shield | D | 437 |  |  |
| 12078 | Common Item - Plate Shield | D | 437 |  |  |
| 15026 | Brigandine Shield of Fortune - 30-day limited period | D | 1320 |  |  |
| 15140 | Brigandine Shield of Fortune - 10-day limited period | D | 1320 |  |  |
| 16914 | Brigandine Shield of Fortune - 90-day limited period | D | 1320 |  |  |
| 20644 | Common Item - Plate Shield | D | 100 |  |  |
| 103 | Tower Shield | C | 1240 |  |  |
| 107 | Composite Shield | C | 1230 |  |  |
| 631 | Eldarake | C | 1290 |  |  |
| 632 | Knight's Shield | C | 1260 |  |  |
| 2495 | Chain Shield | C | 1280 |  |  |
| 2496 | Dwarven Chain Shield | C | 1280 |  |  |
| 2497 | Full Plate Shield | C | 1220 |  |  |
| 9056 | Shadow Item: Composite Shield | C | 410 |  |  |
| 12091 | Common Item - Eldarake | C | 430 |  |  |
| 12096 | Common Item - Chain Shield | C | 427 |  |  |
| 12102 | Common Item - Dwarven Chain Shield | C | 427 |  |  |
| 12107 | Common Item - Knight's Shield | C | 420 |  |  |
| 12126 | Common Item - Composite Shield | C | 410 |  |  |
| 12129 | Common Item - Tower Shield | C | 413 |  |  |
| 12143 | Common Item - Full Plate Shield | C | 407 |  |  |
| 15016 | Full Plate Shield of Fortune - 30-day limited period | C | 1220 |  |  |
| 15130 | Full Plate Shield of Fortune - 10-day limited period | C | 1220 |  |  |
| 16904 | Full Plate Shield of Fortune - 90-day limited period | C | 1220 |  |  |
| 104 | Shield of Victory | B | 6400 |  |  |
| 105 | Implosion Shield | B | 4800 |  |  |
| 106 | Dark Dragon Shield | B | 4800 |  |  |
| 108 | Masterpiece Shield | B | 5600 |  |  |
| 109 | Shield of Solar Eclipse | B | 4800 |  |  |
| 110 | Doom Shield | B | 1200 |  |  |
| 111 | Shield of Pledge | B | 4800 |  |  |
| 633 | Zubei's Shield | B | 1210 |  |  |
| 635 | Wolf Shield | B | 640 |  |  |
| 636 | Shining Dragon Shield | B | 720 |  |  |
| 637 | Shield of Valor | B | 720 |  |  |
| 638 | Glorious Shield | B | 800 |  |  |
| 639 | Red Flame Shield | B | 960 |  |  |
| 640 | Elven Crystal Shield | B | 720 |  |  |
| 642 | Elven Vagian Shield | B | 560 |  |  |
| 643 | Dark Vagian Shield | B | 560 |  |  |
| 644 | Hell Shield | B | 640 |  |  |
| 645 | Art of Shield | B | 560 |  |  |
| 646 | Shield of Silence | B | 640 |  |  |
| 647 | Gust Shield | B | 720 |  |  |
| 648 | Prairie Shield | B | 800 |  |  |
| 649 | Shield of Underworld | B | 880 |  |  |
| 650 | Shield of Concentration | B | 960 |  |  |
| 651 | Ace's Shield | B | 1040 |  |  |
| 652 | Guardian's Shield | B | 1120 |  |  |
| 653 | Marksman Shield | B | 1200 |  |  |
| 654 | Shield of Mana | B | 480 |  |  |
| 655 | Sage's Shield | B | 560 |  |  |
| 656 | Paradia Shield | B | 480 |  |  |
| 657 | Inferno Shield | B | 560 |  |  |
| 658 | Shield of Black Ore | B | 560 |  |  |
| 659 | Shield of Summoning | B | 480 |  |  |
| 660 | Otherworldly Shield | B | 560 |  |  |
| 661 | Elemental Shield | B | 480 |  |  |
| 662 | Shield of Phantom | B | 560 |  |  |
| 663 | Shield of Grace | B | 480 |  |  |
| 664 | Shield of Holy Spirit | B | 560 |  |  |
| 665 | Phoenix Shield | B | 480 |  |  |
| 666 | Cerberus Shield | B | 560 |  |  |
| 667 | Shield of Aid | B | 480 |  |  |
| 668 | Shield of Blessing | B | 560 |  |  |
| 669 | Flame Shield | B | 480 |  |  |
| 670 | Shield of Bravery | B | 560 |  |  |
| 671 | Blood Shield | B | 480 |  |  |
| 672 | Absolute Shield | B | 560 |  |  |
| 673 | Avadon Shield | B | 1210 |  |  |
| 674 | Divine Shield | B | 560 |  |  |
| 9070 | Shadow Item: Zubei's Shield | B | 403 |  |  |
| 11362 | Zubei's Shield | B | 1210 |  |  |
| 11374 | Avadon Shield | B | 1210 |  |  |
| 11385 | Doom Shield | B | 1200 |  |  |
| 12159 | Common Item - Zubei's Shield | B | 403 |  |  |
| 12171 | Common Item - Avadon Shield | B | 403 |  |  |
| 12183 | Common Item - Doom Shield | B | 400 |  |  |
| 14987 | Avadon Shield of Fortune - 30-day limited period | B | 1210 |  |  |
| 15007 | Doom Shield of Fortune - 30-day limited period | B | 1200 |  |  |
| 15101 | Avadon Shield of Fortune - 10-day limited period | B | 1210 |  |  |
| 15121 | Doom Shield of Fortune - 10-day limited period | B | 1200 |  |  |
| 16875 | Avadon Shield of Fortune - 90-day limited period | B | 1210 |  |  |
| 16895 | Doom Shield of Fortune - 90-day limited period | B | 1200 |  |  |
| 641 | Dark Crystal Shield | A | 1190 |  |  |
| 2498 | Shield of Nightmare | A | 1180 |  |  |
| 5292 | Sealed Dark Crystal Shield | A | 1190 |  |  |
| 5315 | Sealed Shield of Nightmare | A | 1180 |  |  |
| 9084 | Shadow Item: Dark Crystal Shield | A | 397 |  |  |
| 9129 | Shadow Item: Shield of Nightmare | A | 400 |  |  |
| 11416 | Dark Crystal Shield | A | 1190 |  |  |
| 11425 | Sealed Dark Crystal Shield | A | 1190 |  |  |
| 11469 | Sealed Shield of Nightmare | A | 1180 |  |  |
| 11480 | Shield of Nightmare | A | 1180 |  |  |
| 12215 | Common Item - Dark Crystal Shield | A | 397 |  |  |
| 12225 | Common Item - Sealed Dark Crystal Shield | A | 397 |  |  |
| 12268 | Common Item - Sealed Shield of Nightmare | A | 393 |  |  |
| 12279 | Common Item - Shield of Nightmare | A | 393 |  |  |
| 14982 | Dark Crystal Shield of Fortune - 30-day limited period | A | 1190 |  |  |
| 15031 | Fortune Shield of Nightmare - 30-day limited period | A | 1180 |  |  |
| 15096 | Dark Crystal Shield of Fortune - 10-day limited period | A | 1190 |  |  |
| 15145 | Fortune Shield of Nightmare - 10-day limited period | A | 1180 |  |  |
| 16870 | Dark Crystal Shield of Fortune - 90-day limited period | A | 1190 |  |  |
| 16919 | Fortune Shield of Nightmare - 90-day limited period | A | 1180 |  |  |
| 634 | Dragon Shield | S | 1170 |  |  |
| 6377 | Imperial Crusader Shield | S | 1170 |  |  |
| 6678 | Sealed Imperial Crusader Shield | S | 1170 |  |  |
| 9441 | Dynasty Shield | S | 1150 |  |  |
| 9529 | Sealed Dynasty Shield | S | 1150 |  |  |
| 11502 | Sealed Imperial Crusader Shield | S | 1170 |  |  |
| 11508 | Imperial Crusader Shield | S | 1170 |  |  |
| 11532 | Dynasty Shield | S | 1390 |  |  |
| 11569 | Sealed Dynasty Shield | S | 1370 |  |  |
| 12302 | Common Item - Sealed Imperial Crusader Shield | S | 390 |  |  |
| 12308 | Common Item - Imperial Crusader Shield | S | 390 |  |  |
| 21780 | Imperial Crusader Shield of Fortune - 90-day limited period | S | 1170 |  |  |
| 21791 | Arcana Sickle of Fortune - 90-day limited period | S | 940 |  |  |
| 21798 | Dynasty Shield of Fortune - 90-day limited period | S | 1150 |  |  |
| 21811 | Dynasty Sickle of Fortune - 90-day limited period | S | 930 |  |  |
| 15621 | Moirai Shield | S80 | 1190 |  |  |
| 15710 | Sealed Moirai Shield | S80 | 1190 |  |  |
| 16304 | Moirai Shield | S80 | 1190 |  |  |
| 16338 | Sealed Moirai Shield | S80 | 1190 |  |  |
| 13471 | Vesper Shield | S84 | 1130 |  |  |
| 14111 | Sealed Vesper Shield | S84 | 1130 |  |  |
| 15587 | Elegia Shield | S84 | 1190 |  |  |
| 15604 | Vorpal Shield | S84 | 1190 |  |  |
| 15741 | Sealed Elegia Shield | S84 | 1190 |  |  |
| 15758 | Sealed Vorpal Shield | S84 | 1190 |  |  |
| 16321 | Vesper Shield | S84 | 1130 |  |  |
| 16355 | Sealed Vesper Shield | S84 | 1130 |  |  |

## Jewelry & accessories (1662)

### Necklace — `bodypart=neck` (140)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 118 | Necklace of Magic | NONE | 150 |  |  |
| 906 | Necklace of Knowledge | NONE | 150 |  |  |
| 907 | Necklace of Anguish | NONE | 150 |  |  |
| 908 | Necklace of Wisdom | NONE | 150 |  |  |
| 909 | Blue Diamond Necklace | NONE | 150 |  |  |
| 1506 | Necklace of Courage | NONE | 150 |  |  |
| 1507 | Necklace of Valor | NONE | 150 |  |  |
| 12746 | Crystal Pendant | NONE | 150 |  |  |
| 12747 | Ruby Pendant | NONE | 150 |  |  |
| 12748 | Sapphire Pendant | NONE | 150 |  |  |
| 12749 | Diamond Pendant | NONE | 150 |  |  |
| 12750 | Enria Pendant | NONE | 150 |  |  |
| 12751 | Thons Pendant | NONE | 150 |  |  |
| 12752 | Asofe Pendant | NONE | 150 |  |  |
| 17187 | National Representative Warrior's Necklace - 3-day limited period | NONE | 150 |  |  |
| 17190 | National Representative Warrior's Necklace - 7-day limited period | NONE | 150 |  |  |
| 17193 | National Representative Warrior's Necklace - 10-day limited period | NONE | 150 |  |  |
| 17196 | National Representative Warrior's Necklace - 30-day limited period | NONE | 150 |  |  |
| 17199 | National Representative Warrior's Necklace | NONE | 150 |  |  |
| 22211 | Angry Bunny Necklace - 7-day limited period (event) | NONE | 30 |  |  |
| 22214 | Angry Bunny Necklace - 30-day limited period (event) | NONE | 30 |  |  |
| 910 | Necklace of Devotion | D | 150 |  |  |
| 911 | Enchanted Necklace | D | 150 |  |  |
| 912 | Near Forest Necklace | D | 150 |  |  |
| 913 | Elven Necklace | D | 150 |  |  |
| 914 | Necklace of Darkness | D | 150 |  |  |
| 10123 | Necklace of Devotion | D | 150 |  |  |
| 10472 | Shadow Item - Necklace of Devotion | D | 150 |  |  |
| 12312 | Common Item - Necklace of Devotion | D | 50 |  |  |
| 12315 | Common Item - Enchanted Necklace | D | 50 |  |  |
| 12317 | Common Item - Near Forest Necklace | D | 50 |  |  |
| 12320 | Common Item - Elven Necklace | D | 50 |  |  |
| 12324 | Common Item - Necklace of Darkness | D | 50 |  |  |
| 14976 | Elven Earring of Fortune - 30-day limited period | D | 150 |  |  |
| 15090 | Elven Earring of Fortune - 10-day limited period | D | 150 |  |  |
| 16864 | Elven Earring of Fortune - 90-day limited period | D | 150 |  |  |
| 119 | Necklace of Seal | C | 150 |  |  |
| 915 | Aquastone Necklace | C | 150 |  |  |
| 916 | Necklace of Protection | C | 150 |  |  |
| 917 | Necklace of Mermaid | C | 150 |  |  |
| 919 | Blessed Necklace | C | 150 |  |  |
| 12327 | Common Item - Aquastone Necklace | C | 50 |  |  |
| 12330 | Common Item - Necklace of Protection | C | 50 |  |  |
| 12334 | Common Item - Necklace of Mermaid | C | 50 |  |  |
| 12336 | Common Item - Necklace of Seal | C | 50 |  |  |
| 14973 | Fortune Necklace of Seal - 30-day limited period | C | 150 |  |  |
| 15087 | Fortune Necklace of Seal - 10-day limited period | C | 150 |  |  |
| 16861 | Fortune Necklace of Seal - 90-day limited period | C | 150 |  |  |
| 918 | Adamantite Necklace | B | 150 |  |  |
| 921 | Necklace of Mana | B | 150 |  |  |
| 922 | Sage's Necklace | B | 150 |  |  |
| 923 | Paradia Necklace | B | 150 |  |  |
| 925 | Necklace of Solar Eclipse | B | 150 |  |  |
| 926 | Necklace of Black Ore | B | 150 |  |  |
| 927 | Necklace of Summoning | B | 150 |  |  |
| 928 | Otherworldly Necklace | B | 150 |  |  |
| 929 | Elemental Necklace | B | 150 |  |  |
| 931 | Necklace of Grace | B | 150 |  |  |
| 932 | Necklace of Holy Spirit | B | 150 |  |  |
| 935 | Necklace of Aid | B | 150 |  |  |
| 936 | Necklace of Blessing | B | 150 |  |  |
| 11576 | Adamantite Necklace | B | 150 |  |  |
| 11579 | Necklace of Black Ore | B | 150 |  |  |
| 12339 | Common Item - Adamantite Necklace | B | 50 |  |  |
| 12342 | Common Item - Necklace of Black Ore | B | 50 |  |  |
| 14970 | Fortune Necklace of Black Ore - 30-day limited period | B | 150 |  |  |
| 15084 | Fortune Necklace of Black Ore - 10-day limited period | B | 150 |  |  |
| 16858 | Fortune Necklace of Black Ore - 90-day limited period | B | 150 |  |  |
| 924 | Majestic Necklace | A | 150 |  |  |
| 930 | Necklace of Phantom | A | 150 |  |  |
| 933 | Phoenix Necklace | A | 150 |  |  |
| 934 | Cerberus Necklace | A | 150 |  |  |
| 6323 | Sealed Phoenix Necklace | A | 150 |  |  |
| 6326 | Sealed Majestic Necklace | A | 150 |  |  |
| 8191 | Necklace of Frintezza | A | 150 |  |  |
| 11581 | Sealed Phoenix Necklace | A | 150 |  |  |
| 11584 | Phoenix Necklace | A | 150 |  |  |
| 11587 | Majestic Necklace | A | 150 |  |  |
| 11590 | Sealed Majestic Necklace | A | 150 |  |  |
| 12344 | Common Item - Sealed Phoenix Necklace | A | 50 |  |  |
| 12347 | Common Item - Phoenix Necklace | A | 50 |  |  |
| 12350 | Common Item - Sealed Majestic Necklace | A | 50 |  |  |
| 12353 | Common Item - Majestic Necklace | A | 50 |  |  |
| 13740 | Gludio Water Resistance Necklace | A | 150 |  |  |
| 13741 | Dion Holy Resistance Necklace | A | 150 |  |  |
| 13742 | Giran Wind Resistance Necklace | A | 150 |  |  |
| 13743 | Oren Dark Resistance Necklace | A | 150 |  |  |
| 13744 | Aden Earth Resistance Necklace | A | 150 |  |  |
| 13745 | Innadril Water Resistance Necklace | A | 150 |  |  |
| 13746 | Goddard Fire Resistance Necklace | A | 150 |  |  |
| 13747 | Rune Fire Resistance Necklace | A | 150 |  |  |
| 13748 | Schuttgart Wind Resistance Necklace | A | 150 |  |  |
| 13753 | Olympiad Warrior's Necklace | A | 150 |  |  |
| 14967 | Majestic Necklace of Fortune - 30-day limited period | A | 150 |  |  |
| 15081 | Majestic Necklace of Fortune - 10-day limited period | A | 150 |  |  |
| 16855 | Majestic Necklace of Fortune - 90-day limited period | A | 150 |  |  |
| 920 | Tateossian Necklace | S | 150 |  |  |
| 6657 | Necklace of Valakas | S | 150 |  |  |
| 6726 | Sealed Tateossian Necklace | S | 150 |  |  |
| 9453 | Sealed Dynasty Necklace | S | 150 |  |  |
| 9456 | Dynasty Necklace | S | 150 |  |  |
| 9459 | Dynasty Necklace - Stun Resistance | S | 150 |  |  |
| 9462 | Dynasty Necklace - Poison Resistance | S | 150 |  |  |
| 9465 | Dynasty Necklace - Bleed Resistance | S | 150 |  |  |
| 9468 | Dynasty Necklace - Sleep Resistance | S | 150 |  |  |
| 9471 | Dynasty Necklace - Paralysis Resistance | S | 150 |  |  |
| 9474 | Dynasty Necklace - Hold Resistance | S | 150 |  |  |
| 9477 | Dynasty Necklace - Fear Resistance | S | 150 |  |  |
| 11593 | Sealed Tateossian Necklace | S | 150 |  |  |
| 11596 | Tateossian Necklace | S | 150 |  |  |
| 11599 | Dynasty Necklace | S | 150 |  |  |
| 11602 | Sealed Dynasty Necklace | S | 150 |  |  |
| 12356 | Common Item - Sealed Tateossian Necklace | S | 50 |  |  |
| 12359 | Common Item - Tateossian Necklace | S | 50 |  |  |
| 21221 | Valakas's Necklace - 180-day limited period | S | 150 |  |  |
| 21815 | Tateossian Necklace of Fortune - 90-day limited period | S | 150 |  |  |
| 21818 | Dynasty Necklace of Fortune - 90-day limited period | S | 150 |  |  |
| 15282 | Gludio Water Royal Guard Necklace | S80 | 150 |  |  |
| 15283 | Dion Holy Royal Guard Necklace | S80 | 150 |  |  |
| 15284 | Giran Wind Royal Guard Necklace | S80 | 150 |  |  |
| 15285 | Oren Dark Royal Guard Necklace | S80 | 150 |  |  |
| 15286 | Aden Earth Royal Guard Necklace | S80 | 150 |  |  |
| 15287 | Innadril Water Royal Guard Necklace | S80 | 150 |  |  |
| 15288 | Goddard Fire Royal Guard Necklace | S80 | 150 |  |  |
| 15289 | Rune Fire Royal Guard Necklace | S80 | 150 |  |  |
| 15290 | Schuttgart Wind Royal Guard Necklace | S80 | 150 |  |  |
| 15725 | Moirai Necklace | S80 | 150 |  |  |
| 15768 | Sealed Moirai Necklace | S80 | 150 |  |  |
| 16374 | Sealed Moirai Necklace | S80 | 150 |  |  |
| 16380 | Moirai Necklace | S80 | 150 |  |  |
| 14161 | Sealed Vesper Necklace | S84 | 150 |  |  |
| 14164 | Vesper Necklace | S84 | 150 |  |  |
| 15719 | Elegia Necklace | S84 | 150 |  |  |
| 15722 | Vorpal Necklace | S84 | 150 |  |  |
| 15762 | Sealed Elegia Necklace | S84 | 150 |  |  |
| 15765 | Sealed Vorpal Necklace | S84 | 150 |  |  |
| 16025 | Necklace of Freya | S84 | 150 |  |  |
| 16026 | Blessed Necklace of Freya | S84 | 150 |  |  |
| 16371 | Sealed Vesper Necklace | S84 | 150 |  |  |
| 16377 | Vesper Necklace | S84 | 150 |  |  |

### Earring — `bodypart=rear;lear` (143)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 112 | Apprentice's Earring | NONE | 150 |  |  |
| 113 | Mystic's Earring | NONE | 150 |  |  |
| 114 | Earring of Strength | NONE | 150 |  |  |
| 115 | Earring of Wisdom | NONE | 150 |  |  |
| 845 | Cat's Eye Earring | NONE | 150 |  |  |
| 846 | Coral Earring | NONE | 150 |  |  |
| 17188 | National Representative Warrior's Earring - 3-day limited period | NONE | 150 |  |  |
| 17191 | National Representative Warrior's Earring - 7-day limited period | NONE | 150 |  |  |
| 17194 | National Representative Warrior's Earring - 10-day limited period | NONE | 150 |  |  |
| 17197 | National Representative Warrior's Earring - 30-day limited period | NONE | 150 |  |  |
| 17200 | National Representative Warrior's Earring | NONE | 150 |  |  |
| 22212 | Angry Bunny Earring - 7-day limited period (event) | NONE | 30 |  |  |
| 22215 | Angry Bunny Earring - 30-day limited period (event) | NONE | 30 |  |  |
| 847 | Red Crescent Earring | D | 150 |  |  |
| 848 | Enchanted Earring | D | 150 |  |  |
| 849 | Tiger's Eye Earring | D | 150 |  |  |
| 850 | Elven Earring | D | 150 |  |  |
| 851 | Omen Beast's Eye Earring | D | 150 |  |  |
| 10122 | Red Crescent Earring | D | 150 |  |  |
| 10470 | Shadow Item - Red Crescent | D | 150 |  |  |
| 12311 | Common Item - Red Crescent | D | 50 |  |  |
| 12314 | Common Item - Enchanted Earring | D | 50 |  |  |
| 12318 | Common Item - Tiger's Eye | D | 50 |  |  |
| 12322 | Common Item - Elven Earring | D | 50 |  |  |
| 12325 | Common Item - Omen Beast's Eye | D | 50 |  |  |
| 13293 | Pailaka Earring | D | 150 |  |  |
| 14975 | Elven Earring of Fortune - 30-day limited period | D | 150 |  |  |
| 15089 | Elven Earring of Fortune - 10-day limited period | D | 150 |  |  |
| 16863 | Elven Earring of Fortune - 90-day limited period | D | 150 |  |  |
| 852 | Moonstone Earring | C | 150 |  |  |
| 853 | Earring of Protection | C | 150 |  |  |
| 854 | Earring of Seal | C | 150 |  |  |
| 855 | Nassen's Earring | C | 150 |  |  |
| 857 | Blessed Earring | C | 150 |  |  |
| 12326 | Common Item - Moonstone Earring | C | 50 |  |  |
| 12329 | Common Item - Earring of Protection | C | 50 |  |  |
| 12332 | Common Item - Earring of Seal | C | 50 |  |  |
| 12335 | Common Item - Nassen's Earring | C | 50 |  |  |
| 14972 | Fortune Earring of Seal - 30-day limited period | C | 150 |  |  |
| 15086 | Fortune Earring of Seal - 10-day limited period | C | 150 |  |  |
| 16860 | Fortune Earring of Seal - 90-day limited period | C | 150 |  |  |
| 856 | Adamantite Earring | B | 150 |  |  |
| 859 | Earring of Mana | B | 150 |  |  |
| 860 | Sage's Earring | B | 150 |  |  |
| 861 | Paradia Earring | B | 150 |  |  |
| 863 | Earring of Solar Eclipse | B | 150 |  |  |
| 864 | Earring of Black Ore | B | 150 |  |  |
| 865 | Earring of Summoning | B | 150 |  |  |
| 866 | Otherworldly Earring | B | 150 |  |  |
| 867 | Elemental Earring | B | 150 |  |  |
| 869 | Earring of Grace | B | 150 |  |  |
| 870 | Earring of Holy Spirit | B | 150 |  |  |
| 873 | Earring of Aid | B | 150 |  |  |
| 874 | Earring of Blessing | B | 150 |  |  |
| 11575 | Adamantite Earring | B | 150 |  |  |
| 11578 | Earring of Black Ore | B | 150 |  |  |
| 12338 | Common Item - Adamantite Earring | B | 50 |  |  |
| 12341 | Common Item - Earring of Black Ore | B | 50 |  |  |
| 14969 | Fortune Earring of Black Ore - 30-day limited period | B | 150 |  |  |
| 15083 | Fortune Earring of Black Ore - 10-day limited period | B | 150 |  |  |
| 16857 | Fortune Earring of Black Ore - 90-day limited period | B | 150 |  |  |
| 862 | Majestic Earring | A | 150 |  |  |
| 868 | Earring of Phantom | A | 150 |  |  |
| 871 | Phoenix Earring | A | 150 |  |  |
| 872 | Cerberus Earring | A | 150 |  |  |
| 6324 | Sealed Phoenix Earring | A | 150 |  |  |
| 6327 | Sealed Majestic Earring | A | 150 |  |  |
| 6661 | Earring of Orfen | A | 150 |  |  |
| 11583 | Sealed Phoenix Earring | A | 150 |  |  |
| 11586 | Phoenix Earring | A | 150 |  |  |
| 11589 | Majestic Earring | A | 150 |  |  |
| 11592 | Sealed Majestic Earring | A | 150 |  |  |
| 12345 | Common Item - Sealed Phoenix Earring | A | 50 |  |  |
| 12349 | Common Item - Phoenix Earring | A | 50 |  |  |
| 12352 | Common Item - Sealed Majestic Earring | A | 50 |  |  |
| 12355 | Common Item - Majestic Earring | A | 50 |  |  |
| 13754 | Olympiad Warrior's Earring | A | 150 |  |  |
| 14664 | Gludio Protection Earring | A | 150 |  |  |
| 14665 | Dion Protection Earring | A | 150 |  |  |
| 14666 | Giran Protection Earring | A | 150 |  |  |
| 14667 | Oren Protection Earring | A | 150 |  |  |
| 14668 | Aden Protection Earring | A | 150 |  |  |
| 14669 | Innadril Protection Earring | A | 150 |  |  |
| 14670 | Goddard Protection Earring | A | 150 |  |  |
| 14671 | Rune Protection Earring | A | 150 |  |  |
| 14672 | Schuttgart Protection Earring | A | 150 |  |  |
| 14966 | Majestic Earring of Fortune - 30-day limited period | A | 150 |  |  |
| 15080 | Majestic Earring of Fortune - 10-day limited period | A | 150 |  |  |
| 15428 | 6th Anniversary Party Earring (Event) - 30-day limited period | A | 150 |  |  |
| 16854 | Majestic Earring of Fortune - 90-day limited period | A | 150 |  |  |
| 858 | Tateossian Earring | S | 150 |  |  |
| 6656 | Earring of Antharas | S | 150 |  |  |
| 6659 | Earring of Zaken | S | 150 |  |  |
| 6724 | Sealed Tateossian Earring | S | 150 |  |  |
| 9452 | Sealed Dynasty Earring | S | 150 |  |  |
| 9455 | Dynasty Earrings | S | 150 |  |  |
| 9458 | Dynasty Earrings - Stun Resistance | S | 150 |  |  |
| 9461 | Dynasty Earrings - Poison Resistance | S | 150 |  |  |
| 9464 | Dynasty Earrings - Bleed Resistance | S | 150 |  |  |
| 9467 | Dynasty Earrings - Sleep Resistance | S | 150 |  |  |
| 9470 | Dynasty Earrings - Paralysis Resistance | S | 150 |  |  |
| 9473 | Dynasty Earrings - Hold Resistance | S | 150 |  |  |
| 9476 | Dynasty Earrings - Fear Resistance | S | 150 |  |  |
| 11595 | Sealed Tateossian Earring | S | 150 |  |  |
| 11598 | Tateossian Earring | S | 150 |  |  |
| 11601 | Dynasty Earrings | S | 150 |  |  |
| 11604 | Sealed Dynasty Earring | S | 150 |  |  |
| 12358 | Common Item - Sealed Tateossian Earring | S | 50 |  |  |
| 12361 | Common Item - Tateossian Earring | S | 50 |  |  |
| 20207 | Earring of Zaken (Event) - 3-day limited period | S | 150 |  |  |
| 20208 | Earring of Zaken (Event) - 7-day limited period | S | 150 |  |  |
| 20209 | Earring of Zaken (Event) - 15-day limited period | S | 150 |  |  |
| 21208 | Earring of Zaken - 30-day limited period | S | 150 |  |  |
| 21220 | Earring of Zaken - 180-day limited period | S | 150 |  |  |
| 21222 | Antharas's Earring - 180-day limited period | S | 150 |  |  |
| 21813 | Tateossian Earring of Fortune - 90-day limited period | S | 150 |  |  |
| 21817 | Dynasty Earrings of Fortune - 90-day limited period | S | 150 |  |  |
| 22302 | Antharas's Earring - 3-day limited period (event) | S | 150 |  |  |
| 22303 | Antharas's Earring - 7-day limited period (event) | S | 150 |  |  |
| 10170 | Baylor's Earring | S80 | 150 |  |  |
| 14801 | Gludio Guard Earring | S80 | 150 |  |  |
| 14802 | Dion Guard Earring | S80 | 150 |  |  |
| 14803 | Giran Guard Earring | S80 | 150 |  |  |
| 14804 | Oren Guard Earring | S80 | 150 |  |  |
| 14805 | Aden Guard Earring | S80 | 150 |  |  |
| 14806 | Innadril Guard Earring | S80 | 150 |  |  |
| 14807 | Goddard Guard Earring | S80 | 150 |  |  |
| 14808 | Rune Guard Earring | S80 | 150 |  |  |
| 14809 | Schuttgart Guard Earring | S80 | 150 |  |  |
| 15724 | Moirai Earring | S80 | 150 |  |  |
| 15767 | Sealed Moirai Earring | S80 | 150 |  |  |
| 16373 | Sealed Moirai Earring | S80 | 150 |  |  |
| 16379 | Moirai Earring | S80 | 150 |  |  |
| 14160 | Sealed Vesper Earring | S84 | 150 |  |  |
| 14163 | Vesper Earring | S84 | 150 |  |  |
| 15718 | Elegia Earring | S84 | 150 |  |  |
| 15721 | Vorpal Earring | S84 | 150 |  |  |
| 15761 | Sealed Elegia Earring | S84 | 150 |  |  |
| 15764 | Sealed Vorpal Earring | S84 | 150 |  |  |
| 16370 | Sealed Vesper Earring | S84 | 150 |  |  |
| 16376 | Vesper Earring | S84 | 150 |  |  |
| 21712 | Blessed Earring of Zaken | S84 | 150 |  |  |
| 22175 | Improved Blessed Earring of Zaken | S84 | 150 |  |  |

### Ring — `bodypart=rfinger;lfinger` (153)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 116 | Magic Ring | NONE | 150 |  |  |
| 875 | Ring of Knowledge | NONE | 150 |  |  |
| 876 | Ring of Anguish | NONE | 150 |  |  |
| 877 | Ring of Wisdom | NONE | 150 |  |  |
| 878 | Blue Coral Ring | NONE | 150 |  |  |
| 1508 | Ring of Raccoon | NONE | 150 |  |  |
| 1509 | Ring of Firefly | NONE | 150 |  |  |
| 9899 | Weight Loss Ring | NONE | 150 |  |  |
| 9900 | Quiet Footsteps Ring | NONE | 150 |  |  |
| 10140 | Blessed Ring of Escape | NONE | 150 |  |  |
| 10211 | Blessed Ring of Resurrection | NONE | 150 |  |  |
| 17050 | Shiny Couple Ring | NONE | 0 |  |  |
| 17186 | National Representative Warrior's Ring - 3-day limited period | NONE | 150 |  |  |
| 17189 | National Representative Warrior's Ring - 7-day limited period | NONE | 150 |  |  |
| 17192 | National Representative Warrior's Ring - 10-day limited period | NONE | 150 |  |  |
| 17195 | National Representative Warrior's Ring - 30-day limited period | NONE | 150 |  |  |
| 17198 | National Representative Warrior's Ring | NONE | 150 |  |  |
| 21159 | Wedding Ring - Male | NONE | 150 |  |  |
| 21160 | Wedding Ring - Female | NONE | 150 |  |  |
| 22213 | Angry Bunny Ring - 7-day limited period (event) | NONE | 30 |  |  |
| 22216 | Angry Bunny Ring - 30-day limited period (event) | NONE | 30 |  |  |
| 22237 | Shiny Couple Ring | NONE | 0 |  |  |
| 879 | Enchanted Ring | D | 150 |  |  |
| 880 | Black Pearl Ring | D | 150 |  |  |
| 881 | Elven Ring | D | 150 |  |  |
| 882 | Mithril Ring | D | 150 |  |  |
| 890 | Ring of Devotion | D | 150 |  |  |
| 10124 | Ring of Devotion | D | 150 |  |  |
| 10471 | Shadow Item - Ring of Devotion | D | 150 |  |  |
| 12313 | Common Item - Ring of Devotion | D | 50 |  |  |
| 12316 | Common Item - Enchanted Ring | D | 50 |  |  |
| 12319 | Common Item - Black Pearl Ring | D | 50 |  |  |
| 12321 | Common Item - Elven Ring | D | 50 |  |  |
| 12323 | Common Item - Mithril Ring | D | 50 |  |  |
| 13294 | Pailaka Ring | D | 150 |  |  |
| 14977 | Elven Ring of Fortune - 30-day limited period | D | 150 |  |  |
| 15091 | Elven Ring of Fortune - 10-day limited period | D | 150 |  |  |
| 16865 | Elven Ring of Fortune - 90-day limited period | D | 150 |  |  |
| 883 | Aquastone Ring | C | 150 |  |  |
| 884 | Ring of Protection | C | 150 |  |  |
| 885 | Ring of Ages | C | 150 |  |  |
| 886 | Ring of Seal | C | 150 |  |  |
| 888 | Blessed Ring | C | 150 |  |  |
| 12328 | Common Item - Aquastone Ring | C | 50 |  |  |
| 12331 | Common Item - Ring of Protection | C | 50 |  |  |
| 12333 | Common Item - Ring of Ages | C | 50 |  |  |
| 12337 | Common Item - Ring of Seal | C | 50 |  |  |
| 14974 | Fortune Ring of Seal - 30-day limited period | C | 150 |  |  |
| 15088 | Fortune Ring of Seal - 10-day limited period | C | 150 |  |  |
| 16862 | Fortune Ring of Seal - 90-day limited period | C | 150 |  |  |
| 117 | Ring of Mana | B | 150 |  |  |
| 887 | Adamantite Ring | B | 150 |  |  |
| 891 | Sage's Ring | B | 150 |  |  |
| 892 | Paradia Ring | B | 150 |  |  |
| 894 | Ring of Solar Eclipse | B | 150 |  |  |
| 895 | Ring of Black Ore | B | 150 |  |  |
| 896 | Ring of Summoning | B | 150 |  |  |
| 897 | Otherworldly Ring | B | 150 |  |  |
| 898 | Elemental Ring | B | 150 |  |  |
| 900 | Ring of Grace | B | 150 |  |  |
| 901 | Ring of Holy Spirit | B | 150 |  |  |
| 904 | Ring of Aid | B | 150 |  |  |
| 905 | Ring of Blessing | B | 150 |  |  |
| 6660 | Ring of Queen Ant | B | 150 |  |  |
| 9677 | Ring of Wind Mastery | B | 150 |  |  |
| 11577 | Adamantite Ring | B | 150 |  |  |
| 11580 | Ring of Black Ore | B | 150 |  |  |
| 12340 | Common Item - Adamantite Ring | B | 50 |  |  |
| 12343 | Common Item - Ring of Black Ore | B | 50 |  |  |
| 14971 | Fortune Ring of Black Ore - 30-day limited period | B | 150 |  |  |
| 15085 | Fortune Ring of Black Ore - 10-day limited period | B | 150 |  |  |
| 16859 | Fortune Ring of Black Ore - 90-day limited period | B | 150 |  |  |
| 20204 | Queen Ant's Ring (Event) - 3-day limited period | B | 150 |  |  |
| 20205 | Queen Ant's Ring (Event) - 7-day limited period | B | 150 |  |  |
| 20206 | Queen Ant's Ring (Event) - 15-day limited period | B | 150 |  |  |
| 21206 | Queen Ant's Ring - 30-day limited period | B | 150 |  |  |
| 21218 | Queen Ant's Ring - 180-day limited period | B | 150 |  |  |
| 22174 | Improved Ring of Queen Ant | B | 150 |  |  |
| 893 | Majestic Ring | A | 150 |  |  |
| 899 | Ring of Phantom | A | 150 |  |  |
| 902 | Phoenix Ring | A | 150 |  |  |
| 903 | Cerberus Ring | A | 150 |  |  |
| 6325 | Sealed Phoenix Ring | A | 150 |  |  |
| 6328 | Sealed Majestic Ring | A | 150 |  |  |
| 6662 | Ring of Core | A | 150 |  |  |
| 11582 | Sealed Phoenix Ring | A | 150 |  |  |
| 11585 | Phoenix Ring | A | 150 |  |  |
| 11588 | Majestic Ring | A | 150 |  |  |
| 11591 | Sealed Majestic Ring | A | 150 |  |  |
| 12346 | Common Item - Sealed Phoenix Ring | A | 50 |  |  |
| 12348 | Common Item - Phoenix Ring | A | 50 |  |  |
| 12351 | Common Item - Sealed Majestic Ring | A | 50 |  |  |
| 12354 | Common Item - Majestic Ring | A | 50 |  |  |
| 13752 | Olympiad Warrior's Ring | A | 150 |  |  |
| 14592 | Gludio Earth Resistance Ring | A | 150 |  |  |
| 14593 | Dion Water Resistance Ring | A | 150 |  |  |
| 14594 | Giran Fire Resistance Ring | A | 150 |  |  |
| 14595 | Oren Earth Resistance Ring | A | 150 |  |  |
| 14596 | Aden Holy Resistance Ring | A | 150 |  |  |
| 14597 | Innadril Holy Resistance Ring | A | 150 |  |  |
| 14598 | Goddard Dark Resistance Ring | A | 150 |  |  |
| 14599 | Rune Wind Resistance Ring | A | 150 |  |  |
| 14600 | Schuttgart Dark Resistance Ring | A | 150 |  |  |
| 14968 | Majestic Ring of Fortune - 30-day limited period | A | 150 |  |  |
| 15082 | Majestic Ring of Fortune - 10-day limited period | A | 150 |  |  |
| 16856 | Majestic Ring of Fortune - 90-day limited period | A | 150 |  |  |
| 889 | Tateossian Ring | S | 150 |  |  |
| 6658 | Ring of Baium | S | 150 |  |  |
| 6725 | Sealed Tateossian Ring | S | 150 |  |  |
| 9454 | Sealed Dynasty Ring | S | 150 |  |  |
| 9457 | Dynasty Ring | S | 150 |  |  |
| 9460 | Dynasty Ring - Stun Resistance | S | 150 |  |  |
| 9463 | Dynasty Ring - Poison Resistance | S | 150 |  |  |
| 9466 | Dynasty Ring - Bleed Resistance | S | 150 |  |  |
| 9469 | Dynasty Ring - Sleep Resistance | S | 150 |  |  |
| 9472 | Dynasty Ring - Paralysis Resistance | S | 150 |  |  |
| 9475 | Dynasty Ring - Hold Resistance | S | 150 |  |  |
| 9478 | Dynasty Ring - Fear Resistance | S | 150 |  |  |
| 10314 | Ring of Beleth | S | 150 |  |  |
| 11594 | Sealed Tateossian Ring | S | 150 |  |  |
| 11597 | Tateossian Ring | S | 150 |  |  |
| 11600 | Dynasty Ring | S | 150 |  |  |
| 11603 | Sealed Dynasty Ring | S | 150 |  |  |
| 12357 | Common Item - Sealed Tateossian Ring | S | 50 |  |  |
| 12360 | Common Item - Tateossian Ring | S | 50 |  |  |
| 21207 | Baium's Ring - 30-day limited period | S | 150 |  |  |
| 21219 | Baium's Ring - 180-day limited period | S | 150 |  |  |
| 21814 | Tateossian Ring of Fortune - 90-day limited period | S | 150 |  |  |
| 21819 | Dynasty Ring of Fortune - 90-day limited period | S | 150 |  |  |
| 22173 | Improved Ring of Baium | S | 150 |  |  |
| 22304 | Baium's Ring - 3-day limited period (event) | S | 150 |  |  |
| 22305 | Baium's Ring - 7-day limited period (event) | S | 150 |  |  |
| 15291 | Gludio Earth Royal Guard Ring | S80 | 150 |  |  |
| 15292 | Dion Water Royal Guard Ring | S80 | 150 |  |  |
| 15293 | Giran Fire Royal Guard Ring | S80 | 150 |  |  |
| 15294 | Oren Earth Royal Guard Ring | S80 | 150 |  |  |
| 15295 | Aden Holy Royal Guard Ring | S80 | 150 |  |  |
| 15296 | Innadril Holy Royal Guard Ring | S80 | 150 |  |  |
| 15297 | Goddard Dark Royal Guard Ring | S80 | 150 |  |  |
| 15298 | Rune Wind Royal Guard Ring | S80 | 150 |  |  |
| 15299 | Schuttgart Dark Royal Guard Ring | S80 | 150 |  |  |
| 15723 | Moirai Ring | S80 | 150 |  |  |
| 15766 | Sealed Moirai Ring | S80 | 150 |  |  |
| 16372 | Sealed Moirai Ring | S80 | 150 |  |  |
| 16378 | Moirai Ring | S80 | 150 |  |  |
| 14162 | Sealed Vesper Ring | S84 | 150 |  |  |
| 14165 | Vesper Ring | S84 | 150 |  |  |
| 15717 | Elegia Ring | S84 | 150 |  |  |
| 15720 | Vorpal Ring | S84 | 150 |  |  |
| 15760 | Sealed Elegia Ring | S84 | 150 |  |  |
| 15763 | Sealed Vorpal Ring | S84 | 150 |  |  |
| 16369 | Sealed Vesper Ring | S84 | 150 |  |  |
| 16375 | Vesper Ring | S84 | 150 |  |  |

### Left bracelet — `bodypart=lbracelet` (317)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 9605 | Agathion Seal Bracelet - Rainbow Clan Hall | NONE | 150 |  |  |
| 9606 | Agathion Seal Bracelet - Wild Beast Reserve | NONE | 150 |  |  |
| 9607 | Agathion Seal Bracelet - Gludio | NONE | 150 |  |  |
| 9608 | Agathion Seal Bracelet - Dion | NONE | 150 |  |  |
| 9609 | Agathion Seal Bracelet - Giran | NONE | 150 |  |  |
| 9610 | Agathion Seal Bracelet - Oren | NONE | 150 |  |  |
| 9611 | Agathion Seal Bracelet - Aden | NONE | 150 |  |  |
| 9612 | Agathion Seal Bracelet - Innadril | NONE | 150 |  |  |
| 9613 | Agathion Seal Bracelet - Goddard | NONE | 150 |  |  |
| 9614 | Agathion Seal Bracelet - Rune | NONE | 150 |  |  |
| 9615 | Agathion Seal Bracelet - Schuttgart | NONE | 150 |  |  |
| 9909 | Agathion Seal Bracelet | NONE | 150 |  |  |
| 10018 | Agathion Seal Bracelet - Fortress | NONE | 150 |  |  |
| 10139 | Agathion Bracelet | NONE | 150 |  |  |
| 10273 | Wolf Summoning Bracelet | NONE | 150 |  |  |
| 10316 | Agathion Seal Bracelet - Little Angel - Firework | NONE | 150 |  |  |
| 10317 | Agathion Seal Bracelet - Little Angel - Big Head | NONE | 150 |  |  |
| 10318 | Agathion Seal Bracelet - Little Angel - Blessed Escape | NONE | 150 |  |  |
| 10319 | Agathion Seal Bracelet - Little Angel - Resurrection | NONE | 150 |  |  |
| 10320 | Agathion Seal Bracelet - Little Angel | NONE | 150 |  |  |
| 10322 | Agathion Seal Bracelet - Little Devil - Firework | NONE | 150 |  |  |
| 10323 | Agathion Seal Bracelet - Little Devil - Big Head | NONE | 150 |  |  |
| 10324 | Agathion Seal Bracelet - Little Devil - Blessed Escape | NONE | 150 |  |  |
| 10325 | Agathion Seal Bracelet - Little Devil - Resurrection | NONE | 150 |  |  |
| 10326 | Agathion Seal Bracelet - Little Devil | NONE | 150 |  |  |
| 10606 | Agathion Seal Bracelet - Rudolph | NONE | 150 |  |  |
| 10659 | Agathion Summon Bracelet - Monkey | NONE | 150 |  |  |
| 10660 | Agathion Summon Bracelet - Griffin | NONE | 150 |  |  |
| 12779 | Agathion Seal Bracelet - Little Angel | NONE | 150 |  |  |
| 12780 | Agathion Seal Bracelet - Little Devil | NONE | 150 |  |  |
| 13022 | Light Purple-Maned Horse Mount Bracelet - 7-day limited period | NONE | 30 |  |  |
| 13023 | Agathion of Love - 30-day limited period | NONE | 30 |  |  |
| 13024 | Sudden Agathion - 30-day limited period | NONE | 30 |  |  |
| 13025 | Shiny Agathion - 30-day limited period | NONE | 30 |  |  |
| 13026 | Sobbing Agathion - 30-day limited period | NONE | 30 |  |  |
| 13254 | Agathion of Love - 7-day limited period | NONE | 30 |  |  |
| 13308 | Light Purple-Maned Horse Mount Bracelet (Event) - 7-day limited period | NONE | 30 |  |  |
| 13309 | Agathion of Love (Event) - 30-day limited period | NONE | 30 |  |  |
| 13340 | Agathion of Love (Event) - 7-day limited period | NONE | 30 |  |  |
| 13543 | Agathion Summon Bracelet - Collection | NONE | 150 |  |  |
| 13544 | Agathion Summon Bracelet - Boy Teddy Bear | NONE | 150 |  |  |
| 13545 | Agathion Summon Bracelet - Girl Teddy Bear | NONE | 150 |  |  |
| 13756 | Agathion Summon Bracelet - Knight | NONE | 150 |  |  |
| 14027 | Collection Agathion Summon Bracelet | NONE | 150 |  |  |
| 14053 | Gold-Maned Lion Mount Bracelet - 7-day limited period | NONE | 30 |  |  |
| 14054 | Steam Beatle Mount Bracelet - 7-day limited period | NONE | 30 |  |  |
| 14059 | Teddy Boy Agathion Bracelet - 30-day limited period | NONE | 30 |  |  |
| 14060 | Teddy Girl Agathion Bracelet - 30-day limited period | NONE | 30 |  |  |
| 14066 | Gold Maned Lion Mount Bracelet (event) - 7-day limited period | NONE | 30 |  |  |
| 14067 | Steam Beatle Mount Bracelet (event) - 7-day limited period | NONE | 30 |  |  |
| 14072 | Teddy Boy Agathion Bracelet (event) - 30-day limited period | NONE | 30 |  |  |
| 14073 | Teddy Girl Agathion Bracelet (event) - 30-day limited period | NONE | 30 |  |  |
| 14075 | Sudden Agathion (Event) - 30-day limited period | NONE | 30 |  |  |
| 14076 | Shiny Agathion (Event) - 30-day limited period | NONE | 30 |  |  |
| 14077 | Sobbing Agathion (Event) - 30-day limited period | NONE | 30 |  |  |
| 14091 | Teddy Boy Agathion Bracelet - 7-day limited period | NONE | 30 |  |  |
| 14092 | Teddy Girl Agathion Bracelet - 7-day limited period | NONE | 30 |  |  |
| 14093 | Sudden Agathion - 7-day limited period | NONE | 30 |  |  |
| 14094 | Shiny Agathion - 7-day limited period | NONE | 30 |  |  |
| 14095 | Sobbing Agathion - 7-day limited period | NONE | 30 |  |  |
| 14099 | Teddy Boy Agathion Bracelet (event) - 7-day limited period | NONE | 30 |  |  |
| 14100 | Teddy Girl Agathion Bracelet (event) - 7-day limited period | NONE | 30 |  |  |
| 14101 | Sudden Agathion (Event) - 7-day limited period | NONE | 30 |  |  |
| 14102 | Shiny Agathion (Event) - 7-day limited period | NONE | 30 |  |  |
| 14103 | Sobbing Agathion (Event) - 7-day limited period | NONE | 30 |  |  |
| 14104 | Shadow Item - Collection Agathion Summon Bracelet | NONE | 150 |  |  |
| 14617 | Agathion Seal Bracelet - Rudolph | NONE | 150 |  |  |
| 14675 | Agathion Seal Bracelet - Neolithica | NONE | 150 |  |  |
| 14775 | Agathion Seal Bracelet - Love - 14-day limited period | NONE | 0 |  |  |
| 14776 | Agathion Seal Bracelet - Juju - 14-day limited period | NONE | 0 |  |  |
| 15208 | Bracelet of Friendship - 30-day limited period | NONE | 0 |  |  |
| 15220 | Agathion Seal Bracelet - Oink Oink - 10-day limited period | NONE | 0 |  |  |
| 15351 | Seal Removal Bracelet_Towbat | NONE | 5 |  |  |
| 15473 | Beast Handler's Whip | NONE | 0 |  |  |
| 16399 | Teddy Boy Summon Bracelet - Permanent Use | NONE | 150 |  |  |
| 16400 | Teddy Girl Summon Bracelet - Permanent Use | NONE | 150 |  |  |
| 16401 | Teddy Boy Summon Bracelet (event) - Permanent Use | NONE | 150 |  |  |
| 16402 | Teddy Girl Summon Bracelet (event) - Permanent Use | NONE | 150 |  |  |
| 17004 | Agathion Seal Bracelet - Kid Rudolph - Event | NONE | 150 |  |  |
| 17203 | Agathion Seal Bracelet - Ball Trapping Gnosian | NONE | 150 |  |  |
| 17204 | Agathion Seal Bracelet - Ball Trapping Orodriel | NONE | 150 |  |  |
| 17205 | Agathion Seal Bracelet - Penalty Kick | NONE | 150 |  |  |
| 17269 | Agathion Seal Bracelet - Antharas | NONE | 150 |  |  |
| 17270 | Agathion Seal Bracelet - Nevit's Messenger Kanna | NONE | 150 |  |  |
| 17271 | Agathion Seal Bracelet - Guardian of the Dawn Kallesin | NONE | 150 |  |  |
| 20006 | Agathion Seal Bracelet - Majo | NONE | 150 |  |  |
| 20007 | Agathion Seal Bracelet - Gold Majo | NONE | 150 |  |  |
| 20008 | Agathion Seal Bracelet - Black Majo | NONE | 150 |  |  |
| 20009 | Agathion Seal Bracelet - Majo - Big Head 30-Day Limited Period | NONE | 150 |  |  |
| 20010 | Agathion Seal Bracelet - Gold Majo - Resurrection 30-Day Limited Period | NONE | 150 |  |  |
| 20011 | Agathion Seal Bracelet - Black Majo - Escape 30-Day Limited Period | NONE | 150 |  |  |
| 20012 | Agathion Seal Bracelet - Plaipitak | NONE | 150 |  |  |
| 20013 | Agathion Seal Bracelet - Plaipitak - Big Head 30-Day Limited Period | NONE | 150 |  |  |
| 20014 | Agathion Seal Bracelet - Plaipitak - Resurrection 30-Day Limited Period | NONE | 150 |  |  |
| 20015 | Agathion Seal Bracelet - Plaipitak - Escape 30-Day Limited Period | NONE | 150 |  |  |
| 20029 | Light Purple-Maned Horse Mount Bracelet | NONE | 30 |  |  |
| 20030 | Light Purple-Maned Horse Mount Bracelet - 30-day limited period | NONE | 30 |  |  |
| 20063 | Agathion Seal Bracelet - Baby Panda | NONE | 150 |  |  |
| 20064 | Agathion Seal Bracelet - Bamboo Panda | NONE | 150 |  |  |
| 20065 | Agathion Seal Bracelet - Sexy Panda | NONE | 150 |  |  |
| 20066 | Agathion Seal Bracelet - Baby Panda - Big Head-15-Day Limited Period | NONE | 150 |  |  |
| 20067 | Agathion Seal Bracelet - Bamboo Panda - Resurrection-15-Day Limited Period | NONE | 150 |  |  |
| 20068 | Agathion Seal Bracelet - Sexy Panda - Escape-15-Day Limited Period | NONE | 150 |  |  |
| 20094 | Agathion Seal Bracelet: Rudolph - Energy - 30-Day Limited Period | NONE | 150 |  |  |
| 20200 | Agathion of Love - 3-day limited period | NONE | 150 |  |  |
| 20201 | Agathion of Love - 7-day limited period | NONE | 150 |  |  |
| 20202 | Agathion of Love - 15-day limited period | NONE | 150 |  |  |
| 20203 | Agathion of Love - 30-day limited period | NONE | 150 |  |  |
| 20212 | Agathion Seal Bracelet - Charming Cupid | NONE | 150 |  |  |
| 20213 | Agathion Seal Bracelet - Naughty Cupid | NONE | 150 |  |  |
| 20221 | Agathion Seal Bracelet - White Maneki Neko | NONE | 150 |  |  |
| 20222 | Agathion Seal Bracelet - Black Maneki Neko | NONE | 150 |  |  |
| 20223 | Agathion Seal Bracelet - Brown Maneki Neko | NONE | 150 |  |  |
| 20224 | Agathion Seal Bracelet - White Maneki Neko - Resurrection - 7-Day Limited Period | NONE | 150 |  |  |
| 20225 | Agathion Seal Bracelet - Black Maneki Neko - Escape - 7-Day Limited Period | NONE | 150 |  |  |
| 20226 | Agathion Seal Bracelet - Brown Maneki Neko - Vitality - 7-day limited time | NONE | 150 |  |  |
| 20230 | Agathion Seal Bracelet - One-Eyed Bat Drove | NONE | 150 |  |  |
| 20231 | Agathion Seal Bracelet - One-Eyed Bat Drove - Resist Unholy - 7-Day Limited Period | NONE | 150 |  |  |
| 20232 | Agathion Seal Bracelet - One-Eyed Bat Drove - Vitality - 7-Day Limited Period | NONE | 150 |  |  |
| 20236 | Agathion Seal Bracelet - Pegasus | NONE | 150 |  |  |
| 20237 | Agathion Seal Bracelet - Pegasus - Wind Walk - 7-Day Limited Period | NONE | 150 |  |  |
| 20238 | Agathion Seal Bracelet - Pegasus - Escape - 7-Day Limited Period | NONE | 150 |  |  |
| 20245 | Agathion Seal Bracelet - Yellow-Robed Tojigong | NONE | 150 |  |  |
| 20246 | Agathion Seal Bracelet - Blue-Robed Tojigong | NONE | 150 |  |  |
| 20247 | Agathion Seal Bracelet - Green-Robed Tojigong | NONE | 150 |  |  |
| 20248 | Agathion Seal Bracelet - Yellow-Robed Tojigong - Greater Heal - 7-Day Limited Period | NONE | 150 |  |  |
| 20249 | Agathion Seal Bracelet - Blue-Robed Tojigong - Reflect Damage - 7-Day Limited Period | NONE | 150 |  |  |
| 20250 | Agathion Seal Bracelet - Green-Robed Tojigong - Mana Regeneration - 7-Day Limited Period | NONE | 150 |  |  |
| 20252 | Agathion Seal Bracelet - Bugbear | NONE | 150 |  |  |
| 20253 | Agathion of Love (Event) | NONE | 150 |  |  |
| 20297 | Agathion Seal Bracelet - Red Sumo Wrestler | NONE | 150 |  |  |
| 20298 | Agathion Seal Bracelet - Red Sumo Wrestler - Death Whisper - 7-Day Limited Period | NONE | 150 |  |  |
| 20299 | Agathion Seal Bracelet - Blue Sumo Wrestler | NONE | 150 |  |  |
| 20300 | Agathion Seal Bracelet - Blue Sumo Wrestler - Wild Magic - 7-Day Limited Period | NONE | 150 |  |  |
| 20301 | Agathion Seal Bracelet - Great Sumo Match | NONE | 150 |  |  |
| 20302 | Agathion Seal Bracelet - Great Sumo Match - Big Head / Firework - 7-Day Limited Period | NONE | 150 |  |  |
| 20303 | Agathion Seal Bracelet - Button-Eyed Bear Doll | NONE | 150 |  |  |
| 20304 | Agathion Seal Bracelet - Button-Eyed Bear Doll - Escape - 7-Day Limited Period | NONE | 150 |  |  |
| 20305 | Agathion Seal Bracelet - Button-Eyed Bear Doll - Resurrection - 7-Day Limited Period | NONE | 150 |  |  |
| 20306 | Agathion Seal Bracelet - Button-Eyed Bear Doll - Energy - 7-Day Limited Period | NONE | 150 |  |  |
| 20307 | Agathion Seal Bracelet - God of Fortune | NONE | 150 |  |  |
| 20308 | Agathion Seal Bracelet - God of Fortune - Energy - 7-Day Limited Period | NONE | 150 |  |  |
| 20309 | Agathion Seal Bracelet - Dryad | NONE | 150 |  |  |
| 20310 | Agathion Seal Bracelet - Wonboso | NONE | 150 |  |  |
| 20311 | Agathion Seal Bracelet - Wonboso - Wind Walk - 7-Day Limited Period | NONE | 150 |  |  |
| 20312 | Agathion Seal Bracelet - Daewoonso | NONE | 150 |  |  |
| 20313 | Agathion Seal Bracelet - Daewoonso - New Year's Gift - 7-Day Limited Period | NONE | 150 |  |  |
| 20396 | Steam Beatle Mount Bracelet | NONE | 30 |  |  |
| 20405 | Agathion Seal Bracelet - Majo - Big Head - 7-day limited period | NONE | 150 |  |  |
| 20406 | Agathion Seal Bracelet - Gold Crown Majo - Resurrection - 7-Day Limited Period | NONE | 150 |  |  |
| 20407 | Agathion Seal Bracelet - Black Crown Majo - Escape - 7-Day Limited Period | NONE | 150 |  |  |
| 20408 | Agathion Seal Bracelet - Plaipitak - Big Head - 7-day limited period | NONE | 150 |  |  |
| 20409 | Agathion Seal Bracelet - Plaipitak - Resurrection - 7-Day Limited Period | NONE | 150 |  |  |
| 20410 | Agathion Seal Bracelet - Plaipitak - Escape - 7-Day Limited Period | NONE | 150 |  |  |
| 20411 | Agathion Seal Bracelet - Baby Panda - Big Head - 7-day limited period | NONE | 150 |  |  |
| 20412 | Agathion Seal Bracelet - Bamboo Panda - Resurrection - 7-Day Limited Period | NONE | 150 |  |  |
| 20413 | Agathion Seal Bracelet - Sexy Panda - Escape - 7-Day Limited Period | NONE | 150 |  |  |
| 20448 | Darkmane Pacer Mount Bracelet - 7-day limited period | NONE | 30 |  |  |
| 20449 | Steam Beatle Mount Bracelet - 7-day limited period | NONE | 30 |  |  |
| 20495 | Agathion Seal Bracelet - Live Event Souvenir | NONE | 150 |  |  |
| 20496 | Agathion Seal Bracelet - Pomona - Mental Shield - 7-day limited period | NONE | 150 |  |  |
| 20502 | Gold Maned Lion Mount Bracelet | NONE | 30 |  |  |
| 20503 | Gold Maned Lion Mount Bracelet - 30-day limited period | NONE | 30 |  |  |
| 20504 | Steam Beatle Mount Bracelet - 30-day limited period | NONE | 30 |  |  |
| 20591 | Agathion Seal Bracelet - Weaver | NONE | 150 |  |  |
| 20592 | Agathion Seal Bracelet - Weaver - Power of the Golden Calf - 24-hour limited period | NONE | 150 |  |  |
| 20593 | Agathion Seal Bracelet - Weaver - Power of the Golden Calf - 3-day limited period | NONE | 150 |  |  |
| 20594 | Summon of Love Bracelet (event) - 24-hour limited period | NONE | 0 |  |  |
| 20621 | Agathion Seal Bracelet - Female Weaver - Flute Sound - 24-hour limited period | NONE | 150 |  |  |
| 20622 | Agathion Seal Bracelet - Female Weaver - Flute Sound - 3-day limited period | NONE | 150 |  |  |
| 20628 | Summon of Love Bracelet - 7-day limited period | NONE | 150 |  |  |
| 20654 | Agathion Seal Bracelet - Chon-chon | NONE | 150 |  |  |
| 20655 | Agathion Seal Bracelet - Chon-chon - Great Warrior's Soul Power - 7-day limited period | NONE | 150 |  |  |
| 20656 | Agathion Seal Bracelet - Tang-tang | NONE | 150 |  |  |
| 20657 | Agathion Seal Bracelet - Tang-tang - Great Wizard's Soul Power - 7-day limited period | NONE | 150 |  |  |
| 20658 | Agthion Seal Bracelet - Dancing Lucky Kid | NONE | 150 |  |  |
| 20659 | Agthion Seal Bracelet - Dancing Lucky Kid - Great Adventurer's Soul Power - 7-day limited period | NONE | 150 |  |  |
| 20660 | Agathion Seal Bracelet - Monkey King | NONE | 150 |  |  |
| 20661 | Agathion Seal Bracelet - Monkey King - Great Wizard's Soul Power - 7-day limited period | NONE | 150 |  |  |
| 20662 | Agathion Seal Bracelet - Utanka Agathion | NONE | 150 |  |  |
| 20663 | Agathion Seal Bracelet - Utanka Agathion - Great Warrior's Soul Power - 7-day limited period | NONE | 150 |  |  |
| 20664 | Agathion Seal Bracelet - Bonus B Agathion | NONE | 150 |  |  |
| 20665 | Agathion Seal Bracelet - Bonus B Agathion - Great Adventurer's Soul Power - 7-day limited period | NONE | 150 |  |  |
| 20726 | Agathion Seal Bracelet - Zombie | NONE | 150 |  |  |
| 20727 | Agathion Seal Bracelet - Zombie - Escape from Death - 7-day limited period | NONE | 150 |  |  |
| 20732 | Agathion Seal Bracelet - Baekyi Hwamae | NONE | 150 |  |  |
| 20733 | Agathion Seal Bracelet - Kwanwoo Hwamae | NONE | 150 |  |  |
| 20774 | GG - Aura of Fury - 7-day limited period | NONE | 150 |  |  |
| 20775 | Agathion Seal Bracelet - Gwanseum Nyang Nyang - Blessing of Mercy - 7-day limited period | NONE | 150 |  |  |
| 20776 | Agathion Seal Bracelet - Blue Opera - Sword of Recovery - 7-day limited period | NONE | 150 |  |  |
| 20777 | Agathion Seal Bracelet - Blue Opera - Sword of Lightning - 7-day limited period | NONE | 150 |  |  |
| 20778 | Agathion Seal Bracelet - Red Opera - Spear of Flames - 7-day limited period | NONE | 150 |  |  |
| 20779 | Agathion Seal Bracelet - Opera | NONE | 150 |  |  |
| 20780 | Agathion Seal Bracelet - Opera - Sword of Life - 30-day limited period | NONE | 150 |  |  |
| 20781 | Agathion Seal Bracelet - Miss Chipao - Miss Chipao's Blessing - 7-day limited period | NONE | 150 |  |  |
| 20782 | Agathion Seal Bracelet - Nepal Snow | NONE | 150 |  |  |
| 20783 | Agathion Seal Bracelet - Round Ball Snow | NONE | 150 |  |  |
| 20784 | Agathion Seal Bracelet - Ladder Snow | NONE | 150 |  |  |
| 20785 | Agathion Seal Bracelet - Nepal Snow - Snow's Haste - 7-day limited period | NONE | 150 |  |  |
| 20786 | Agathion Seal Bracelet - Round Ball Snow - Snow's Acumen - 7-day limited period | NONE | 150 |  |  |
| 20787 | Agathion Seal Bracelet - Ladder Snow - Snow's Wind Walk - 7-day limited period | NONE | 150 |  |  |
| 20818 | Soul Avatar Seal Bracelet - Iken | NONE | 150 |  |  |
| 20819 | Agathion Seal Bracelet - Iken - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20820 | Soul Avatar Seal Bracelet - Lana | NONE | 150 |  |  |
| 20821 | Agathion Seal Bracelet - Lana - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20822 | Soul Avatar Seal Bracelet - Gnosian | NONE | 150 |  |  |
| 20823 | Agathion Seal Bracelet - Gnocian - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20824 | Soul Avatar Seal Bracelet - Orodriel | NONE | 150 |  |  |
| 20825 | Agathion Seal Bracelet - Orodriel - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20826 | Soul Avatar Seal Bracelet - Lakinos | NONE | 150 |  |  |
| 20827 | Agathion Seal Bracelet - Lakinos - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20828 | Soul Avatar Seal Bracelet - Mortia | NONE | 150 |  |  |
| 20829 | Agathion Seal Bracelet - Mortia - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20830 | Soul Avatar Seal Bracelet - Heintz | NONE | 150 |  |  |
| 20831 | Agathion Seal Bracelet - Hayance - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20832 | Soul Avatar Seal Bracelet - Meruril | NONE | 150 |  |  |
| 20833 | Agathion Seal Bracelet - Meruril - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20834 | Soul Avatar Seal Bracelet - Taman Zu Rapatui | NONE | 150 |  |  |
| 20835 | Agathion Seal Bracelet - Taman ze Lapatui - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20836 | Soul Avatar Seal Bracelet - Kaurin | NONE | 150 |  |  |
| 20837 | Agathion Seal Bracelet - Kaurin - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20838 | Soul Avatar Seal Bracelet - Ahertbein | NONE | 150 |  |  |
| 20839 | Agathion Seal Bracelet - Ahertbein - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20840 | Soul Avatar Seal Bracelet - Naonin | NONE | 150 |  |  |
| 20841 | Agathion Seal Bracelet - Naonin - Prominent Outsider Adventurer's Ability - 7-day limited period | NONE | 150 |  |  |
| 20938 | Jet Bike Mount Bracelet - 7-day limited period | NONE | 30 |  |  |
| 20939 | Jet Bike Mount Bracelet - 30-day limited period | NONE | 30 |  |  |
| 20940 | Phoenix Agthion Seal Bracelet - Nirvana Rebirth - 7-day limited period | NONE | 150 |  |  |
| 20941 | Phoenix Agthion Seal Bracelet - Oriental Phoenix - 7-day limited period | NONE | 150 |  |  |
| 20956 | Agathion Seal Bracelet - Frozen Corpse - Soul Stealth - 7-day limited period | NONE | 150 |  |  |
| 20968 | Agathion Seal Bracelet - Guangong | NONE | 150 |  |  |
| 20970 | Agathion Seal Bracelet - Three-headed Dragon - Wind Walk | NONE | 150 |  |  |
| 20983 | Agathion Seal Bracelet - Ball Trapping Gnosian - Soccer Ball of Cheers, Buff of Cheers | NONE | 150 |  |  |
| 20984 | Agathion Seal Bracelet - Ball Trapping Orodriel - Soccer Ball of Cheers, Buff of Cheers | NONE | 150 |  |  |
| 20985 | Agathion Seal Bracelet - Penalty Kick - Soccer Ball of Cheers, Buff of Cheers | NONE | 150 |  |  |
| 20986 | Agathion Seal Bracelet - Ball Trapping Gnosian - Soccer Ball of Cheers, Buff of Cheers | NONE | 150 |  |  |
| 20987 | Agathion Seal Bracelet - Ball Trapping Orodriel - Soccer Ball of Cheers, Buff of Cheers | NONE | 150 |  |  |
| 20988 | Agathion Seal Bracelet - Penalty Kick - Soccer Ball of Cheers, Buff of Cheers | NONE | 150 |  |  |
| 20989 | Agathion Seal Bracelet - Ball Trapping Gnosian - Soccer Ball of Cheers, Buff of Cheers | NONE | 150 |  |  |
| 20990 | Agathion Seal Bracelet - Ball Trapping Orodriel - Soccer Ball of Cheers, Buff of Cheers | NONE | 150 |  |  |
| 20991 | Agathion Seal Bracelet - Penalty Kick - Soccer Ball of Cheers, Buff of Cheers | NONE | 150 |  |  |
| 21046 | Agathion Seal Bracelet - Granny Tiger - 7-day limited period | NONE | 150 |  |  |
| 21047 | Agathion Seal Bracelet - Granny Tiger | NONE | 150 |  |  |
| 21048 | Agathion Seal Bracelet - Flower Fairy Spirit | NONE | 150 |  |  |
| 21049 | Agathion Seal Bracelet - Cheerleader Orodriel - 7-day limited period | NONE | 150 |  |  |
| 21050 | Agathion Seal Bracelet - Cheerleader Orodriel | NONE | 150 |  |  |
| 21051 | Agathion Seal Bracelet - Cheerleader Lana - 7-day limited period | NONE | 150 |  |  |
| 21052 | Agathion Seal Bracelet - Cheerleader Lana | NONE | 150 |  |  |
| 21053 | Agathion Seal Bracelet - Cheerleader Naonin - 7-day limited period | NONE | 150 |  |  |
| 21054 | Agathion Seal Bracelet - Cheerleader Naonin | NONE | 150 |  |  |
| 21055 | Agathion Seal Bracelet - Cheerleader Mortia - 7-day limited period | NONE | 150 |  |  |
| 21056 | Agathion Seal Bracelet - Cheerleader Mortia | NONE | 150 |  |  |
| 21057 | Agathion Seal Bracelet - Cheerleader Kaurin - 7-day limited period | NONE | 150 |  |  |
| 21058 | Agathion Seal Bracelet - Cheerleader Kaurin | NONE | 150 |  |  |
| 21059 | Agathion Seal Bracelet - Cheerleader Meruril - 7-day limited period | NONE | 150 |  |  |
| 21060 | Agathion Seal Bracelet - Cheerleader Meruril | NONE | 150 |  |  |
| 21061 | Agathion Seal Bracelet - Handy - 7-day limited period | NONE | 150 |  |  |
| 21062 | Agathion Seal Bracelet - Handy | NONE | 150 |  |  |
| 21088 | Jet Bike Mount Bracelet | NONE | 30 |  |  |
| 21152 | Agathion Seal Bracelet - Singer and Dancer | NONE | 150 |  |  |
| 21153 | Agathion Seal Bracelet - Singer and Dancer - 7-day limited period | NONE | 150 |  |  |
| 21165 | Agathion Seal Bracelet - Zaken Spirit Sword | NONE | 150 |  |  |
| 21166 | Agathion Seal Bracelet - Zaken's Spirit Swords - 7-day limited period | NONE | 150 |  |  |
| 21331 | Agathion Summon Bracelet - Griffin - 7-day limited period | NONE | 120 |  |  |
| 21332 | Agathion Summon Bracelet - Griffin - 7-day limited period (event) | NONE | 120 |  |  |
| 21333 | Agathion Summon Bracelet - Griffin - 30-day limited period | NONE | 120 |  |  |
| 21334 | Agathion Summon Bracelet - Griffin - 30-day limited period (event) | NONE | 120 |  |  |
| 21335 | Agathion Summon Bracelet - Griffin | NONE | 120 |  |  |
| 21336 | Agathion Summon Bracelet - Griffin - Event | NONE | 120 |  |  |
| 21343 | Agathion Summon Bracelet - Cow - 7-day limited period | NONE | 120 |  |  |
| 21344 | Agathion Summon Bracelet - Cow - 7-day limited period (event) | NONE | 120 |  |  |
| 21345 | Agathion Summon Bracelet - Cow - 30-day limited period | NONE | 120 |  |  |
| 21346 | Agathion Summon Bracelet - Cow - 30-day limited period (event) | NONE | 120 |  |  |
| 21347 | Agathion Summon Bracelet - Cow | NONE | 120 |  |  |
| 21348 | Agathion Summon Bracelet - Cow - Event | NONE | 120 |  |  |
| 21355 | Agathion Summon Bracelet - Tow - 7-day limited period | NONE | 120 |  |  |
| 21356 | Agathion Summon Bracelet - Tow - 7-day limited period (event) | NONE | 120 |  |  |
| 21357 | Agathion Summon Bracelet - Tow - 30-day limited period | NONE | 120 |  |  |
| 21358 | Agathion Summon Bracelet - Tow - 30-day limited period (event) | NONE | 120 |  |  |
| 21359 | Agathion Summon Bracelet - Tow | NONE | 120 |  |  |
| 21360 | Agathion Summon Bracelet - Tow - Event | NONE | 120 |  |  |
| 21379 | Mount Bracelet - Darkmane Pacer - 7-day limited period | NONE | 30 |  |  |
| 21380 | Mount Bracelet - Darkmane Pacer - 7-day limited period (event) | NONE | 30 |  |  |
| 21381 | Mount Bracelet - Darkmane Pacer - 30-day limited period | NONE | 30 |  |  |
| 21382 | Mount Bracelet - Darkmane Pacer - 30-day limited period (event) | NONE | 30 |  |  |
| 21383 | Mount Bracelet - Darkmane Pacer | NONE | 30 |  |  |
| 21384 | Mount Bracelet - Darkmane Pacer - Event | NONE | 30 |  |  |
| 21391 | Mount Bracelet - Steam Beatle - 7-day limited period | NONE | 0 |  |  |
| 21392 | Mount Bracelet - Steam Beatle - 7-day limited period (event) | NONE | 0 |  |  |
| 21393 | Mount Bracelet - Steam Beatle - 30-day limited period | NONE | 0 |  |  |
| 21394 | Mount Bracelet - Steam Beatle - 30-day limited period (event) | NONE | 0 |  |  |
| 21395 | Mount Bracelet - Steam Beatle | NONE | 0 |  |  |
| 21396 | Mount Bracelet - Steam Beatle - Event | NONE | 0 |  |  |
| 21403 | Mount Bracelet - Gold Maned Lion - 7-day limited period | NONE | 0 |  |  |
| 21404 | Mount Bracelet - Gold Maned Lion - 7-day limited period (event) | NONE | 0 |  |  |
| 21405 | Mount Bracelet - Gold Maned Lion - 30-day limited period | NONE | 0 |  |  |
| 21406 | Mount Bracelet - Gold Maned Lion - 30-day limited period (event) | NONE | 0 |  |  |
| 21407 | Mount Bracelet - Gold Maned Lion | NONE | 0 |  |  |
| 21408 | Mount Bracelet - Gold Maned Lion - Event | NONE | 0 |  |  |
| 21415 | Mount Bracelet - Jet Bike - 7-day limited period | NONE | 30 |  |  |
| 21416 | Mount Bracelet - Jet Bike - 7-day limited period (event) | NONE | 30 |  |  |
| 21417 | Mount Bracelet - Jet Bike - 30-day limited period | NONE | 30 |  |  |
| 21418 | Mount Bracelet - Jet Bike - 30-day limited period (event) | NONE | 30 |  |  |
| 21419 | Mount Bracelet - Jet Bike | NONE | 30 |  |  |
| 21420 | Mount Bracelet - Jet Bike - Event | NONE | 30 |  |  |
| 21709 | Agathion Seal Bracelet - Rudolph - Event | NONE | 150 |  |  |
| 21727 | Zinenze Agathion Bracelet (3 day) - 3-day limited period | NONE | 120 |  |  |
| 21728 | Zinenze Agathion Bracelet (7 day) - 7-day limited period | NONE | 120 |  |  |
| 21729 | Enze Agathion Bracelet - Permanent | NONE | 120 |  |  |
| 21870 | Agathion Seal Bracelet - Neolithica - 14-day limited period | NONE | 150 |  |  |
| 21986 | Agathion Seal Bracelet - Antharas | NONE | 150 |  |  |
| 22191 | Rocking Horse Mount Bracelet - 7-day limited period | NONE | 30 |  |  |
| 22192 | Rocking Horse Mount Bracelet - 30-day limited period | NONE | 30 |  |  |
| 22193 | Rocking Horse Mount Bracelet | NONE | 30 |  |  |
| 22200 | Agathion Seal Bracelet - Lantern - 33-day limited period (event) | NONE | 150 |  |  |
| 22287 | Agathion Seal Bracelet - Juju - 33-day limited period (event) | NONE | 150 |  |  |
| 15312 | Dawn's Bracelet | S | 15 |  |  |

### Right bracelet (talisman carrier) — `bodypart=rbracelet` (12)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 13546 | Steam Sledge Mount Bracelet | NONE | 150 |  |  |
| 13547 | Tawny-Maned Lion Mount Bracelet | NONE | 150 |  |  |
| 17049 | Shiny Bracelet | NONE | 0 |  |  |
| 20535 | Steam Beatle Mount Bracelet - 30-day limited period | NONE | 150 |  |  |
| 20536 | Gold-Maned Lion Mount Bracelet - 30-day limited period | NONE | 150 |  |  |
| 9589 | Iron Bracelet | C | 150 |  |  |
| 9590 | Bronze Bracelet | B | 150 |  |  |
| 13295 | Pailaka Bracelet | B | 150 |  |  |
| 9591 | Steel Bracelet | A | 150 |  |  |
| 10209 | Enhanced Steel Bracelet | A | 150 |  |  |
| 9592 | Mithril Bracelet | S | 150 |  |  |
| 10210 | Enhanced Mithril Bracelet | S | 150 |  |  |

### Talisman — `bodypart=deco1` (101)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 9913 | Talisman_Test | NONE | 150 |  |  |
| 9914 | Blue Talisman of Power | NONE | 150 |  |  |
| 9915 | Blue Talisman of Wild Magic | NONE | 150 |  |  |
| 9916 | Blue Talisman of Defense | NONE | 150 |  |  |
| 9917 | Red Talisman of Minimum Clarity | NONE | 150 |  |  |
| 9918 | Red Talisman of Maximum Clarity | NONE | 150 |  |  |
| 9919 | Blue Talisman of Reflection | NONE | 150 |  |  |
| 9920 | Blue Talisman of Invisibility | NONE | 150 |  |  |
| 9921 | Blue Talisman - Shield Protection | NONE | 150 |  |  |
| 9922 | Black Talisman - Mending | NONE | 150 |  |  |
| 9923 | Black Talisman - Escape | NONE | 150 |  |  |
| 9924 | Blue Talisman of Healing | NONE | 150 |  |  |
| 9925 | Red Talisman of Recovery | NONE | 150 |  |  |
| 9926 | Blue Talisman of Defense | NONE | 150 |  |  |
| 9927 | Blue Talisman of Magic Defense | NONE | 150 |  |  |
| 9928 | Red Talisman of Mental Regeneration | NONE | 150 |  |  |
| 9929 | Blue Talisman of Protection | NONE | 150 |  |  |
| 9930 | Blue Talisman of Evasion | NONE | 150 |  |  |
| 9931 | Red Talisman of Meditation | NONE | 150 |  |  |
| 9932 | Blue Talisman - Divine Protection | NONE | 150 |  |  |
| 9933 | Yellow Talisman of Power | NONE | 150 |  |  |
| 9934 | Yellow Talisman of Violent Haste | NONE | 150 |  |  |
| 9935 | Yellow Talisman of Arcane Defense | NONE | 150 |  |  |
| 9936 | Yellow Talisman of Arcane Power | NONE | 150 |  |  |
| 9937 | Yellow Talisman of Arcane Haste | NONE | 150 |  |  |
| 9938 | Yellow Talisman of Accuracy | NONE | 150 |  |  |
| 9939 | Yellow Talisman of Defense | NONE | 150 |  |  |
| 9940 | Yellow Talisman of Alacrity | NONE | 150 |  |  |
| 9941 | Yellow Talisman of Speed | NONE | 150 |  |  |
| 9942 | Yellow Talisman of Critical Reduction | NONE | 150 |  |  |
| 9943 | Yellow Talisman of Critical Damage | NONE | 150 |  |  |
| 9944 | Yellow Talisman of Critical Dodging | NONE | 150 |  |  |
| 9945 | Yellow Talisman of Evasion | NONE | 150 |  |  |
| 9946 | Yellow Talisman of Healing | NONE | 150 |  |  |
| 9947 | Yellow Talisman of CP Regeneration | NONE | 150 |  |  |
| 9948 | Yellow Talisman of Physical Regeneration | NONE | 150 |  |  |
| 9949 | Yellow Talisman of Mental Regeneration | NONE | 150 |  |  |
| 9950 | Grey Talisman of Weight Training | NONE | 150 |  |  |
| 9951 | Grey Talisman of Mid-Grade Fishing | NONE | 150 |  |  |
| 9952 | Orange Talisman - Hot Springs CP Potion | NONE | 150 |  |  |
| 9953 | Orange Talisman - Elixir of Life | NONE | 150 |  |  |
| 9954 | Orange Talisman - Elixir of Mental Strength | NONE | 150 |  |  |
| 9955 | Black Talisman - Vocalization | NONE | 150 |  |  |
| 9956 | Black Talisman - Arcane Freedom | NONE | 150 |  |  |
| 9957 | Black Talisman - Physical Freedom | NONE | 150 |  |  |
| 9958 | Black Talisman - Rescue | NONE | 150 |  |  |
| 9959 | Black Talisman - Free Speech | NONE | 150 |  |  |
| 9960 | White Talisman of Bravery | NONE | 150 |  |  |
| 9961 | White Talisman of Motion | NONE | 150 |  |  |
| 9962 | White Talisman of Grounding | NONE | 150 |  |  |
| 9963 | White Talisman of Attention | NONE | 150 |  |  |
| 9964 | White Talisman of Bandages | NONE | 150 |  |  |
| 9965 | White Talisman of Protection | NONE | 150 |  |  |
| 9966 | White Talisman of Freedom | NONE | 150 |  |  |
| 10141 | Grey Talisman - Yeti Transform | NONE | 150 |  |  |
| 10142 | Grey Talisman - Buffalo Transform | NONE | 150 |  |  |
| 10158 | Grey Talisman of Upper Grade Fishing | NONE | 150 |  |  |
| 10416 | Blue Talisman - Explosion | NONE | 150 |  |  |
| 10417 | Blue Talisman - Magic Explosion | NONE | 150 |  |  |
| 10418 | White Talisman - Storm | NONE | 150 |  |  |
| 10419 | White Talisman - Darkness | NONE | 150 |  |  |
| 10420 | White Talisman - Water | NONE | 150 |  |  |
| 10421 | White Talisman - Fire | NONE | 150 |  |  |
| 10422 | White Talisman - Light | NONE | 150 |  |  |
| 10423 | Blue Talisman - Self-Destruction | NONE | 150 |  |  |
| 10424 | Blue Talisman - Greater Healing | NONE | 150 |  |  |
| 10518 | Red Talisman - Life Force | NONE | 150 |  |  |
| 10519 | White Talisman - Earth | NONE | 150 |  |  |
| 10533 | Blue Talisman - P. Atk. | NONE | 150 |  |  |
| 10534 | Blue Talisman - Shield Defense | NONE | 150 |  |  |
| 10535 | Yellow Talisman - P. Def. | NONE | 150 |  |  |
| 10536 | Yellow Talisman - M. Atk. | NONE | 150 |  |  |
| 10537 | Yellow Talisman - Evasion | NONE | 150 |  |  |
| 10538 | Yellow Talisman - Healing Power | NONE | 150 |  |  |
| 10539 | Yellow Talisman - CP Recovery Rate | NONE | 150 |  |  |
| 10540 | Yellow Talisman - HP Recovery Rate | NONE | 150 |  |  |
| 10541 | Yellow Talisman - Low Grade MP Recovery Rate | NONE | 150 |  |  |
| 10542 | Red Talisman - HP/CP Recovery | NONE | 150 |  |  |
| 10543 | Yellow Talisman - Speed | NONE | 150 |  |  |
| 12815 | Red Talisman - Max CP | NONE | 150 |  |  |
| 12816 | Red Talisman - CP Regeneration | NONE | 150 |  |  |
| 12817 | Yellow Talisman - Increase Force | NONE | 150 |  |  |
| 12818 | Yellow Talisman - Damage Transition | NONE | 150 |  |  |
| 14604 | Red Talisman - Territory Guardian | NONE | 150 |  |  |
| 14605 | Red Talisman - Territory Guard | NONE | 150 |  |  |
| 14810 | Blue Talisman - Buff Cancel | NONE | 150 |  |  |
| 14811 | Blue Talisman - Buff Steal | NONE | 150 |  |  |
| 14812 | Red Talisman - Territory Guard | NONE | 150 |  |  |
| 14813 | Blue Talisman - Lord's Divine Protection | NONE | 150 |  |  |
| 14814 | White Talisman - All Resistance | NONE | 150 |  |  |
| 17051 | Talisman - STR | NONE | 0 |  |  |
| 17052 | Talisman - DEX | NONE | 0 |  |  |
| 17053 | Talisman - CON | NONE | 0 |  |  |
| 17054 | Talisman - WIT | NONE | 0 |  |  |
| 17055 | Talisman - INT | NONE | 0 |  |  |
| 17056 | Talisman - MEN | NONE | 0 |  |  |
| 17057 | Talisman - Resistance to Stun | NONE | 0 |  |  |
| 17058 | Talisman - Resistance to Sleep | NONE | 0 |  |  |
| 17059 | Talisman - Resistance to Hold | NONE | 0 |  |  |
| 17060 | Talisman - Paralyze Resistance | NONE | 0 |  |  |
| 17061 | Talisman - ALL STAT | NONE | 0 |  |  |

### Belt — `bodypart=waist` (93)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 13526 | Test Belt | NONE | 4830 |  |  |
| 15393 | Vitality Belt - 7-day limited period | NONE | 0 |  |  |
| 15394 | Vitality Belt - 30-day limited period | NONE | 0 |  |  |
| 15395 | Vitality Belt - 60-day limited period | NONE | 0 |  |  |
| 15396 | Vitality Belt - 90-day limited period | NONE | 0 |  |  |
| 15397 | Vitality Belt - Permanent Use | NONE | 0 |  |  |
| 15398 | Vitality Belt (Event) - 7-day limited period | NONE | 0 |  |  |
| 15399 | Vitality Belt (Event) - 30-day limited period | NONE | 0 |  |  |
| 15400 | Vitality Belt (Event) - 60-day limited period | NONE | 0 |  |  |
| 15401 | Vitality Belt (Event) - 90-day limited period | NONE | 0 |  |  |
| 15402 | Vitality Belt (Event) - Permanent Use | NONE | 0 |  |  |
| 15429 | 6th Anniversary Party Belt (Event) - 7-day limited period | NONE | 0 |  |  |
| 13894 | Cloth Belt | C | 500 |  |  |
| 13938 | Low-Grade Magic Pouch Cloth Belt | C | 500 |  |  |
| 13939 | Regular Magic Pouch Cloth Belt | C | 500 |  |  |
| 13940 | High-Grade Magic Pouch Cloth Belt | C | 500 |  |  |
| 13941 | Top-Grade Magic Pouch Cloth Belt | C | 500 |  |  |
| 13954 | Low-Grade Magic Pin Cloth Belt | C | 500 |  |  |
| 13955 | Regular Magic Pin Cloth Belt | C | 500 |  |  |
| 13956 | High-Grade Magic Pin Cloth Belt | C | 500 |  |  |
| 13957 | Top-Grade Magic Pin Cloth Belt | C | 500 |  |  |
| 13975 | Poison Bottle 1 | C | 4830 |  |  |
| 22312 | Top-Grade Magic Pin Cloth Belt | C | 500 |  |  |
| 22313 | Top-Grade Magic Pouch Cloth Belt | C | 500 |  |  |
| 13895 | Leather Belt | B | 480 |  |  |
| 13942 | Low-Grade Magic Pouch Leather Belt | B | 480 |  |  |
| 13943 | Regular Magic Pouch Leather Belt | B | 480 |  |  |
| 13944 | High-Grade Magic Pouch Leather Belt | B | 480 |  |  |
| 13945 | Top-Grade Magic Pouch Leather Belt | B | 480 |  |  |
| 13958 | Low-Grade Magic Pin Leather Belt | B | 480 |  |  |
| 13959 | Regular Magic Pin Leather Belt | B | 480 |  |  |
| 13960 | High-Grade Magic Pin Leather Belt | B | 480 |  |  |
| 13961 | Top-Grade Magic Pin Leather Belt | B | 480 |  |  |
| 13976 | Poison Bottle 2 | B | 4830 |  |  |
| 13896 | Iron Belt | A | 460 |  |  |
| 13946 | Low-Grade Magic Pouch Iron Belt | A | 460 |  |  |
| 13947 | Regular Magic Pouch Iron Belt | A | 460 |  |  |
| 13948 | High-Grade Magic Pouch Iron Belt | A | 460 |  |  |
| 13949 | Top-Grade Magic Pouch Iron Belt | A | 460 |  |  |
| 13962 | Low-Grade Magic Pin Iron Belt | A | 460 |  |  |
| 13963 | Regular Magic Pin Iron Belt | A | 460 |  |  |
| 13964 | High-Grade Magic Pin Iron Belt | A | 460 |  |  |
| 13965 | Top-Grade Magic Pin Iron Belt | A | 460 |  |  |
| 13977 | Poison Bottle 3 | A | 4830 |  |  |
| 14922 | Low-grade Magic Rune Clip Iron Belt - HP Recovery | A | 460 |  |  |
| 14923 | Ordinary Magic Rune Clip Iron Belt - HP Recovery | A | 460 |  |  |
| 14924 | High-grade Magic Rune Clip Iron Belt - HP Recovery | A | 460 |  |  |
| 14925 | Top-grade Magic Rune Clip Iron Belt - HP Recovery | A | 460 |  |  |
| 14930 | Low-grade Magic Rune Clip Iron Belt - MP Recovery | A | 460 |  |  |
| 14931 | Ordinary Magic Rune Clip Iron Belt - MP Recovery | A | 460 |  |  |
| 14932 | High-grade Magic Rune Clip Iron Belt - MP Recovery | A | 460 |  |  |
| 14933 | Top-grade Magic Rune Clip Iron Belt - MP Recovery | A | 460 |  |  |
| 14938 | Low-grade Magic Ornament Iron Belt - PvP Physical Attack | A | 440 |  |  |
| 14939 | Regular Magic Ornament Iron Belt - PvP Physical Attack | A | 440 |  |  |
| 14940 | High-grade Magic Ornament Iron Belt - PvP Physical Attack | A | 440 |  |  |
| 14941 | Top-grade Magic Ornament Iron Belt - PvP Physical Attack | A | 440 |  |  |
| 14942 | Low-grade Magic Ornament Iron Belt - PvP Skill Attack | A | 440 |  |  |
| 14943 | Regular Magic Ornament Iron Belt - PvP Skill Attack | A | 440 |  |  |
| 14944 | High-grade Magic Ornament Iron Belt - PvP Skill Attack | A | 440 |  |  |
| 14945 | Top-grade Magic Ornament Iron Belt - PvP Skill Attack | A | 440 |  |  |
| 14946 | Low-grade Magic Ornament Iron Belt - PVP Defense | A | 440 |  |  |
| 14947 | Regular Magic Ornament Iron Belt - PVP Defense | A | 440 |  |  |
| 14948 | High-grade Magic Ornament Iron Belt - PVP Defense | A | 440 |  |  |
| 14949 | Top-grade Magic Ornament Iron Belt - PVP Defense | A | 440 |  |  |
| 13897 | Mithril Belt | S | 440 |  |  |
| 13950 | Low-Grade Magic Pouch Mithril Belt | S | 440 |  |  |
| 13951 | Regular Magic Pouch Mithril Belt | S | 440 |  |  |
| 13952 | High-Grade Magic Pouch Mithril Belt | S | 440 |  |  |
| 13953 | Top-Grade Magic Pouch Mithril Belt | S | 440 |  |  |
| 13966 | Low-Grade Magic Pin Mithril Belt | S | 440 |  |  |
| 13967 | Regular Magic Pin Mithril Belt | S | 440 |  |  |
| 13968 | High-Grade Magic Pin Mithril Belt | S | 440 |  |  |
| 13969 | Top-Grade Magic Pin Mithril Belt | S | 440 |  |  |
| 14926 | Low-grade Magic Rune Clip Mithril Belt - HP Recovery | S | 440 |  |  |
| 14927 | Ordinary Magic Rune Clip Mithril Belt - HP Recovery | S | 440 |  |  |
| 14928 | High-grade Magic Rune Clip Mithril Belt - HP Recovery | S | 440 |  |  |
| 14929 | Top-grade Magic Rune Clip Mithril Belt - HP Recovery | S | 440 |  |  |
| 14934 | Low-grade Magic Rune Clip Mithril Belt - MP Recovery | S | 440 |  |  |
| 14935 | Ordinary Magic Rune Clip Mithril Belt - MP Recovery | S | 440 |  |  |
| 14936 | High-grade Magic Rune Clip Mithril Belt - MP Recovery | S | 440 |  |  |
| 14937 | Top-grade Magic Rune Clip Mithril Belt - MP Recovery | S | 440 |  |  |
| 14950 | Low-grade Magic Ornament Mithril Belt - PvP Physical Attack | S | 440 |  |  |
| 14951 | Regular Magic Ornament Mithril Belt - PvP Physical Attack | S | 440 |  |  |
| 14952 | High-grade Magic Ornament Mithril Belt - PvP Physical Attack | S | 440 |  |  |
| 14953 | Top-grade Magic Ornament Mithril Belt - PvP Physical Attack | S | 440 |  |  |
| 14954 | Low-grade Magic Ornament Mithril Belt - PvP Skill Attack | S | 440 |  |  |
| 14955 | Regular Magic Ornament Mithril Belt - PvP Skill Attack | S | 440 |  |  |
| 14956 | High-grade Magic Ornament Mithril Belt - PvP Skill Attack | S | 440 |  |  |
| 14957 | Top-grade Magic Ornament Mithril Belt - PvP Skill Attack | S | 440 |  |  |
| 14958 | Low-grade Magic Ornament Mithril Belt - PVP Defense | S | 440 |  |  |
| 14959 | Regular Magic Ornament Mithril Belt - PVP Defense | S | 440 |  |  |
| 14960 | High-grade Magic Ornament Mithril Belt - PVP Defense | S | 440 |  |  |
| 14961 | Top-grade Magic Ornament Mithril Belt - PVP Defense | S | 440 |  |  |

### Hair accessory — `bodypart=hair` (113)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 5808 | Party Mask | NONE | 10 |  |  |
| 6394 | Red Party Mask | NONE | 10 |  |  |
| 6834 | Circlet of Innadril | NONE | 10 |  |  |
| 6835 | Circlet of Dion | NONE | 10 |  |  |
| 6836 | Goddard Circlet | NONE | 10 |  |  |
| 6837 | Circlet of Oren | NONE | 10 |  |  |
| 6838 | Circlet of Gludio | NONE | 10 |  |  |
| 6839 | Circlet of Giran | NONE | 10 |  |  |
| 6840 | Circlet of Aden | NONE | 10 |  |  |
| 6841 | The Lord's Crown | NONE | 10 |  |  |
| 6842 | Wings of Destiny Circlet | NONE | 10 |  |  |
| 6843 | Cat Ears | NONE | 10 |  |  |
| 6844 | Lady's Hair Pin | NONE | 10 |  |  |
| 6845 | Pirate's Eye Patch | NONE | 10 |  |  |
| 6846 | Monocle | NONE | 10 |  |  |
| 7059 | Golden Festival Mask | NONE | 10 |  |  |
| 7060 | Tateossian Hairband | NONE | 10 |  |  |
| 7680 | Raccoon Ears | NONE | 10 |  |  |
| 7681 | Outlaw's Eyepatch | NONE | 10 |  |  |
| 7682 | Maiden's Hairpin | NONE | 10 |  |  |
| 7683 | Rabbit Ears | NONE | 10 |  |  |
| 7694 | Noblesse Tiara | NONE | 10 |  |  |
| 7695 | Forget-me-not Hairpin | NONE | 10 |  |  |
| 7696 | Daisy Hairpin | NONE | 10 |  |  |
| 7837 | Sayha's White Mask | NONE | 10 |  |  |
| 7839 | Gran Kain's Black Mask | NONE | 10 |  |  |
| 7840 | Rabbit Ears - Event | NONE | 10 |  |  |
| 7841 | Racoon Ears | NONE | 10 |  |  |
| 7842 | Cat Ears | NONE | 10 |  |  |
| 7843 | Pirate's Eyepatch | NONE | 10 |  |  |
| 7844 | Monocle | NONE | 10 |  |  |
| 7845 | Outlaw's Eyepatch | NONE | 10 |  |  |
| 7846 | Maiden's Hairpin | NONE | 10 |  |  |
| 7847 | Lady's Hairpin | NONE | 10 |  |  |
| 7848 | Forget-me-not Hairpin | NONE | 10 |  |  |
| 7849 | Daisy Hairpin | NONE | 10 |  |  |
| 8177 | Raid Challenger's Circlet | NONE | 10 |  |  |
| 8178 | Raid Adventurer's Circlet | NONE | 10 |  |  |
| 8179 | Raid Master's Circlet | NONE | 10 |  |  |
| 8180 | Circlet of Ice Fairy Sirra | NONE | 10 |  |  |
| 8181 | Academy Circlet | NONE | 10 |  |  |
| 8182 | Circlet of Rune | NONE | 10 |  |  |
| 8183 | Circlet of Schuttgart | NONE | 10 |  |  |
| 8187 | Demon Horns | NONE | 10 |  |  |
| 8188 | Little Angel Wings | NONE | 10 |  |  |
| 8189 | Fairy Antennae | NONE | 10 |  |  |
| 8552 | Mask of Spirits | NONE | 10 |  |  |
| 8558 | Eva's Mark (Event) | NONE | 10 |  |  |
| 8567 | Valakas Slayer Circlet | NONE | 10 |  |  |
| 8568 | Antharas Slayer Circlet | NONE | 10 |  |  |
| 8569 | Half Face Mask | NONE | 10 |  |  |
| 8660 | Demon Horns | NONE | 10 |  |  |
| 8661 | Mask of Spirits | NONE | 10 |  |  |
| 8662 | Fairy Antennae (Event) | NONE | 10 |  |  |
| 8911 | Black Half Mask (Event) | NONE | 10 |  |  |
| 8912 | Single Stem Flower | NONE | 10 |  |  |
| 8913 | Butterfly Hairpin | NONE | 10 |  |  |
| 8916 | Eye Patch | NONE | 10 |  |  |
| 8923 | Scar | NONE | 10 |  |  |
| 8947 | L2day - Rabbit Ears | NONE | 10 |  |  |
| 8948 | L2day - Little Angel Wings | NONE | 10 |  |  |
| 8949 | L2day - Fairy Antennae | NONE | 10 |  |  |
| 9145 | Little Angel Wings (Event) | NONE | 10 |  |  |
| 10175 | Goblin Circlet (Event) | NONE | 10 |  |  |
| 10176 | White Half Mask | NONE | 10 |  |  |
| 10177 | Black Half Mask | NONE | 10 |  |  |
| 17173 | Mark of Victory - Korea | NONE | 0 |  |  |
| 17174 | Mark of Cheers | NONE | 0 |  |  |
| 20016 | Horn-Rimmed Glasses - Agility | NONE | 10 |  |  |
| 20022 | Ruthless Tribe Mask | NONE | 10 |  |  |
| 20023 | Ribbon Hairband | NONE | 10 |  |  |
| 20086 | Horn Rimmed Glasses - Vitality - 3-Hour Limited Period | NONE | 10 |  |  |
| 20087 | Horn Rimmed Glasses - Vitality - 3-Day Limited Period | NONE | 10 |  |  |
| 20088 | Horn Rimmed Glasses - Vitality - 30-Day Limited Period | NONE | 10 |  |  |
| 20321 | Goggle | NONE | 10 |  |  |
| 20322 | Napoleon Hat | NONE | 10 |  |  |
| 20323 | Horn Hairband | NONE | 10 |  |  |
| 20324 | Black Gem Mask | NONE | 10 |  |  |
| 20399 | Laborer Hat - Blessed Body - 7-day limited period | NONE | 10 |  |  |
| 20400 | Laborer Hat - Blessed Soul - 7-day limited period | NONE | 10 |  |  |
| 20401 | Laborer Hat | NONE | 10 |  |  |
| 20414 | Horn Rimmed Glasses - Agility - 7-day limited period | NONE | 10 |  |  |
| 20419 | Ruthless Tribe Mask - Agility - 7-day limited period | NONE | 10 |  |  |
| 20420 | Ribbon Hairband - Reflect Damage - 7-Day Limited Period | NONE | 10 |  |  |
| 20426 | Goggles - Wind Walk - 7-Day Limited Period | NONE | 10 |  |  |
| 20427 | Napoleon Hat - Mana Regeneration - 7-Day Limited Period | NONE | 10 |  |  |
| 20428 | Horn Hairband - Reflect Damage - 7-Day Limited Period | NONE | 10 |  |  |
| 20429 | Black Gem Mask - Vitality - 7-Day Limited Period | NONE | 10 |  |  |
| 20433 | Outlaw's Eyepatch - Death Whisper - 7-Day Limited Period | NONE | 10 |  |  |
| 20434 | Pirate's Eyepatch - Agility - 7-day limited period | NONE | 10 |  |  |
| 20435 | Monocle - Wild Magic - 7-Day Limited Period | NONE | 10 |  |  |
| 20436 | Red Mask of Victory - Mana Regeneration - 7-Day Limited Period | NONE | 10 |  |  |
| 20438 | Party Mask - Greater Heal - 7-Day Limited Period | NONE | 10 |  |  |
| 20439 | Red Party Mask - Resist Unholy - 7-Day Limited Period | NONE | 10 |  |  |
| 20538 | Horn Rimmed Glasses - Energy - 7-Day Limited Period | NONE | 10 |  |  |
| 20613 | Headphone - Town Theme | NONE | 10 |  |  |
| 20614 | Headphone - Hero Theme | NONE | 10 |  |  |
| 20615 | Headphone - Park Theme | NONE | 10 |  |  |
| 20616 | Headphone - Town Theme - 7-day limited period | NONE | 10 |  |  |
| 20617 | Headphone - Hero Theme - 7-day limited period | NONE | 10 |  |  |
| 20618 | Headphone - Park Theme - 7-day limited period | NONE | 10 |  |  |
| 21012 | Mark of Victory - Korea | NONE | 10 |  |  |
| 21013 | Mark of Victory - Japan | NONE | 10 |  |  |
| 21014 | Mark of Cheers | NONE | 10 |  |  |
| 21122 | Gold-rimmed Glasses | NONE | 10 |  |  |
| 21123 | Gold-rimmed Glasses - 7-day limited period | NONE | 10 |  |  |
| 21202 | Magic Glasses - 30-day limited period | NONE | 10 |  |  |
| 22158 | Outlaw's Eyepatch | NONE | 10 |  |  |
| 22159 | Pirate's Eyepatch | NONE | 10 |  |  |
| 22160 | Monocle | NONE | 10 |  |  |
| 22161 | Red Mask of Victory | NONE | 10 |  |  |
| 22163 | Party Mask | NONE | 10 |  |  |
| 22164 | Red Party Mask | NONE | 10 |  |  |

### Hair accessory (slot 2) — `bodypart=hair2` (18)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 20431 | Daisy Hairpin - Resist Unholy - 7-Day Limited Period | NONE | 10 |  |  |
| 20432 | Forget-me-not Hairpin - Wind Walk - 7-Day Limited Period | NONE | 10 |  |  |
| 20437 | Red Horn of Victory - Reflect Damage - 7-Day Limited Period | NONE | 10 |  |  |
| 20440 | Cat Ears - Wind Walk - 7-Day Limited Period | NONE | 10 |  |  |
| 20441 | Lady's Hair Pin - Death Whisper - 7-Day Limited Period | NONE | 10 |  |  |
| 20442 | Raccoon Ears - Agility - 7-day limited period | NONE | 10 |  |  |
| 20443 | Rabbit Ear - Wild Magic - 7-Day Limited Period | NONE | 10 |  |  |
| 20444 | Little Angel Wings - Mana Regeneration - 7-Day Limited Period | NONE | 10 |  |  |
| 20445 | Fairy's Tentacle - Reflect Damage - 7-Day Limited Period | NONE | 10 |  |  |
| 22156 | Daisy Hairpin | NONE | 10 |  |  |
| 22157 | Forget-me-not Hairpin | NONE | 10 |  |  |
| 22162 | Red Horn of Victory | NONE | 10 |  |  |
| 22165 | Cat Ears | NONE | 10 |  |  |
| 22166 | Lady's Hair Pin | NONE | 10 |  |  |
| 22167 | Raccoon Ears | NONE | 10 |  |  |
| 22168 | Rabbit Ear | NONE | 10 |  |  |
| 22169 | Little Angel Wings | NONE | 10 |  |  |
| 22170 | Fairy's Tentacle | NONE | 10 |  |  |

### Hair accessory (covers both slots) — `bodypart=hairall` (572)

| Id | Name | Grade | Weight | mDef | Notes |
| ---: | --- | --- | ---: | ---: | --- |
| 7836 | Santa's Hat | NONE | 10 |  |  |
| 8184 | Party Hat | NONE | 10 |  |  |
| 8185 | Feathered Hat | NONE | 10 |  |  |
| 8186 | Artisan's Goggles | NONE | 10 |  |  |
| 8557 | Blue Party Hat | NONE | 10 |  |  |
| 8559 | Diadem | NONE | 10 |  |  |
| 8560 | Teddy Bear Hat | NONE | 10 |  |  |
| 8561 | Piggy Hat | NONE | 10 |  |  |
| 8562 | Jester Hat | NONE | 10 |  |  |
| 8563 | Wizard Hat | NONE | 10 |  |  |
| 8564 | Dapper Cap | NONE | 10 |  |  |
| 8565 | Romantic Chapeau | NONE | 10 |  |  |
| 8566 | Iron Circlet | NONE | 10 |  |  |
| 8910 | Black Feather Mask | NONE | 10 |  |  |
| 8914 | Luxurious Gold Circlet | NONE | 10 |  |  |
| 8915 | Luxurious Silver Circlet | NONE | 10 |  |  |
| 8917 | Goddess Circlet | NONE | 10 |  |  |
| 8918 | Leather Cap | NONE | 10 |  |  |
| 8919 | First Mate's Hat | NONE | 10 |  |  |
| 8920 | Angel Halo | NONE | 10 |  |  |
| 8921 | Demon Circlet | NONE | 10 |  |  |
| 8922 | Pirate Hat | NONE | 10 |  |  |
| 8936 | Santa's Antlers | NONE | 10 |  |  |
| 8950 | L2day - Feathered Hat | NONE | 10 |  |  |
| 8951 | L2day - Artisan's Goggles | NONE | 10 |  |  |
| 9138 | Santa's Hat | NONE | 10 |  |  |
| 9158 | Gold Circlet of Redemption | NONE | 10 |  |  |
| 9159 | Silver Circlet of Salvation | NONE | 10 |  |  |
| 9160 | Pig Wrangler's Cap | NONE | 10 |  |  |
| 9177 | Shadow Item - Teddy Bear Hat - Resurrection | NONE | 10 |  |  |
| 9178 | Shadow Item - Piggy Hat - Resurrection | NONE | 10 |  |  |
| 9179 | Shadow Item - Jester Hat - Resurrection | NONE | 10 |  |  |
| 9180 | Shadow Item - Wizard Hat - Resurrection | NONE | 10 |  |  |
| 9181 | Shadow Item - Dapper Cap - Resurrection | NONE | 10 |  |  |
| 9182 | Shadow Item - Romantic Chapeau - Resurrection | NONE | 10 |  |  |
| 9183 | Shadow Item - Iron Circlet - Resurrection | NONE | 10 |  |  |
| 9184 | Shadow Item - Teddy Bear Hat - Blessed Escape | NONE | 10 |  |  |
| 9185 | Shadow Item - Piggy Hat - Blessed Escape | NONE | 10 |  |  |
| 9186 | Shadow Item - Jester Hat - Blessed Escape | NONE | 10 |  |  |
| 9187 | Shadow Item - Wizard Hat - Blessed Escape | NONE | 10 |  |  |
| 9188 | Shadow Item - Dapper Cap - Blessed Escape | NONE | 10 |  |  |
| 9189 | Shadow Item - Romantic Chapeau - Blessed Escape | NONE | 10 |  |  |
| 9190 | Shadow Item - Iron Circlet - Blessed Escape | NONE | 10 |  |  |
| 9191 | Shadow Item - Teddy Bear Hat - Big Head | NONE | 10 |  |  |
| 9192 | Shadow Item - Piggy Hat - Big Head | NONE | 10 |  |  |
| 9193 | Shadow Item - Jester Hat - Big Head | NONE | 10 |  |  |
| 9194 | Shadow Item - Wizard Hat - Big Head | NONE | 10 |  |  |
| 9195 | Shadow Item - Dapper Cap - Big Head | NONE | 10 |  |  |
| 9196 | Shadow Item - Romantic Chapeau - Big Head | NONE | 10 |  |  |
| 9197 | Shadow Item - Iron Circlet - Big Head | NONE | 10 |  |  |
| 9198 | Shadow Item - Teddy Bear Hat - Firework | NONE | 10 |  |  |
| 9199 | Shadow Item - Piggy Hat - Firework | NONE | 10 |  |  |
| 9200 | Shadow Item - Jester Hat - Firework | NONE | 10 |  |  |
| 9201 | Shadow Item - Wizard Hat - Firework | NONE | 10 |  |  |
| 9202 | Shadow Item - Dapper Cap - Firework | NONE | 10 |  |  |
| 9203 | Shadow Item - Romantic Chapeau - Firework | NONE | 10 |  |  |
| 9204 | Shadow Item - Iron Circlet - Firework | NONE | 10 |  |  |
| 9208 | Phantom Mask (Event) | NONE | 10 |  |  |
| 9391 | Human Circlet | NONE | 10 |  |  |
| 9392 | Elven Circlet | NONE | 10 |  |  |
| 9393 | Dark Elven Circlet | NONE | 10 |  |  |
| 9394 | Orcish Circlet | NONE | 10 |  |  |
| 9395 | Dwarven Circlet | NONE | 10 |  |  |
| 9396 | Kamaelic Circlet | NONE | 10 |  |  |
| 9397 | Shield Master Circlet | NONE | 10 |  |  |
| 9398 | Bard Circlet | NONE | 10 |  |  |
| 9399 | Force Master Circlet | NONE | 10 |  |  |
| 9400 | Weapon Master Circlet | NONE | 10 |  |  |
| 9401 | Dagger Master Circlet | NONE | 10 |  |  |
| 9402 | Bow Master Circlet | NONE | 10 |  |  |
| 9403 | Wizard Circlet | NONE | 10 |  |  |
| 9404 | Summoner Circlet | NONE | 10 |  |  |
| 9405 | Healer Circlet | NONE | 10 |  |  |
| 9406 | Enchanter Circlet | NONE | 10 |  |  |
| 9407 | Weapon Master Circlet (Kamael only) | NONE | 10 |  |  |
| 9408 | Bow Master Circlet (Kamael only) | NONE | 10 |  |  |
| 9409 | Black Phantom Mask (Event) | NONE | 10 |  |  |
| 9410 | Human Veteran's Circlet | NONE | 10 |  |  |
| 9411 | Elven Veteran's Circlet | NONE | 10 |  |  |
| 9412 | Dark Elven Veteran's Circlet | NONE | 10 |  |  |
| 9413 | Orcish Veteran's Circlet | NONE | 10 |  |  |
| 9414 | Dwarf Veteran's Circlet | NONE | 10 |  |  |
| 9415 | Kamaelic Veteran's Circlet | NONE | 10 |  |  |
| 9883 | Teddy Bear Hat - Big Head | NONE | 10 |  |  |
| 9884 | Piggy Hat - Big Head | NONE | 10 |  |  |
| 9885 | Jester Hat - Big Head | NONE | 10 |  |  |
| 9886 | Wizard Hat - Big Head | NONE | 10 |  |  |
| 9887 | Dapper Cap - Big Head | NONE | 10 |  |  |
| 9888 | Romantic Chapeau - Big Head | NONE | 10 |  |  |
| 9889 | Iron Circlet - Big Head | NONE | 10 |  |  |
| 9890 | Teddy Bear Hat - Firework | NONE | 10 |  |  |
| 9891 | Piggy Hat - Firework | NONE | 10 |  |  |
| 9892 | Jester Hat - Firework | NONE | 10 |  |  |
| 9893 | Wizard Hat - Firework | NONE | 10 |  |  |
| 9894 | Dapper Cap - Firework | NONE | 10 |  |  |
| 9895 | Romantic Chapeau - Firework | NONE | 10 |  |  |
| 9896 | Iron Circlet - Firework | NONE | 10 |  |  |
| 10169 | Enchanter Circlet (Kamael only) | NONE | 10 |  |  |
| 10240 | Bird Nest | NONE | 10 |  |  |
| 10241 | Purple Viking Circlet | NONE | 10 |  |  |
| 10242 | Golden Viking Circlet | NONE | 10 |  |  |
| 10243 | Panda Hat | NONE | 10 |  |  |
| 10244 | White Sheep Hat | NONE | 10 |  |  |
| 10245 | Black Sheep Hat | NONE | 10 |  |  |
| 10246 | Frog Hat | NONE | 10 |  |  |
| 10247 | Fish Hat | NONE | 10 |  |  |
| 10248 | Straw Hat | NONE | 10 |  |  |
| 10249 | Chicken Hat | NONE | 10 |  |  |
| 10250 | Adventurer Hat (Event) | NONE | 10 |  |  |
| 10251 | Medieval Party Mask | NONE | 10 |  |  |
| 10315 | Shadow Item - Purple Viking Circlet | NONE | 10 |  |  |
| 10321 | Shadow Item - Golden Viking Circlet | NONE | 10 |  |  |
| 10613 | Bird Nest (Event) | NONE | 10 |  |  |
| 10614 | White Wool Hat (Event) | NONE | 10 |  |  |
| 10615 | Black Wool Hat (Event) | NONE | 10 |  |  |
| 10616 | Straw Hat (Event) | NONE | 10 |  |  |
| 10617 | Ant Hat - Year 2008 | NONE | 10 |  |  |
| 10618 | Ol Mahum Hat - Year 2008 | NONE | 10 |  |  |
| 10619 | Wolf Hat - Year 2008 | NONE | 10 |  |  |
| 10620 | Shadow Item - Ant Hat - Blessed Scroll of Escape | NONE | 10 |  |  |
| 10621 | Shadow Item - Ant Hat - Blessed Scroll of Resurrection | NONE | 10 |  |  |
| 10622 | Shadow Item - Ant Hat - Firework | NONE | 10 |  |  |
| 10623 | Shadow Item - Ant Hat - Big Head | NONE | 10 |  |  |
| 10624 | Shadow Item - Ol Mahum Hat - Blessed Scroll of Escape | NONE | 10 |  |  |
| 10625 | Shadow Item - Ol Mahum Hat - Blessed Scroll of Resurrection | NONE | 10 |  |  |
| 10626 | Shadow Item - Ol Mahum Hat - Firework | NONE | 10 |  |  |
| 10627 | Shadow Item - Ol Mahum Hat - Big Head | NONE | 10 |  |  |
| 10628 | Shadow Item - Wolf Hat - Blessed Scroll of Escape | NONE | 10 |  |  |
| 10629 | Shadow Item - Wolf Hat - Blessed Scroll of Resurrection | NONE | 10 |  |  |
| 10630 | Shadow Item - Wolf Hat - Firework | NONE | 10 |  |  |
| 10631 | Shadow Item - Wolf Hat - Big Head | NONE | 10 |  |  |
| 12372 | Monkey Hat | NONE | 10 |  |  |
| 12373 | Pig Hat | NONE | 10 |  |  |
| 12766 | Gold Circlet | NONE | 10 |  |  |
| 12767 | Silver Circlet | NONE | 10 |  |  |
| 12781 | Ol Mahum Hat | NONE | 10 |  |  |
| 12782 | Kat the Cat Hat - 30-day limited period | NONE | 10 |  |  |
| 12783 | Feline Queen Hat - 30-day limited period | NONE | 10 |  |  |
| 12784 | Ant Hat | NONE | 10 |  |  |
| 12785 | Wolf Hat | NONE | 10 |  |  |
| 12786 | Monster Eye Hat - 30-day limited period | NONE | 10 |  |  |
| 12787 | Brown Bear Hat - 30-day limited period | NONE | 10 |  |  |
| 12788 | Fungus Hat - 30-day limited period | NONE | 10 |  |  |
| 12789 | Skull Hat - 30-day limited period | NONE | 10 |  |  |
| 12790 | Ornithomimus Hat - 30-day limited period | NONE | 10 |  |  |
| 12791 | Feline King Hat - 30-day limited period | NONE | 10 |  |  |
| 12792 | Kai the Cat Hat - 30-day limited period | NONE | 10 |  |  |
| 12835 | Shadow Item - Teddy Bear Hat | NONE | 10 |  |  |
| 12836 | Shadow Item - Piggy Hat | NONE | 10 |  |  |
| 12837 | Shadow Item - Jester Hat | NONE | 10 |  |  |
| 12838 | Fish Hat (Event) | NONE | 10 |  |  |
| 12839 | Medieval Style Party Mask (Event) | NONE | 10 |  |  |
| 13058 | Silenos Hair Accessory | NONE | 10 |  |  |
| 13074 | Shadow Item - Top Hat | NONE | 10 |  |  |
| 13075 | Shadow Item - Black Mask | NONE | 10 |  |  |
| 13076 | Shadow Item - Rider Goggles | NONE | 10 |  |  |
| 13234 | Varka Karm (used by Varka Silenos) | NONE | 10 |  |  |
| 13235 | Ketra Karm (used by Ketra Orcs) | NONE | 10 |  |  |
| 13236 | Bronze Kamaloka Circlet | NONE | 10 |  |  |
| 13237 | Silver Kamaloka Circlet | NONE | 10 |  |  |
| 13238 | Gold Kamaloka Circlet | NONE | 10 |  |  |
| 13239 | Kat the Cat Hat - 7-day limited period | NONE | 10 |  |  |
| 13240 | Feline Queen Hat - 7-day limited period | NONE | 10 |  |  |
| 13241 | Monster Eye Hat - 7-day limited period | NONE | 10 |  |  |
| 13242 | Brown Bear Hat - 7-day limited period | NONE | 10 |  |  |
| 13243 | Fungus Hat - 7-day limited period | NONE | 10 |  |  |
| 13244 | Skull Hat - 7-day limited period | NONE | 10 |  |  |
| 13245 | Ornithomimus Hat - 7-day limited period | NONE | 10 |  |  |
| 13246 | Feline King Hat - 7-day limited period | NONE | 10 |  |  |
| 13247 | Kai the Cat Hat - 7-day limited period | NONE | 10 |  |  |
| 13310 | Kat the Cat Hat (Event) - 30-day limited period | NONE | 10 |  |  |
| 13311 | Feline Queen Hat (Event) - 30-day limited period | NONE | 10 |  |  |
| 13312 | Monster Eye Hat (Event) - 30-day limited period | NONE | 10 |  |  |
| 13313 | Brown Bear Hat (Event) - 30-day limited period | NONE | 10 |  |  |
| 13314 | Fungus Hat (Event) - 30-day limited period | NONE | 10 |  |  |
| 13315 | Skull Hat (Event) - 30-day limited period | NONE | 10 |  |  |
| 13316 | Ornithomimus Hat (Event) - 30-day limited period | NONE | 10 |  |  |
| 13317 | Feline King Hat (Event) - 30-day limited period | NONE | 10 |  |  |
| 13318 | Kai the Cat Hat (Event) - 30-day limited period | NONE | 10 |  |  |
| 13325 | Kat the Cat Hat (Event) - 7-day limited period | NONE | 10 |  |  |
| 13326 | Feline Queen Hat (Event) - 7-day limited period | NONE | 10 |  |  |
| 13327 | Monster Eye Hat (Event) - 7-day limited period | NONE | 10 |  |  |
| 13328 | Brown Bear Hat (Event) - 7-day limited period | NONE | 10 |  |  |
| 13329 | Fungus Hat (Event) - 7-day limited period | NONE | 10 |  |  |
| 13330 | Skull Hat (Event) - 7-day limited period | NONE | 10 |  |  |
| 13331 | Ornithomimus Hat (Event) - 7-day limited period | NONE | 10 |  |  |
| 13332 | Feline King Hat (Event) - 7-day limited period | NONE | 10 |  |  |
| 13333 | Kai the Cat Hat (Event) - 7-day limited period | NONE | 10 |  |  |
| 13393 | Shadow Item - Monkey Hat | NONE | 10 |  |  |
| 13394 | Shadow Item - Pig Hat | NONE | 10 |  |  |
| 13415 | Frog Hat | NONE | 10 |  |  |
| 13416 | Chicken Hat | NONE | 10 |  |  |
| 13429 | Teddy Bear Hat (Event) | NONE | 10 |  |  |
| 13430 | Piggy Hat (Event) | NONE | 10 |  |  |
| 13431 | Jester Hat (Event) | NONE | 10 |  |  |
| 13472 | Circlet of Innadril Valor | NONE | 10 |  |  |
| 13473 | Circlet of Aden Valor | NONE | 10 |  |  |
| 13474 | Circlet of Dion Valor | NONE | 10 |  |  |
| 13475 | Circlet of Dion Sniper | NONE | 10 |  |  |
| 13476 | Circlet of Innadril Sniper | NONE | 10 |  |  |
| 13477 | Circlet of Oren Sniper | NONE | 10 |  |  |
| 13478 | Circlet of Gludio Sage | NONE | 10 |  |  |
| 13479 | Circlet of Rune Sage | NONE | 10 |  |  |
| 13480 | Circlet of Giran Sage | NONE | 10 |  |  |
| 13481 | Goddard Circlet of Combat | NONE | 10 |  |  |
| 13482 | Circlet of Schuttgart Combat | NONE | 10 |  |  |
| 13483 | Circlet of Oren Combat | NONE | 10 |  |  |
| 13484 | Gludio Circlet Silence | NONE | 10 |  |  |
| 13485 | Circlet of Schuttgart Silence | NONE | 10 |  |  |
| 13486 | Circlet of Aden Unity | NONE | 10 |  |  |
| 13487 | Circlet of Rune Silence | NONE | 10 |  |  |
| 13488 | Birthday Hat | NONE | 10 |  |  |
| 13489 | Halloween Hat | NONE | 10 |  |  |
| 13490 | Arrow-Pierced Apple | NONE | 10 |  |  |
| 13491 | Popped-Out Eye | NONE | 10 |  |  |
| 13492 | Graduation Cap | NONE | 10 |  |  |
| 13493 | Refined Carnival Circlet | NONE | 10 |  |  |
| 13494 | Refined Angel Ring | NONE | 10 |  |  |
| 13495 | Refined Devil Horn | NONE | 10 |  |  |
| 13496 | Refined Pirate Hat | NONE | 10 |  |  |
| 13497 | Refined Chick Hat | NONE | 10 |  |  |
| 13498 | Refined Wizard Hat | NONE | 10 |  |  |
| 13499 | Refined Jester Hat | NONE | 10 |  |  |
| 13500 | Refined Black Feather Mask | NONE | 10 |  |  |
| 13501 | Refined Romantic Chapeau | NONE | 10 |  |  |
| 13502 | Refined Carnival Circlet | NONE | 10 |  |  |
| 13503 | Refined Medieval Style Party Mask | NONE | 10 |  |  |
| 13504 | Refined Dapper Cap | NONE | 10 |  |  |
| 13505 | Clownfish Hat | NONE | 10 |  |  |
| 13506 | Improved Lord's Crown | NONE | 10 |  |  |
| 13507 | Circlet of Flames | NONE | 10 |  |  |
| 13508 | Circlet of Freeze | NONE | 10 |  |  |
| 13509 | Circlet of Storm | NONE | 10 |  |  |
| 13510 | Circlet of Earthquake | NONE | 10 |  |  |
| 13511 | Circlet of Darkness | NONE | 10 |  |  |
| 13512 | Circlet of Splendor | NONE | 10 |  |  |
| 13513 | Mining Hat | NONE | 10 |  |  |
| 13514 | Improved Mining Hat | NONE | 10 |  |  |
| 13515 | Search Hat | NONE | 10 |  |  |
| 13516 | Improved Search Hat | NONE | 10 |  |  |
| 13517 | Event - Raccoon Hat | NONE | 10 |  |  |
| 13518 | Event - Top Hat | NONE | 10 |  |  |
| 13519 | Event - Black Mask | NONE | 10 |  |  |
| 13520 | Event - Jindo Dog Hat | NONE | 10 |  |  |
| 13521 | Event - Shaggy Dog Hat | NONE | 10 |  |  |
| 13522 | Event - Rider Goggles | NONE | 10 |  |  |
| 13523 | Event - Lineage Souvenir Circlet | NONE | 10 |  |  |
| 14611 | Rudolph's Nose | NONE | 10 |  |  |
| 14613 | Rock-Paper-Scissors Santa Hat | NONE | 10 |  |  |
| 14712 | Cow Hair Accessory | NONE | 10 |  |  |
| 14746 | For Events - Refined Chick Hat | NONE | 10 |  |  |
| 14747 | For Events - Refined Black Feather Mask | NONE | 10 |  |  |
| 14748 | For Events - Refined Carnival Circlet | NONE | 10 |  |  |
| 14749 | Afro Perm Wig | NONE | 10 |  |  |
| 14750 | Bamboo Hat | NONE | 10 |  |  |
| 14751 | Smart Glasses | NONE | 10 |  |  |
| 14752 | For Events - Refined Medieval Style Party Mask | NONE | 10 |  |  |
| 14753 | Shadow Item - Refined Chick Hat - Blessed Escape | NONE | 10 |  |  |
| 14754 | Shadow Item - Refined Chick Hat - Big Head | NONE | 10 |  |  |
| 14755 | Shadow Item - Refined Chick Hat - Firework | NONE | 10 |  |  |
| 14756 | Shadow Item - Refined Black Feather Mask - Blessed Escape | NONE | 10 |  |  |
| 14757 | Shadow Item - Refined Black Feather Mask - Big Head | NONE | 10 |  |  |
| 14758 | Shadow Item - Refined Black Feather Mask - Firework | NONE | 10 |  |  |
| 14759 | Shadow Item - Refined Carnival Circlet - Blessed Escape | NONE | 10 |  |  |
| 14760 | Shadow Item - Refined Carnival Circlet - Big Head | NONE | 10 |  |  |
| 14761 | Shadow Item - Refined Carnival Circlet - Firework | NONE | 10 |  |  |
| 14762 | Shadow Item - Refined Medieval Style Party Mask - Blessed Escape | NONE | 10 |  |  |
| 14763 | Shadow Item - Refined Medieval Style Party Mask - Big Head | NONE | 10 |  |  |
| 14764 | Shadow Item - Refined Medieval Style Party Mask - Firework | NONE | 10 |  |  |
| 14771 | Kat the Cat Hat - 14-day limited period | NONE | 0 |  |  |
| 14772 | Coronet | NONE | 10 |  |  |
| 14962 | Gold Skeleton Circlet | NONE | 10 |  |  |
| 14963 | Silver Skeleton Circlet | NONE | 10 |  |  |
| 14964 | Red Skeleton Circlet | NONE | 10 |  |  |
| 14965 | Black Skeleton Circlet | NONE | 10 |  |  |
| 15221 | Puffy Hat of Friendship | NONE | 10 |  |  |
| 15441 | Red Flare Valakas Hair Accessory | NONE | 10 |  |  |
| 15442 | Jack O'Lantern Mask | NONE | 10 |  |  |
| 15443 | Super Strong Giant's Mask | NONE | 10 |  |  |
| 15444 | Silent Scream's Mask | NONE | 10 |  |  |
| 15445 | Wrathful Spirit's Mask | NONE | 10 |  |  |
| 15446 | Unrotten Corpse's Mask | NONE | 10 |  |  |
| 15447 | Planet X235 Alien's Mask | NONE | 10 |  |  |
| 15448 | Golden Jack O'Lantern Mask - Permanent Use | NONE | 10 |  |  |
| 15449 | Shiny Planet X235 Alien's Mask | NONE | 10 |  |  |
| 15450 | Shiny Super Strong Giant's Mask | NONE | 10 |  |  |
| 15451 | Shiny Silent Scream's Mask | NONE | 10 |  |  |
| 15452 | Shiny Wrathful Spirit's Mask | NONE | 10 |  |  |
| 15453 | Shiny Unrotten Corpse's Mask | NONE | 10 |  |  |
| 15464 | Golden Jack O'Lantern Mask - 7-day limited period | NONE | 0 |  |  |
| 15484 | High-level Angel Circlet | NONE | 10 |  |  |
| 16098 | Refined Black Skeleton Circlet | NONE | 10 |  |  |
| 16099 | Refined Orange Skeleton Circlet | NONE | 10 |  |  |
| 16100 | Refined Green Skeleton Circlet | NONE | 10 |  |  |
| 16101 | Refined Brown Skeleton Circlet | NONE | 10 |  |  |
| 16102 | Refined Shark Hat | NONE | 10 |  |  |
| 16103 | Chic Gold Horn Cap | NONE | 10 |  |  |
| 16104 | Chic Silver Horn Cap | NONE | 10 |  |  |
| 16105 | Refined Penguin Hat | NONE | 10 |  |  |
| 16106 | Refined Brown Turban | NONE | 10 |  |  |
| 16107 | Refined Yellow Turban | NONE | 10 |  |  |
| 16108 | Refined Turtle Hat | NONE | 10 |  |  |
| 16109 | Refined Cow Hat | NONE | 10 |  |  |
| 17033 | Circlet of Freeze - For Events - 30-day limited period | NONE | 10 |  |  |
| 17141 | Ribbon Hairband - Promotion | NONE | 10 |  |  |
| 17142 | Refined Wizard Hat - Promotion | NONE | 10 |  |  |
| 17143 | Refined Jester Hat - Promotion | NONE | 10 |  |  |
| 17144 | Refined Romantic Chapeau - Promotion | NONE | 10 |  |  |
| 17145 | Refined Dapper Cap - Promotion | NONE | 10 |  |  |
| 17146 | Refined Angel Ring - Promotion | NONE | 10 |  |  |
| 17147 | Popped-Out Eye - Promotion | NONE | 10 |  |  |
| 17148 | Bird Nest - Promotion | NONE | 10 |  |  |
| 17149 | Varka Karm (used by Varka Silenos) - Promotion | NONE | 10 |  |  |
| 17150 | Ketra Karm (used by Ketra Orcs) - Promotion | NONE | 10 |  |  |
| 17151 | Puffy Hat of Friendship - Promotion | NONE | 10 |  |  |
| 17152 | Arrow-Pierced Apple - Promotion | NONE | 10 |  |  |
| 17153 | Fish Hat - Promotion | NONE | 10 |  |  |
| 17154 | Purple Viking Circlet - Promotion | NONE | 10 |  |  |
| 17155 | Golden Viking Circlet - Promotion | NONE | 10 |  |  |
| 17156 | White Sheep Hat - Promotion | NONE | 10 |  |  |
| 17157 | Black Sheep Hat - Promotion | NONE | 10 |  |  |
| 17170 | Soccer Ball Afro Hair - White | NONE | 0 |  |  |
| 17171 | Soccer Ball Afro Hair - Blue | NONE | 0 |  |  |
| 17172 | Soccer Ball Afro Hair - Red | NONE | 0 |  |  |
| 17288 | Ice Watermelon Hat - Event | NONE | 10 |  |  |
| 17289 | Ice Watermelon Hat | NONE | 10 |  |  |
| 20017 | Afro Hair | NONE | 10 |  |  |
| 20018 | Afro Hair - Big Head, Firework | NONE | 10 |  |  |
| 20019 | Afro Hair - Wind Walk | NONE | 10 |  |  |
| 20020 | Uniform Hat | NONE | 10 |  |  |
| 20021 | Assassin's Bamboo Hat | NONE | 10 |  |  |
| 20024 | Visor | NONE | 10 |  |  |
| 20031 | Kat the Cat Hat | NONE | 10 |  |  |
| 20032 | Skull Hat | NONE | 10 |  |  |
| 20083 | Afro Hair - Vitality - 3-Hour Limited Period | NONE | 10 |  |  |
| 20084 | Afro Hair - Vitality - 3-Day Limited Period | NONE | 10 |  |  |
| 20085 | Afro Hair - Vitality - 30-Day Limited Period | NONE | 10 |  |  |
| 20089 | Assassin's Bamboo Hat - Vitality - 3-Hour Limited Period | NONE | 10 |  |  |
| 20090 | Assassin's Bamboo Hat - Vitality - 3-Day Limited Period | NONE | 10 |  |  |
| 20091 | Assassin's Bamboo Hat - Vitality - 30-Day Limited Period | NONE | 10 |  |  |
| 20095 | Santa Horn Hat | NONE | 10 |  |  |
| 20100 | Saving Santa Hat - 24-hour limited period | NONE | 10 |  |  |
| 20275 | Gold Afro | NONE | 10 |  |  |
| 20276 | Pink Afro | NONE | 10 |  |  |
| 20325 | Plastic Hair | NONE | 10 |  |  |
| 20415 | Afro Hair - Big Head, Firework - 7-day limited period | NONE | 10 |  |  |
| 20416 | Afro Hair - Wind Walk - 7-Day Limited Period | NONE | 10 |  |  |
| 20417 | Uniform Hat - Blessed Resurrection - 7-day limited period | NONE | 10 |  |  |
| 20418 | Assassin's Bamboo Hat - Wind Walk - 7-Day Limited Period | NONE | 10 |  |  |
| 20421 | Visor - Mana Regeneration - 7-Day Limited Period | NONE | 10 |  |  |
| 20422 | Kat the Cat Hat - Greater Heal - 7-Day Limited Period | NONE | 10 |  |  |
| 20423 | Skull Hat - Death Whisper - 7-Day Limited Period | NONE | 10 |  |  |
| 20424 | Afro Hair - Gold - Agility - 7-day limited period | NONE | 10 |  |  |
| 20425 | Afro Hair - Pink - Wild Magic - 7-Day Limited Period | NONE | 10 |  |  |
| 20430 | Plastic Hair - Blessed Escape - 7-day limited period | NONE | 10 |  |  |
| 20446 | Dandy's Chapeau - Greater Heal - 7-Day Limited Period | NONE | 10 |  |  |
| 20447 | Artisan's Goggles - Energy - 7-Day Limited Period | NONE | 10 |  |  |
| 20499 | Feline Queen Hat | NONE | 10 |  |  |
| 20500 | Feline King Hat | NONE | 10 |  |  |
| 20501 | Kai the Cat Hat | NONE | 10 |  |  |
| 20537 | Afro Hair - Energy - 7-Day Limited Period | NONE | 10 |  |  |
| 20539 | Assassin's Bamboo Hat - Energy - 7-Day Limited Period | NONE | 10 |  |  |
| 20567 | Eva's Circlet (event) - 3-day limited period | NONE | 10 |  |  |
| 20568 | Eva's Circlet - 7-day limited period | NONE | 10 |  |  |
| 20569 | Eva's Circlet | NONE | 10 |  |  |
| 20601 | Anniversary Hat - Soul of Phoenix - 7-day limited period | NONE | 10 |  |  |
| 20626 | Anniversary Hat - Resurrection - 7-Day Limited Period | NONE | 10 |  |  |
| 20633 | Watermelon Hat - Ability of a Cool Watermelon - 7-day limited period | NONE | 10 |  |  |
| 20634 | Watermelon Hat | NONE | 10 |  |  |
| 20666 | Valkyrie Hat | NONE | 10 |  |  |
| 20667 | Valkyrie Hat - Great Adventurer's Soul Power - 7-day limited period | NONE | 10 |  |  |
| 20668 | Tiger Hat | NONE | 10 |  |  |
| 20669 | Tiger Hat - Great Warrior's Soul Power - 7-day limited period | NONE | 10 |  |  |
| 20670 | Maid's Hairband | NONE | 10 |  |  |
| 20671 | Maid Hairband - Great Wizard's Soul Power - 7-day limited period | NONE | 10 |  |  |
| 20672 | Baby Panda Hat | NONE | 10 |  |  |
| 20673 | Baby Panda Hat - Blessed Escape - 7-day limited period | NONE | 10 |  |  |
| 20674 | Bamboo Panda Hat | NONE | 10 |  |  |
| 20675 | Bamboo Panda Hat - Great Adventurer's Soul Power - 7-day limited period | NONE | 10 |  |  |
| 20676 | Sexy Panda Hat | NONE | 10 |  |  |
| 20677 | Sexy Panda Hat - Blessed Resurrection - 7-day limited period | NONE | 10 |  |  |
| 20678 | Gatekeeper Hat | NONE | 10 |  |  |
| 20679 | Gatekeeper Hat - Destroy Instinct - 7-day limited period | NONE | 10 |  |  |
| 20711 | Jack O'Lantern Mask (Event) | NONE | 10 |  |  |
| 20712 | Super Strong Giant's Mask (Event) - Blessing of Skooldy : Protection of Darkness - 2 Hour Limited Period | NONE | 10 |  |  |
| 20713 | Mask of Silent Scream (Event) - Blessing of Skooldy : Protection of Darkness - 2 Hour Limited Period | NONE | 10 |  |  |
| 20714 | Spirit of Wrath Mask (Event) - Blessing of Skooldy : Protection of Darkness - 2 Hour Limited Period | NONE | 10 |  |  |
| 20715 | Undecaying Corpse Mask (Event) - Blessing of Skooldy : Protection of Darkness - 2 Hour Limited Period | NONE | 10 |  |  |
| 20716 | Planet X235 Alien Mask (Event) - Blessing of Skooldy : Protection of Darkness - 2 Hour Limited Period | NONE | 10 |  |  |
| 20718 | Shiny Super Strong Giant's Mask (Event) - Blessing of Halloween - 4-Hour Limited Period | NONE | 10 |  |  |
| 20719 | Shiny Mask of Silent Scream (Event) - Blessing of Halloween - 4-Hour Limited Period | NONE | 10 |  |  |
| 20720 | Shiny Spirit of Wrath Mask (Event) - Blessing of Halloween - 4-Hour Limited Period | NONE | 10 |  |  |
| 20721 | Shiny Undecaying Corpse Mask (Event) - Blessing of Halloween - 4-Hour Limited Period | NONE | 10 |  |  |
| 20722 | Shiny Planet X235 Alien Mask (Event) - Blessing of Halloween - 4-Hour Limited Period | NONE | 10 |  |  |
| 20723 | Golden Jack O'Lantern Mask. | NONE | 10 |  |  |
| 20724 | Golden Jack O'Lantern Mask. - Authority of Golden Jack O'Lantern - 7-Day Limited Period | NONE | 10 |  |  |
| 20725 | Red Flame of Valakas | NONE | 10 |  |  |
| 20743 | Shiny Super Strong Giant's Mask. - Blessing of Halloween - 7-day limited period | NONE | 10 |  |  |
| 20744 | Shiny Mask of Silent Scream. - Blessing of Halloween - 7-day limited period | NONE | 10 |  |  |
| 20745 | Shiny Spirit of Wrath Mast. - Blessing of Halloween - 7-day limited period | NONE | 10 |  |  |
| 20746 | Shiny Undecaying Corpse Mask. - Blessing of Halloween - 7-day limited period | NONE | 10 |  |  |
| 20747 | Shiny Planet X235 Alien Mask. - Blessing of Halloween - 7-day limited period | NONE | 10 |  |  |
| 20789 | Rocket Gun Hat - Fireworks | NONE | 10 |  |  |
| 20790 | Yellow Paper Hat - Blessed Body - 7-day limited period | NONE | 10 |  |  |
| 20791 | Pink Paper Mask Set - Blessed Soul - 7-day limited period | NONE | 10 |  |  |
| 20792 | Flavorful Cheese Hat | NONE | 10 |  |  |
| 20793 | Sweet Cheese Hat | NONE | 10 |  |  |
| 20794 | Flavorful Cheese Hat - Scent of Flavorful Cheese - 7-day limited period | NONE | 10 |  |  |
| 20795 | Sweet Cheese Hat - Scent of Sweet Cheese - 7-day limited period | NONE | 10 |  |  |
| 20897 | Purple Paper Mask - Blessed Soul - 7-day limited period | NONE | 10 |  |  |
| 20900 | Santa Hat - 14-day limited period | NONE | 10 |  |  |
| 20922 | Adventurer Hat | NONE | 10 |  |  |
| 20929 | Royal Crown of Vesper | NONE | 10 |  |  |
| 20930 | Royal Circlet of Vesper | NONE | 10 |  |  |
| 20931 | Noblesse Oblige | NONE | 10 |  |  |
| 20932 | Royal Crown of Vesper - 30-day limited period | NONE | 10 |  |  |
| 20933 | Royal Circlet of Vesper - 30-day limited period | NONE | 10 |  |  |
| 20934 | Noblesse Oblige - 30-day limited period | NONE | 10 |  |  |
| 20935 | Royal Crown of Vesper | NONE | 10 |  |  |
| 20936 | Royal Circlet of Vesper | NONE | 10 |  |  |
| 20937 | Noblesse Oblige | NONE | 10 |  |  |
| 20942 | Fox Mask | NONE | 10 |  |  |
| 20943 | Fox Mask - Silent Move - 7-day limited period | NONE | 10 |  |  |
| 20944 | Paiwan Hat | NONE | 10 |  |  |
| 20945 | Paiwan Hat - Power of Guardian Deity - 7-day limited period | NONE | 10 |  |  |
| 20973 | Opera Mask - Liu Bei - Buff of Virtue, Age of the Three Kingdoms | NONE | 10 |  |  |
| 20974 | Opera Mask - Guan Yu - Silence of Fidelity, Age of the Three Kingdoms | NONE | 10 |  |  |
| 20975 | Opera Mask - Zhang Fei - Vitality of Courage, Age of the Three Kingdoms | NONE | 10 |  |  |
| 20981 | Dragon Boat | NONE | 10 |  |  |
| 20982 | Dragon Boat - Haste - 7-day limited period | NONE | 10 |  |  |
| 21009 | Soccer Ball Afro Hair - White | NONE | 10 |  |  |
| 21010 | Soccer Ball Afro Hair - Blue | NONE | 10 |  |  |
| 21011 | Soccer Ball Afro Hair - Red - Blessing of Victory | NONE | 10 |  |  |
| 21042 | Flag Hat - 7-day limited period | NONE | 10 |  |  |
| 21043 | Flag Hat | NONE | 10 |  |  |
| 21044 | Granny Tiger Hat | NONE | 10 |  |  |
| 21045 | Mischievous Bee Hat | NONE | 10 |  |  |
| 21090 | Plastic Hair | NONE | 10 |  |  |
| 21108 | Warm Bear Hat | NONE | 10 |  |  |
| 21109 | Warm Bear Hat - 7-day limited period | NONE | 10 |  |  |
| 21112 | Stag Beetle Hat | NONE | 10 |  |  |
| 21113 | Stag Beetle Hat - 7-day limited period | NONE | 10 |  |  |
| 21114 | Beetle Hat | NONE | 10 |  |  |
| 21115 | Beetle Hat - 7-day limited period | NONE | 10 |  |  |
| 21116 | Ladybug Hat | NONE | 10 |  |  |
| 21117 | Ladybug Hat - 7-day limited period | NONE | 10 |  |  |
| 21118 | Preying Mantis Hat | NONE | 10 |  |  |
| 21119 | Preying Mantis Hat - 7-day limited period | NONE | 10 |  |  |
| 21120 | Grasshopper Hat | NONE | 10 |  |  |
| 21121 | Grasshopper Hat - 7-day limited period | NONE | 10 |  |  |
| 21124 | White Uniform Hat | NONE | 10 |  |  |
| 21125 | White Uniform Hat - 7-day limited period | NONE | 10 |  |  |
| 21126 | Warrior's Helmet | NONE | 10 |  |  |
| 21127 | Warrior's Helmet - 7-day limited period | NONE | 10 |  |  |
| 21162 | Wedding Veil | NONE | 10 |  |  |
| 21429 | Brown Bear Hat - 7-day limited period | NONE | 10 |  |  |
| 21430 | Brown Bear Hat - 7-day limited period (event) | NONE | 10 |  |  |
| 21431 | Brown Bear Hat - 30-day limited period | NONE | 10 |  |  |
| 21432 | Brown Bear Hat - 30-day limited period (event) | NONE | 10 |  |  |
| 21433 | Brown Bear Hat | NONE | 10 |  |  |
| 21434 | Brown Bear Hat - Event | NONE | 10 |  |  |
| 21441 | Chicken Hat - 7-day limited period | NONE | 10 |  |  |
| 21442 | Chicken Hat - 7-day limited period (event) | NONE | 10 |  |  |
| 21443 | Chicken Hat - 30-day limited period | NONE | 10 |  |  |
| 21444 | Chicken Hat - 30-day limited period (event) | NONE | 10 |  |  |
| 21445 | Chicken Hat | NONE | 10 |  |  |
| 21446 | Chicken Hat - Event | NONE | 10 |  |  |
| 21453 | Coronet - 7-day limited period | NONE | 10 |  |  |
| 21454 | Coronet - 7-day limited period (event) | NONE | 10 |  |  |
| 21455 | Coronet - 30-day limited period | NONE | 10 |  |  |
| 21456 | Coronet - 30-day limited period (event) | NONE | 10 |  |  |
| 21457 | Coronet | NONE | 10 |  |  |
| 21458 | Coronet - Event | NONE | 10 |  |  |
| 21465 | White Sheep Hat - 7-day limited period | NONE | 10 |  |  |
| 21466 | White Sheep Hat - 7-day limited period (event) | NONE | 10 |  |  |
| 21467 | White Sheep Hat - 30-day limited period | NONE | 10 |  |  |
| 21468 | White Sheep Hat - 30-day limited period (event) | NONE | 10 |  |  |
| 21469 | White Sheep Hat | NONE | 10 |  |  |
| 21470 | White Sheep Hat - Event | NONE | 10 |  |  |
| 21477 | Frog Hat - 7-day limited period | NONE | 10 |  |  |
| 21478 | Frog Hat - 7-day limited period (event) | NONE | 10 |  |  |
| 21479 | Frog Hat - 30-day limited period | NONE | 10 |  |  |
| 21480 | Frog Hat - 30-day limited period (event) | NONE | 10 |  |  |
| 21481 | Frog Hat | NONE | 10 |  |  |
| 21482 | Frog Hat - Event | NONE | 10 |  |  |
| 21489 | Kat the Cat Hat - 7-day limited period | NONE | 10 |  |  |
| 21490 | Kat the Cat Hat - 7-day limited period (event) | NONE | 10 |  |  |
| 21491 | Kat the Cat Hat - 30-day limited period | NONE | 10 |  |  |
| 21492 | Kat the Cat Hat - 30-day limited period (event) | NONE | 10 |  |  |
| 21493 | Kat the Cat Hat | NONE | 10 |  |  |
| 21494 | Kat the Cat Hat - Event | NONE | 10 |  |  |
| 21501 | Kai the Cat Hat - 7-day limited period | NONE | 10 |  |  |
| 21502 | Kai the Cat Hat - 7-day limited period (event) | NONE | 10 |  |  |
| 21503 | Kai the Cat Hat - 30-day limited period | NONE | 10 |  |  |
| 21504 | Kai the Cat Hat - 30-day limited period (event) | NONE | 10 |  |  |
| 21505 | Kai the Cat Hat | NONE | 10 |  |  |
| 21506 | Kai the Cat Hat - Event | NONE | 10 |  |  |
| 21513 | Feline Queen Hat - 7-day limited period | NONE | 10 |  |  |
| 21514 | Feline Queen Hat - 7-day limited period (event) | NONE | 10 |  |  |
| 21515 | Feline Queen Hat - 30-day limited period | NONE | 10 |  |  |
| 21516 | Feline Queen Hat - 30-day limited period (event) | NONE | 10 |  |  |
| 21517 | Feline Queen Hat | NONE | 10 |  |  |
| 21518 | Feline Queen Hat - Event | NONE | 10 |  |  |
| 21525 | Feline King Hat - 7-day limited period | NONE | 10 |  |  |
| 21526 | Feline King Hat - 7-day limited period (event) | NONE | 10 |  |  |
| 21527 | Feline King Hat - 30-day limited period | NONE | 10 |  |  |
| 21528 | Feline King Hat - 30-day limited period (event) | NONE | 10 |  |  |
| 21529 | Feline King Hat | NONE | 10 |  |  |
| 21530 | Feline King Hat - Event | NONE | 10 |  |  |
| 21537 | Ribbon Hairband - 7-day limited period | NONE | 10 |  |  |
| 21538 | Ribbon Hairband - 7-day limited period (event) | NONE | 10 |  |  |
| 21539 | Ribbon Hairband - 30-day limited period | NONE | 10 |  |  |
| 21540 | Ribbon Hairband - 30-day limited period (event) | NONE | 10 |  |  |
| 21541 | Ribbon Hairband | NONE | 10 |  |  |
| 21542 | Ribbon Hairband - Event | NONE | 10 |  |  |
| 21549 | Refined Dapper Cap - 7-day limited period | NONE | 10 |  |  |
| 21550 | Refined Dapper Cap - 7-day limited period (event) | NONE | 10 |  |  |
| 21551 | Refined Dapper Cap - 30-day limited period | NONE | 10 |  |  |
| 21552 | Refined Dapper Cap - 30-day limited period (event) | NONE | 10 |  |  |
| 21553 | Refined Dapper Cap | NONE | 10 |  |  |
| 21554 | Refined Dapper Cap - Event | NONE | 10 |  |  |
| 21561 | Valkyrie Circlet - 7-day limited period | NONE | 10 |  |  |
| 21562 | Valkyrie Circlet - 7-day limited period (event) | NONE | 10 |  |  |
| 21563 | Valkyrie Circlet - 30-day limited period | NONE | 10 |  |  |
| 21564 | Valkyrie Circlet - 30-day limited period (event) | NONE | 10 |  |  |
| 21565 | Valkyrie Circlet | NONE | 10 |  |  |
| 21566 | Valkyrie Circlet - Event | NONE | 10 |  |  |
| 21573 | Plastic Hair - 7-day limited period | NONE | 10 |  |  |
| 21574 | Plastic Hair - 7-day limited period (event) | NONE | 10 |  |  |
| 21575 | Plastic Hair - 30-day limited period | NONE | 10 |  |  |
| 21576 | Plastic Hair - 30-day limited period (event) | NONE | 10 |  |  |
| 21577 | Plastic Hair | NONE | 10 |  |  |
| 21578 | Plastic Hair - Event | NONE | 10 |  |  |
| 21594 | Birthday Hat | NONE | 10 |  |  |
| 21755 | Manor Scholar's Hat | NONE | 10 |  |  |
| 21756 | Rank 1 Scholar's Hat | NONE | 10 |  |  |
| 21757 | Rank 2 Scholar's Hat | NONE | 10 |  |  |
| 21758 | Rank 3 Scholar's Hat | NONE | 10 |  |  |
| 21882 | Shiny Party Hat - Blessed Body - 90-day limited period | NONE | 10 |  |  |
| 21892 | Pirate King Hat | NONE | 10 |  |  |
| 21893 | Halisha's Helmet | NONE | 10 |  |  |
| 21894 | Ice Queen's Tiara | NONE | 10 |  |  |
| 21981 | Clownfish Hat | NONE | 10 |  |  |
| 21982 | Refined Angel Ring | NONE | 10 |  |  |
| 21983 | Refined Wizard Hat | NONE | 10 |  |  |
| 21984 | Refined Jester Hat | NONE | 10 |  |  |
| 21985 | Refined Romantic Chapeau | NONE | 10 |  |  |
| 21987 | Pirate Hat | NONE | 10 |  |  |
| 21989 | Warm Bear Hat | NONE | 10 |  |  |
| 22154 | Shadow Weapon - Wolf Hat - Blessed Escape | NONE | 10 |  |  |
| 22155 | Shadow Weapon - Wolf Hat - Blessed Resurrection | NONE | 10 |  |  |
| 22171 | Dandy's Chapeau | NONE | 10 |  |  |
| 22172 | Artisan's Goggles | NONE | 10 |  |  |
| 22183 | Graduation Cap | NONE | 10 |  |  |
| 22184 | Admiral's Hat | NONE | 10 |  |  |
| 22189 | Child's Hat - Boy | NONE | 10 |  |  |
| 22190 | Child's Hat - Girl | NONE | 10 |  |  |
| 22256 | Chic Silver Chapeau | NONE | 10 |  |  |
| 22257 | Fancy Flower Hat | NONE | 10 |  |  |
| 22258 | Unicorn Horn Circlet | NONE | 10 |  |  |
| 22259 | Forest Forget-me-not Hat | NONE | 10 |  |  |
| 22260 | White Uniform Hat | NONE | 10 |  |  |
| 22261 | Golden Viking Circlet | NONE | 10 |  |  |
| 22262 | Mischievous Bee Hat | NONE | 10 |  |  |
| 22263 | Chic Silver Chapeau - Event | NONE | 10 |  |  |
| 22264 | Fancy Flower Hat - Event | NONE | 10 |  |  |
| 22265 | Unicorn Horn Circlet - Event | NONE | 10 |  |  |
| 22266 | Forest Forget-me-not Hat - Event | NONE | 10 |  |  |
| 22267 | White Uniform Hat - Event | NONE | 10 |  |  |
| 22268 | Golden Viking Circlet - Event | NONE | 10 |  |  |
| 22269 | Mischievous Bee Hat - Event | NONE | 10 |  |  |
| 22285 | Eva's Circlet - Event | NONE | 10 |  |  |

