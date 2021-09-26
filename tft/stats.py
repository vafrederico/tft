from dataclasses import dataclass
from typing import List

@dataclass
class Stats:
    armor: int = 0
    mr: int = 0
    ad: int = 0
    crit_chance: float = 0
    crit_dmg: float = 0
    armor_shred_flat: int = 0
    armor_shred_pct: float = 0
    armor_ignore: float = 0
    extra_hp: int = 0
    damage_reduction_pct: float = 0
    damage_reduction_flat: int = 0
    aspd: float = 0.0

@dataclass
class BaseChampStats:
    hp: List[int]
    ad: List[int]
    armor: int = 0
    mr: int = 0
    crit_chance: float = 0.25
    crit_dmg: float = 0.3
    armor_shred_flat: int = 0
    armor_shred_pct: float = 0
    armor_ignore: float = 0
    damage_reduction_pct: float = 0
    damage_reduction_flat: int = 0
    aspd: float = 0.0
    level: int = 0
    mana: int = 0
