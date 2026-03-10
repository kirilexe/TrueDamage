# TrueDamage

A Python based build damage calculator for League of Legends that models champion abilities, item interactions, and full combo damage - with the goal of creating a script that's as close as possible to real in game scenarios and damage, to find the most optimal build for a character.

## What it does

TrueDamage lets you simulate how much damage a champion deals across a full ability combo at any level, with any items. Instead of jumping into a practice tool and manually testing every build variation, you define the setup in code and get the numbers instantly.
Currently the project is WIP and it's at the stage of a Minimum Viable Product. 

The long term goal is to have a good LoL build damage calculator, with a really easy to understand codebase that is fast to add upon.

## How it works

Champions inherit from a shared `BaseChampion` class that handles stats, item loading, and other types of damage. Subclasses take care of more complex champion mechanics.

```
TrueDamage/
├── data/
│   ├── champions.json   # Base stats + ability ratios per champion
│   └── items.json       # Item stats (AP, AD, on-hit effects, etc.)
├── src/
│   ├── models/
│   │   └── champion.py  # BaseChampion — shared stat/item logic
│   └── champions/
│       ├── katarina.py
│       └── irelia.py
└── main.py              # Usage examples
```

Stats and values are data driven, stored in a json file (not using an external API due to item "uniqueness" reasons)

## Example

```python
kat = Katarina(level=1)
kat.inventory.append(item_data["Nashors Tooth"])
kat.bonus_ap = 62

print(kat.get_qewr_damage(q_rank=3, e_rank=1, r_rank=3))
# Full Q + E + W + R combo damage with Nashor's
```

## Current champions

| Champion | Abilities modeled | Combos |
|----------|------------------|--------|
| Katarina | P, Q, E, R | Q-E-W-R |
| Irelia | P, Q, W, E, R | Standard, Ult |

Adding a new champion requires knowing its ability ratios and defining the combo order, as well as having the items and their mechanics added.

## Status

Unfinished but functional for the champions implemented. The core architecture is solid - item loading (from json), stat scaling, on-hit damage.
