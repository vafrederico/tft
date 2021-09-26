from stats import Stats
from champions.champion import BaseChampion

class Debuff:
    duration: int
    stats: Stats

    def apply(self, champ: BaseChampion):
        pass

class ArmorShredPct(Debuff):
    def __init__(self, amount: float) -> None:
        super().__init__()
        self.stats.armor_shred_pct = amount

class ArmorShredFlat(Debuff):
    def __init__(self, amount: int) -> None:
        super().__init__()
        self.stats.armor_shred_flat = amount