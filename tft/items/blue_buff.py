from __future__ import annotations
from logging import getLogger
from os import stat
from typing import TYPE_CHECKING
from .item import Item
from tft.stats import Stats

if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion

log = getLogger(__name__)


class BlueBuff(Item):
    stats = Stats(starting_mana=30)

    def on_ult(self, origin: BaseChampion) -> None:
        origin.gain_mana(20)
        log.debug('%sgaining 20 mana', origin)