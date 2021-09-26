import logging
from logging import StreamHandler
from tft.items.deathblade import Deathblade
from tft.game.constant import BOARD, GAME_LOOP
from tft.game.game_loop import GameLoop
from tft.game.board import Board
from tft.traits.knight import Knight
from tft.stats import BaseChampStats

from tft.champions.draven import Draven
from tft.champions.dummy import Dummy
from tft.items.giant_slayer import GiantSlayer
from tft.items.infinity_edge import InfinityEdge
from tft.traits.forgotten import Forgotten
from statistics import mean

# from logging.handlers import RotatingFileHandler
FORMAT = (
    "%(asctime)s [%(threadName)10s][%(name)30s][%(funcName)20s][%(levelname)8s] %(message)s"
)
logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT,
    handlers=(
        # RotatingFileHandler('assistant.log',
        #                     maxBytes=500000,
        #                     backupCount=4),
        StreamHandler(), ))

print(
    BaseChampStats([700, 1260, 2268], [80, 144, 259],
                   armor=30,
                   mr=30,
                   aspd=0.8))

times = []

def iteration():
    draven_ie = Draven(2, 0)
    draven_ie.items = [InfinityEdge(), Deathblade()]
    draven_ie.traits = [Forgotten(2)]

    draven_gs = Draven(2, 0)
    draven_gs.items = [GiantSlayer(), Deathblade()]
    draven_gs.traits = [Forgotten(2)]

    dummy_1 = Dummy(1, 1)
    dummy_1.traits = [Knight(4)]
    dummy_2 = Dummy(1, 1)
    dummy_2.traits = [Knight(4)]

    # draven_ie.ult(dummy_1)
    # draven_ie.attack(dummy_1)
    # draven_ie.ult(dummy_1)
    # draven_ie.attack(dummy_1)
    # print(dummy_1)

    # draven_gs.ult(dummy_2)
    # draven_gs.attack(dummy_2)
    # draven_gs.ult(dummy_2)
    # draven_gs.attack(dummy_2)
    # print(dummy_2)


    # print(draven_ie.base_stats)

    draven = draven_gs
    BOARD.champions.append(draven)
    BOARD.champions.append(dummy_1)
    BOARD.champions.append(dummy_2)

    GAME_LOOP.start()

for i in range(100):
    try: 
        iteration()
    except:
        times.append(GAME_LOOP.game_time)
    BOARD.reset()
    GAME_LOOP.reset()

print(times)
print(mean(times))