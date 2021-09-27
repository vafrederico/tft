from __future__ import annotations

import abc
from logging import getLogger

from tft.stats import Stats

from .item import Item

log = getLogger(__name__)


class StackingItem(Item, metaclass=abc.ABCMeta):
    stacks: int
    stats: Stats

    def __init__(self) -> None:
        super().__init__()
        self.stacks = self.initial_stacks
        self.stats = self.calculate_stats()

    def stack(self, stacks=1) -> None:
        self.stacks += stacks
        self.stats = self.calculate_stats()
        log.debug('+1 stack, total stacks = %d, stats = %s', self.stacks,
                  self.stats)

    @property
    @abc.abstractmethod
    def initial_stacks() -> int:
        pass

    @abc.abstractmethod
    def calculate_stats(self) -> None:
        pass
