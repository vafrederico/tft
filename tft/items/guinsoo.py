from __future__ import annotations
from .item import Item
from tft.stats import Stats

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion

from logging import getLogger

log = getLogger(__name__)


class Guinsoo(Item):
    stacks = 4
    base_aspd = 0.1
    stats = Stats(aspd=stacks * 0.06 + base_aspd, ap=10)

    def on_attack(self, target: BaseChampion, crit: BaseChampion) -> None:
        self.stacks += 1
        self.stats.aspd = self.stacks * 0.06 + self.base_aspd
        log.debug('+1 stack, total stacks = %d, aspd = %d', self.stacks,
                  self.stats.aspd)
        return super().on_attack(target, crit)