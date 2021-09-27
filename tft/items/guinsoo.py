from __future__ import annotations

from typing import TYPE_CHECKING

from tft.items.stacking_item import StackingItem
from tft.stats import Stats

if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion

from logging import getLogger

log = getLogger(__name__)


class Guinsoo(StackingItem):
    _base_aspd = 0.1

    def initial_stacks() -> int:
        return 0

    def calculate_stats(self) -> None:
        return Stats(aspd=self.stacks * 0.06 + Guinsoo._base_aspd, ap=10)

    def on_attack(self, target: BaseChampion, crit: BaseChampion) -> None:
        self.stack()
