from .trait import Trait
from tft.stats import Stats


class Legionnaire(Trait):
    stat_by_level = [0, 0.0, 0.25, 0.25, 0.75, 0.75, 1.35, 1.35, 2.50, 2.50]

    def __init__(self, num_champs: int) -> None:
        super().__init__()

        tier = min(num_champs, len(self.stat_by_level) - 1)
        self.stats = Stats(aspd=self.stat_by_level[tier])