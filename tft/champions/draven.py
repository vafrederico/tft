from os import stat
from tft.game.constant import GAME_LOOP
from time import time
from tft.stats import BaseChampStats
from tft.champions.champion import BaseChampion


class Draven(BaseChampion):
    AXE_RETURN_SECONDS = 1
    base_stats = BaseChampStats([700, 1260, 2268], [80, 144, 259],
                                armor=30,
                                armor_ignore=0.5,
                                mr=30,
                                aspd=0.8)
    axes = []

    def ult(self, target: 'BaseChampion') -> None:
        self.axes.append(time())

    def axe(self, target: 'BaseChampion') -> None:
        self.do_damage(target, 1.4 * self.ad + [125, 200, 700][self.level - 1],
                       True)

    def do_attack(self, target: 'BaseChampion') -> None:
        if len(self.axes) > 0 and self.axes[0] + self.AXE_RETURN_SECONDS < GAME_LOOP.game_time:
            self.axe()
        else:
            super().do_attack(target)
