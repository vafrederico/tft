from dataclasses import dataclass
from logging import DEBUG, INFO, Logger, getLogger
from random import random
from re import L
from tft.logging import CustomLambdaFilter
from time import time
from typing import ClassVar, List

from tft.game.constant import GAME_LOOP
from tft.items.infinity_edge import InfinityEdge
from tft.items.item import Item
from tft.stats import BaseChampStats
from tft.traits.trait import Trait

LEVEL = None


class BaseChampion:
    base_stats: BaseChampStats
    current_hp: int
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

    def __init__(self, level: int, team: int) -> None:
        self.level = level - 1
        self.current_hp = self.base_stats.hp[self.level]
        self.team = team
        self.__class__.count += 1
        self.index = self.__class__.count
        self.log = getLogger(
            f'{__name__}_{self.__class__.__name__:8s}_{self.index}')
        if LEVEL:
            self.log.setLevel(LEVEL)
        self.log.addFilter(CustomLambdaFilter(fn=self.__str__))

    def __str__(self) -> str:
        return f'{self.__class__.__name__:8s} ({self.index:02d}) (HP: {self.current_hp:5.0f}, Mana: {self.current_mana:3d}/{self.base_stats.mana:3d})'

    @property
    def ad(self) -> int:
        from_items = sum(i.stats.ad for i in self.items)
        from_base = self.base_stats.ad[self.level]
        from_traits = sum(i.stats.ad for i in self.traits)
        f = from_base + from_items + from_traits
        self.log.debug('AD = %d (%d I, %d B, %d T)', f, from_items, from_base,
                       from_traits)
        return f

    @property
    def ap(self) -> float:
        from_items = sum(i.stats.ap for i in self.items)
        from_traits = sum(i.stats.ap for i in self.traits)
        f = 1 + (from_items + from_traits) / 100
        self.log.debug('AP = %.2f (%d I, %d T)', f, from_items, from_traits)
        return f

    @property
    def armor(self) -> int:
        from_items = sum(i.stats.armor for i in self.items)
        from_base = self.base_stats.armor
        from_traits = sum(i.stats.armor for i in self.traits)
        f = from_base + from_items + from_traits
        self.log.debug('armor = %.2f (%.2f I, %.2f B, %.2f T)', f, from_items,
                       from_base, from_traits)
        return f

    @property
    def damage_reduction_flat(self) -> int:
        f = self.base_stats.damage_reduction_flat + sum(
            i.stats.damage_reduction_flat
            for i in self.items) + sum(i.stats.damage_reduction_flat
                                       for i in self.traits)
        return f

    @property
    def crit_chance_stat(self) -> float:
        from_items = sum(i.stats.crit_chance for i in self.items)
        from_base = self.base_stats.crit_chance
        from_traits = sum(i.stats.crit_chance for i in self.traits)
        f = from_base + from_items + from_traits
        self.log.debug('crit_chance_stat = %.2f (%.2f I, %.2f B, %.2f T)', f,
                       from_items, from_base, from_traits)
        return f

    @property
    def crit_chance(self) -> float:
        for i in self.items:
            if isinstance(i, InfinityEdge):
                return 1.0

        return self.crit_chance_stat

    @property
    def crit_dmg(self) -> float:
        from_items = sum(i.stats.crit_dmg for i in self.items)
        from_base = self.base_stats.crit_dmg
        from_traits = sum(i.stats.crit_dmg for i in self.traits)
        from_crit_chance = 0
        for i in self.items:
            if isinstance(i, InfinityEdge):
                from_crit_chance += self.crit_chance_stat - self.base_stats.crit_chance
                break

        f = from_base + from_items + from_traits + from_crit_chance

        self.log.debug('crit_dmg = %.2f (%.2f I, %.2f B, %.2f T, %.2f IE)', f,
                       from_items, from_base, from_traits, from_crit_chance)
        return f

    @property
    def aspd(self) -> float:
        from_items = sum(i.stats.aspd for i in self.items)
        from_base = self.base_stats.aspd
        from_traits = sum(i.stats.aspd for i in self.traits)
        f = from_base * (1 + from_items + from_traits)
        # self.log.debug('%s: ASPD = %.2f (%.2f I, %.2f B, %.2f T)', self, f, from_items,
        #          from_base, from_traits)
        return f

    def do_attack(self) -> None:
        self.do_damage(self.target, self.ad, True, True)

    def attack(self) -> None:
        if self.last_attack_ts + 1 / self.aspd <= GAME_LOOP.game_time:
            self.log.info('attacking %s', self.target)
            self.do_attack()
            self.last_attack_ts = GAME_LOOP.game_time
            self.current_mana += 10

    def ult(self) -> None:
        self.log.info('Ult')
        self.current_mana = 0
        self.do_ult()

    def do_ult(self) -> None:
        pass

    def do_damage(self, target: 'BaseChampion', amount: float, can_crit: bool,
                  is_attack: bool) -> None:
        dmg = amount
        target_resist = target.armor
        resist_ignore = self.base_stats.armor_ignore
        shredded_flat = 0
        shredded_pct = 0
        dmg_multi = 0

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
        final_dmg = dmg * resist_reduction

        target.take_dmg(self, final_dmg, pre_mitigation, did_crit)
        if is_attack:
            for item in self.items:
                item.on_attack(target, did_crit)

    def take_dmg(self, origin: 'BaseChampion', amount: int, pre_mitigation: int,
                 did_crit: bool) -> None:
        red_flat = self.damage_reduction_flat
        self.log.info('Took %d dmg from %s (pre: %d, flat: %d)', amount - red_flat,
                      origin, pre_mitigation, red_flat)
        self.current_hp -= amount - red_flat
        self.log.debug('HP = %d', self.current_hp)
        for item in origin.items:
            item.on_hit(origin, did_crit)

        if self.current_hp <= 0:
            self.alive = False
            self.log.info('died')
            for item in origin.items:
                item.on_killed_champion(self)
