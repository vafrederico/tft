from .trait import Trait
from tft.stats import Stats

class Ironclad(Trait):
    stat_by_level = [0, 0,  30, 70, 125]
    def __init__(self, num_champs: int) -> None:
        super().__init__()
        
        tier = min(num_champs, len(self.stat_by_level) - 1)
        self.stats = Stats(armor=self.stat_by_level[tier])