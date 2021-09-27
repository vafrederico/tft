from __future__ import annotations

import abc
from logging import Logger, getLogger
from typing import ClassVar

from tft.logging import CustomLambdaFilter
from tft.stats import Stats

from .item import Item

log = getLogger(__name__)


class StackingItem(Item, metaclass=abc.ABCMeta):
    stacks: int
    stats: Stats
    index: int
    count: ClassVar[int] = 0
    log: Logger = None

    def __init__(self) -> None:
        super().__init__()
        self.stacks = self.__class__.initial_stacks()
        self.stats = self.calculate_stats()
        self.__class__.count += 1
        self.index = self.__class__.count
        self.log = getLogger(
            f'{__name__}_{self.__class__.__name__:8s}_{self.index}')
        self.log.addFilter(CustomLambdaFilter(fn=self.__str__))

    def __str__(self) -> str:
        return f'{self.__class__.__name__:10s} ({self.index:02d}) (stacks: {self.stacks}, {self.stats})'

    def stack(self, stacks=1) -> None:
        self.stacks += stacks
        self.stats = self.calculate_stats()
        self.log.debug('+1 stack')

    @property
    @abc.abstractmethod
    def initial_stacks() -> int:
        pass

    @abc.abstractmethod
    def calculate_stats(self) -> None:
        pass
