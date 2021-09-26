from .trait import Trait
from tft.stats import Stats

class Knight(Trait):
    stat_by_level = [0, 0,  20, 20, 40, 40, 70]
    def __init__(self, num_champs: int) -> None:
        super().__init__()
        
        tier = min(num_champs, len(self.stat_by_level) - 1)
        self.stats = Stats(damage_reduction_flat=self.stat_by_level[tier])