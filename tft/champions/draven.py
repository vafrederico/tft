from os import stat
from tft.game.constant import GAME_LOOP
from time import time
from tft.stats import BaseChampStats
from tft.champions.champion import BaseChampion
from logging import getLogger

log = getLogger(__name__)


class Draven(BaseChampion):
    AXE_RETURN_SECONDS = 1.5
    base_stats = BaseChampStats([700, 1260, 2268], [80, 144, 259],
                                armor=30,
                                armor_ignore=0.5,
                                mr=30,
                                aspd=0.8,
                                mana=40)
    axes = []

    def do_ult(self) -> None:
        self.axes.insert(0, 0)

    def axe(self) -> None:
        log.debug('%s: Axe', self)
        self.do_damage(self.target, 1.4 * self.ad + [125, 200, 700][self.level - 1],
                       True)

    def do_attack(self) -> None:
        if len(
                self.axes
        ) > 0 and self.axes[0] + self.AXE_RETURN_SECONDS < GAME_LOOP.game_time:
            self.axes.pop()
            self.axes.append(GAME_LOOP.game_time)
            self.axe()
        else:
            super().do_attack()
