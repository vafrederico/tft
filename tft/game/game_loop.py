from __future__ import annotations

from time import sleep, time
from logging import getLogger

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from tft.champions.champion import BaseChampion
    from tft.game.board import Board

log = getLogger(__name__)

TICK = 100
SEC_PER_TICK = 1 / TICK


class GameLoop:
    board: Board
    running: bool = False
    ticks: int = 0
    game_time: float = 0.0
    tick_team: Optional[int] = None

    def __init__(self, board: Board) -> None:
        self.board = board

    def reset(self) -> None:
        self.running = False
        self.ticks = 0
        self.game_time = 0.0
        self.tick_team = None

    def start(self) -> None:
        for c in self.board.champions:
            c.set_initial_stats()
        self.running = True
        self.loop()

    def find_next_target(self, origin: BaseChampion) -> BaseChampion:
        for c in self.board.champions:
            if c.alive and c.team != origin.team:
                return c
        self.running = False

    def loop(self) -> None:
        while self.running:
            self.tick()
        log.info('Ending at %d ticks (%.2f seconds)', self.ticks,
                 self.ticks * SEC_PER_TICK)

    def tick(self) -> None:
        for c in self.board.champions:
            if self.tick_team is not None and self.tick_team == c.team:
                continue
            if c.alive:
                if c.target is None or c.target.alive == False:
                    c.target = self.find_next_target(c)
                    log.debug('%s new target is %s', c, c.target)
                if c.target is None:
                    continue
                if c.base_stats.mana > 0 and c.current_mana >= c.base_stats.mana and not c.mana_locked:
                    c.ult()
                    continue
                need_move = False
                if need_move:
                    pass
                else:
                    c.attack()
        self.ticks += 1
        self.game_time += SEC_PER_TICK
