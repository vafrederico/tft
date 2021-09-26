from .item import Item
from tft.stats import Stats

class GiantSlayer(Item):
    stats = Stats(ad=10, aspd=0.1)
    
    def on_damage_multiplier(self, origin, target):
        return 1.8 if target.base_stats.hp[target.level] >= 1600 else 1.2
