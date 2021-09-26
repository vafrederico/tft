from __future__ import annotations

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion


class Board:
    champions: List[BaseChampion] = []

    def reset(self):
        self.champions = []
