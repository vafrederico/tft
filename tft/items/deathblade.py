from __future__ import annotations
from .item import Item
from tft.stats import Stats

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion

from logging import getLogger

log = getLogger(__name__)


class Deathblade(Item):
    stacks = 4
    base_ad = 20
    stats = Stats(ad=stacks * 10 + base_ad)

    def on_killed_champion(self, target: BaseChampion) -> None:
        self.stacks += 1
        self.stats.ad = self.stacks * 10 + self.base_ad
        log.debug('+1 stack, total stacks = %d, ad = %d', self.stacks, self.stats.ad)
        return super().on_killed_champion(target)
