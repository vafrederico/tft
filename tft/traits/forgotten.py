from .trait import Trait
from tft.stats import Stats

class Forgotten(Trait):
    stat_by_level = [0, 0,  30, 30, 60, 60, 105, 105, 300]
    def __init__(self, num_champs: int) -> None:
        super().__init__()
        
        tier = min(num_champs, len(self.stat_by_level) - 1)
        self.stats = Stats(ad=self.stat_by_level[tier])