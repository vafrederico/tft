from dataclasses import dataclass
from tft.game.constant import GAME_LOOP
from time import time
from tft.items.infinity_edge import InfinityEdge
from typing import List, final
from tft.stats import BaseChampStats
from tft.items.item import Item
from tft.traits.trait import Trait
from random import random
from logging import getLogger

log = getLogger(__name__)


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


    def __init__(self, level: int, team: int) -> None:
        self.level = level - 1
        self.current_hp = self.base_stats.hp[self.level]
        self.team = team

    def __str__(self) -> str:
        return f'{self.__class__.__name__} ({self.current_hp})'

    @property
    def ad(self) -> int:
        from_items = sum(i.stats.ad for i in self.items)
        from_base = self.base_stats.ad[self.level]
        from_traits = sum(i.stats.ad for i in self.traits)
        f = from_base + from_items + from_traits
        log.debug('%s: AD = %d (%d I, %d B, %d T)', self, f, from_items, from_base, from_traits)
        return f

    @property
    def armor(self) -> int:
        f = self.base_stats.armor + sum(
            i.stats.armor for i in self.items) + sum(i.stats.armor
                                                     for i in self.traits)
        log.debug('%s: armor = %d', self, f)
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
        f = self.base_stats.crit_chance + sum(i.stats.crit_chance
                                              for i in self.items)
        return f

    @property
    def crit_chance(self) -> float:
        for i in self.items:
            if isinstance(i, InfinityEdge):
                return 1.0

        return self.crit_chance_stat

    @property
    def crit_dmg(self) -> float:
        f = self.base_stats.crit_dmg + sum(i.stats.crit_dmg
                                           for i in self.items)
        log.debug('%s: crit_dmg_base = %f', self, f)

        for i in self.items:
            if isinstance(i, InfinityEdge):
                f += self.crit_chance_stat - self.base_stats.crit_chance
                break
        return f

    @property
    def aspd(self) -> float:
        return self.base_stats.aspd

    def do_attack(self, target: 'BaseChampion') -> None:
        self.do_damage(target, self.ad, True)

    def attack(self, target: 'BaseChampion') -> None:
        if self.last_attack_ts + 1/self.aspd <= GAME_LOOP.game_time:
            self.last_attack_ts = GAME_LOOP.game_time
            log.debug('%s attacking %s', self, target)
            self.do_attack(target)

    def ult(self, target: 'BaseChampion') -> None:
        self.current_mana = 0

    def do_damage(self, target: 'BaseChampion', amount: float,
                  can_crit: bool) -> None:
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
            log.debug('%s: %.2f crit chance', self, crit_chance)
            crit_dmg = self.crit_dmg
            log.debug('%s: %.2f crit dmg', self, crit_dmg)

            roll = random()
            log.debug('crit roll: %f', roll)
            did_crit = roll <= crit_chance
            if did_crit:
                log.info('Critted')
                dmg *= 1 + crit_dmg

        final_resist = target_resist * (1 - shredded_pct) * (
            1 - resist_ignore) - shredded_flat
        resist_reduction = 100 / (100 + final_resist)
        log.info('final_resist: %.2f, reduction: %.2f', final_resist,
                 resist_reduction)

        final_dmg = dmg * resist_reduction * dmg_multi

        target.take_dmg(self, final_dmg, did_crit)
        for item in self.items:
            item.on_attack(target, did_crit)

    def take_dmg(self, origin: 'BaseChampion', amount: int, did_crit: bool) -> None:
        red_flat = self.damage_reduction_flat
        log.info('%s: Reduced damage by %d flat', self, red_flat)
        log.info('%s: Took %d dmg from %s (original: %d)', self,
                 amount - red_flat, origin, amount)
        self.current_hp -= amount - red_flat
        log.info('%s: HP = %d', self, self.current_hp)
        for item in origin.items:
            item.on_hit(origin, did_crit)

        if self.current_hp <= 0:
            self.alive = False
            log.info('%s died', self)
            for item in origin.items:
                item.on_killed_champion(self)