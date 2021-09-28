from os import stat

from tft.champions.champion import BaseChampion
from tft.stats import BaseChampStats


class Dummy(BaseChampion):
    base_stats = BaseChampStats(1599, 80, armor=60, mr=60, aspd=0.8)
