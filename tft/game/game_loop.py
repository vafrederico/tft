from __future__ import annotations

from time import sleep, time
from logging import getLogger

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion
    from tft.game.board import Board

log = getLogger(__name__)


TICK = 60
SEC_PER_TICK = 1/60

class GameLoop:
    board: Board
    running: bool = False
    ticks: int = 0
    game_time: float = 0.0

    def __init__(self, board: Board) -> None:
        self.board = board
    
    def reset(self):
        self.running = False
        self.ticks = 0
        self.game_time = 0.0

    def start(self) -> None:
        self.running = True
        self.loop()

    def find_next_target(self, origin: BaseChampion) -> BaseChampion:
        for c in self.board.champions:
            if c.alive and c.team != origin.team:
                return c
        raise Exception('no more units')

    def loop(self) -> None:
        while self.running:
            try:
                self.tick()
            except Exception as e:
                log.fatal('Ending at %d ticks (%.2f seconds)', self.ticks, self.ticks * SEC_PER_TICK)
                log.exception(e)
                raise e
            # sleep(SEC_PER_TICK)

    def tick(self) -> None:
        for c in self.board.champions:
            if c.__class__.__name__ == 'Dummy':
                continue
            if c.alive:
                if c.target is None or c.target.alive == False:
                    c.target = self.find_next_target(c)
                    log.debug('%s new target is %s', c, c.target)
                if c.base_stats.mana > 0 and c.current_mana <= c.base_stats.mana:
                    c.ult()
                else:
                    c.attack(c.target)
        self.ticks += 1
        self.game_time += SEC_PER_TICK
