from dataclasses import dataclass
from logging import DEBUG, INFO, Logger, disable, getLogger
from random import random
from re import L
from tft.logging import CustomLambdaFilter
from time import time
from typing import Callable, ClassVar, List, Union

from tft.game.constant import GAME_LOOP
from tft.items.infinity_edge import InfinityEdge
from tft.items.item import Item
from tft.stats import BaseChampStats, Stats
from tft.traits.trait import Trait
from typing import TypeVar

LEVEL = None
T = TypeVar('T')


class BaseChampion:
    base_stats: BaseChampStats
    current_hp: int = 1
    alive: bool = True
    level: int
    items: List[Item] = []
    traits: List[Trait] = []
    target: 'BaseChampion' = None
    last_attack_ts: float = 0
    current_mana: int = 0
    team: int
    index: int
    count: ClassVar[int] = 0
    log: Logger = None
    mana_lock_ts: float = 0

    def __init__(self, level: int, team: int) -> None:
        self.level = level - 1
        self.team = team
        self.__class__.count += 1
        self.index = self.__class__.count
        self.log = getLogger(
            f'{__name__}_{self.__class__.__name__:8s}_{self.index}')
        if LEVEL:
            self.log.setLevel(LEVEL)
        self.log.addFilter(CustomLambdaFilter(fn=self.__str__))

    def set_initial_stats(self) -> None:
        self.current_hp = self.hp
        self.current_mana = self.get_specific_stat(lambda x: x.starting_mana,
                                                   'StartingMana')

    def __str__(self) -> str:
        return f'{self.__class__.__name__:10s} ({self.index:02d}) (HP: {self.current_hp:5.0f}, Mana: {self.current_mana:3d}/{self.base_stats.mana:3d}) '

    def get_specific_stat(self,
                          fn: Callable[[Union[BaseChampStats, Stats]],
                                       Union[int, float]],
                          caller_name: str,
                          level_scaling: bool = False,
                          disable_log: bool = False) -> Union[int, float]:
        from_items = sum(fn(i.stats) for i in self.items)
        from_base = fn(
            self.base_stats) * (1.8**self.level if level_scaling else 1)
        from_traits = sum(fn(i.stats) for i in self.traits)
        f = from_base + from_items + from_traits
        if not disable_log and self.log.getEffectiveLevel() <= DEBUG:
            if isinstance(f, float):
                self.log.debug('%s = %.2f (%.2f I, %.2f B, %.2f T)',
                               caller_name, f, from_items, from_base,
                               from_traits)
            else:
                self.log.debug('%s = %d (%d I, %d B, %d T)', caller_name, f,
                               from_items, from_base, from_traits)
        return f

    @property
    def hp(self) -> int:
        return self.get_specific_stat(lambda x: x.hp, 'HP', True)

    @property
    def ad(self) -> int:
        return self.get_specific_stat(lambda x: x.ad, 'AD', True)

    @property
    def ap(self) -> float:
        return self.get_specific_stat(lambda x: x.ap, 'AP', False) / 100

    @property
    def armor(self) -> int:
        return self.get_specific_stat(lambda x: x.armor, 'Armor')

    @property
    def damage_reduction_flat(self) -> int:
        return self.get_specific_stat(lambda x: x.damage_reduction_flat,
                                      'DmgRedFlat')

    @property
    def crit_chance_stat(self) -> float:
        return self.get_specific_stat(lambda x: x.crit_chance,
                                      'crit_chance_stat')

    @property
    def crit_chance(self) -> float:
        for i in self.items:
            if isinstance(i, InfinityEdge):
                return 1.0

        return self.crit_chance_stat

    @property
    def crit_dmg(self) -> float:
        f = self.get_specific_stat(lambda x: x.crit_dmg, 'crit_dmg')
        from_crit_chance = 0
        for i in self.items:
            if isinstance(i, InfinityEdge):
                from_crit_chance += self.crit_chance_stat - self.base_stats.crit_chance
                self.log.debug('crit_dmg from chance: %.2f', from_crit_chance)
                f += from_crit_chance
                break
        return f

    @property
    def aspd(self) -> float:
        f = self.get_specific_stat(lambda x: x.aspd, 'ASPD', False, True)
        return f

    def do_attack(self) -> None:
        self.do_damage(self.target, self.ad, True, True)

    def attack(self) -> None:
        if self.last_attack_ts + 1 / self.aspd <= GAME_LOOP.game_time:
            self.log.info('attacking %s', self.target)
            self.do_attack()
            self.last_attack_ts = GAME_LOOP.game_time
            self.gain_mana(10)

    def ult(self) -> None:
        self.log.info('Ult')
        self.current_mana = 0
        self.do_ult()
        for i in self.items:
            i.on_ult(self)
        self.mana_lock_ts = GAME_LOOP.game_time + self.base_stats.mana_lock_seconds

    def do_ult(self) -> None:
        pass

    @property
    def mana_locked(self) -> bool:
        return self.mana_lock_ts > GAME_LOOP.game_time

    def gain_mana(self, amount: int, skip_lock: bool = False) -> None:
        if skip_lock or not self.mana_locked:
            self.current_mana += amount

    def do_damage(self, target: 'BaseChampion', amount: float, can_crit: bool,
                  is_attack: bool) -> None:
        dmg = amount
        target_resist = target.armor
        resist_ignore = self.base_stats.armor_ignore
        shredded_flat = 0
        shredded_pct = 0
        dmg_multi = 1

        for i in self.items:
            shredded_flat += i.stats.armor_shred_flat
            shredded_pct += i.stats.armor_shred_pct
            dmg_multi += i.on_damage_multiplier(self, target)

        did_crit = False
        if can_crit:
            crit_chance = self.crit_chance
            crit_dmg = self.crit_dmg
            roll = random()
            did_crit = roll <= crit_chance
            if did_crit:
                self.log.debug('CRIT!')
                dmg *= 1 + crit_dmg

        final_resist = target_resist * (1 - shredded_pct) * (
            1 - resist_ignore) - shredded_flat
        resist_reduction = 100 / (100 + final_resist)
        self.log.debug('final_resist: %.2f, reduction: %.2f', final_resist,
                       resist_reduction)

        pre_mitigation = dmg * dmg_multi
        final_dmg = pre_mitigation * resist_reduction
        target.take_dmg(self, final_dmg, pre_mitigation, did_crit)
        if is_attack:
            for item in self.items:
                item.on_attack(target, did_crit)

    def take_dmg(self, origin: 'BaseChampion', amount: int,
                 pre_mitigation: int, did_crit: bool) -> None:
        red_flat = self.damage_reduction_flat
        dmg_taken = amount - red_flat
        self.log.info('Took %d dmg from %s (crit: %d, pre: %d, flat: %d)',
                      dmg_taken, origin, did_crit, pre_mitigation, red_flat)
        self.current_hp -= dmg_taken
        self.log.debug('HP = %d', self.current_hp)
        for item in origin.items:
            item.on_hit(origin, did_crit)

        if self.current_hp <= 0:
            self.alive = False
            self.log.info('died')
            for item in origin.items:
                item.on_killed_champion(self)
