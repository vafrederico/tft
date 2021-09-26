from os import stat

from tft.champions.champion import BaseChampion
from tft.stats import BaseChampStats


class Dummy(BaseChampion):
    base_stats = BaseChampStats([1000, 1800, 3240], [80, 144, 259],
                                armor=60,
                                mr=60,
                                aspd=0.8)
