from tft.stats import Stats
from .debuff import Debuff

class ArmorShredPct(Debuff):
    def __init__(self) -> None:
        super().__init__()
        self.stats.armor_shred_flat=30