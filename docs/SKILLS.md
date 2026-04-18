# Character Skills (L2JMobius CT 2.6 HighFive)

## Overview

This file enumerates every class skill that a playable character can learn on a vanilla L2JMobius CT 2.6 HighFive server.

- **Scope:** 1st/2nd/3rd class skill trees only. Fishing, collect, transfer, transform, sub-class, sub-pledge, noble, hero, GM, and clan trees are intentionally excluded.
- **Source of truth:** `dist/game/data/stats/players/skillTrees/{1stClass,2ndClass,3rdClass}/*.xml` in the L2JMobius CT 2.6 HighFive server tree.
- **Regenerate with:** `python scripts/gen_skills_doc.py`. The output is deterministic — rerunning on unchanged server data produces a byte-identical file.

### Column meanings

| Column | Meaning |
|--------|---------|
| **Id** | `skillId` — stable numeric identifier used on the wire (e.g. in `MagicSkillUse`, `AcquireSkill`). |
| **Skill** | `skillName` as shipped by the server. |
| **Max Lvl** | Highest `skillLevel` this class can reach for that skill in its own tree. |
| **Learned At** | Lowest character `getLevel` at which any sub-level of this skill becomes available. |
| **SP Total** | Sum of `levelUpSp` across every `<skill>` row in this class's tree for that `skillId` (cumulative SP to reach Max Lvl from the bottom). |

### Notes

- Per-sub-level rows in the XML are coalesced: one table row per `skillId`. Expand the raw XML if you need the per-sub-level SP breakdown.
- Classes inherit skills from their parents in L2 canon, but each class's XML already contains only the skills that class itself grants — parent skills are *not* duplicated here.
- Per-level skill mechanics (damage, effects, cooldowns, MP cost, target type) are **not** covered in this spec. See `dist/game/data/stats/skills/*.xml` on the server for those.

## Class index

| Tier | Class Id | Class | Parent | # Skills |
|------|---------:|-------|--------|---------:|
| 1st Class | 56 | [Artisan](#artisan) | classId 53 | 14 |
| 1st Class | 35 | [Assassin](#assassin) | classId 31 | 28 |
| 1st Class | 15 | [Cleric](#cleric) | classId 10 | 30 |
| 1st Class | 39 | [DarkWizard](#darkwizard) | classId 38 | 30 |
| 1st Class | 19 | [ElvenKnight](#elvenknight) | classId 18 | 16 |
| 1st Class | 29 | [ElvenOracle](#elvenoracle) | classId 25 | 30 |
| 1st Class | 22 | [ElvenScout](#elvenscout) | classId 18 | 28 |
| 1st Class | 26 | [ElvenWizard](#elvenwizard) | classId 25 | 26 |
| 1st Class | 4 | [HumanKnight](#humanknight) | classId 0 | 12 |
| 1st Class | 11 | [HumanWizard](#humanwizard) | classId 10 | 30 |
| 1st Class | 47 | [OrcMonk](#orcmonk) | classId 44 | 13 |
| 1st Class | 45 | [OrcRaider](#orcraider) | classId 44 | 19 |
| 1st Class | 50 | [OrcShaman](#orcshaman) | classId 49 | 32 |
| 1st Class | 32 | [PalusKnight](#palusknight) | classId 31 | 16 |
| 1st Class | 7 | [Rogue](#rogue) | classId 0 | 25 |
| 1st Class | 54 | [Scavenger](#scavenger) | classId 53 | 17 |
| 1st Class | 42 | [ShillienOracle](#shillienoracle) | classId 38 | 29 |
| 1st Class | 125 | [Trooper](#trooper) | classId 123 | 23 |
| 1st Class | 126 | [Warder](#warder) | classId 124 | 25 |
| 1st Class | 1 | [Warrior](#warrior) | classId 0 | 16 |
| 2nd Class | 36 | [AbyssWalker](#abysswalker) | Assassin | 36 |
| 2nd Class | 130 | [Arbalester](#arbalester) | Warder | 41 |
| 2nd Class | 127 | [Berserker](#berserker) | Trooper | 30 |
| 2nd Class | 16 | [Bishop](#bishop) | Cleric | 39 |
| 2nd Class | 34 | [Bladedancer](#bladedancer) | PalusKnight | 27 |
| 2nd Class | 55 | [BountyHunter](#bountyhunter) | Scavenger | 27 |
| 2nd Class | 6 | [DarkAvenger](#darkavenger) | HumanKnight | 31 |
| 2nd Class | 46 | [Destroyer](#destroyer) | OrcRaider | 26 |
| 2nd Class | 28 | [ElementalSummoner](#elementalsummoner) | ElvenWizard | 34 |
| 2nd Class | 30 | [ElvenElder](#elvenelder) | ElvenOracle | 46 |
| 2nd Class | 129 | [FemaleSoulBreaker](#femalesoulbreaker) | Warder | 36 |
| 2nd Class | 2 | [Gladiator](#gladiator) | Warrior | 28 |
| 2nd Class | 9 | [Hawkeye](#hawkeye) | Rogue | 23 |
| 2nd Class | 135 | [Inspector](#inspector) | Warder | 32 |
| 2nd Class | 128 | [MaleSoulBreaker](#malesoulbreaker) | Trooper | 36 |
| 2nd Class | 13 | [Necromancer](#necromancer) | HumanWizard | 35 |
| 2nd Class | 51 | [Overlord](#overlord) | OrcShaman | 47 |
| 2nd Class | 5 | [Paladin](#paladin) | HumanKnight | 33 |
| 2nd Class | 37 | [PhantomRanger](#phantomranger) | Assassin | 26 |
| 2nd Class | 41 | [PhantomSummoner](#phantomsummoner) | DarkWizard | 36 |
| 2nd Class | 23 | [PlainsWalker](#plainswalker) | ElvenScout | 37 |
| 2nd Class | 17 | [Prophet](#prophet) | Cleric | 46 |
| 2nd Class | 43 | [ShillienElder](#shillienelder) | ShillienOracle | 38 |
| 2nd Class | 33 | [ShillienKnight](#shillienknight) | PalusKnight | 36 |
| 2nd Class | 24 | [SilverRanger](#silverranger) | ElvenScout | 26 |
| 2nd Class | 12 | [Sorcerer](#sorcerer) | HumanWizard | 31 |
| 2nd Class | 40 | [Spellhowler](#spellhowler) | DarkWizard | 33 |
| 2nd Class | 27 | [Spellsinger](#spellsinger) | ElvenWizard | 35 |
| 2nd Class | 21 | [Swordsinger](#swordsinger) | ElvenKnight | 28 |
| 2nd Class | 20 | [TempleKnight](#templeknight) | ElvenKnight | 34 |
| 2nd Class | 8 | [TreasureHunter](#treasurehunter) | Rogue | 34 |
| 2nd Class | 48 | [Tyrant](#tyrant) | OrcMonk | 26 |
| 2nd Class | 52 | [Warcryer](#warcryer) | OrcShaman | 41 |
| 2nd Class | 14 | [Warlock](#warlock) | HumanWizard | 34 |
| 2nd Class | 3 | [Warlord](#warlord) | Warrior | 28 |
| 2nd Class | 57 | [Warsmith](#warsmith) | Artisan | 35 |
| 3rd Class | 93 | [Adventurer](#adventurer) | TreasureHunter | 23 |
| 3rd Class | 96 | [ArcanaLord](#arcanalord) | Warlock | 22 |
| 3rd Class | 94 | [Archmage](#archmage) | Sorcerer | 20 |
| 3rd Class | 97 | [Cardinal](#cardinal) | Bishop | 23 |
| 3rd Class | 115 | [Dominator](#dominator) | Overlord | 24 |
| 3rd Class | 131 | [Doombringer](#doombringer) | Berserker | 17 |
| 3rd Class | 116 | [Doomcryer](#doomcryer) | Warcryer | 19 |
| 3rd Class | 89 | [Dreadnought](#dreadnought) | Warlord | 21 |
| 3rd Class | 88 | [Duelist](#duelist) | Gladiator | 23 |
| 3rd Class | 104 | [ElementalMaster](#elementalmaster) | ElementalSummoner | 21 |
| 3rd Class | 105 | [Eva'sSaint](#evassaint) | ElvenElder | 22 |
| 3rd Class | 99 | [Eva'sTemplar](#evastemplar) | TempleKnight | 24 |
| 3rd Class | 133 | [FemaleSoulHound](#femalesoulhound) | FemaleSoulBreaker | 22 |
| 3rd Class | 117 | [FortuneSeeker](#fortuneseeker) | BountyHunter | 23 |
| 3rd Class | 108 | [GhostHunter](#ghosthunter) | AbyssWalker | 23 |
| 3rd Class | 109 | [GhostSentinel](#ghostsentinel) | PhantomRanger | 20 |
| 3rd Class | 114 | [GrandKhavatari](#grandkhavatari) | Tyrant | 22 |
| 3rd Class | 91 | [HellKnight](#hellknight) | DarkAvenger | 25 |
| 3rd Class | 98 | [Hierophant](#hierophant) | Prophet | 20 |
| 3rd Class | 136 | [Judicator](#judicator) | Inspector | 9 |
| 3rd Class | 118 | [Maestro](#maestro) | Warsmith | 20 |
| 3rd Class | 132 | [MaleSoulHound](#malesoulhound) | MaleSoulBreaker | 22 |
| 3rd Class | 102 | [MoonlightSentinel](#moonlightsentinel) | SilverRanger | 20 |
| 3rd Class | 103 | [MysticMuse](#mysticmuse) | Spellsinger | 22 |
| 3rd Class | 90 | [PhoenixKnight](#phoenixknight) | Paladin | 25 |
| 3rd Class | 92 | [Sagittarius](#sagittarius) | Hawkeye | 19 |
| 3rd Class | 112 | [ShillienSaint](#shilliensaint) | ShillienElder | 22 |
| 3rd Class | 106 | [ShillienTemplar](#shillientemplar) | ShillienKnight | 24 |
| 3rd Class | 95 | [Soultaker](#soultaker) | Necromancer | 21 |
| 3rd Class | 107 | [SpectralDancer](#spectraldancer) | Bladedancer | 18 |
| 3rd Class | 111 | [SpectralMaster](#spectralmaster) | PhantomSummoner | 22 |
| 3rd Class | 110 | [StormScreamer](#stormscreamer) | Spellhowler | 23 |
| 3rd Class | 100 | [Swordmuse](#swordmuse) | Swordsinger | 19 |
| 3rd Class | 113 | [Titan](#titan) | Destroyer | 20 |
| 3rd Class | 134 | [Trickster](#trickster) | Arbalester | 17 |
| 3rd Class | 101 | [WindRider](#windrider) | PlainsWalker | 23 |

## 1st Class Skills

### Artisan  (classId 56, parent classId 53)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 34 | Bandage | 1 | 20 | 3 700 |
| 100 | Stun Attack | 15 | 20 | 81 600 |
| 172 | Create Item | 4 | 20 | 50 700 |
| 205 | Sword/Blunt Weapon Mastery | 8 | 20 | 84 100 |
| 211 | Boost HP | 3 | 20 | 50 700 |
| 216 | Polearm Mastery | 8 | 20 | 84 100 |
| 227 | Light Armor Mastery | 13 | 20 | 81 900 |
| 231 | Heavy Armor Mastery | 13 | 20 | 81 900 |
| 245 | Wild Sweep | 15 | 20 | 81 600 |
| 248 | Crystallize | 1 | 20 | 3 700 |
| 148 | Vital Force | 2 | 24 | 32 000 |
| 150 | Weight Limit | 2 | 24 | 7 000 |
| 212 | Fast HP Recovery | 2 | 24 | 32 000 |
| 25 | Summon Mechanic Golem | 2 | 28 | 47 000 |

### Assassin  (classId 35, parent classId 31)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 16 | Mortal Blow | 24 | 20 | 53 400 |
| 27 | Unlock | 5 | 20 | 52 300 |
| 56 | Power Shot | 24 | 20 | 53 400 |
| 70 | Drain Health | 16 | 20 | 53 400 |
| 91 | Defense Aura | 2 | 20 | 2 800 |
| 113 | Long Shot | 1 | 20 | 2 800 |
| 129 | Poison | 1 | 20 | 2 800 |
| 173 | Acrobatics | 1 | 20 | 2 800 |
| 195 | Boost Breath | 1 | 20 | 2 800 |
| 208 | Bow Mastery | 15 | 20 | 53 250 |
| 209 | Dagger Mastery | 8 | 20 | 52 600 |
| 233 | Light Armor Mastery | 10 | 20 | 52 600 |
| 312 | Vicious Stance | 5 | 20 | 52 300 |
| 2 | Confusion | 4 | 24 | 49 500 |
| 96 | Bleed | 2 | 24 | 19 000 |
| 193 | Critical Damage | 2 | 24 | 19 000 |
| 198 | Boost Evasion | 1 | 24 | 5 000 |
| 223 | Sting | 12 | 24 | 50 400 |
| 256 | Accuracy | 1 | 24 | 5 000 |
| 77 | Attack Aura | 2 | 28 | 8 500 |
| 111 | Ultimate Evasion | 1 | 28 | 8 500 |
| 169 | Quick Step | 1 | 28 | 8 500 |
| 225 | Acrobatic Move | 1 | 28 | 8 500 |
| 99 | Rapid Shot | 1 | 32 | 14 000 |
| 115 | Power Break | 2 | 32 | 36 000 |
| 101 | Stun Shot | 3 | 36 | 22 200 |
| 105 | Freezing Strike | 2 | 36 | 22 000 |
| 171 | Esprit | 1 | 36 | 22 000 |

### Cleric  (classId 15, parent classId 10)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 12 | 20 | 45 200 |
| 164 | Quick Recycle | 2 | 20 | 16 300 |
| 213 | Boost Mana | 2 | 20 | 16 300 |
| 235 | Robe Mastery | 8 | 20 | 45 200 |
| 236 | Light Armor Mastery | 8 | 20 | 45 200 |
| 249 | Weapon Mastery | 9 | 20 | 45 300 |
| 1011 | Heal | 18 | 20 | 45 300 |
| 1015 | Battle Heal | 15 | 20 | 45 300 |
| 1016 | Resurrection | 2 | 20 | 16 300 |
| 1027 | Group Heal | 15 | 20 | 45 300 |
| 1031 | Disrupt Undead | 8 | 20 | 45 200 |
| 1068 | Might | 2 | 20 | 3 300 |
| 1073 | Kiss of Eva | 1 | 20 | 3 300 |
| 1078 | Concentration | 2 | 20 | 16 300 |
| 1085 | Acumen | 2 | 20 | 24 300 |
| 1204 | Wind Walk | 2 | 20 | 16 300 |
| 228 | Fast Spell Casting | 1 | 25 | 6 900 |
| 229 | Fast Mana Recovery | 2 | 25 | 27 900 |
| 1035 | Mental Shield | 1 | 25 | 6 900 |
| 1040 | Shield | 2 | 25 | 6 900 |
| 1043 | Holy Weapon | 1 | 25 | 6 900 |
| 1069 | Sleep | 9 | 25 | 42 000 |
| 1077 | Focus | 1 | 25 | 6 900 |
| 1201 | Dryad Root | 9 | 25 | 42 000 |
| 1191 | Resist Fire | 1 | 30 | 13 000 |
| 212 | Fast HP Recovery | 1 | 35 | 21 000 |
| 1012 | Cure Poison | 2 | 35 | 21 000 |
| 1044 | Regeneration | 1 | 35 | 21 000 |
| 1062 | Berserker Spirit | 1 | 35 | 21 000 |
| 1075 | Peace | 1 | 35 | 21 000 |

### DarkWizard  (classId 39, parent classId 38)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 12 | 20 | 36 800 |
| 164 | Quick Recycle | 2 | 20 | 13 600 |
| 213 | Boost Mana | 2 | 20 | 13 600 |
| 234 | Robe Mastery | 8 | 20 | 36 800 |
| 249 | Weapon Mastery | 9 | 20 | 36 900 |
| 285 | Higher Mana Gain | 8 | 20 | 36 800 |
| 1078 | Concentration | 2 | 20 | 13 600 |
| 1127 | Servitor Heal | 12 | 20 | 36 600 |
| 1128 | Summon Shadow | 4 | 20 | 36 700 |
| 1147 | Vampiric Touch | 6 | 20 | 8 600 |
| 1168 | Curse Poison | 3 | 20 | 13 600 |
| 1172 | Aura Burn | 8 | 20 | 36 800 |
| 1178 | Twister | 8 | 20 | 36 800 |
| 1181 | Flame Strike | 3 | 20 | 19 100 |
| 1184 | Ice Bolt | 6 | 20 | 3 000 |
| 1206 | Wind Shackle | 5 | 20 | 36 700 |
| 1228 | Summon Silhouette | 4 | 20 | 36 700 |
| 228 | Fast Spell Casting | 1 | 25 | 5 500 |
| 229 | Fast Mana Recovery | 2 | 25 | 23 100 |
| 1069 | Sleep | 9 | 25 | 33 600 |
| 1126 | Servitor Recharge | 6 | 25 | 33 800 |
| 1157 | Body To Mind | 1 | 25 | 5 500 |
| 1167 | Poisonous Cloud | 2 | 25 | 23 100 |
| 1224 | Surrender To Poison | 3 | 25 | 33 600 |
| 1266 | Shadow Spark | 3 | 25 | 33 600 |
| 1151 | Corpse Life Drain | 2 | 30 | 28 100 |
| 212 | Fast HP Recovery | 1 | 35 | 17 600 |
| 1146 | Mighty Servitor | 1 | 35 | 17 600 |
| 1160 | Slow | 1 | 35 | 17 600 |
| 1222 | Curse Chaos | 1 | 35 | 17 600 |

### ElvenKnight  (classId 19, parent classId 18)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 15 | Charm | 15 | 20 | 91 800 |
| 21 | Poison Recovery | 1 | 20 | 4 100 |
| 58 | Elemental Heal | 18 | 20 | 91 800 |
| 91 | Defense Aura | 2 | 20 | 4 100 |
| 110 | Ultimate Defense | 1 | 20 | 4 100 |
| 147 | M. Def. | 14 | 20 | 91 800 |
| 153 | Shield Mastery | 2 | 20 | 19 100 |
| 217 | Sword/Blunt Weapon Mastery | 8 | 20 | 91 900 |
| 232 | Heavy Armor Mastery | 15 | 20 | 91 800 |
| 28 | Aggression | 12 | 24 | 87 600 |
| 61 | Cure Bleeding | 1 | 24 | 8 800 |
| 112 | Deflect Arrow | 2 | 24 | 33 800 |
| 77 | Attack Aura | 2 | 28 | 15 000 |
| 230 | Sprint | 1 | 32 | 25 000 |
| 102 | Entangle | 1 | 36 | 39 000 |
| 191 | Focus Mind | 1 | 36 | 39 000 |

### ElvenOracle  (classId 29, parent classId 25)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 12 | 20 | 42 000 |
| 164 | Quick Recycle | 2 | 20 | 15 300 |
| 213 | Boost Mana | 2 | 20 | 15 300 |
| 235 | Robe Mastery | 8 | 20 | 42 000 |
| 236 | Light Armor Mastery | 8 | 20 | 42 000 |
| 249 | Weapon Mastery | 9 | 20 | 42 100 |
| 1011 | Heal | 18 | 20 | 42 900 |
| 1015 | Battle Heal | 15 | 20 | 42 900 |
| 1016 | Resurrection | 2 | 20 | 15 300 |
| 1027 | Group Heal | 15 | 20 | 42 900 |
| 1031 | Disrupt Undead | 8 | 20 | 42 000 |
| 1068 | Might | 2 | 20 | 3 300 |
| 1073 | Kiss of Eva | 1 | 20 | 3 300 |
| 1078 | Concentration | 2 | 20 | 15 300 |
| 1204 | Wind Walk | 2 | 20 | 15 300 |
| 1206 | Wind Shackle | 5 | 20 | 42 800 |
| 228 | Fast Spell Casting | 1 | 25 | 6 500 |
| 229 | Fast Mana Recovery | 2 | 25 | 27 500 |
| 1035 | Mental Shield | 1 | 25 | 6 500 |
| 1040 | Shield | 2 | 25 | 6 500 |
| 1043 | Holy Weapon | 1 | 25 | 6 500 |
| 1069 | Sleep | 9 | 25 | 39 600 |
| 1087 | Agility | 1 | 25 | 6 500 |
| 1201 | Dryad Root | 9 | 25 | 39 600 |
| 1013 | Recharge | 4 | 30 | 32 400 |
| 212 | Fast HP Recovery | 1 | 35 | 21 000 |
| 1012 | Cure Poison | 2 | 35 | 21 000 |
| 1033 | Resist Poison | 1 | 35 | 21 000 |
| 1044 | Regeneration | 1 | 35 | 21 000 |
| 1257 | Decrease Weight | 1 | 35 | 21 000 |

### ElvenScout  (classId 22, parent classId 18)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 15 | Charm | 15 | 20 | 58 350 |
| 16 | Mortal Blow | 24 | 20 | 59 100 |
| 27 | Unlock | 5 | 20 | 58 000 |
| 56 | Power Shot | 24 | 20 | 59 100 |
| 58 | Elemental Heal | 18 | 20 | 59 100 |
| 91 | Defense Aura | 2 | 20 | 2 800 |
| 113 | Long Shot | 1 | 20 | 2 800 |
| 173 | Acrobatics | 1 | 20 | 2 800 |
| 195 | Boost Breath | 1 | 20 | 2 800 |
| 208 | Bow Mastery | 15 | 20 | 58 350 |
| 209 | Dagger Mastery | 8 | 20 | 58 400 |
| 233 | Light Armor Mastery | 10 | 20 | 58 400 |
| 312 | Vicious Stance | 5 | 20 | 58 000 |
| 21 | Poison Recovery | 1 | 24 | 5 000 |
| 61 | Cure Bleeding | 1 | 24 | 5 000 |
| 96 | Bleed | 2 | 24 | 20 000 |
| 198 | Boost Evasion | 1 | 24 | 5 000 |
| 256 | Accuracy | 1 | 24 | 5 000 |
| 77 | Attack Aura | 2 | 28 | 9 200 |
| 111 | Ultimate Evasion | 1 | 28 | 9 200 |
| 169 | Quick Step | 1 | 28 | 9 200 |
| 225 | Acrobatic Move | 1 | 28 | 9 200 |
| 99 | Rapid Shot | 1 | 32 | 15 000 |
| 137 | Critical Chance | 1 | 32 | 15 000 |
| 230 | Sprint | 1 | 32 | 15 000 |
| 101 | Stun Shot | 3 | 36 | 25 800 |
| 102 | Entangle | 1 | 36 | 26 000 |
| 171 | Esprit | 1 | 36 | 26 000 |

### ElvenWizard  (classId 26, parent classId 25)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 12 | 20 | 39 200 |
| 164 | Quick Recycle | 2 | 20 | 14 200 |
| 213 | Boost Mana | 2 | 20 | 14 200 |
| 234 | Robe Mastery | 8 | 20 | 39 200 |
| 249 | Weapon Mastery | 9 | 20 | 39 300 |
| 285 | Higher Mana Gain | 8 | 20 | 39 200 |
| 1078 | Concentration | 2 | 20 | 14 200 |
| 1127 | Servitor Heal | 12 | 20 | 39 300 |
| 1164 | Curse Weakness | 5 | 20 | 39 500 |
| 1172 | Aura Burn | 8 | 20 | 39 200 |
| 1175 | Aqua Swirl | 8 | 20 | 39 200 |
| 1181 | Flame Strike | 3 | 20 | 20 000 |
| 1184 | Ice Bolt | 6 | 20 | 3 000 |
| 1206 | Wind Shackle | 5 | 20 | 39 500 |
| 1226 | Summon Boxer the Unicorn | 4 | 20 | 39 500 |
| 1227 | Summon Mirage the Unicorn | 4 | 20 | 39 500 |
| 1274 | Energy Bolt | 4 | 20 | 39 500 |
| 228 | Fast Spell Casting | 1 | 25 | 5 800 |
| 229 | Fast Mana Recovery | 2 | 25 | 25 300 |
| 1069 | Sleep | 9 | 25 | 36 300 |
| 1126 | Servitor Recharge | 6 | 25 | 36 200 |
| 1182 | Resist Aqua | 1 | 25 | 5 800 |
| 1264 | Solar Spark | 3 | 25 | 36 400 |
| 212 | Fast HP Recovery | 1 | 35 | 19 500 |
| 1145 | Bright Servitor | 1 | 35 | 19 500 |
| 1223 | Surrender To Earth | 1 | 35 | 19 500 |

### HumanKnight  (classId 4, parent classId 0)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 70 | Drain Health | 13 | 20 | 90 500 |
| 82 | Majesty | 1 | 20 | 4 700 |
| 92 | Shield Stun | 15 | 20 | 90 300 |
| 110 | Ultimate Defense | 1 | 20 | 4 700 |
| 147 | M. Def. | 14 | 20 | 90 400 |
| 153 | Shield Mastery | 2 | 20 | 16 700 |
| 217 | Sword/Blunt Weapon Mastery | 8 | 20 | 90 700 |
| 232 | Heavy Armor Mastery | 15 | 20 | 90 300 |
| 28 | Aggression | 12 | 24 | 85 800 |
| 112 | Deflect Arrow | 2 | 24 | 35 000 |
| 45 | Divine Heal | 9 | 28 | 75 900 |
| 191 | Focus Mind | 1 | 36 | 39 000 |

### HumanWizard  (classId 11, parent classId 10)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 12 | 20 | 36 600 |
| 164 | Quick Recycle | 2 | 20 | 13 900 |
| 213 | Boost Mana | 2 | 20 | 13 900 |
| 234 | Robe Mastery | 8 | 20 | 36 600 |
| 249 | Weapon Mastery | 9 | 20 | 36 700 |
| 285 | Higher Mana Gain | 8 | 20 | 36 600 |
| 1078 | Concentration | 2 | 20 | 13 900 |
| 1111 | Summon Kat the Cat | 4 | 20 | 37 400 |
| 1127 | Servitor Heal | 12 | 20 | 36 480 |
| 1147 | Vampiric Touch | 6 | 20 | 8 400 |
| 1164 | Curse Weakness | 5 | 20 | 37 400 |
| 1168 | Curse Poison | 3 | 20 | 13 900 |
| 1172 | Aura Burn | 8 | 20 | 36 600 |
| 1181 | Flame Strike | 3 | 20 | 19 400 |
| 1184 | Ice Bolt | 6 | 20 | 2 800 |
| 1220 | Blaze | 8 | 20 | 36 600 |
| 1225 | Summon Mew the Cat | 4 | 20 | 37 400 |
| 1274 | Energy Bolt | 4 | 20 | 37 400 |
| 228 | Fast Spell Casting | 1 | 25 | 5 500 |
| 229 | Fast Mana Recovery | 2 | 25 | 23 500 |
| 1069 | Sleep | 9 | 25 | 33 600 |
| 1083 | Surrender To Fire | 3 | 25 | 34 500 |
| 1126 | Servitor Recharge | 6 | 25 | 33 800 |
| 1157 | Body To Mind | 1 | 25 | 5 500 |
| 1167 | Poisonous Cloud | 2 | 25 | 23 500 |
| 1151 | Corpse Life Drain | 2 | 30 | 29 000 |
| 212 | Fast HP Recovery | 1 | 35 | 18 000 |
| 1144 | Servitor Wind Walk | 1 | 35 | 18 000 |
| 1160 | Slow | 1 | 35 | 18 000 |
| 1222 | Curse Chaos | 1 | 35 | 18 000 |

### OrcMonk  (classId 47, parent classId 44)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 29 | Iron Punch | 24 | 20 | 97 500 |
| 83 | Wolf Spirit Totem | 1 | 20 | 5 300 |
| 95 | Cripple | 5 | 20 | 95 100 |
| 120 | Stunning Fist | 15 | 20 | 97 500 |
| 210 | Fist Weapon Mastery | 8 | 20 | 94 300 |
| 233 | Light Armor Mastery | 10 | 20 | 94 000 |
| 319 | Agile Movement | 1 | 20 | 5 300 |
| 50 | Focused Force | 2 | 24 | 33 800 |
| 54 | Force Blaster | 12 | 24 | 89 700 |
| 993 | Force Mastery | 2 | 24 | 33 800 |
| 76 | Bear Spirit Totem | 1 | 28 | 17 000 |
| 168 | Boost Attack Speed | 1 | 36 | 39 000 |
| 284 | Hurricane Assault | 3 | 36 | 39 000 |

### OrcRaider  (classId 45, parent classId 44)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 34 | Bandage | 1 | 20 | 3 400 |
| 100 | Stun Attack | 15 | 20 | 62 100 |
| 211 | Boost HP | 3 | 20 | 31 400 |
| 216 | Polearm Mastery | 8 | 20 | 62 300 |
| 227 | Light Armor Mastery | 13 | 20 | 62 200 |
| 231 | Heavy Armor Mastery | 13 | 20 | 62 200 |
| 245 | Wild Sweep | 15 | 20 | 62 100 |
| 255 | Power Smash | 15 | 20 | 62 100 |
| 257 | Sword/Blunt Weapon Mastery | 8 | 20 | 62 300 |
| 293 | Two-handed Weapon Mastery | 5 | 20 | 53 700 |
| 312 | Vicious Stance | 5 | 20 | 53 700 |
| 94 | Rage | 1 | 24 | 5 300 |
| 148 | Vital Force | 2 | 24 | 22 300 |
| 212 | Fast HP Recovery | 2 | 24 | 22 300 |
| 256 | Accuracy | 1 | 24 | 5 300 |
| 121 | Battle Roar | 1 | 28 | 11 000 |
| 176 | Frenzy | 1 | 32 | 17 000 |
| 139 | Guts | 1 | 36 | 17 000 |
| 287 | Lionheart | 1 | 36 | 17 000 |

### OrcShaman  (classId 50, parent classId 49)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 100 | Stun Attack | 12 | 20 | 36 780 |
| 146 | Anti Magic | 12 | 20 | 36 800 |
| 164 | Quick Recycle | 2 | 20 | 13 900 |
| 213 | Boost Mana | 2 | 20 | 13 900 |
| 250 | Weapon Mastery | 9 | 20 | 36 900 |
| 251 | Robe Mastery | 12 | 20 | 36 800 |
| 252 | Light Armor Mastery | 12 | 20 | 36 800 |
| 253 | Heavy Armor Mastery | 10 | 20 | 36 800 |
| 1006 | Chant of Fire | 1 | 20 | 2 900 |
| 1009 | Chant of Shielding | 2 | 20 | 13 900 |
| 1090 | Life Drain | 6 | 20 | 37 700 |
| 1092 | Fear | 5 | 20 | 37 700 |
| 1095 | Venom | 3 | 20 | 2 900 |
| 1097 | Dreaming Spirit | 6 | 20 | 37 700 |
| 1105 | Madness | 4 | 20 | 37 700 |
| 1107 | Frost Flame | 2 | 20 | 13 900 |
| 1209 | Seal of Poison | 2 | 20 | 13 900 |
| 1229 | Chant of Life | 4 | 20 | 37 700 |
| 228 | Fast Spell Casting | 1 | 25 | 5 800 |
| 229 | Fast Mana Recovery | 2 | 25 | 23 800 |
| 1001 | Soul Cry | 4 | 25 | 23 800 |
| 1007 | Chant of Battle | 2 | 25 | 5 800 |
| 1010 | Soul Shield | 3 | 25 | 23 800 |
| 1101 | Blaze Quake | 2 | 25 | 23 800 |
| 1102 | Aura Sink | 2 | 25 | 23 800 |
| 1208 | Seal of Binding | 3 | 25 | 34 800 |
| 1002 | Flame Chant | 1 | 30 | 11 000 |
| 1003 | Pa'agrian Gift | 1 | 30 | 11 000 |
| 1096 | Seal of Chaos | 2 | 30 | 29 000 |
| 212 | Fast HP Recovery | 1 | 35 | 18 000 |
| 1005 | Blessings of Pa'agrio | 1 | 35 | 18 000 |
| 1099 | Seal of Slow | 1 | 35 | 18 000 |

### PalusKnight  (classId 32, parent classId 31)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 70 | Drain Health | 16 | 20 | 75 700 |
| 91 | Defense Aura | 2 | 20 | 4 700 |
| 110 | Ultimate Defense | 1 | 20 | 4 700 |
| 129 | Poison | 1 | 20 | 4 700 |
| 147 | M. Def. | 14 | 20 | 75 700 |
| 153 | Shield Mastery | 2 | 20 | 17 700 |
| 217 | Sword/Blunt Weapon Mastery | 8 | 20 | 76 900 |
| 232 | Heavy Armor Mastery | 15 | 20 | 75 600 |
| 2 | Confusion | 4 | 24 | 71 800 |
| 28 | Aggression | 12 | 24 | 71 100 |
| 112 | Deflect Arrow | 2 | 24 | 30 800 |
| 223 | Sting | 12 | 24 | 71 100 |
| 77 | Attack Aura | 2 | 28 | 13 000 |
| 115 | Power Break | 2 | 32 | 50 000 |
| 105 | Freezing Strike | 2 | 36 | 28 000 |
| 191 | Focus Mind | 1 | 36 | 28 000 |

### Rogue  (classId 7, parent classId 0)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 4 | Dash | 1 | 20 | 3 400 |
| 16 | Mortal Blow | 24 | 20 | 69 000 |
| 27 | Unlock | 5 | 20 | 69 300 |
| 56 | Power Shot | 24 | 20 | 69 000 |
| 113 | Long Shot | 1 | 20 | 3 400 |
| 173 | Acrobatics | 1 | 20 | 3 400 |
| 195 | Boost Breath | 1 | 20 | 3 400 |
| 208 | Bow Mastery | 15 | 20 | 68 100 |
| 209 | Dagger Mastery | 8 | 20 | 70 500 |
| 233 | Light Armor Mastery | 10 | 20 | 70 400 |
| 312 | Vicious Stance | 5 | 20 | 69 300 |
| 96 | Bleed | 2 | 24 | 23 900 |
| 148 | Vital Force | 2 | 24 | 23 900 |
| 193 | Critical Damage | 2 | 24 | 23 900 |
| 198 | Boost Evasion | 1 | 24 | 5 900 |
| 256 | Accuracy | 1 | 24 | 5 900 |
| 111 | Ultimate Evasion | 1 | 28 | 11 000 |
| 137 | Critical Chance | 1 | 28 | 11 000 |
| 169 | Quick Step | 1 | 28 | 11 000 |
| 225 | Acrobatic Move | 1 | 28 | 11 000 |
| 99 | Rapid Shot | 1 | 32 | 18 000 |
| 101 | Stun Shot | 3 | 36 | 30 000 |
| 168 | Boost Attack Speed | 1 | 36 | 31 000 |
| 171 | Esprit | 1 | 36 | 31 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |

### Scavenger  (classId 54, parent classId 53)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 34 | Bandage | 1 | 20 | 3 400 |
| 100 | Stun Attack | 15 | 20 | 72 300 |
| 205 | Sword/Blunt Weapon Mastery | 8 | 20 | 74 400 |
| 209 | Dagger Mastery | 8 | 20 | 74 400 |
| 211 | Boost HP | 3 | 20 | 44 400 |
| 216 | Polearm Mastery | 8 | 20 | 74 400 |
| 227 | Light Armor Mastery | 13 | 20 | 72 500 |
| 231 | Heavy Armor Mastery | 13 | 20 | 72 500 |
| 245 | Wild Sweep | 15 | 20 | 72 300 |
| 248 | Crystallize | 1 | 20 | 3 400 |
| 254 | Spoil | 4 | 20 | 44 400 |
| 148 | Vital Force | 2 | 24 | 29 000 |
| 150 | Weight Limit | 2 | 24 | 7 000 |
| 212 | Fast HP Recovery | 2 | 24 | 29 000 |
| 302 | Spoil Festival | 2 | 28 | 41 000 |
| 444 | Sweeper Festival | 1 | 28 | 10 000 |
| 1559 | Potential Ability | 1 | 28 | 10 000 |

### ShillienOracle  (classId 42, parent classId 38)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 12 | 20 | 45 200 |
| 164 | Quick Recycle | 2 | 20 | 15 300 |
| 213 | Boost Mana | 2 | 20 | 15 300 |
| 235 | Robe Mastery | 8 | 20 | 45 200 |
| 236 | Light Armor Mastery | 8 | 20 | 45 200 |
| 249 | Weapon Mastery | 9 | 20 | 45 300 |
| 1011 | Heal | 18 | 20 | 44 700 |
| 1015 | Battle Heal | 15 | 20 | 44 700 |
| 1016 | Resurrection | 2 | 20 | 15 300 |
| 1027 | Group Heal | 15 | 20 | 44 700 |
| 1031 | Disrupt Undead | 8 | 20 | 45 200 |
| 1068 | Might | 2 | 20 | 3 300 |
| 1073 | Kiss of Eva | 1 | 20 | 3 300 |
| 1078 | Concentration | 2 | 20 | 15 300 |
| 1204 | Wind Walk | 2 | 20 | 15 300 |
| 1206 | Wind Shackle | 5 | 20 | 44 800 |
| 228 | Fast Spell Casting | 1 | 25 | 6 500 |
| 229 | Fast Mana Recovery | 2 | 25 | 29 500 |
| 1035 | Mental Shield | 1 | 25 | 6 500 |
| 1040 | Shield | 2 | 25 | 6 500 |
| 1059 | Empower | 1 | 25 | 6 500 |
| 1069 | Sleep | 9 | 25 | 41 400 |
| 1077 | Focus | 1 | 25 | 6 500 |
| 1201 | Dryad Root | 9 | 25 | 41 400 |
| 1013 | Recharge | 4 | 30 | 35 600 |
| 1268 | Vampiric Rage | 1 | 30 | 12 000 |
| 212 | Fast HP Recovery | 1 | 35 | 23 000 |
| 1012 | Cure Poison | 2 | 35 | 23 000 |
| 1189 | Resist Wind | 1 | 35 | 23 000 |

### Trooper  (classId 125, parent classId 123)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 465 | Light Armor Mastery | 13 | 20 | 56 500 |
| 466 | Magic Immunity | 18 | 20 | 56 500 |
| 467 | Soul Mastery | 8 | 20 | 56 900 |
| 472 | Ancient Sword Mastery | 8 | 20 | 56 900 |
| 474 | Rapier Mastery | 8 | 20 | 57 300 |
| 475 | Strike Back | 1 | 20 | 3 700 |
| 476 | Dark Strike | 15 | 20 | 56 400 |
| 478 | Double Thrust | 15 | 20 | 56 400 |
| 1433 | Abyssal Blaze | 10 | 20 | 56 800 |
| 1473 | Change Weapon | 1 | 20 | 3 700 |
| 482 | Furious Soul | 1 | 24 | 5 800 |
| 1434 | Dark Explosion | 4 | 24 | 53 200 |
| 1435 | Death Mark | 2 | 24 | 21 100 |
| 1475 | Erase Mark | 1 | 24 | 5 800 |
| 479 | Hard March | 1 | 28 | 10 000 |
| 1432 | Increase Power | 2 | 28 | 10 000 |
| 1445 | Surrender to Dark | 3 | 28 | 47 400 |
| 481 | Dark Armor | 1 | 32 | 15 300 |
| 484 | Rush | 1 | 32 | 15 300 |
| 480 | Dark Blade | 1 | 36 | 22 100 |
| 483 | Sword Shield | 1 | 36 | 22 100 |
| 485 | Disarm | 1 | 36 | 22 100 |
| 499 | Courage | 1 | 36 | 22 100 |

### Warder  (classId 126, parent classId 124)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 465 | Light Armor Mastery | 13 | 20 | 56 500 |
| 466 | Magic Immunity | 18 | 20 | 56 500 |
| 467 | Soul Mastery | 8 | 20 | 56 900 |
| 473 | Crossbow Mastery | 8 | 20 | 52 900 |
| 474 | Rapier Mastery | 8 | 20 | 57 300 |
| 478 | Double Thrust | 15 | 20 | 56 400 |
| 487 | Penetrating Shot | 15 | 20 | 54 600 |
| 1433 | Abyssal Blaze | 10 | 20 | 56 800 |
| 1473 | Change Weapon | 1 | 20 | 3 700 |
| 470 | Detect Trap | 3 | 24 | 11 700 |
| 471 | Defuse Trap | 3 | 24 | 11 700 |
| 482 | Furious Soul | 1 | 24 | 5 800 |
| 486 | Increase Range | 1 | 24 | 4 400 |
| 1434 | Dark Explosion | 4 | 24 | 53 200 |
| 1435 | Death Mark | 2 | 24 | 21 100 |
| 1475 | Erase Mark | 1 | 24 | 5 800 |
| 479 | Hard March | 1 | 28 | 10 000 |
| 514 | Fire Trap | 2 | 28 | 29 000 |
| 1445 | Surrender to Dark | 3 | 28 | 47 400 |
| 481 | Dark Armor | 1 | 32 | 15 300 |
| 490 | Fast Shot | 1 | 32 | 14 300 |
| 628 | Warp | 1 | 32 | 14 300 |
| 480 | Dark Blade | 1 | 36 | 22 100 |
| 622 | Ultimate Escape | 1 | 36 | 19 000 |
| 627 | Soul Shock | 3 | 36 | 19 500 |

### Warrior  (classId 1, parent classId 0)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 78 | War Cry | 1 | 20 | 3 700 |
| 100 | Stun Attack | 15 | 20 | 70 200 |
| 211 | Boost HP | 3 | 20 | 46 700 |
| 216 | Polearm Mastery | 8 | 20 | 72 300 |
| 227 | Light Armor Mastery | 13 | 20 | 70 500 |
| 231 | Heavy Armor Mastery | 13 | 20 | 70 500 |
| 245 | Wild Sweep | 15 | 20 | 70 200 |
| 255 | Power Smash | 15 | 20 | 70 200 |
| 257 | Sword/Blunt Weapon Mastery | 8 | 20 | 72 300 |
| 312 | Vicious Stance | 5 | 20 | 71 100 |
| 148 | Vital Force | 2 | 24 | 24 400 |
| 212 | Fast HP Recovery | 2 | 24 | 24 400 |
| 256 | Accuracy | 1 | 24 | 6 400 |
| 121 | Battle Roar | 1 | 28 | 12 000 |
| 75 | Detect Insect Weakness | 1 | 32 | 18 000 |
| 287 | Lionheart | 1 | 36 | 31 000 |

## 2nd Class Skills

### AbyssWalker  (classId 36, parent Assassin)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 2 | Confusion | 19 | 40 | 4 537 000 |
| 27 | Unlock | 14 | 40 | 1 950 000 |
| 30 | Backstab | 37 | 40 | 4 507 700 |
| 70 | Drain Health | 53 | 40 | 4 507 700 |
| 105 | Freezing Strike | 24 | 40 | 4 537 000 |
| 115 | Power Break | 17 | 40 | 4 537 000 |
| 122 | Hex | 15 | 40 | 4 537 000 |
| 193 | Critical Damage | 7 | 40 | 2 306 000 |
| 209 | Dagger Mastery | 45 | 40 | 4 507 700 |
| 221 | Silent Move | 1 | 40 | 28 000 |
| 223 | Sting | 49 | 40 | 4 507 700 |
| 233 | Light Armor Mastery | 47 | 40 | 4 507 700 |
| 263 | Deadly Blow | 37 | 40 | 4 507 700 |
| 312 | Vicious Stance | 20 | 40 | 4 537 000 |
| 821 | Shadow Step | 1 | 40 | 28 000 |
| 106 | Veil | 14 | 43 | 4 509 000 |
| 169 | Quick Step | 2 | 43 | 29 000 |
| 171 | Esprit | 8 | 43 | 2 126 000 |
| 225 | Acrobatic Move | 3 | 43 | 145 000 |
| 198 | Boost Evasion | 3 | 46 | 164 000 |
| 419 | Summon Treasure Key | 4 | 46 | 1 714 000 |
| 11 | Trick | 12 | 49 | 4 442 000 |
| 96 | Bleed | 6 | 49 | 1 137 000 |
| 129 | Poison | 5 | 49 | 1 737 000 |
| 51 | Lure | 1 | 52 | 88 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 111 | Ultimate Evasion | 2 | 55 | 116 000 |
| 173 | Acrobatics | 2 | 55 | 116 000 |
| 195 | Boost Breath | 2 | 55 | 116 000 |
| 412 | Sand Bomb | 10 | 55 | 4 293 000 |
| 410 | Mortal Strike | 3 | 58 | 1 676 000 |
| 453 | Escape Shackle | 1 | 60 | 181 000 |
| 321 | Blinding Blow | 10 | 66 | 3 280 000 |
| 623 | Find Trap | 1 | 74 | 1 180 000 |
| 624 | Remove Trap | 1 | 74 | 1 180 000 |
| 818 | Evasion Counter | 1 | 74 | 0 |

### Arbalester  (classId 130, parent Warder)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 465 | Light Armor Mastery | 50 | 40 | 4 999 000 |
| 466 | Magic Immunity | 55 | 40 | 4 999 000 |
| 467 | Soul Mastery | 23 | 40 | 4 979 000 |
| 473 | Crossbow Mastery | 45 | 40 | 4 999 000 |
| 486 | Increase Range | 2 | 40 | 35 000 |
| 489 | Shift Target | 1 | 40 | 33 000 |
| 502 | Life to Soul | 5 | 40 | 1 360 000 |
| 507 | Twin Shot | 37 | 40 | 4 999 000 |
| 518 | Binding Trap | 8 | 40 | 2 988 000 |
| 522 | Real Target | 4 | 40 | 1 003 000 |
| 626 | Critical Sense | 4 | 40 | 676 000 |
| 627 | Soul Shock | 40 | 40 | 4 999 000 |
| 481 | Dark Armor | 2 | 43 | 39 000 |
| 509 | Bleeding Shot | 34 | 43 | 4 966 000 |
| 514 | Fire Trap | 9 | 43 | 1 991 000 |
| 525 | Decoy | 6 | 43 | 2 662 000 |
| 621 | Create Special Bolt | 1 | 43 | 39 000 |
| 832 | Fast Recovery | 1 | 43 | 39 000 |
| 470 | Detect Trap | 7 | 46 | 1 957 000 |
| 471 | Defuse Trap | 7 | 46 | 1 957 000 |
| 508 | Rising Shot | 31 | 46 | 4 927 000 |
| 625 | Soul Gathering | 1 | 46 | 50 000 |
| 511 | Temptation | 1 | 49 | 82 000 |
| 515 | Poison Trap | 6 | 49 | 1 952 000 |
| 516 | Slow Trap | 6 | 52 | 2 905 000 |
| 620 | Quiver of Bolts: B Grade | 1 | 52 | 100 000 |
| 622 | Ultimate Escape | 2 | 52 | 100 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 490 | Fast Shot | 2 | 55 | 157 000 |
| 517 | Flash Trap | 5 | 55 | 1 870 000 |
| 1514 | Soul Barrier | 1 | 58 | 185 000 |
| 519 | Quiver of Bolts: A Grade | 1 | 60 | 193 000 |
| 521 | Sharpshooting | 8 | 60 | 4 333 000 |
| 513 | Create Dark Seed | 1 | 62 | 290 000 |
| 523 | Imbue Dark Seed | 7 | 62 | 4 140 000 |
| 524 | Cure Dark Seed | 1 | 64 | 320 000 |
| 836 | Oblivion Trap | 3 | 64 | 1 360 000 |
| 510 | Deadly Roulette | 5 | 66 | 3 530 000 |
| 1510 | Soul Cleanse | 1 | 66 | 350 000 |
| 835 | Imbue Seed of Destruction | 4 | 68 | 3 180 000 |
| 520 | Quiver of Bolts: S Grade | 1 | 74 | 1 400 000 |

### Berserker  (classId 127, parent Trooper)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 465 | Light Armor Mastery | 50 | 40 | 5 948 000 |
| 466 | Magic Immunity | 55 | 40 | 5 948 000 |
| 467 | Soul Mastery | 23 | 40 | 5 998 000 |
| 472 | Ancient Sword Mastery | 45 | 40 | 5 948 000 |
| 477 | Dark Smash | 37 | 40 | 5 948 000 |
| 494 | Shoulder Charge | 37 | 40 | 5 948 000 |
| 500 | True Berserker | 2 | 40 | 150 000 |
| 502 | Life to Soul | 5 | 40 | 1 610 000 |
| 626 | Critical Sense | 4 | 40 | 813 000 |
| 481 | Dark Armor | 2 | 43 | 46 000 |
| 485 | Disarm | 7 | 43 | 3 005 000 |
| 503 | Scorn | 3 | 43 | 533 000 |
| 832 | Fast Recovery | 1 | 43 | 46 000 |
| 496 | Slashing Blade | 31 | 46 | 5 861 000 |
| 625 | Soul Gathering | 1 | 46 | 75 000 |
| 493 | Storm Assault | 28 | 49 | 5 786 000 |
| 499 | Courage | 3 | 49 | 352 000 |
| 501 | Violent Temper | 12 | 49 | 5 834 000 |
| 483 | Sword Shield | 2 | 52 | 107 000 |
| 492 | Spread Wing | 25 | 52 | 5 705 000 |
| 833 | Body Reconstruction | 1 | 52 | 107 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 482 | Furious Soul | 2 | 55 | 147 000 |
| 495 | Blade Rush | 10 | 55 | 5 645 000 |
| 834 | Blood Pact | 1 | 55 | 147 000 |
| 1514 | Soul Barrier | 1 | 58 | 185 000 |
| 497 | Crush of Pain | 16 | 60 | 5 264 000 |
| 20006 | Soul Roar | 1 | 62 | 270 000 |
| 498 | Contagion | 12 | 64 | 4 780 000 |
| 1510 | Soul Cleanse | 1 | 66 | 440 000 |

### Bishop  (classId 16, parent Cleric)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 3 431 000 |
| 213 | Boost Mana | 8 | 40 | 1 227 000 |
| 228 | Fast Spell Casting | 3 | 40 | 114 000 |
| 235 | Robe Mastery | 41 | 40 | 3 431 000 |
| 236 | Light Armor Mastery | 41 | 40 | 3 431 000 |
| 249 | Weapon Mastery | 42 | 40 | 3 431 000 |
| 1016 | Resurrection | 9 | 40 | 1 757 000 |
| 1028 | Might of Heaven | 19 | 40 | 3 394 000 |
| 1049 | Requiem | 14 | 40 | 3 392 000 |
| 1069 | Sleep | 42 | 40 | 3 431 000 |
| 1075 | Peace | 15 | 40 | 3 392 000 |
| 1217 | Greater Heal | 33 | 40 | 3 431 000 |
| 1218 | Greater Battle Heal | 33 | 40 | 3 431 000 |
| 1219 | Greater Group Heal | 33 | 40 | 3 431 000 |
| 1254 | Mass Resurrection | 6 | 40 | 649 000 |
| 1520 | Inquisitor | 1 | 40 | 33 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 285 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 1 447 000 |
| 1018 | Purify | 3 | 44 | 297 000 |
| 1034 | Repose | 13 | 44 | 3 359 000 |
| 1258 | Restore Life | 4 | 44 | 271 000 |
| 164 | Quick Recycle | 3 | 48 | 63 000 |
| 1020 | Vitalize | 27 | 48 | 3 356 000 |
| 1042 | Hold Undead | 12 | 48 | 3 316 000 |
| 1311 | Body of Avatar | 6 | 48 | 1 424 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1394 | Trance | 10 | 56 | 3 169 000 |
| 1395 | Erase | 10 | 56 | 3 169 000 |
| 1396 | Magical BackFire | 10 | 56 | 3 169 000 |
| 1398 | Mana Burn | 10 | 56 | 3 169 000 |
| 1400 | Turn Undead | 10 | 56 | 3 169 000 |
| 1401 | Major Heal | 11 | 56 | 4 049 000 |
| 1430 | Invocation | 5 | 56 | 1 361 000 |
| 1012 | Cure Poison | 3 | 58 | 88 000 |
| 1399 | Mana Storm | 5 | 58 | 1 808 000 |
| 1402 | Major Group Heal | 5 | 58 | 1 808 000 |
| 1418 | Celestial Shield | 1 | 64 | 190 000 |
| 1271 | Benediction | 1 | 66 | 280 000 |
| 1307 | Prayer | 3 | 66 | 1 550 000 |

### Bladedancer  (classId 34, parent PalusKnight)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 2 | Confusion | 19 | 40 | 6 633 000 |
| 70 | Drain Health | 53 | 40 | 6 634 000 |
| 105 | Freezing Strike | 24 | 40 | 6 632 000 |
| 115 | Power Break | 17 | 40 | 6 633 000 |
| 122 | Hex | 15 | 40 | 6 633 000 |
| 144 | Dual Weapon Mastery | 37 | 40 | 6 634 000 |
| 147 | M. Def. | 51 | 40 | 6 634 000 |
| 223 | Sting | 49 | 40 | 6 634 000 |
| 274 | Dance of Fire | 1 | 40 | 39 000 |
| 986 | Deadly Strike | 15 | 40 | 6 633 000 |
| 191 | Focus Mind | 6 | 43 | 1 604 000 |
| 277 | Dance of Light | 1 | 43 | 42 000 |
| 272 | Dance of Inspiration | 1 | 46 | 60 000 |
| 129 | Poison | 5 | 49 | 2 802 000 |
| 273 | Dance of the Mystic | 1 | 49 | 82 000 |
| 276 | Dance of Concentration | 1 | 52 | 150 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 84 | Poison Blade Dance | 3 | 55 | 1 320 000 |
| 271 | Dance of the Warrior | 1 | 55 | 160 000 |
| 402 | Arrest | 10 | 55 | 6 260 000 |
| 408 | Demonic Blade Dance | 10 | 55 | 6 260 000 |
| 275 | Dance of Fury | 1 | 58 | 180 000 |
| 989 | Defense Motion | 1 | 60 | 240 000 |
| 309 | Dance of Earth Guard | 1 | 62 | 330 000 |
| 311 | Dance of Protection | 1 | 66 | 540 000 |
| 307 | Dance of Aqua Guard | 1 | 70 | 780 000 |
| 310 | Dance of the Vampire | 1 | 74 | 2 000 000 |

### BountyHunter  (classId 55, parent Scavenger)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 30 | Backstab | 37 | 40 | 5 274 800 |
| 36 | Whirlwind | 37 | 40 | 5 274 800 |
| 60 | Fake Death | 1 | 40 | 23 000 |
| 148 | Vital Force | 8 | 40 | 1 556 000 |
| 190 | Fatal Strike | 37 | 40 | 5 274 800 |
| 205 | Sword/Blunt Weapon Mastery | 45 | 40 | 5 274 800 |
| 209 | Dagger Mastery | 45 | 40 | 5 274 800 |
| 212 | Fast HP Recovery | 8 | 40 | 2 273 000 |
| 216 | Polearm Mastery | 45 | 40 | 5 274 800 |
| 227 | Light Armor Mastery | 50 | 40 | 5 274 800 |
| 231 | Heavy Armor Mastery | 50 | 40 | 5 274 800 |
| 248 | Crystallize | 5 | 40 | 933 000 |
| 260 | Hammer Crush | 37 | 40 | 5 274 800 |
| 263 | Deadly Blow | 37 | 40 | 5 274 800 |
| 997 | Crushing Strike | 15 | 40 | 5 251 000 |
| 998 | Blazing Boost | 1 | 40 | 23 000 |
| 1559 | Potential Ability | 3 | 40 | 88 000 |
| 211 | Boost HP | 10 | 43 | 2 915 000 |
| 254 | Spoil | 11 | 43 | 2 265 000 |
| 302 | Spoil Festival | 9 | 43 | 2 915 000 |
| 34 | Bandage | 3 | 46 | 313 000 |
| 150 | Weight Limit | 3 | 46 | 60 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 422 | Polearm Accuracy | 3 | 58 | 1 960 000 |
| 424 | War Frenzy | 3 | 58 | 1 960 000 |
| 952 | Collector's Experience | 5 | 58 | 2 810 000 |
| 320 | Wrath | 10 | 66 | 3 860 000 |

### DarkAvenger  (classId 6, parent HumanKnight)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 18 | Aura of Hate | 37 | 40 | 4 741 000 |
| 28 | Aggression | 49 | 40 | 4 741 000 |
| 46 | Life Scavenge | 15 | 40 | 4 721 000 |
| 70 | Drain Health | 53 | 40 | 4 771 000 |
| 82 | Majesty | 3 | 40 | 159 000 |
| 86 | Reflect Damage | 3 | 40 | 168 000 |
| 92 | Shield Stun | 52 | 40 | 4 741 000 |
| 147 | M. Def. | 51 | 40 | 4 741 000 |
| 153 | Shield Mastery | 4 | 40 | 128 000 |
| 217 | Sword/Blunt Weapon Mastery | 45 | 40 | 4 741 000 |
| 232 | Heavy Armor Mastery | 52 | 40 | 4 741 000 |
| 283 | Summon Dark Panther | 7 | 40 | 2 864 000 |
| 811 | Vanguard | 1 | 40 | 28 000 |
| 984 | Shield Strike | 15 | 40 | 4 721 000 |
| 72 | Iron Will | 3 | 43 | 231 000 |
| 112 | Deflect Arrow | 4 | 43 | 101 000 |
| 127 | Hamstring | 14 | 43 | 4 693 000 |
| 191 | Focus Mind | 6 | 43 | 1 151 000 |
| 65 | Horror | 13 | 46 | 4 657 000 |
| 103 | Corpse Plague | 4 | 46 | 901 000 |
| 110 | Ultimate Defense | 2 | 46 | 40 000 |
| 318 | Aegis Stance | 1 | 46 | 40 000 |
| 291 | Final Fortress | 11 | 52 | 4 552 000 |
| 982 | Combat Aura | 3 | 52 | 840 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 401 | Judgment | 10 | 55 | 4 452 000 |
| 403 | Shackle | 10 | 55 | 4 452 000 |
| 450 | Banish Seraph | 10 | 55 | 4 452 000 |
| 916 | Shield Deflect Magic | 4 | 60 | 1 551 000 |
| 983 | Patience | 1 | 60 | 171 000 |
| 322 | Shield Fortress | 6 | 64 | 3 780 000 |

### Destroyer  (classId 46, parent OrcRaider)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 36 | Whirlwind | 37 | 40 | 5 981 000 |
| 121 | Battle Roar | 6 | 40 | 1 416 000 |
| 148 | Vital Force | 8 | 40 | 1 789 000 |
| 190 | Fatal Strike | 37 | 40 | 5 981 000 |
| 212 | Fast HP Recovery | 8 | 40 | 2 557 000 |
| 216 | Polearm Mastery | 45 | 40 | 5 981 000 |
| 227 | Light Armor Mastery | 50 | 40 | 5 981 000 |
| 231 | Heavy Armor Mastery | 50 | 40 | 5 981 000 |
| 257 | Sword/Blunt Weapon Mastery | 45 | 40 | 5 981 000 |
| 260 | Hammer Crush | 37 | 40 | 5 981 000 |
| 293 | Two-handed Weapon Mastery | 20 | 40 | 5 991 000 |
| 312 | Vicious Stance | 20 | 40 | 5 991 000 |
| 994 | Rush | 1 | 40 | 33 000 |
| 139 | Guts | 3 | 43 | 163 000 |
| 211 | Boost HP | 10 | 43 | 3 262 000 |
| 34 | Bandage | 3 | 46 | 360 000 |
| 176 | Frenzy | 3 | 46 | 192 000 |
| 287 | Lionheart | 3 | 49 | 392 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 94 | Rage | 2 | 55 | 142 000 |
| 420 | Zealot | 3 | 58 | 2 151 000 |
| 422 | Polearm Accuracy | 3 | 58 | 2 151 000 |
| 423 | Dark Form | 3 | 58 | 2 151 000 |
| 424 | War Frenzy | 3 | 58 | 2 151 000 |
| 315 | Crush of Doom | 16 | 60 | 5 330 000 |
| 320 | Wrath | 10 | 66 | 4 340 000 |

### ElementalSummoner  (classId 28, parent ElvenWizard)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 67 | Summon Life Cubic | 7 | 40 | 2 233 000 |
| 146 | Anti Magic | 45 | 40 | 5 049 500 |
| 213 | Boost Mana | 8 | 40 | 1 784 000 |
| 228 | Fast Spell Casting | 3 | 40 | 123 000 |
| 234 | Robe Mastery | 41 | 40 | 5 049 500 |
| 249 | Weapon Mastery | 42 | 40 | 5 049 500 |
| 258 | Light Armor Mastery | 33 | 40 | 5 049 500 |
| 1126 | Servitor Recharge | 34 | 40 | 5 050 000 |
| 1127 | Servitor Heal | 45 | 40 | 5 052 500 |
| 1140 | Servitor Physical Shield | 3 | 40 | 183 000 |
| 1206 | Wind Shackle | 19 | 40 | 5 065 000 |
| 1226 | Summon Boxer the Unicorn | 18 | 40 | 5 065 000 |
| 1227 | Summon Mirage the Unicorn | 18 | 40 | 5 065 000 |
| 1262 | Transfer Pain | 5 | 40 | 953 000 |
| 1277 | Summon Merrow the Unicorn | 14 | 40 | 5 065 000 |
| 1280 | Summon Aqua Cubic | 9 | 40 | 2 875 000 |
| 1300 | Servitor Cure | 3 | 40 | 268 000 |
| 1329 | Mass Summon Aqua Cubic | 9 | 40 | 2 875 000 |
| 1558 | Dimension Spiral | 14 | 40 | 5 035 000 |
| 143 | Cubic Mastery | 2 | 44 | 155 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 915 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 2 193 000 |
| 1139 | Servitor Magic Shield | 2 | 44 | 132 000 |
| 1141 | Servitor Haste | 2 | 44 | 132 000 |
| 1547 | Spirit Sharing | 3 | 44 | 887 000 |
| 164 | Quick Recycle | 3 | 48 | 63 000 |
| 1145 | Bright Servitor | 3 | 48 | 155 000 |
| 1299 | Servitor Empowerment | 2 | 52 | 725 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1332 | Summon Seraphim the Unicorn | 10 | 56 | 4 845 000 |
| 1380 | Betray | 10 | 56 | 4 845 000 |
| 1403 | Summon Friend | 1 | 56 | 95 000 |
| 1384 | Mass Surrender to Water | 5 | 58 | 2 700 000 |
| 1301 | Servitor Blessing | 1 | 62 | 220 000 |

### ElvenElder  (classId 30, parent ElvenOracle)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 3 946 000 |
| 213 | Boost Mana | 8 | 40 | 1 358 000 |
| 228 | Fast Spell Casting | 3 | 40 | 125 000 |
| 235 | Robe Mastery | 41 | 40 | 3 946 000 |
| 236 | Light Armor Mastery | 41 | 40 | 3 946 000 |
| 249 | Weapon Mastery | 42 | 40 | 3 946 000 |
| 1013 | Recharge | 32 | 40 | 3 923 000 |
| 1016 | Resurrection | 7 | 40 | 1 468 000 |
| 1028 | Might of Heaven | 19 | 40 | 3 923 000 |
| 1033 | Resist Poison | 3 | 40 | 71 000 |
| 1035 | Mental Shield | 4 | 40 | 188 000 |
| 1068 | Might | 3 | 40 | 30 000 |
| 1069 | Sleep | 42 | 40 | 3 949 000 |
| 1206 | Wind Shackle | 19 | 40 | 3 946 000 |
| 1217 | Greater Heal | 33 | 40 | 3 875 000 |
| 1243 | Bless Shield | 6 | 40 | 1 208 000 |
| 1259 | Resist Shock | 4 | 40 | 1 047 000 |
| 1521 | Inquisitor | 1 | 40 | 30 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 496 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 1 696 000 |
| 1040 | Shield | 3 | 44 | 41 000 |
| 1050 | Return | 2 | 44 | 136 000 |
| 1078 | Concentration | 6 | 44 | 648 000 |
| 1087 | Agility | 3 | 44 | 118 000 |
| 1257 | Decrease Weight | 3 | 44 | 118 000 |
| 1273 | Serenade of Eva | 13 | 44 | 3 916 000 |
| 164 | Quick Recycle | 3 | 48 | 63 000 |
| 1020 | Vitalize | 27 | 48 | 3 877 000 |
| 1044 | Regeneration | 3 | 48 | 158 000 |
| 1219 | Greater Group Heal | 29 | 48 | 3 886 000 |
| 1255 | Party Recall | 2 | 48 | 158 000 |
| 1073 | Kiss of Eva | 2 | 52 | 77 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1394 | Trance | 10 | 56 | 3 735 000 |
| 1395 | Erase | 10 | 56 | 3 735 000 |
| 1398 | Mana Burn | 10 | 56 | 3 735 000 |
| 1400 | Turn Undead | 10 | 56 | 3 735 000 |
| 1401 | Major Heal | 11 | 56 | 4 785 000 |
| 1430 | Invocation | 5 | 56 | 1 565 000 |
| 1012 | Cure Poison | 3 | 58 | 100 000 |
| 1304 | Advanced Block | 3 | 58 | 1 130 000 |
| 1393 | Resist Dark | 3 | 58 | 1 470 000 |
| 1397 | Clarity | 3 | 58 | 1 470 000 |
| 1303 | Wild Magic | 2 | 62 | 700 000 |
| 1503 | Improve Shield Defense | 1 | 70 | 0 |
| 1504 | Improve Movement | 1 | 70 | 0 |

### FemaleSoulBreaker  (classId 129, parent Warder)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 465 | Light Armor Mastery | 50 | 40 | 4 600 000 |
| 466 | Magic Immunity | 55 | 40 | 4 600 000 |
| 467 | Soul Mastery | 23 | 40 | 4 584 000 |
| 474 | Rapier Mastery | 45 | 40 | 4 600 000 |
| 502 | Life to Soul | 5 | 40 | 1 143 000 |
| 504 | Triple Thrust | 37 | 40 | 4 600 000 |
| 626 | Critical Sense | 4 | 40 | 611 000 |
| 1435 | Death Mark | 10 | 40 | 2 870 000 |
| 1436 | Soul of Pain | 30 | 40 | 4 618 000 |
| 1445 | Surrender to Dark | 18 | 40 | 4 584 000 |
| 1527 | Expert Casting | 3 | 40 | 244 000 |
| 1565 | Mana Pump | 6 | 40 | 1 533 000 |
| 481 | Dark Armor | 2 | 43 | 42 000 |
| 832 | Fast Recovery | 2 | 43 | 112 000 |
| 1441 | Soul to Empower | 3 | 43 | 453 000 |
| 1474 | Abyssal Power | 1 | 43 | 42 000 |
| 625 | Soul Gathering | 1 | 46 | 50 000 |
| 1437 | Dark Flame | 26 | 46 | 4 544 000 |
| 1443 | Dark Weapon | 1 | 46 | 50 000 |
| 1475 | Erase Mark | 3 | 46 | 360 000 |
| 505 | Shining Edge | 28 | 49 | 4 474 000 |
| 1444 | Pride of Kamael | 1 | 49 | 70 000 |
| 492 | Spread Wing | 25 | 52 | 4 405 000 |
| 506 | Checkmate | 4 | 52 | 1 178 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1446 | Shadow Bind | 11 | 52 | 4 389 000 |
| 1440 | Steal Divinity | 5 | 55 | 1 602 000 |
| 837 | Painkiller | 1 | 58 | 130 000 |
| 1438 | Annihilation Circle | 9 | 58 | 4 141 000 |
| 1442 | Protection from Darkness | 3 | 58 | 1 880 000 |
| 1447 | Voice Bind | 9 | 58 | 4 141 000 |
| 1448 | Blink | 1 | 60 | 161 000 |
| 1511 | Curse of Life Flow | 8 | 60 | 4 011 000 |
| 1529 | Soul Web | 7 | 62 | 3 850 000 |
| 1439 | Curse of Divinity | 5 | 66 | 3 330 000 |
| 1510 | Soul Cleanse | 1 | 66 | 310 000 |

### Gladiator  (classId 2, parent Warrior)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 1 | Triple Slash | 37 | 40 | 5 220 000 |
| 8 | Sonic Focus | 7 | 40 | 1 432 000 |
| 87 | Detect Animal Weakness | 1 | 40 | 30 000 |
| 144 | Dual Weapon Mastery | 37 | 40 | 5 220 000 |
| 190 | Fatal Strike | 37 | 40 | 5 220 000 |
| 212 | Fast HP Recovery | 8 | 40 | 2 446 000 |
| 227 | Light Armor Mastery | 50 | 40 | 5 220 000 |
| 231 | Heavy Armor Mastery | 50 | 40 | 5 220 000 |
| 257 | Sword/Blunt Weapon Mastery | 45 | 40 | 5 220 000 |
| 260 | Hammer Crush | 37 | 40 | 5 220 000 |
| 312 | Vicious Stance | 20 | 40 | 5 218 000 |
| 992 | Sonic Mastery | 7 | 40 | 1 432 000 |
| 994 | Rush | 1 | 40 | 30 000 |
| 6 | Sonic Blaster | 37 | 43 | 5 223 000 |
| 9 | Sonic Buster | 34 | 43 | 5 190 000 |
| 78 | War Cry | 2 | 43 | 32 000 |
| 290 | Final Frenzy | 14 | 43 | 5 188 000 |
| 104 | Detect Plant Weakness | 1 | 46 | 43 000 |
| 5 | Double Sonic Slash | 31 | 49 | 5 154 000 |
| 7 | Sonic Storm | 28 | 49 | 5 112 000 |
| 287 | Lionheart | 3 | 49 | 311 000 |
| 80 | Detect Beast Weakness | 1 | 52 | 100 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 261 | Triple Sonic Slash | 22 | 55 | 4 953 000 |
| 88 | Detect Dragon Weakness | 1 | 58 | 153 000 |
| 424 | War Frenzy | 3 | 58 | 2 193 000 |
| 451 | Sonic Move | 2 | 62 | 740 000 |
| 297 | Duelist Spirit | 2 | 64 | 1 120 000 |

### Hawkeye  (classId 9, parent Rogue)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 19 | Double Shot | 37 | 40 | 8 121 000 |
| 101 | Stun Shot | 40 | 40 | 8 121 000 |
| 113 | Long Shot | 2 | 40 | 43 000 |
| 131 | Hawk Eye | 3 | 40 | 389 000 |
| 148 | Vital Force | 8 | 40 | 2 389 000 |
| 208 | Bow Mastery | 52 | 40 | 8 121 000 |
| 233 | Light Armor Mastery | 47 | 40 | 8 121 000 |
| 303 | Soul of Sagittarius | 4 | 40 | 1 826 000 |
| 312 | Vicious Stance | 20 | 40 | 8 133 000 |
| 169 | Quick Step | 2 | 43 | 58 000 |
| 171 | Esprit | 8 | 43 | 3 764 000 |
| 225 | Acrobatic Move | 3 | 43 | 271 000 |
| 24 | Burst Shot | 31 | 46 | 8 022 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 99 | Rapid Shot | 2 | 55 | 213 000 |
| 415 | Spirit of Sagittarius | 3 | 58 | 2 763 000 |
| 416 | Blessing of Sagittarius | 3 | 58 | 2 763 000 |
| 417 | Pain of Sagittarius | 5 | 58 | 4 233 000 |
| 418 | Quiver of Holding | 3 | 58 | 2 763 000 |
| 313 | Snipe | 8 | 60 | 7 210 000 |
| 323 | Quiver of Arrow: A Grade | 1 | 60 | 360 000 |
| 324 | Quiver of Arrow: S Grade | 1 | 72 | 1 330 000 |
| 933 | Detection | 1 | 74 | 1 900 000 |

### Inspector  (classId 135, parent Warder)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 465 | Light Armor Mastery | 50 | 40 | 7 002 000 |
| 466 | Magic Immunity | 55 | 40 | 7 002 000 |
| 467 | Soul Mastery | 23 | 40 | 6 995 000 |
| 474 | Rapier Mastery | 45 | 40 | 7 002 000 |
| 502 | Life to Soul | 5 | 40 | 1 837 000 |
| 504 | Triple Thrust | 37 | 40 | 7 002 000 |
| 1476 | Appetite for Destruction | 3 | 40 | 337 000 |
| 1487 | Restoration | 8 | 40 | 4 223 000 |
| 1527 | Expert Casting | 1 | 40 | 39 000 |
| 481 | Dark Armor | 2 | 43 | 58 000 |
| 626 | Critical Sense | 4 | 43 | 936 000 |
| 832 | Fast Recovery | 1 | 43 | 58 000 |
| 1481 | Oblivion | 7 | 43 | 2 771 000 |
| 625 | Soul Gathering | 1 | 46 | 67 000 |
| 1478 | Protection Instinct | 2 | 46 | 308 000 |
| 1483 | Thin Skin | 7 | 46 | 4 184 000 |
| 505 | Shining Edge | 28 | 49 | 6 840 000 |
| 1488 | Restoration Impact | 3 | 49 | 989 000 |
| 492 | Spread Wing | 25 | 52 | 6 741 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1477 | Vampiric Impulse | 3 | 52 | 1 617 000 |
| 1479 | Magic Impulse | 3 | 55 | 1 254 000 |
| 837 | Painkiller | 1 | 58 | 200 000 |
| 1484 | Enervation | 4 | 60 | 2 371 000 |
| 1482 | Weak Constitution | 4 | 62 | 3 780 000 |
| 1485 | Spite | 3 | 66 | 3 420 000 |
| 1510 | Soul Cleanse | 1 | 66 | 500 000 |
| 1486 | Mental Impoverish | 4 | 68 | 4 570 000 |
| 1480 | Soul Harmony | 1 | 70 | 720 000 |
| 841 | Aura Bird - Falcon | 1 | 75 | 0 |
| 842 | Aura Bird - Owl | 1 | 75 | 0 |
| 840 | Final Flying Form | 1 | 79 | 0 |

### MaleSoulBreaker  (classId 128, parent Trooper)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 465 | Light Armor Mastery | 50 | 40 | 4 600 000 |
| 466 | Magic Immunity | 55 | 40 | 4 600 000 |
| 467 | Soul Mastery | 23 | 40 | 4 584 000 |
| 474 | Rapier Mastery | 45 | 40 | 4 600 000 |
| 502 | Life to Soul | 5 | 40 | 1 143 000 |
| 504 | Triple Thrust | 37 | 40 | 4 600 000 |
| 626 | Critical Sense | 4 | 40 | 611 000 |
| 1435 | Death Mark | 10 | 40 | 2 870 000 |
| 1436 | Soul of Pain | 30 | 40 | 4 618 000 |
| 1445 | Surrender to Dark | 18 | 40 | 4 584 000 |
| 1527 | Expert Casting | 3 | 40 | 244 000 |
| 1565 | Mana Pump | 6 | 40 | 1 533 000 |
| 481 | Dark Armor | 2 | 43 | 42 000 |
| 832 | Fast Recovery | 2 | 43 | 112 000 |
| 1441 | Soul to Empower | 3 | 43 | 453 000 |
| 1474 | Abyssal Power | 1 | 43 | 42 000 |
| 625 | Soul Gathering | 1 | 46 | 50 000 |
| 1437 | Dark Flame | 26 | 46 | 4 544 000 |
| 1443 | Dark Weapon | 1 | 46 | 50 000 |
| 1475 | Erase Mark | 3 | 46 | 360 000 |
| 505 | Shining Edge | 28 | 49 | 4 474 000 |
| 1444 | Pride of Kamael | 1 | 49 | 70 000 |
| 492 | Spread Wing | 25 | 52 | 4 405 000 |
| 506 | Checkmate | 4 | 52 | 1 178 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1446 | Shadow Bind | 11 | 52 | 4 389 000 |
| 1440 | Steal Divinity | 5 | 55 | 1 602 000 |
| 837 | Painkiller | 1 | 58 | 130 000 |
| 1438 | Annihilation Circle | 9 | 58 | 4 141 000 |
| 1442 | Protection from Darkness | 3 | 58 | 1 880 000 |
| 1447 | Voice Bind | 9 | 58 | 4 141 000 |
| 1448 | Blink | 1 | 60 | 161 000 |
| 1511 | Curse of Life Flow | 8 | 60 | 4 011 000 |
| 1529 | Soul Web | 7 | 62 | 3 850 000 |
| 1439 | Curse of Divinity | 5 | 66 | 3 330 000 |
| 1510 | Soul Cleanse | 1 | 66 | 310 000 |

### Necromancer  (classId 13, parent HumanWizard)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 3 344 000 |
| 213 | Boost Mana | 8 | 40 | 1 208 000 |
| 228 | Fast Spell Casting | 3 | 40 | 113 000 |
| 234 | Robe Mastery | 41 | 40 | 3 344 000 |
| 249 | Weapon Mastery | 42 | 40 | 3 344 000 |
| 285 | Higher Mana Gain | 27 | 40 | 3 344 000 |
| 1064 | Silence | 14 | 40 | 3 344 000 |
| 1069 | Sleep | 42 | 40 | 3 344 000 |
| 1151 | Corpse Life Drain | 16 | 40 | 3 344 000 |
| 1154 | Summon Corrupted Man | 6 | 40 | 998 000 |
| 1157 | Body To Mind | 5 | 40 | 480 000 |
| 1163 | Curse Discord | 14 | 40 | 3 344 000 |
| 1164 | Curse Weakness | 19 | 40 | 3 344 000 |
| 1169 | Curse Fear | 14 | 40 | 3 344 000 |
| 1170 | Anchor | 13 | 40 | 3 308 000 |
| 1222 | Curse Chaos | 15 | 40 | 3 344 000 |
| 1234 | Vampiric Claw | 28 | 40 | 3 344 000 |
| 1262 | Transfer Pain | 5 | 40 | 640 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 256 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 1 424 000 |
| 1129 | Summon Reanimated Man | 7 | 44 | 2 224 000 |
| 1148 | Death Spike | 13 | 44 | 3 314 000 |
| 1156 | Forget | 13 | 44 | 3 314 000 |
| 1168 | Curse Poison | 7 | 44 | 914 000 |
| 1263 | Curse Gloom | 13 | 44 | 3 314 000 |
| 164 | Quick Recycle | 3 | 48 | 55 000 |
| 1155 | Corpse Burst | 15 | 48 | 3 278 000 |
| 1167 | Poisonous Cloud | 6 | 48 | 1 188 000 |
| 1159 | Curse Death Link | 22 | 52 | 3 224 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1334 | Summon Cursed Man | 7 | 56 | 2 603 000 |
| 1269 | Curse Disease | 9 | 58 | 3 062 000 |
| 1381 | Mass Fear | 5 | 58 | 1 772 000 |
| 1382 | Mass Gloom | 5 | 58 | 1 772 000 |
| 1298 | Mass Slow | 14 | 62 | 3 300 000 |

### Overlord  (classId 51, parent OrcShaman)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 3 238 000 |
| 211 | Boost HP | 7 | 40 | 764 000 |
| 213 | Boost Mana | 8 | 40 | 1 110 000 |
| 228 | Fast Spell Casting | 3 | 40 | 86 000 |
| 250 | Weapon Mastery | 42 | 40 | 3 238 000 |
| 251 | Robe Mastery | 45 | 40 | 3 238 000 |
| 252 | Light Armor Mastery | 45 | 40 | 3 238 000 |
| 253 | Heavy Armor Mastery | 43 | 40 | 3 238 000 |
| 260 | Hammer Crush | 35 | 40 | 3 238 000 |
| 927 | Burning Chop | 14 | 40 | 3 245 000 |
| 1001 | Soul Cry | 10 | 40 | 1 110 000 |
| 1003 | Pa'agrian Gift | 3 | 40 | 60 000 |
| 1004 | The Wisdom of Pa'agrio | 3 | 40 | 125 000 |
| 1008 | The Glory of Pa'agrio | 3 | 40 | 125 000 |
| 1092 | Fear | 19 | 40 | 3 245 000 |
| 1096 | Seal of Chaos | 16 | 40 | 3 245 000 |
| 1097 | Dreaming Spirit | 20 | 40 | 3 245 000 |
| 1099 | Seal of Slow | 15 | 40 | 3 245 000 |
| 1104 | Seal of Winter | 14 | 40 | 3 245 000 |
| 1105 | Madness | 18 | 40 | 3 245 000 |
| 1208 | Seal of Binding | 17 | 40 | 3 245 000 |
| 1209 | Seal of Poison | 6 | 40 | 633 000 |
| 1245 | Steal Essence | 14 | 40 | 3 245 000 |
| 1247 | Seal of Scourge | 14 | 40 | 3 245 000 |
| 1250 | Under the Protection of Pa'agrio | 3 | 40 | 125 000 |
| 1260 | The Tact of Pa'agrio | 3 | 40 | 125 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 275 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 1 424 000 |
| 1005 | Blessings of Pa'agrio | 3 | 44 | 89 000 |
| 1210 | Seal of Gloom | 4 | 44 | 859 000 |
| 1213 | Seal of Mirage | 13 | 44 | 3 224 000 |
| 1249 | The Vision of Pa'agrio | 3 | 44 | 154 000 |
| 1256 | The Heart of Pa'agrio | 13 | 44 | 3 224 000 |
| 1261 | Rage of Pa'agrio | 2 | 44 | 89 000 |
| 1283 | Soul Guard | 13 | 44 | 3 224 000 |
| 164 | Quick Recycle | 3 | 48 | 39 000 |
| 1108 | Seal of Flame | 4 | 48 | 1 314 000 |
| 1246 | Seal of Silence | 12 | 48 | 3 197 000 |
| 1248 | Seal of Suspension | 12 | 48 | 3 197 000 |
| 1563 | Fury of Pa'agrio | 2 | 48 | 104 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1282 | Pa'agrian Haste | 2 | 58 | 286 000 |
| 1306 | Ritual of Life | 6 | 64 | 2 640 000 |
| 1305 | The Honor of Pa'agrio | 5 | 66 | 2 450 000 |
| 1536 | Combat of Paagrio | 1 | 70 | 0 |
| 1538 | Condition of Paagrio | 1 | 72 | 0 |
| 1537 | Critical of Paagrio | 1 | 74 | 0 |

### Paladin  (classId 5, parent HumanKnight)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 18 | Aura of Hate | 37 | 40 | 4 763 000 |
| 28 | Aggression | 49 | 40 | 4 763 000 |
| 44 | Remedy | 3 | 40 | 346 000 |
| 82 | Majesty | 3 | 40 | 171 000 |
| 92 | Shield Stun | 52 | 40 | 4 763 000 |
| 147 | M. Def. | 51 | 40 | 4 763 000 |
| 153 | Shield Mastery | 4 | 40 | 140 000 |
| 197 | Divine Armor | 2 | 40 | 80 000 |
| 217 | Sword/Blunt Weapon Mastery | 45 | 40 | 4 743 000 |
| 232 | Heavy Armor Mastery | 52 | 40 | 4 763 000 |
| 262 | Divine Blessing | 37 | 40 | 4 763 000 |
| 810 | Vanguard | 1 | 40 | 30 000 |
| 984 | Shield Strike | 15 | 40 | 4 676 000 |
| 72 | Iron Will | 3 | 43 | 244 000 |
| 112 | Deflect Arrow | 4 | 43 | 114 000 |
| 191 | Focus Mind | 6 | 43 | 1 164 000 |
| 196 | Divine Blade | 1 | 43 | 38 000 |
| 49 | Divine Strike | 26 | 46 | 4 636 000 |
| 110 | Ultimate Defense | 2 | 46 | 50 000 |
| 318 | Aegis Stance | 1 | 46 | 50 000 |
| 69 | Sacrifice | 25 | 52 | 4 568 000 |
| 97 | Sanctuary | 11 | 52 | 4 482 000 |
| 291 | Final Fortress | 11 | 52 | 4 482 000 |
| 982 | Combat Aura | 3 | 52 | 880 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 400 | Tribunal | 10 | 55 | 4 372 000 |
| 403 | Shackle | 10 | 55 | 4 372 000 |
| 405 | Banish Undead | 10 | 55 | 4 372 000 |
| 404 | Mass Shackling | 5 | 58 | 2 691 000 |
| 406 | Angelic Icon | 3 | 58 | 1 931 000 |
| 916 | Shield Deflect Magic | 4 | 60 | 1 551 000 |
| 983 | Patience | 1 | 60 | 171 000 |
| 322 | Shield Fortress | 6 | 64 | 3 690 000 |

### PhantomRanger  (classId 37, parent Assassin)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 2 | Confusion | 19 | 40 | 5 376 000 |
| 19 | Double Shot | 37 | 40 | 5 356 000 |
| 70 | Drain Health | 53 | 40 | 5 356 000 |
| 101 | Stun Shot | 40 | 40 | 5 356 000 |
| 105 | Freezing Strike | 24 | 40 | 5 378 000 |
| 113 | Long Shot | 2 | 40 | 33 000 |
| 115 | Power Break | 17 | 40 | 5 376 000 |
| 122 | Hex | 15 | 40 | 5 376 000 |
| 208 | Bow Mastery | 52 | 40 | 5 356 000 |
| 223 | Sting | 49 | 40 | 5 356 000 |
| 233 | Light Armor Mastery | 47 | 40 | 5 356 000 |
| 303 | Soul of Sagittarius | 4 | 40 | 1 163 000 |
| 312 | Vicious Stance | 20 | 40 | 5 376 000 |
| 169 | Quick Step | 2 | 43 | 33 000 |
| 171 | Esprit | 8 | 43 | 2 549 000 |
| 225 | Acrobatic Move | 3 | 43 | 187 000 |
| 129 | Poison | 5 | 49 | 2 128 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 99 | Rapid Shot | 2 | 55 | 154 000 |
| 415 | Spirit of Sagittarius | 3 | 58 | 2 053 000 |
| 417 | Pain of Sagittarius | 5 | 58 | 2 943 000 |
| 314 | Fatal Counter | 16 | 60 | 4 720 000 |
| 323 | Quiver of Arrow: A Grade | 1 | 60 | 210 000 |
| 414 | Dead Eye | 8 | 60 | 4 740 000 |
| 324 | Quiver of Arrow: S Grade | 1 | 72 | 860 000 |
| 933 | Detection | 1 | 74 | 1 440 000 |

### PhantomSummoner  (classId 41, parent DarkWizard)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 33 | Summon Phantom Cubic | 8 | 40 | 2 566 000 |
| 146 | Anti Magic | 45 | 40 | 4 562 000 |
| 213 | Boost Mana | 8 | 40 | 1 422 000 |
| 228 | Fast Spell Casting | 3 | 40 | 119 000 |
| 234 | Robe Mastery | 41 | 40 | 4 562 000 |
| 249 | Weapon Mastery | 42 | 40 | 4 562 000 |
| 258 | Light Armor Mastery | 33 | 40 | 4 562 000 |
| 1126 | Servitor Recharge | 34 | 40 | 4 562 000 |
| 1127 | Servitor Heal | 45 | 40 | 4 562 000 |
| 1128 | Summon Shadow | 18 | 40 | 4 550 000 |
| 1140 | Servitor Physical Shield | 3 | 40 | 182 000 |
| 1206 | Wind Shackle | 19 | 40 | 4 550 000 |
| 1228 | Summon Silhouette | 18 | 40 | 4 550 000 |
| 1262 | Transfer Pain | 5 | 40 | 802 000 |
| 1278 | Summon Soulless | 14 | 40 | 4 550 000 |
| 1281 | Summon Spark Cubic | 9 | 40 | 2 130 000 |
| 1300 | Servitor Cure | 3 | 40 | 261 000 |
| 1330 | Mass Summon Phantom Cubic | 8 | 40 | 2 566 000 |
| 1558 | Dimension Spiral | 14 | 40 | 4 550 000 |
| 143 | Cubic Mastery | 2 | 44 | 123 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 748 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 1 978 000 |
| 1139 | Servitor Magic Shield | 2 | 44 | 118 000 |
| 1141 | Servitor Haste | 2 | 44 | 118 000 |
| 1168 | Curse Poison | 7 | 44 | 1 198 000 |
| 1530 | Death Spike | 13 | 44 | 4 522 000 |
| 1547 | Spirit Sharing | 3 | 44 | 732 000 |
| 164 | Quick Recycle | 3 | 48 | 67 000 |
| 1146 | Mighty Servitor | 3 | 48 | 154 000 |
| 1299 | Servitor Empowerment | 2 | 52 | 586 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1333 | Summon Nightshade | 10 | 56 | 4 341 000 |
| 1380 | Betray | 10 | 56 | 4 341 000 |
| 1403 | Summon Friend | 1 | 56 | 91 000 |
| 1385 | Mass Surrender to Wind | 5 | 58 | 2 420 000 |
| 1301 | Servitor Blessing | 1 | 62 | 200 000 |

### PlainsWalker  (classId 23, parent ElvenScout)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 15 | Charm | 52 | 40 | 6 092 000 |
| 21 | Poison Recovery | 3 | 40 | 249 000 |
| 27 | Unlock | 14 | 40 | 2 626 000 |
| 30 | Backstab | 37 | 40 | 6 092 000 |
| 58 | Elemental Heal | 55 | 40 | 6 092 000 |
| 60 | Fake Death | 1 | 40 | 26 000 |
| 102 | Entangle | 16 | 40 | 6 091 000 |
| 123 | Spirit Barrier | 3 | 40 | 251 000 |
| 137 | Critical Chance | 4 | 40 | 251 000 |
| 209 | Dagger Mastery | 45 | 40 | 6 092 000 |
| 221 | Silent Move | 1 | 40 | 26 000 |
| 233 | Light Armor Mastery | 47 | 40 | 6 092 000 |
| 263 | Deadly Blow | 37 | 40 | 6 092 000 |
| 312 | Vicious Stance | 20 | 40 | 6 091 000 |
| 821 | Shadow Step | 1 | 40 | 26 000 |
| 12 | Switch | 14 | 43 | 6 065 000 |
| 169 | Quick Step | 2 | 43 | 35 000 |
| 171 | Esprit | 8 | 43 | 2 825 000 |
| 225 | Acrobatic Move | 3 | 43 | 182 000 |
| 61 | Cure Bleeding | 3 | 46 | 370 000 |
| 198 | Boost Evasion | 3 | 46 | 190 000 |
| 296 | Chameleon Rest | 1 | 46 | 40 000 |
| 419 | Summon Treasure Key | 4 | 46 | 2 320 000 |
| 96 | Bleed | 6 | 49 | 1 505 000 |
| 51 | Lure | 1 | 52 | 115 000 |
| 230 | Sprint | 2 | 52 | 115 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 111 | Ultimate Evasion | 2 | 55 | 147 000 |
| 173 | Acrobatics | 2 | 55 | 147 000 |
| 195 | Boost Breath | 2 | 55 | 147 000 |
| 412 | Sand Bomb | 10 | 55 | 5 800 000 |
| 410 | Mortal Strike | 3 | 58 | 2 280 000 |
| 453 | Escape Shackle | 1 | 60 | 223 000 |
| 321 | Blinding Blow | 10 | 66 | 4 500 000 |
| 623 | Find Trap | 1 | 74 | 1 630 000 |
| 624 | Remove Trap | 1 | 74 | 1 630 000 |
| 819 | Evasion Chance | 1 | 74 | 0 |

### Prophet  (classId 17, parent Cleric)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 6 243 000 |
| 211 | Boost HP | 7 | 40 | 1 402 000 |
| 213 | Boost Mana | 8 | 40 | 2 357 000 |
| 228 | Fast Spell Casting | 3 | 40 | 123 000 |
| 235 | Robe Mastery | 41 | 40 | 6 243 000 |
| 236 | Light Armor Mastery | 41 | 40 | 6 243 000 |
| 249 | Weapon Mastery | 42 | 40 | 6 243 000 |
| 259 | Heavy Armor Mastery | 33 | 40 | 6 243 000 |
| 1032 | Invigor | 3 | 40 | 186 000 |
| 1035 | Mental Shield | 4 | 40 | 186 000 |
| 1050 | Return | 2 | 40 | 123 000 |
| 1068 | Might | 3 | 40 | 32 000 |
| 1191 | Resist Fire | 3 | 40 | 69 000 |
| 1201 | Dryad Root | 33 | 40 | 6 255 000 |
| 1240 | Guidance | 3 | 40 | 186 000 |
| 1242 | Death Whisper | 3 | 40 | 186 000 |
| 1243 | Bless Shield | 3 | 40 | 186 000 |
| 212 | Fast HP Recovery | 6 | 44 | 2 164 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 2 527 000 |
| 1036 | Magic Barrier | 2 | 44 | 126 000 |
| 1040 | Shield | 3 | 44 | 37 000 |
| 1045 | Bless the Body | 6 | 44 | 1 430 000 |
| 1048 | Bless the Soul | 6 | 44 | 1 361 000 |
| 1077 | Focus | 3 | 44 | 126 000 |
| 1078 | Concentration | 6 | 44 | 997 000 |
| 1086 | Haste | 2 | 44 | 126 000 |
| 1272 | Word of Fear | 13 | 44 | 6 220 000 |
| 1526 | Steal Mana | 3 | 44 | 498 000 |
| 164 | Quick Recycle | 3 | 48 | 63 000 |
| 1044 | Regeneration | 3 | 48 | 154 000 |
| 1085 | Acumen | 3 | 48 | 63 000 |
| 1062 | Berserker Spirit | 2 | 52 | 89 000 |
| 1073 | Kiss of Eva | 2 | 52 | 89 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1395 | Erase | 10 | 56 | 6 031 000 |
| 1398 | Mana Burn | 10 | 56 | 6 031 000 |
| 1182 | Resist Aqua | 3 | 58 | 889 000 |
| 1189 | Resist Wind | 3 | 58 | 889 000 |
| 1388 | Greater Might | 3 | 58 | 2 118 000 |
| 1389 | Greater Shield | 3 | 58 | 2 118 000 |
| 1392 | Resist Holy | 3 | 58 | 2 118 000 |
| 1393 | Resist Dark | 3 | 58 | 2 118 000 |
| 1033 | Resist Poison | 3 | 60 | 1 241 000 |
| 1548 | Resist Earth | 3 | 60 | 1 241 000 |
| 1499 | Improved Combat | 1 | 70 | 0 |
| 1501 | Improved Condition | 1 | 70 | 0 |

### ShillienElder  (classId 43, parent ShillienOracle)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 5 615 000 |
| 213 | Boost Mana | 8 | 40 | 1 951 000 |
| 228 | Fast Spell Casting | 3 | 40 | 141 000 |
| 235 | Robe Mastery | 41 | 40 | 5 615 000 |
| 236 | Light Armor Mastery | 41 | 40 | 5 615 000 |
| 249 | Weapon Mastery | 42 | 40 | 5 615 000 |
| 1013 | Recharge | 32 | 40 | 5 616 000 |
| 1035 | Mental Shield | 4 | 40 | 221 000 |
| 1068 | Might | 3 | 40 | 34 000 |
| 1189 | Resist Wind | 3 | 40 | 71 000 |
| 1201 | Dryad Root | 33 | 40 | 5 659 000 |
| 1206 | Wind Shackle | 19 | 40 | 5 655 000 |
| 1217 | Greater Heal | 33 | 40 | 7 148 000 |
| 1240 | Guidance | 3 | 40 | 221 000 |
| 1242 | Death Whisper | 3 | 40 | 221 000 |
| 1522 | Inquisitor | 1 | 40 | 30 000 |
| 1531 | Blessed Blood | 7 | 40 | 2 171 000 |
| 1539 | Stigma of Shilien | 4 | 40 | 1 146 000 |
| 212 | Fast HP Recovery | 6 | 44 | 2 228 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 2 451 000 |
| 1018 | Purify | 3 | 44 | 437 000 |
| 1040 | Shield | 3 | 44 | 41 000 |
| 1059 | Empower | 3 | 44 | 147 000 |
| 1077 | Focus | 3 | 44 | 147 000 |
| 1078 | Concentration | 6 | 44 | 807 000 |
| 1268 | Vampiric Rage | 4 | 44 | 1 188 000 |
| 164 | Quick Recycle | 3 | 48 | 80 000 |
| 1219 | Greater Group Heal | 29 | 48 | 5 547 000 |
| 1073 | Kiss of Eva | 2 | 52 | 106 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1395 | Erase | 10 | 56 | 5 398 000 |
| 1398 | Mana Burn | 10 | 56 | 5 398 000 |
| 1430 | Invocation | 5 | 56 | 2 061 000 |
| 1012 | Cure Poison | 3 | 58 | 147 000 |
| 1392 | Resist Holy | 3 | 58 | 2 327 000 |
| 1303 | Wild Magic | 2 | 62 | 1 010 000 |
| 1500 | Improve Magic | 1 | 70 | 0 |
| 1502 | Improve Critical | 1 | 70 | 0 |

### ShillienKnight  (classId 33, parent PalusKnight)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 2 | Confusion | 19 | 40 | 3 825 000 |
| 18 | Aura of Hate | 37 | 40 | 3 872 000 |
| 28 | Aggression | 49 | 40 | 3 872 000 |
| 33 | Summon Phantom Cubic | 8 | 40 | 2 380 000 |
| 70 | Drain Health | 53 | 40 | 3 872 000 |
| 105 | Freezing Strike | 24 | 40 | 3 824 000 |
| 115 | Power Break | 17 | 40 | 3 825 000 |
| 122 | Hex | 15 | 40 | 3 825 000 |
| 147 | M. Def. | 51 | 40 | 3 872 000 |
| 153 | Shield Mastery | 4 | 40 | 107 000 |
| 217 | Sword/Blunt Weapon Mastery | 45 | 40 | 3 872 000 |
| 223 | Sting | 49 | 40 | 3 872 000 |
| 232 | Heavy Armor Mastery | 52 | 40 | 3 872 000 |
| 289 | Life Leech | 15 | 40 | 3 825 000 |
| 813 | Vanguard | 1 | 40 | 24 000 |
| 984 | Shield Strike | 15 | 40 | 3 825 000 |
| 22 | Summon Vampiric Cubic | 7 | 43 | 1 445 000 |
| 112 | Deflect Arrow | 4 | 43 | 80 000 |
| 143 | Cubic Mastery | 2 | 43 | 131 000 |
| 191 | Focus Mind | 6 | 43 | 945 000 |
| 288 | Guard Stance | 4 | 43 | 699 000 |
| 103 | Corpse Plague | 4 | 46 | 743 000 |
| 110 | Ultimate Defense | 2 | 46 | 38 000 |
| 129 | Poison | 5 | 49 | 1 699 000 |
| 278 | Summon Viper Cubic | 6 | 49 | 1 419 000 |
| 291 | Final Fortress | 11 | 52 | 3 683 000 |
| 982 | Combat Aura | 3 | 52 | 693 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 401 | Judgment | 10 | 55 | 3 600 000 |
| 402 | Arrest | 10 | 55 | 3 600 000 |
| 450 | Banish Seraph | 10 | 55 | 3 600 000 |
| 279 | Lightning Strike | 5 | 58 | 2 235 000 |
| 316 | Aegis | 1 | 60 | 130 000 |
| 916 | Shield Deflect Magic | 4 | 60 | 1 260 000 |
| 983 | Patience | 1 | 60 | 130 000 |
| 322 | Shield Fortress | 6 | 64 | 3 060 000 |

### SilverRanger  (classId 24, parent ElvenScout)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 15 | Charm | 52 | 40 | 6 835 000 |
| 19 | Double Shot | 37 | 40 | 6 835 000 |
| 21 | Poison Recovery | 3 | 40 | 273 000 |
| 58 | Elemental Heal | 55 | 40 | 6 835 000 |
| 101 | Stun Shot | 40 | 40 | 6 835 000 |
| 102 | Entangle | 16 | 40 | 6 832 000 |
| 113 | Long Shot | 2 | 40 | 35 000 |
| 123 | Spirit Barrier | 3 | 40 | 322 000 |
| 208 | Bow Mastery | 52 | 40 | 6 835 000 |
| 233 | Light Armor Mastery | 47 | 40 | 6 835 000 |
| 303 | Soul of Sagittarius | 4 | 40 | 1 523 000 |
| 312 | Vicious Stance | 20 | 40 | 6 832 000 |
| 169 | Quick Step | 2 | 43 | 42 000 |
| 171 | Esprit | 8 | 43 | 3 217 000 |
| 225 | Acrobatic Move | 3 | 43 | 224 000 |
| 24 | Burst Shot | 31 | 46 | 6 760 000 |
| 61 | Cure Bleeding | 3 | 46 | 380 000 |
| 230 | Sprint | 2 | 52 | 136 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 99 | Rapid Shot | 2 | 55 | 182 000 |
| 415 | Spirit of Sagittarius | 3 | 58 | 2 640 000 |
| 416 | Blessing of Sagittarius | 3 | 58 | 2 640 000 |
| 323 | Quiver of Arrow: A Grade | 1 | 60 | 240 000 |
| 413 | Rapid Fire | 8 | 60 | 6 100 000 |
| 324 | Quiver of Arrow: S Grade | 1 | 72 | 1 090 000 |
| 933 | Detection | 1 | 74 | 1 860 000 |

### Sorcerer  (classId 12, parent HumanWizard)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 4 458 000 |
| 213 | Boost Mana | 8 | 40 | 1 622 000 |
| 228 | Fast Spell Casting | 3 | 40 | 142 000 |
| 234 | Robe Mastery | 41 | 40 | 4 458 000 |
| 249 | Weapon Mastery | 42 | 40 | 4 458 000 |
| 285 | Higher Mana Gain | 27 | 40 | 4 468 000 |
| 1069 | Sleep | 42 | 40 | 4 458 000 |
| 1074 | Surrender To Wind | 14 | 40 | 4 466 000 |
| 1083 | Surrender To Fire | 17 | 40 | 4 466 000 |
| 1160 | Slow | 15 | 40 | 4 466 000 |
| 1169 | Curse Fear | 14 | 40 | 4 466 000 |
| 1171 | Blazing Circle | 19 | 40 | 4 468 000 |
| 1230 | Prominence | 28 | 40 | 4 458 000 |
| 1231 | Aura Flare | 28 | 40 | 4 458 000 |
| 1232 | Blazing Skin | 3 | 40 | 205 000 |
| 1275 | Aura Bolt | 14 | 40 | 4 466 000 |
| 1297 | Clear Mind | 6 | 40 | 1 985 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 694 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 1 862 000 |
| 1072 | Sleeping Cloud | 5 | 44 | 1 261 000 |
| 1078 | Concentration | 6 | 44 | 712 000 |
| 164 | Quick Recycle | 3 | 48 | 63 000 |
| 1056 | Cancellation | 12 | 48 | 4 393 000 |
| 1233 | Decay | 4 | 48 | 1 603 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1296 | Rain of Fire | 9 | 58 | 4 126 000 |
| 1417 | Aura Flash | 5 | 58 | 2 389 000 |
| 1285 | Seed of Fire | 1 | 66 | 370 000 |
| 1288 | Aura Symphony | 1 | 68 | 410 000 |
| 1289 | Inferno | 1 | 70 | 520 000 |
| 1292 | Elemental Assault | 1 | 72 | 880 000 |

### Spellhowler  (classId 40, parent DarkWizard)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 3 867 000 |
| 213 | Boost Mana | 8 | 40 | 1 356 000 |
| 228 | Fast Spell Casting | 3 | 40 | 119 000 |
| 234 | Robe Mastery | 41 | 40 | 3 867 000 |
| 249 | Weapon Mastery | 42 | 40 | 3 867 000 |
| 285 | Higher Mana Gain | 27 | 40 | 3 849 000 |
| 1064 | Silence | 14 | 40 | 3 850 000 |
| 1069 | Sleep | 42 | 40 | 3 865 000 |
| 1074 | Surrender To Wind | 14 | 40 | 3 850 000 |
| 1151 | Corpse Life Drain | 16 | 40 | 3 850 000 |
| 1157 | Body To Mind | 5 | 40 | 535 000 |
| 1160 | Slow | 15 | 40 | 3 850 000 |
| 1169 | Curse Fear | 14 | 40 | 3 850 000 |
| 1222 | Curse Chaos | 15 | 40 | 3 850 000 |
| 1224 | Surrender To Poison | 17 | 40 | 3 850 000 |
| 1234 | Vampiric Claw | 28 | 40 | 3 868 000 |
| 1239 | Hurricane | 28 | 40 | 3 868 000 |
| 1267 | Shadow Flare | 14 | 40 | 3 850 000 |
| 1297 | Clear Mind | 6 | 40 | 1 736 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 464 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 1 639 000 |
| 1148 | Death Spike | 13 | 44 | 3 822 000 |
| 1168 | Curse Poison | 7 | 44 | 1 019 000 |
| 164 | Quick Recycle | 3 | 48 | 57 000 |
| 1167 | Poisonous Cloud | 6 | 48 | 1 388 000 |
| 1176 | Tempest | 15 | 48 | 3 785 000 |
| 1159 | Curse Death Link | 22 | 52 | 3 852 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1417 | Aura Flash | 5 | 58 | 2 085 000 |
| 1287 | Seed of Wind | 1 | 66 | 320 000 |
| 1288 | Aura Symphony | 1 | 68 | 370 000 |
| 1291 | Demon Wind | 1 | 70 | 470 000 |
| 1294 | Elemental Storm | 1 | 72 | 710 000 |

### Spellsinger  (classId 27, parent ElvenWizard)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 3 852 000 |
| 213 | Boost Mana | 8 | 40 | 1 388 000 |
| 228 | Fast Spell Casting | 3 | 40 | 118 000 |
| 234 | Robe Mastery | 41 | 40 | 3 852 000 |
| 249 | Weapon Mastery | 42 | 40 | 3 852 000 |
| 285 | Higher Mana Gain | 27 | 40 | 3 855 000 |
| 1047 | Mana Regeneration | 4 | 40 | 657 000 |
| 1069 | Sleep | 42 | 40 | 3 852 000 |
| 1071 | Surrender To Water | 14 | 40 | 3 853 000 |
| 1164 | Curse Weakness | 19 | 40 | 3 853 000 |
| 1169 | Curse Fear | 14 | 40 | 3 853 000 |
| 1182 | Resist Aqua | 3 | 40 | 62 000 |
| 1223 | Surrender To Earth | 15 | 40 | 3 853 000 |
| 1231 | Aura Flare | 28 | 40 | 3 854 000 |
| 1235 | Hydro Blast | 28 | 40 | 3 854 000 |
| 1236 | Frost Bolt | 19 | 40 | 3 855 000 |
| 1238 | Freezing Skin | 3 | 40 | 175 000 |
| 1265 | Solar Flare | 14 | 40 | 3 853 000 |
| 1275 | Aura Bolt | 14 | 40 | 3 853 000 |
| 1297 | Clear Mind | 6 | 40 | 1 735 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 475 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 1 638 000 |
| 1072 | Sleeping Cloud | 5 | 44 | 1 066 000 |
| 1183 | Freezing Shackle | 4 | 44 | 1 365 000 |
| 1237 | Ice Dagger | 17 | 44 | 3 827 000 |
| 164 | Quick Recycle | 3 | 48 | 57 000 |
| 1056 | Cancellation | 12 | 48 | 3 791 000 |
| 1174 | Frost Wall | 22 | 52 | 3 732 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1295 | Aqua Splash | 9 | 58 | 3 553 000 |
| 1417 | Aura Flash | 5 | 58 | 2 050 000 |
| 1286 | Seed of Water | 1 | 66 | 320 000 |
| 1288 | Aura Symphony | 1 | 68 | 370 000 |
| 1290 | Blizzard | 1 | 70 | 430 000 |
| 1293 | Elemental Symphony | 1 | 72 | 750 000 |

### Swordsinger  (classId 21, parent ElvenKnight)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 15 | Charm | 52 | 40 | 8 932 000 |
| 21 | Poison Recovery | 3 | 40 | 309 000 |
| 58 | Elemental Heal | 55 | 40 | 8 932 000 |
| 102 | Entangle | 16 | 40 | 8 795 000 |
| 123 | Spirit Barrier | 3 | 40 | 359 000 |
| 147 | M. Def. | 51 | 40 | 8 932 000 |
| 217 | Sword/Blunt Weapon Mastery | 45 | 40 | 8 932 000 |
| 269 | Song of Hunter | 1 | 40 | 49 000 |
| 986 | Deadly Strike | 15 | 40 | 8 795 000 |
| 191 | Focus Mind | 6 | 43 | 2 041 000 |
| 196 | Divine Blade | 1 | 43 | 51 000 |
| 267 | Song of Warding | 1 | 43 | 51 000 |
| 61 | Cure Bleeding | 3 | 46 | 475 000 |
| 268 | Song of Wind | 1 | 46 | 75 000 |
| 988 | Battle Whisper | 3 | 46 | 525 000 |
| 270 | Song of Invocation | 1 | 49 | 110 000 |
| 230 | Sprint | 2 | 52 | 190 000 |
| 265 | Song of Life | 1 | 52 | 190 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 98 | Sword Symphony | 5 | 55 | 3 010 000 |
| 264 | Song of Earth | 1 | 55 | 200 000 |
| 402 | Arrest | 10 | 55 | 8 320 000 |
| 407 | Psycho Symphony | 10 | 55 | 8 320 000 |
| 266 | Song of Water | 1 | 58 | 200 000 |
| 306 | Song of Flame Guard | 1 | 62 | 400 000 |
| 304 | Song of Vitality | 1 | 66 | 780 000 |
| 308 | Song of Storm Guard | 1 | 70 | 1 030 000 |
| 305 | Song of Vengeance | 1 | 74 | 2 900 000 |

### TempleKnight  (classId 20, parent ElvenKnight)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 10 | Summon Storm Cubic | 8 | 40 | 3 162 000 |
| 15 | Charm | 52 | 40 | 5 007 000 |
| 18 | Aura of Hate | 37 | 40 | 5 007 000 |
| 21 | Poison Recovery | 3 | 40 | 186 000 |
| 28 | Aggression | 49 | 40 | 5 007 000 |
| 58 | Elemental Heal | 55 | 40 | 5 007 000 |
| 102 | Entangle | 16 | 40 | 5 047 000 |
| 123 | Spirit Barrier | 3 | 40 | 261 000 |
| 147 | M. Def. | 51 | 40 | 5 007 000 |
| 153 | Shield Mastery | 4 | 40 | 126 000 |
| 197 | Divine Armor | 2 | 40 | 72 000 |
| 217 | Sword/Blunt Weapon Mastery | 45 | 40 | 5 007 000 |
| 232 | Heavy Armor Mastery | 52 | 40 | 5 007 000 |
| 812 | Vanguard | 1 | 40 | 26 000 |
| 984 | Shield Strike | 15 | 40 | 4 676 000 |
| 67 | Summon Life Cubic | 7 | 43 | 1 885 000 |
| 112 | Deflect Arrow | 4 | 43 | 108 000 |
| 143 | Cubic Mastery | 2 | 43 | 180 000 |
| 191 | Focus Mind | 6 | 43 | 1 235 000 |
| 288 | Guard Stance | 4 | 43 | 893 000 |
| 61 | Cure Bleeding | 3 | 46 | 286 000 |
| 110 | Ultimate Defense | 2 | 46 | 46 000 |
| 230 | Sprint | 2 | 52 | 100 000 |
| 291 | Final Fortress | 11 | 52 | 4 867 000 |
| 982 | Combat Aura | 3 | 52 | 890 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 400 | Tribunal | 10 | 55 | 4 767 000 |
| 402 | Arrest | 10 | 55 | 4 767 000 |
| 107 | Divine Aura | 9 | 58 | 4 620 000 |
| 316 | Aegis | 1 | 60 | 160 000 |
| 916 | Shield Deflect Magic | 4 | 60 | 1 630 000 |
| 983 | Patience | 1 | 60 | 160 000 |
| 449 | Summon Attractive Cubic | 4 | 62 | 2 830 000 |
| 322 | Shield Fortress | 6 | 64 | 4 060 000 |

### TreasureHunter  (classId 8, parent Rogue)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 27 | Unlock | 14 | 40 | 2 562 000 |
| 30 | Backstab | 37 | 40 | 6 280 000 |
| 60 | Fake Death | 1 | 40 | 33 000 |
| 137 | Critical Chance | 3 | 40 | 122 000 |
| 148 | Vital Force | 8 | 40 | 1 631 000 |
| 193 | Critical Damage | 6 | 40 | 1 438 000 |
| 209 | Dagger Mastery | 45 | 40 | 6 280 000 |
| 221 | Silent Move | 1 | 40 | 33 000 |
| 233 | Light Armor Mastery | 47 | 40 | 6 280 000 |
| 263 | Deadly Blow | 37 | 40 | 6 280 000 |
| 312 | Vicious Stance | 20 | 40 | 6 281 000 |
| 821 | Shadow Step | 1 | 40 | 33 000 |
| 12 | Switch | 14 | 43 | 6 248 000 |
| 106 | Veil | 14 | 43 | 6 248 000 |
| 169 | Quick Step | 2 | 43 | 42 000 |
| 171 | Esprit | 8 | 43 | 3 029 000 |
| 225 | Acrobatic Move | 3 | 43 | 189 000 |
| 4 | Dash | 2 | 46 | 43 000 |
| 168 | Boost Attack Speed | 3 | 46 | 193 000 |
| 198 | Boost Evasion | 3 | 46 | 193 000 |
| 419 | Summon Treasure Key | 4 | 46 | 2 463 000 |
| 11 | Trick | 12 | 49 | 6 163 000 |
| 96 | Bleed | 6 | 49 | 1 629 000 |
| 51 | Lure | 1 | 52 | 115 000 |
| 111 | Ultimate Evasion | 2 | 55 | 147 000 |
| 173 | Acrobatics | 2 | 55 | 147 000 |
| 195 | Boost Breath | 2 | 55 | 147 000 |
| 409 | Critical Blow | 10 | 55 | 5 959 000 |
| 412 | Sand Bomb | 10 | 55 | 5 959 000 |
| 411 | Stealth | 3 | 58 | 2 420 000 |
| 453 | Escape Shackle | 1 | 60 | 242 000 |
| 623 | Find Trap | 1 | 74 | 1 730 000 |
| 624 | Remove Trap | 1 | 74 | 1 730 000 |
| 820 | Evasion Haste | 1 | 74 | 0 |

### Tyrant  (classId 48, parent OrcMonk)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 50 | Focused Force | 7 | 40 | 1 973 000 |
| 54 | Force Blaster | 49 | 40 | 7 280 000 |
| 95 | Cripple | 20 | 40 | 7 275 000 |
| 210 | Fist Weapon Mastery | 45 | 40 | 7 280 000 |
| 233 | Light Armor Mastery | 47 | 40 | 7 280 000 |
| 280 | Burning Fist | 37 | 40 | 7 280 000 |
| 281 | Soul Breaker | 37 | 40 | 7 280 000 |
| 282 | Puma Spirit Totem | 1 | 40 | 33 000 |
| 284 | Hurricane Assault | 40 | 40 | 7 280 000 |
| 319 | Agile Movement | 2 | 40 | 39 000 |
| 993 | Focus Mastery | 7 | 40 | 1 973 000 |
| 994 | Rush | 1 | 40 | 33 000 |
| 17 | Force Burst | 34 | 43 | 7 247 000 |
| 222 | Fury Fists | 1 | 43 | 51 000 |
| 109 | Ogre Spirit Totem | 1 | 46 | 60 000 |
| 168 | Boost Attack Speed | 3 | 46 | 283 000 |
| 35 | Force Storm | 28 | 49 | 7 136 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 81 | Punch of Doom | 3 | 55 | 1 740 000 |
| 420 | Zealot | 3 | 58 | 2 693 000 |
| 423 | Dark Form | 3 | 58 | 2 693 000 |
| 424 | War Frenzy | 3 | 58 | 2 693 000 |
| 461 | Break Duress | 2 | 60 | 710 000 |
| 298 | Rabbit Spirit Totem | 1 | 62 | 400 000 |
| 292 | Bison Spirit Totem | 1 | 68 | 780 000 |
| 425 | Hawk Spirit Totem | 1 | 74 | 2 000 000 |

### Warcryer  (classId 52, parent OrcShaman)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 146 | Anti Magic | 45 | 40 | 3 238 000 |
| 211 | Boost HP | 7 | 40 | 764 000 |
| 213 | Boost Mana | 8 | 40 | 1 110 000 |
| 228 | Fast Spell Casting | 3 | 40 | 86 000 |
| 250 | Weapon Mastery | 42 | 40 | 3 238 000 |
| 251 | Robe Mastery | 45 | 40 | 3 238 000 |
| 252 | Light Armor Mastery | 45 | 40 | 3 238 000 |
| 253 | Heavy Armor Mastery | 43 | 40 | 3 238 000 |
| 260 | Hammer Crush | 35 | 40 | 5 095 000 |
| 927 | Burning Chop | 14 | 40 | 3 245 000 |
| 1001 | Soul Cry | 10 | 40 | 1 110 000 |
| 1006 | Chant of Fire | 3 | 40 | 116 000 |
| 1092 | Fear | 19 | 40 | 3 245 000 |
| 1095 | Venom | 5 | 40 | 116 000 |
| 1097 | Dreaming Spirit | 20 | 40 | 3 245 000 |
| 1105 | Madness | 18 | 40 | 3 245 000 |
| 1229 | Chant of Life | 18 | 40 | 5 121 000 |
| 1244 | Freezing Flame | 4 | 40 | 1 412 000 |
| 1245 | Steal Essence | 14 | 40 | 3 245 000 |
| 1252 | Chant of Evasion | 3 | 40 | 183 000 |
| 1308 | Chant of Predator | 3 | 40 | 736 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 275 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 1 424 000 |
| 1002 | Flame Chant | 3 | 44 | 135 000 |
| 1007 | Chant of Battle | 3 | 44 | 35 000 |
| 1102 | Aura Sink | 6 | 44 | 1 095 000 |
| 1253 | Chant of Rage | 3 | 44 | 219 000 |
| 1310 | Chant of Vampire | 4 | 44 | 1 873 000 |
| 1562 | Chant of Berserker | 2 | 44 | 119 000 |
| 164 | Quick Recycle | 3 | 48 | 57 000 |
| 1009 | Chant of Shielding | 3 | 48 | 57 000 |
| 1251 | Chant of Fury | 2 | 48 | 157 000 |
| 1309 | Chant of Eagle | 3 | 48 | 487 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1390 | War Chant | 3 | 58 | 1 840 000 |
| 1391 | Earth Chant | 3 | 58 | 1 840 000 |
| 1284 | Chant of Revenge | 3 | 62 | 2 100 000 |
| 1517 | Chant of Combat | 1 | 70 | 0 |
| 1518 | Chant of Critical Attack | 1 | 72 | 0 |
| 1535 | Chant of Movement | 1 | 72 | 0 |
| 1519 | Chant of Blood Awakening | 1 | 74 | 0 |

### Warlock  (classId 14, parent HumanWizard)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 10 | Summon Storm Cubic | 8 | 40 | 2 737 000 |
| 146 | Anti Magic | 45 | 40 | 5 072 000 |
| 213 | Boost Mana | 8 | 40 | 1 804 000 |
| 228 | Fast Spell Casting | 3 | 40 | 135 000 |
| 234 | Robe Mastery | 41 | 40 | 5 072 000 |
| 249 | Weapon Mastery | 42 | 40 | 5 072 000 |
| 258 | Light Armor Mastery | 33 | 40 | 5 072 000 |
| 1111 | Summon Kat the Cat | 18 | 40 | 4 933 000 |
| 1126 | Servitor Recharge | 34 | 40 | 4 942 000 |
| 1127 | Servitor Heal | 45 | 40 | 4 939 000 |
| 1140 | Servitor Physical Shield | 3 | 40 | 206 000 |
| 1225 | Summon Mew the Cat | 18 | 40 | 4 933 000 |
| 1262 | Transfer Pain | 5 | 40 | 846 000 |
| 1276 | Summon Kai the Cat | 14 | 40 | 4 933 000 |
| 1279 | Summon Binding Cubic | 9 | 40 | 2 363 000 |
| 1300 | Servitor Cure | 3 | 40 | 281 000 |
| 1328 | Mass Summon Storm Cubic | 8 | 40 | 2 737 000 |
| 1558 | Dimension Spiral | 14 | 40 | 4 933 000 |
| 143 | Cubic Mastery | 2 | 44 | 142 000 |
| 212 | Fast HP Recovery | 6 | 44 | 1 877 000 |
| 229 | Fast Mana Recovery | 7 | 44 | 2 145 000 |
| 1139 | Servitor Magic Shield | 2 | 44 | 137 000 |
| 1141 | Servitor Haste | 2 | 44 | 137 000 |
| 1547 | Spirit Sharing | 3 | 44 | 777 000 |
| 164 | Quick Recycle | 3 | 48 | 75 000 |
| 1144 | Servitor Wind Walk | 2 | 48 | 75 000 |
| 1299 | Servitor Empowerment | 2 | 52 | 620 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 1331 | Summon Feline Queen | 10 | 56 | 4 695 000 |
| 1380 | Betray | 10 | 56 | 4 695 000 |
| 1386 | Arcane Disruption | 10 | 56 | 4 695 000 |
| 1403 | Summon Friend | 1 | 56 | 105 000 |
| 1383 | Mass Surrender to Fire | 5 | 58 | 2 570 000 |
| 1301 | Servitor Blessing | 1 | 62 | 220 000 |

### Warlord  (classId 3, parent Warrior)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 36 | Whirlwind | 37 | 40 | 6 246 000 |
| 48 | Thunder Storm | 37 | 40 | 6 246 000 |
| 87 | Detect Animal Weakness | 1 | 40 | 33 000 |
| 121 | Battle Roar | 6 | 40 | 1 425 000 |
| 212 | Fast HP Recovery | 8 | 40 | 2 630 000 |
| 216 | Polearm Mastery | 45 | 40 | 6 246 000 |
| 227 | Light Armor Mastery | 50 | 40 | 6 246 000 |
| 231 | Heavy Armor Mastery | 50 | 40 | 6 246 000 |
| 312 | Vicious Stance | 20 | 40 | 6 221 000 |
| 317 | Focus Attack | 5 | 40 | 2 335 000 |
| 920 | Power Crush | 37 | 40 | 6 246 000 |
| 994 | Rush | 1 | 40 | 33 000 |
| 116 | Howl | 14 | 43 | 6 188 000 |
| 211 | Boost HP | 10 | 43 | 3 387 000 |
| 286 | Provoke | 3 | 43 | 456 000 |
| 290 | Final Frenzy | 14 | 43 | 6 188 000 |
| 104 | Detect Plant Weakness | 1 | 46 | 50 000 |
| 130 | Thrill Fight | 2 | 46 | 200 000 |
| 287 | Lionheart | 3 | 49 | 405 000 |
| 80 | Detect Beast Weakness | 1 | 52 | 140 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 181 | Revival | 1 | 55 | 150 000 |
| 452 | Shock Stomp | 5 | 55 | 2 604 000 |
| 88 | Detect Dragon Weakness | 1 | 58 | 157 000 |
| 421 | Fell Swoop | 5 | 58 | 3 277 000 |
| 422 | Polearm Accuracy | 3 | 58 | 2 227 000 |
| 424 | War Frenzy | 3 | 58 | 2 227 000 |
| 320 | Wrath | 10 | 66 | 4 560 000 |

### Warsmith  (classId 57, parent Artisan)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 36 | Whirlwind | 37 | 40 | 6 989 000 |
| 148 | Vital Force | 8 | 40 | 2 039 000 |
| 190 | Fatal Strike | 37 | 40 | 6 989 000 |
| 205 | Sword/Blunt Weapon Mastery | 45 | 40 | 6 989 000 |
| 212 | Fast HP Recovery | 8 | 40 | 3 061 000 |
| 216 | Polearm Mastery | 45 | 40 | 6 989 000 |
| 227 | Light Armor Mastery | 50 | 40 | 6 989 000 |
| 231 | Heavy Armor Mastery | 50 | 40 | 6 989 000 |
| 248 | Crystallize | 5 | 40 | 1 195 000 |
| 260 | Hammer Crush | 37 | 40 | 6 989 000 |
| 822 | Repair Golem | 3 | 40 | 260 000 |
| 824 | Golem Reinforcement | 3 | 40 | 260 000 |
| 994 | Rush | 1 | 40 | 28 000 |
| 1561 | Battle Cry | 5 | 40 | 1 449 000 |
| 25 | Summon Mechanic Golem | 9 | 43 | 2 982 000 |
| 172 | Create Item | 9 | 43 | 1 350 000 |
| 211 | Boost HP | 10 | 43 | 3 930 000 |
| 823 | Strengthen Golem | 3 | 43 | 323 000 |
| 34 | Bandage | 3 | 46 | 406 000 |
| 150 | Weight Limit | 3 | 46 | 46 000 |
| 828 | Case Harden | 1 | 46 | 46 000 |
| 829 | Hard Tanning | 1 | 46 | 46 000 |
| 830 | Embroider | 1 | 46 | 46 000 |
| 13 | Summon Siege Golem | 1 | 49 | 700 000 |
| 825 | Sharp Edge | 1 | 49 | 61 000 |
| 826 | Spike | 1 | 49 | 61 000 |
| 827 | Restring | 1 | 49 | 61 000 |
| 831 | Summon Merchant Golem | 1 | 52 | 125 000 |
| 1405 | Divine Inspiration | 4 | 52 | 0 |
| 299 | Summon Wild Hog Cannon | 1 | 58 | 800 000 |
| 301 | Summon Big Boom | 5 | 58 | 3 820 000 |
| 422 | Polearm Accuracy | 3 | 58 | 2 740 000 |
| 424 | War Frenzy | 3 | 58 | 2 740 000 |
| 320 | Wrath | 10 | 66 | 5 200 000 |
| 448 | Summon Swoop Cannon | 1 | 68 | 3 300 000 |

## 3rd Class Skills

### Adventurer  (classId 93, parent TreasureHunter)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 12 500 000 |
| 344 | Lethal Blow | 1 | 76 | 12 500 000 |
| 330 | Skill Mastery | 1 | 77 | 14 670 000 |
| 358 | Bluff | 1 | 77 | 14 670 000 |
| 334 | Focus Skill Mastery | 1 | 78 | 16 000 000 |
| 356 | Focus Chance | 1 | 78 | 16 000 000 |
| 357 | Focus Power | 1 | 78 | 16 000 000 |
| 432 | Assassination | 1 | 78 | 16 000 000 |
| 445 | Mirage | 1 | 79 | 60 000 000 |
| 531 | Critical Wound | 1 | 79 | 60 000 000 |
| 460 | Symbol of the Assassin | 1 | 80 | 150 000 000 |
| 991 | Throwing Dagger | 1 | 80 | 90 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 922 | Hide | 1 | 81 | 0 |
| 923 | Dual Dagger Mastery | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 768 | Exciting Adventure | 1 | 83 | 0 |
| 928 | Dual Blow | 1 | 83 | 100 000 000 |

### ArcanaLord  (classId 96, parent Warlock)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 934 | Sigil Mastery | 1 | 76 | 6 250 000 |
| 1350 | Warrior Bane | 1 | 76 | 6 250 000 |
| 1558 | Dimension Spiral | 24 | 76 | 173 250 000 |
| 331 | Skill Mastery | 1 | 77 | 11 000 000 |
| 1346 | Warrior Servitor | 1 | 77 | 11 000 000 |
| 1351 | Mage Bane | 1 | 77 | 11 000 000 |
| 338 | Arcane Agility | 1 | 78 | 16 000 000 |
| 435 | Summon Lore | 1 | 78 | 16 000 000 |
| 1349 | Final Servitor | 1 | 78 | 16 000 000 |
| 1406 | Summon Feline King | 1 | 79 | 60 000 000 |
| 781 | Summon Smart Cubic | 1 | 80 | 150 000 000 |
| 1424 | Anti-Summoning Field | 1 | 80 | 150 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1496 | Servitor Barrier | 1 | 81 | 0 |
| 1497 | Excessive Loyalty | 1 | 81 | 0 |
| 1498 | Mutual Response | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 929 | Spirit of the Cat | 1 | 83 | 0 |
| 1557 | Servitor Share | 1 | 83 | 100 000 000 |

### Archmage  (classId 94, parent Sorcerer)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 12 500 000 |
| 925 | Sigil Mastery | 1 | 76 | 12 500 000 |
| 331 | Skill Mastery | 1 | 77 | 18 000 000 |
| 1339 | Fire Vortex | 1 | 77 | 18 000 000 |
| 337 | Arcane Power | 1 | 78 | 21 340 000 |
| 433 | Arcane Roar | 1 | 78 | 21 340 000 |
| 1338 | Arcane Chaos | 1 | 78 | 21 340 000 |
| 1451 | Fire Vortex Buster | 1 | 79 | 60 000 000 |
| 1452 | Count of Fire | 1 | 79 | 60 000 000 |
| 1419 | Volcano | 1 | 80 | 150 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1467 | Meteor | 1 | 81 | 0 |
| 1532 | Enlightement | 1 | 81 | 0 |
| 1554 | Aura Blast | 1 | 81 | 80 000 000 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1555 | Aura Cannon | 1 | 82 | 90 000 000 |
| 1492 | Flame Armor | 1 | 83 | 0 |
| 1556 | Arcane Shield | 1 | 83 | 100 000 000 |

### Cardinal  (classId 97, parent Bishop)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 926 | Sigil Mastery | 1 | 76 | 6 250 000 |
| 1335 | Balance Life | 1 | 76 | 6 250 000 |
| 331 | Skill Mastery | 1 | 77 | 11 000 000 |
| 1353 | Divine Protection | 1 | 77 | 11 000 000 |
| 1360 | Mass Block Shield | 1 | 77 | 11 000 000 |
| 336 | Arcane Wisdom | 1 | 78 | 16 000 000 |
| 436 | Divine Lore | 1 | 78 | 16 000 000 |
| 1361 | Mass Block Wind Walk | 1 | 78 | 16 000 000 |
| 1409 | Cleanse | 1 | 78 | 16 000 000 |
| 1410 | Salvation | 1 | 79 | 60 000 000 |
| 1459 | Divine Power | 1 | 79 | 60 000 000 |
| 1425 | Purification Field | 1 | 80 | 150 000 000 |
| 1426 | Miracle | 1 | 80 | 100 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1533 | Enlightement | 1 | 81 | 0 |
| 1540 | Turn Stone | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1505 | Sublime Self-sacrifice | 1 | 83 | 0 |
| 1553 | Chain Heal | 1 | 83 | 100 000 000 |

### Dominator  (classId 115, parent Overlord)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 926 | Sigil Mastery | 1 | 76 | 6 250 000 |
| 1367 | Seal of Disease | 1 | 76 | 6 250 000 |
| 331 | Skill Mastery | 1 | 77 | 11 000 000 |
| 1364 | Eye of Pa'agrio | 1 | 77 | 11 000 000 |
| 1365 | Soul of Pa'agrio | 1 | 77 | 11 000 000 |
| 337 | Arcane Power | 1 | 78 | 16 000 000 |
| 436 | Divine Lore | 1 | 78 | 16 000 000 |
| 1366 | Seal of Despair | 1 | 78 | 16 000 000 |
| 1415 | Pa'agrio's Emblem | 1 | 78 | 16 000 000 |
| 1414 | Victory of Pa'agrio | 1 | 79 | 60 000 000 |
| 1416 | Pa'agrio's Fist | 1 | 79 | 60 000 000 |
| 1462 | Seal of Blockade | 1 | 79 | 60 000 000 |
| 1427 | Flames of Invincibility | 1 | 80 | 150 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1533 | Enlightement | 1 | 81 | 0 |
| 1540 | Turn Stone | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 949 | Onslaught of Paagrio | 1 | 83 | 0 |
| 1509 | Seal of Limit | 1 | 83 | 0 |
| 1553 | Chain Heal | 1 | 83 | 100 000 000 |

### Doombringer  (classId 131, parent Berserker)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 340 000 |
| 329 | Health | 1 | 76 | 8 340 000 |
| 335 | Fortitude | 1 | 76 | 8 340 000 |
| 330 | Skill Mastery | 1 | 77 | 22 000 000 |
| 526 | Enuma Elish | 1 | 78 | 22 000 000 |
| 793 | Rush Impact | 1 | 78 | 22 000 000 |
| 939 | Soul Rage | 1 | 78 | 22 000 000 |
| 538 | Final Form | 1 | 79 | 60 000 000 |
| 794 | Mass Disarm | 1 | 79 | 60 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 917 | Final Secret | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 948 | Eye for Eye | 1 | 83 | 0 |

### Doomcryer  (classId 116, parent Warcryer)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 300 000 |
| 329 | Health | 1 | 76 | 8 300 000 |
| 935 | Sigil Mastery | 1 | 76 | 8 300 000 |
| 1549 | Chant of Elements | 1 | 76 | 14 670 000 |
| 331 | Skill Mastery | 1 | 77 | 14 670 000 |
| 1362 | Chant of Spirit | 1 | 77 | 14 670 000 |
| 336 | Arcane Wisdom | 1 | 78 | 16 000 000 |
| 436 | Divine Lore | 1 | 78 | 16 000 000 |
| 1363 | Chant of Victory | 1 | 78 | 16 000 000 |
| 1429 | Gate Chant | 1 | 78 | 16 000 000 |
| 1413 | Magnus' Chant | 1 | 79 | 60 000 000 |
| 1461 | Chant of Protection | 1 | 79 | 60 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1533 | Enlightement | 1 | 81 | 0 |
| 1540 | Turn Stone | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1543 | Great Fury | 1 | 83 | 0 |

### Dreadnought  (classId 89, parent Warlord)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 300 000 |
| 329 | Health | 1 | 76 | 8 300 000 |
| 921 | Cursed Pierce | 1 | 76 | 8 300 000 |
| 330 | Skill Mastery | 1 | 77 | 12 250 000 |
| 359 | Eye of Hunter | 1 | 77 | 12 250 000 |
| 361 | Shock Blast | 1 | 77 | 12 250 000 |
| 339 | Parry Stance | 1 | 78 | 12 800 000 |
| 347 | Earthquake | 1 | 78 | 12 800 000 |
| 360 | Eye of Slayer | 1 | 78 | 12 800 000 |
| 430 | Master of Combat | 1 | 78 | 12 800 000 |
| 440 | Braveheart | 1 | 78 | 12 800 000 |
| 457 | Symbol of Honor | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 917 | Final Secret | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 774 | Dread Pool | 1 | 83 | 0 |
| 995 | Rush Impact | 1 | 83 | 100 000 000 |

### Duelist  (classId 88, parent Gladiator)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 10 000 000 |
| 329 | Health | 1 | 76 | 10 000 000 |
| 330 | Skill Mastery | 1 | 77 | 12 250 000 |
| 340 | Riposte Stance | 1 | 77 | 12 250 000 |
| 359 | Eye of Hunter | 1 | 77 | 12 250 000 |
| 345 | Sonic Rage | 1 | 78 | 16 000 000 |
| 360 | Eye of Slayer | 1 | 78 | 16 000 000 |
| 430 | Master of Combat | 1 | 78 | 16 000 000 |
| 440 | Braveheart | 1 | 78 | 16 000 000 |
| 8 | Sonic Focus | 8 | 79 | 80 000 000 |
| 442 | Sonic Barrier | 1 | 79 | 60 000 000 |
| 992 | Sonic Mastery | 8 | 79 | 60 000 000 |
| 458 | Symbol of Energy | 1 | 80 | 150 000 000 |
| 775 | Weapon Blockade | 1 | 80 | 100 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 917 | Final Secret | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 919 | Maximum Sonic Focus | 1 | 83 | 0 |
| 995 | Rush Impact | 1 | 83 | 100 000 000 |

### ElementalMaster  (classId 104, parent ElementalSummoner)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 300 000 |
| 934 | Sigil Mastery | 1 | 76 | 8 300 000 |
| 1350 | Warrior Bane | 1 | 76 | 8 300 000 |
| 1558 | Dimension Spiral | 24 | 76 | 170 300 000 |
| 331 | Skill Mastery | 1 | 77 | 14 000 000 |
| 1347 | Wizard Servitor | 1 | 77 | 14 000 000 |
| 338 | Arcane Agility | 1 | 78 | 21 000 000 |
| 435 | Summon Lore | 1 | 78 | 21 000 000 |
| 1349 | Final Servitor | 1 | 78 | 21 000 000 |
| 1407 | Summon Magnus the Unicorn | 1 | 79 | 60 000 000 |
| 782 | Summon Smart Cubic | 1 | 80 | 150 000 000 |
| 1424 | Anti-Summoning Field | 1 | 80 | 150 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1496 | Servitor Barrier | 1 | 81 | 0 |
| 1497 | Excessive Loyalty | 1 | 81 | 0 |
| 1498 | Mutual Response | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 931 | Spirit of the Unicorn | 1 | 83 | 0 |
| 1557 | Servitor Share | 1 | 83 | 100 000 000 |

### Eva'sSaint  (classId 105, parent ElvenElder)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 926 | Sigil Mastery | 1 | 76 | 6 250 000 |
| 1354 | Arcane Protection | 1 | 76 | 6 250 000 |
| 1550 | Mass Cure Poison | 1 | 76 | 11 000 000 |
| 1552 | Mass Vitalize | 1 | 76 | 11 000 000 |
| 331 | Skill Mastery | 1 | 77 | 11 000 000 |
| 1353 | Divine Protection | 1 | 77 | 11 000 000 |
| 1359 | Block Wind Walk | 1 | 77 | 11 000 000 |
| 336 | Arcane Wisdom | 1 | 78 | 21 000 000 |
| 436 | Divine Lore | 1 | 78 | 21 000 000 |
| 1355 | Prophecy of Water | 1 | 78 | 21 000 000 |
| 1460 | Mana Gain | 1 | 79 | 60 000 000 |
| 1428 | Mass Recharge | 1 | 80 | 150 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1533 | Enlightement | 1 | 81 | 0 |
| 1540 | Turn Stone | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1506 | Blessing of Eva | 1 | 83 | 0 |
| 1553 | Chain Heal | 1 | 83 | 100 000 000 |

### Eva'sTemplar  (classId 99, parent TempleKnight)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 335 | Fortitude | 1 | 76 | 6 250 000 |
| 984 | Shield Strike | 25 | 76 | 175 250 000 |
| 352 | Shield Bash | 1 | 77 | 13 000 000 |
| 368 | Vengeance | 1 | 77 | 13 000 000 |
| 341 | Touch of Life | 1 | 78 | 16 000 000 |
| 351 | Magical Mirror | 1 | 78 | 16 000 000 |
| 429 | Knighthood | 1 | 78 | 16 000 000 |
| 527 | Iron Shield | 1 | 79 | 60 000 000 |
| 528 | Shield of Faith | 1 | 79 | 60 000 000 |
| 454 | Symbol of Defense | 1 | 80 | 150 000 000 |
| 779 | Summon Smart Cubic | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 760 | Anti-magic Armor | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 913 | Deflect Magic | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 786 | Evas Will | 1 | 83 | 0 |
| 787 | Touch of Eva | 1 | 83 | 0 |
| 985 | Challenge for Fate | 1 | 83 | 100 000 000 |

### FemaleSoulHound  (classId 133, parent FemaleSoulBreaker)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 300 000 |
| 329 | Health | 1 | 76 | 8 300 000 |
| 1516 | Soul Strike | 1 | 76 | 8 300 000 |
| 330 | Skill Mastery | 1 | 77 | 11 000 000 |
| 1512 | Soul Vortex | 1 | 77 | 11 000 000 |
| 939 | Soul Rage | 1 | 78 | 32 000 000 |
| 1469 | Leopold | 1 | 78 | 32 000 000 |
| 538 | Final Form | 1 | 79 | 60 000 000 |
| 1513 | Soul Vortex Extinction | 1 | 79 | 60 000 000 |
| 1515 | Lightning Barrier | 1 | 80 | 100 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 1532 | Enlightement | 1 | 81 | 0 |
| 1554 | Aura Blast | 1 | 81 | 80 000 000 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1555 | Aura Cannon | 1 | 82 | 90 000 000 |
| 791 | Lightning Shock | 1 | 83 | 0 |
| 1556 | Arcane Shield | 1 | 83 | 100 000 000 |

### FortuneSeeker  (classId 117, parent BountyHunter)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 348 | Spoil Crush | 1 | 76 | 6 250 000 |
| 997 | Crushing Strike | 25 | 76 | 147 650 000 |
| 330 | Skill Mastery | 1 | 77 | 11 000 000 |
| 340 | Riposte Stance | 1 | 77 | 11 000 000 |
| 362 | Armor Crush | 1 | 77 | 11 000 000 |
| 339 | Parry Stance | 1 | 78 | 12 800 000 |
| 347 | Earthquake | 1 | 78 | 12 800 000 |
| 430 | Master of Combat | 1 | 78 | 12 800 000 |
| 440 | Braveheart | 1 | 78 | 12 800 000 |
| 537 | Spoil Bomb | 1 | 79 | 60 000 000 |
| 456 | Symbol of Resistance | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 917 | Final Secret | 1 | 81 | 0 |
| 923 | Dual Dagger Mastery | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 947 | Lucky Strike | 1 | 83 | 0 |
| 1560 | Lucky Blow | 1 | 83 | 100 000 000 |

### GhostHunter  (classId 108, parent AbyssWalker)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 12 500 000 |
| 344 | Lethal Blow | 1 | 76 | 12 500 000 |
| 330 | Skill Mastery | 1 | 77 | 14 670 000 |
| 358 | Bluff | 1 | 77 | 14 670 000 |
| 334 | Focus Skill Mastery | 1 | 78 | 16 000 000 |
| 355 | Focus Death | 1 | 78 | 16 000 000 |
| 357 | Focus Power | 1 | 78 | 16 000 000 |
| 432 | Assassination | 1 | 78 | 16 000 000 |
| 447 | Counterattack | 1 | 79 | 60 000 000 |
| 531 | Critical Wound | 1 | 79 | 60 000 000 |
| 460 | Symbol of the Assassin | 1 | 80 | 150 000 000 |
| 991 | Throwing Dagger | 1 | 80 | 70 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 922 | Hide | 1 | 81 | 0 |
| 923 | Dual Dagger Mastery | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 770 | Ghost Walking | 1 | 83 | 0 |
| 928 | Dual Blow | 1 | 83 | 100 000 000 |

### GhostSentinel  (classId 109, parent PhantomRanger)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 12 500 000 |
| 343 | Lethal Shot | 1 | 76 | 12 500 000 |
| 330 | Skill Mastery | 1 | 77 | 14 670 000 |
| 354 | Hamstring Shot | 1 | 77 | 14 670 000 |
| 334 | Focus Skill Mastery | 1 | 78 | 21 340 000 |
| 369 | Evade Shot | 1 | 78 | 21 340 000 |
| 431 | Archery | 1 | 78 | 21 340 000 |
| 532 | Counter Chance | 1 | 79 | 60 000 000 |
| 535 | Counter Mind | 1 | 79 | 60 000 000 |
| 459 | Symbol of the Sniper | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 924 | Seven Arrow | 1 | 81 | 0 |
| 946 | Silent Mind | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 987 | Multiple Shot | 1 | 82 | 90 000 000 |
| 773 | Ghost Piercing | 1 | 83 | 0 |
| 990 | Death Shot | 1 | 83 | 100 000 000 |

### GrandKhavatari  (classId 114, parent Tyrant)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 330 000 |
| 329 | Health | 1 | 76 | 8 330 000 |
| 335 | Fortitude | 1 | 76 | 8 330 000 |
| 330 | Skill Mastery | 1 | 77 | 13 000 000 |
| 340 | Riposte Stance | 1 | 77 | 13 000 000 |
| 346 | Raging Force | 1 | 78 | 21 340 000 |
| 430 | Master of Combat | 1 | 78 | 21 340 000 |
| 441 | Force Meditation | 1 | 78 | 21 340 000 |
| 50 | Focused Force | 8 | 79 | 80 000 000 |
| 443 | Force Barrier | 1 | 79 | 60 000 000 |
| 993 | Focus Mastery | 8 | 79 | 60 000 000 |
| 458 | Symbol of Energy | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 917 | Final Secret | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 776 | Force Of Destruction | 1 | 83 | 0 |
| 918 | Maximum Focus Force | 1 | 83 | 0 |
| 995 | Rush Impact | 1 | 83 | 100 000 000 |

### HellKnight  (classId 91, parent DarkAvenger)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 335 | Fortitude | 1 | 76 | 6 250 000 |
| 984 | Shield Strike | 25 | 76 | 175 250 000 |
| 353 | Shield Slam | 1 | 77 | 13 000 000 |
| 368 | Vengeance | 1 | 77 | 13 000 000 |
| 342 | Touch of Death | 1 | 78 | 16 000 000 |
| 350 | Physical Mirror | 1 | 78 | 16 000 000 |
| 429 | Knighthood | 1 | 78 | 16 000 000 |
| 439 | Shield of Revenge | 1 | 79 | 60 000 000 |
| 527 | Iron Shield | 1 | 79 | 60 000 000 |
| 528 | Shield of Faith | 1 | 79 | 60 000 000 |
| 454 | Symbol of Defense | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 760 | Anti-magic Armor | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 913 | Deflect Magic | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 761 | Seed of Revenge | 1 | 83 | 0 |
| 762 | Insane Crusher | 1 | 83 | 0 |
| 763 | Hell Scream | 1 | 83 | 0 |
| 985 | Challenge for Fate | 1 | 83 | 100 000 000 |

### Hierophant  (classId 98, parent Prophet)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 935 | Sigil Mastery | 1 | 76 | 6 250 000 |
| 1352 | Elemental Protection | 1 | 76 | 8 340 000 |
| 331 | Skill Mastery | 1 | 77 | 11 000 000 |
| 1358 | Block Shield | 1 | 77 | 11 000 000 |
| 1359 | Block Wind Walk | 1 | 77 | 11 000 000 |
| 336 | Arcane Wisdom | 1 | 78 | 21 340 000 |
| 436 | Divine Lore | 1 | 78 | 21 340 000 |
| 1356 | Prophecy of Fire | 1 | 78 | 21 340 000 |
| 1411 | Mystic Immunity | 1 | 79 | 60 000 000 |
| 1412 | Spell Turning | 1 | 79 | 60 000 000 |
| 1564 | Piercing Attack | 1 | 80 | 90 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1533 | Enlightement | 1 | 81 | 0 |
| 1540 | Turn Stone | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1542 | Counter Critical | 1 | 83 | 0 |

### Judicator  (classId 136, parent Inspector)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 12 500 000 |
| 329 | Health | 1 | 76 | 12 500 000 |
| 330 | Skill Mastery | 1 | 77 | 14 700 000 |
| 939 | Soul Rage | 1 | 78 | 60 000 000 |
| 538 | Final Form | 1 | 79 | 60 000 000 |
| 1515 | Lightning Barrier | 1 | 80 | 100 000 000 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |

### Maestro  (classId 118, parent Warsmith)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 10 000 000 |
| 329 | Health | 1 | 76 | 10 000 000 |
| 330 | Skill Mastery | 1 | 77 | 12 250 000 |
| 340 | Riposte Stance | 1 | 77 | 12 250 000 |
| 362 | Armor Crush | 1 | 77 | 12 250 000 |
| 339 | Parry Stance | 1 | 78 | 16 000 000 |
| 347 | Earthquake | 1 | 78 | 16 000 000 |
| 430 | Master of Combat | 1 | 78 | 16 000 000 |
| 440 | Braveheart | 1 | 78 | 16 000 000 |
| 457 | Symbol of Honor | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 917 | Final Secret | 1 | 81 | 0 |
| 172 | Create Item | 10 | 82 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 778 | Golem Armor | 1 | 83 | 0 |
| 995 | Rush Impact | 1 | 83 | 100 000 000 |

### MaleSoulHound  (classId 132, parent MaleSoulBreaker)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 300 000 |
| 329 | Health | 1 | 76 | 8 300 000 |
| 1516 | Soul Strike | 1 | 76 | 8 300 000 |
| 330 | Skill Mastery | 1 | 77 | 11 000 000 |
| 1512 | Soul Vortex | 1 | 77 | 11 000 000 |
| 939 | Soul Rage | 1 | 78 | 32 000 000 |
| 1469 | Leopold | 1 | 78 | 32 000 000 |
| 538 | Final Form | 1 | 79 | 60 000 000 |
| 1513 | Soul Vortex Extinction | 1 | 79 | 60 000 000 |
| 1515 | Lightning Barrier | 1 | 80 | 100 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 1532 | Enlightement | 1 | 81 | 0 |
| 1554 | Aura Blast | 1 | 81 | 80 000 000 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1555 | Aura Cannon | 1 | 82 | 90 000 000 |
| 791 | Lightning Shock | 1 | 83 | 0 |
| 1556 | Arcane Shield | 1 | 83 | 100 000 000 |

### MoonlightSentinel  (classId 102, parent SilverRanger)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 12 500 000 |
| 343 | Lethal Shot | 1 | 76 | 12 500 000 |
| 330 | Skill Mastery | 1 | 77 | 14 670 000 |
| 354 | Hamstring Shot | 1 | 77 | 14 670 000 |
| 334 | Focus Skill Mastery | 1 | 78 | 21 340 000 |
| 369 | Evade Shot | 1 | 78 | 21 340 000 |
| 431 | Archery | 1 | 78 | 21 340 000 |
| 533 | Counter Rapid Shot | 1 | 79 | 60 000 000 |
| 534 | Counter Dash | 1 | 79 | 60 000 000 |
| 459 | Symbol of the Sniper | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 924 | Seven Arrow | 1 | 81 | 0 |
| 946 | Silent Mind | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 987 | Multiple Shot | 1 | 82 | 90 000 000 |
| 772 | Arrow Rain | 1 | 83 | 0 |
| 990 | Death Shot | 1 | 83 | 100 000 000 |

### MysticMuse  (classId 103, parent Spellsinger)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 300 000 |
| 925 | Sigil Mastery | 1 | 76 | 8 300 000 |
| 1342 | Light Vortex | 1 | 76 | 8 300 000 |
| 331 | Skill Mastery | 1 | 77 | 14 670 000 |
| 1340 | Ice Vortex | 1 | 77 | 14 670 000 |
| 337 | Arcane Power | 1 | 78 | 21 340 000 |
| 433 | Arcane Roar | 1 | 78 | 21 340 000 |
| 1338 | Arcane Chaos | 1 | 78 | 21 340 000 |
| 1453 | Ice Vortex Crusher | 1 | 79 | 60 000 000 |
| 1454 | Diamond Dust | 1 | 79 | 60 000 000 |
| 1455 | Throne of Ice | 1 | 79 | 60 000 000 |
| 1421 | Raging Waves | 1 | 80 | 150 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1468 | Star Fall | 1 | 81 | 0 |
| 1532 | Enlightement | 1 | 81 | 0 |
| 1554 | Aura Blast | 1 | 81 | 80 000 000 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1555 | Aura Cannon | 1 | 82 | 90 000 000 |
| 1493 | Frost Armor | 1 | 83 | 0 |
| 1556 | Arcane Shield | 1 | 83 | 100 000 000 |

### PhoenixKnight  (classId 90, parent Paladin)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 335 | Fortitude | 1 | 76 | 6 250 000 |
| 984 | Shield Strike | 25 | 76 | 175 250 000 |
| 353 | Shield Slam | 1 | 77 | 13 000 000 |
| 368 | Vengeance | 1 | 77 | 13 000 000 |
| 341 | Touch of Life | 1 | 78 | 16 000 000 |
| 350 | Physical Mirror | 1 | 78 | 16 000 000 |
| 429 | Knighthood | 1 | 78 | 16 000 000 |
| 438 | Soul of the Phoenix | 1 | 79 | 60 000 000 |
| 527 | Iron Shield | 1 | 79 | 60 000 000 |
| 528 | Shield of Faith | 1 | 79 | 60 000 000 |
| 454 | Symbol of Defense | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 760 | Anti-magic Armor | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 913 | Deflect Magic | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 784 | Spirit of Phoenix | 1 | 83 | 0 |
| 785 | Flame Icon | 1 | 83 | 0 |
| 912 | Summon Imperial Phoenix | 1 | 83 | 0 |
| 985 | Challenge for Fate | 1 | 83 | 100 000 000 |

### Sagittarius  (classId 92, parent Hawkeye)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 12 500 000 |
| 343 | Lethal Shot | 1 | 76 | 12 500 000 |
| 330 | Skill Mastery | 1 | 77 | 14 670 000 |
| 354 | Hamstring Shot | 1 | 77 | 14 670 000 |
| 334 | Focus Skill Mastery | 1 | 78 | 32 000 000 |
| 431 | Archery | 1 | 78 | 32 000 000 |
| 534 | Counter Dash | 1 | 79 | 60 000 000 |
| 535 | Counter Mind | 1 | 79 | 60 000 000 |
| 459 | Symbol of the Sniper | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 924 | Seven Arrow | 1 | 81 | 0 |
| 946 | Silent Mind | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 987 | Multiple Shot | 1 | 82 | 90 000 000 |
| 771 | Flame Hawk | 1 | 83 | 0 |
| 990 | Death Shot | 1 | 83 | 100 000 000 |

### ShillienSaint  (classId 112, parent ShillienElder)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 926 | Sigil Mastery | 1 | 76 | 6 250 000 |
| 1354 | Arcane Protection | 1 | 76 | 6 250 000 |
| 1550 | Mass Cure Poison | 1 | 76 | 13 000 000 |
| 1551 | Mass Purify | 1 | 76 | 13 000 000 |
| 331 | Skill Mastery | 1 | 77 | 13 000 000 |
| 1358 | Block Shield | 1 | 77 | 13 000 000 |
| 336 | Arcane Wisdom | 1 | 78 | 21 340 000 |
| 436 | Divine Lore | 1 | 78 | 21 340 000 |
| 1357 | Prophecy of Wind | 1 | 78 | 21 340 000 |
| 1460 | Mana Gain | 1 | 79 | 60 000 000 |
| 1428 | Mass Recharge | 1 | 80 | 150 000 000 |
| 1508 | Thorn Root | 1 | 80 | 100 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1533 | Enlightement | 1 | 81 | 0 |
| 1540 | Turn Stone | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1507 | Lord of Vampire | 1 | 83 | 0 |
| 1553 | Chain Heal | 1 | 83 | 100 000 000 |

### ShillienTemplar  (classId 106, parent ShillienKnight)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 335 | Fortitude | 1 | 76 | 6 250 000 |
| 984 | Shield Strike | 25 | 76 | 166 250 000 |
| 352 | Shield Bash | 1 | 77 | 13 000 000 |
| 368 | Vengeance | 1 | 77 | 13 000 000 |
| 342 | Touch of Death | 1 | 78 | 21 000 000 |
| 351 | Magical Mirror | 1 | 78 | 21 000 000 |
| 429 | Knighthood | 1 | 78 | 21 000 000 |
| 527 | Iron Shield | 1 | 79 | 60 000 000 |
| 528 | Shield of Faith | 1 | 79 | 60 000 000 |
| 454 | Symbol of Defense | 1 | 80 | 150 000 000 |
| 780 | Summon Smart Cubic | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 760 | Anti-magic Armor | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 913 | Deflect Magic | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 788 | Pain of Shilen | 1 | 83 | 0 |
| 789 | Spirit of Shilen | 1 | 83 | 0 |
| 985 | Challenge for Fate | 1 | 83 | 100 000 000 |

### Soultaker  (classId 95, parent Necromancer)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 925 | Sigil Mastery | 1 | 76 | 6 250 000 |
| 1343 | Dark Vortex | 1 | 76 | 6 250 000 |
| 331 | Skill Mastery | 1 | 77 | 14 600 000 |
| 1336 | Curse of Doom | 1 | 77 | 14 600 000 |
| 1344 | Mass Warrior Bane | 1 | 77 | 14 600 000 |
| 337 | Arcane Power | 1 | 78 | 16 000 000 |
| 434 | Necromancy | 1 | 78 | 16 000 000 |
| 1337 | Curse of Abyss | 1 | 78 | 16 000 000 |
| 1345 | Mass Mage Bane | 1 | 78 | 16 000 000 |
| 1422 | Day of Doom | 1 | 80 | 150 000 000 |
| 1423 | Gehenna | 1 | 80 | 150 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1467 | Meteor | 1 | 81 | 0 |
| 1532 | Enlightement | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1495 | Vampiric Mist | 1 | 83 | 0 |
| 1557 | Servitor Share | 1 | 83 | 100 000 000 |

### SpectralDancer  (classId 107, parent Bladedancer)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 330 000 |
| 329 | Health | 1 | 76 | 8 330 000 |
| 765 | Dance of Blade Storm | 1 | 76 | 0 |
| 986 | Deadly Strike | 25 | 76 | 219 000 000 |
| 366 | Dance of Shadows | 1 | 77 | 14 670 000 |
| 367 | Dance of Medusa | 1 | 77 | 14 670 000 |
| 365 | Dance of Siren | 1 | 78 | 21 000 000 |
| 428 | Inner Rhythm | 1 | 78 | 21 000 000 |
| 530 | Dance of Alignment | 1 | 79 | 60 000 000 |
| 455 | Symbol of Noise | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 913 | Deflect Magic | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 915 | Dance of Berserker | 1 | 83 | 0 |

### SpectralMaster  (classId 111, parent PhantomSummoner)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 934 | Sigil Mastery | 1 | 76 | 6 250 000 |
| 1558 | Dimension Spiral | 24 | 76 | 173 250 000 |
| 331 | Skill Mastery | 1 | 77 | 11 000 000 |
| 1348 | Assassin Servitor | 1 | 77 | 11 000 000 |
| 1351 | Mage Bane | 1 | 77 | 11 000 000 |
| 338 | Arcane Agility | 1 | 78 | 16 000 000 |
| 435 | Summon Lore | 1 | 78 | 16 000 000 |
| 1349 | Final Servitor | 1 | 78 | 16 000 000 |
| 1408 | Summon Spectral Lord | 1 | 79 | 60 000 000 |
| 783 | Summon Smart Cubic | 1 | 80 | 150 000 000 |
| 1424 | Anti-Summoning Field | 1 | 80 | 150 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1496 | Servitor Barrier | 1 | 81 | 0 |
| 1497 | Excessive Loyalty | 1 | 81 | 0 |
| 1498 | Mutual Response | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 930 | Spirit of the Demon | 1 | 83 | 0 |
| 1557 | Servitor Share | 1 | 83 | 100 000 000 |

### StormScreamer  (classId 110, parent Spellhowler)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 6 250 000 |
| 329 | Health | 1 | 76 | 6 250 000 |
| 925 | Sigil Mastery | 1 | 76 | 6 250 000 |
| 1343 | Dark Vortex | 1 | 76 | 6 250 000 |
| 331 | Skill Mastery | 1 | 77 | 13 000 000 |
| 1341 | Wind Vortex | 1 | 77 | 13 000 000 |
| 337 | Arcane Power | 1 | 78 | 21 340 000 |
| 433 | Arcane Roar | 1 | 78 | 21 340 000 |
| 1338 | Arcane Chaos | 1 | 78 | 21 340 000 |
| 1456 | Wind Vortex Slug | 1 | 79 | 60 000 000 |
| 1457 | Empowering Echo | 1 | 79 | 60 000 000 |
| 1458 | Throne of Wind | 1 | 79 | 60 000 000 |
| 1420 | Cyclone | 1 | 80 | 150 000 000 |
| 945 | Magician Will | 1 | 81 | 0 |
| 1468 | Star Fall | 1 | 81 | 0 |
| 1532 | Enlightement | 1 | 81 | 0 |
| 1554 | Aura Blast | 1 | 81 | 80 000 000 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 1555 | Aura Cannon | 1 | 82 | 90 000 000 |
| 1494 | Hurricane Armor | 1 | 83 | 0 |
| 1556 | Arcane Shield | 1 | 83 | 100 000 000 |

### Swordmuse  (classId 100, parent Swordsinger)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 8 330 000 |
| 329 | Health | 1 | 76 | 8 330 000 |
| 764 | Song of Wind Storm | 1 | 76 | 0 |
| 986 | Deadly Strike | 25 | 76 | 219 000 000 |
| 349 | Song of Renewal | 1 | 77 | 14 670 000 |
| 363 | Song of Meditation | 1 | 77 | 14 670 000 |
| 364 | Song of Champion | 1 | 78 | 21 000 000 |
| 428 | Inner Rhythm | 1 | 78 | 21 000 000 |
| 437 | Song of Silence | 1 | 79 | 60 000 000 |
| 529 | Song of Elemental | 1 | 79 | 60 000 000 |
| 455 | Symbol of Noise | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 913 | Deflect Magic | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 914 | Song of Purification | 1 | 83 | 0 |

### Titan  (classId 113, parent Destroyer)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 10 000 000 |
| 329 | Health | 1 | 76 | 10 000 000 |
| 335 | Fortitude | 1 | 76 | 10 000 000 |
| 330 | Skill Mastery | 1 | 77 | 13 000 000 |
| 362 | Armor Crush | 1 | 77 | 13 000 000 |
| 339 | Parry Stance | 1 | 78 | 16 000 000 |
| 347 | Earthquake | 1 | 78 | 16 000 000 |
| 430 | Master of Combat | 1 | 78 | 16 000 000 |
| 440 | Braveheart | 1 | 78 | 16 000 000 |
| 536 | Over the Body | 1 | 79 | 60 000 000 |
| 456 | Symbol of Resistance | 1 | 80 | 150 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 917 | Final Secret | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 777 | Demolition Impact | 1 | 83 | 0 |
| 995 | Rush Impact | 1 | 83 | 150 000 000 |

### Trickster  (classId 134, parent Arbalester)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 12 500 000 |
| 329 | Health | 1 | 76 | 12 500 000 |
| 330 | Skill Mastery | 1 | 77 | 16 000 000 |
| 334 | Focus Skill Mastery | 1 | 78 | 22 000 000 |
| 792 | Betrayal Mark | 1 | 78 | 22 000 000 |
| 939 | Soul Rage | 1 | 78 | 22 000 000 |
| 1470 | Prahnah | 1 | 78 | 16 000 000 |
| 538 | Final Form | 1 | 79 | 60 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 987 | Multiple Shot | 1 | 82 | 90 000 000 |
| 790 | Wild Shot | 1 | 83 | 0 |
| 990 | Death Shot | 1 | 83 | 100 000 000 |

### WindRider  (classId 101, parent PlainsWalker)

| Id | Skill | Max Lvl | Learned At | SP Total |
|---:|-------|--------:|-----------:|---------:|
| 328 | Wisdom | 1 | 76 | 12 500 000 |
| 344 | Lethal Blow | 1 | 76 | 12 500 000 |
| 330 | Skill Mastery | 1 | 77 | 14 670 000 |
| 358 | Bluff | 1 | 77 | 14 670 000 |
| 334 | Focus Skill Mastery | 1 | 78 | 16 000 000 |
| 355 | Focus Death | 1 | 78 | 16 000 000 |
| 356 | Focus Chance | 1 | 78 | 16 000 000 |
| 432 | Assassination | 1 | 78 | 16 000 000 |
| 446 | Dodge | 1 | 79 | 60 000 000 |
| 531 | Critical Wound | 1 | 79 | 60 000 000 |
| 460 | Symbol of the Assassin | 1 | 80 | 150 000 000 |
| 991 | Throwing Dagger | 1 | 80 | 70 000 000 |
| 758 | Fighters Will | 1 | 81 | 0 |
| 759 | Archers Will | 1 | 81 | 0 |
| 766 | Sixth Sense | 1 | 81 | 0 |
| 767 | Expose Weak Point | 1 | 81 | 0 |
| 922 | Hide | 1 | 81 | 0 |
| 923 | Dual Dagger Mastery | 1 | 81 | 0 |
| 755 | Protection of Rune | 1 | 82 | 0 |
| 756 | Protection of Elemental | 1 | 82 | 0 |
| 757 | Protection of Alignment | 1 | 82 | 0 |
| 769 | Wind Riding | 1 | 83 | 0 |
| 928 | Dual Blow | 1 | 83 | 100 000 000 |

