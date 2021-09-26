from .trait import Trait
from stats import Stats

class Ironclad(Trait):
    armor = [0, 0,  30, 70, 125]
    def __init__(self, num_champs: int) -> None:
        super().__init__()
        
        tier = min(num_champs, len(self.armor) - 1)
        self.stats = Stats(armor=self.armor[tier])