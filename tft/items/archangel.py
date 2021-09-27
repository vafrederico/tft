from __future__ import annotations

from math import floor
from typing import TYPE_CHECKING

from tft.items.stacking_item import StackingItem
from tft.stats import Stats

if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion


class Archangel(StackingItem):
    _base_ap = 10
    _base_mana = 10

    def initial_stacks() -> int:
        return 0

    def calculate_stats(self) -> None:
        return Stats(ap=self.stacks + self._base_ap)

    def on_ult(self, origin: BaseChampion) -> None:
        self.stack(floor(origin.base_stats.mana * 0.4))
