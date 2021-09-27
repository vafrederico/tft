from __future__ import annotations

from typing import TYPE_CHECKING

from tft.items.stacking_item import StackingItem
from tft.stats import Stats

if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion

from logging import getLogger

log = getLogger(__name__)


class Deathblade(StackingItem):
    _base_ad = 20

    def initial_stacks() -> int:
        return 0

    def calculate_stats(self) -> None:
        return Stats(ad=self.stacks * 10 + Deathblade._base_ad)

    def on_killed_champion(self, target: BaseChampion) -> None:
        self.stack()
