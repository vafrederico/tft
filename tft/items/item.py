from __future__ import annotations
from tft.stats import Stats

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion

class Item:
    duration: int
    stats: Stats

    def on_damage_multiplier(self, origin, target) -> None:
        return 1

    def on_killed_champion(self, target: BaseChampion) -> None:
        pass

    def on_ult(self) -> None:
        pass

    def on_attack(self, target: BaseChampion, crit: BaseChampion) -> None:
        pass

    def on_hit(self, target: BaseChampion, crit: BaseChampion) -> None:
        pass
