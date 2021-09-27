import logging
from logging import StreamHandler
from tft.traits.legionnaire import Legionnaire

from tft.champions.draven import Draven
from tft.champions.dummy import Dummy
from tft.items.giant_slayer import GiantSlayer
from tft.items.infinity_edge import InfinityEdge
from tft.traits.forgotten import Forgotten
from statistics import mean

# from logging.handlers import RotatingFileHandler
FORMAT = (
    # "%(asctime)s [%(threadName)10s][%(name)30s][%(funcName)20s][%(levelname)8s] %(message)s"
    "%(game_time).2f [%(name)30s][%(funcName)20s][%(levelname)8s] %(message)s"
)

logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT,
    handlers=(
        # RotatingFileHandler('assistant.log',
        #                     maxBytes=500000,
        #                     backupCount=4),
        StreamHandler(), ),)
old_factory = logging.getLogRecordFactory()
def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.game_time = GAME_LOOP.game_time
    return record
logging.setLogRecordFactory(record_factory)

print(
    BaseChampStats([700, 1260, 2268], [80, 144, 259],
                   armor=30,
                   mr=30,
                   aspd=0.8))

times = []

def iteration():
    draven_ie = Draven(2, 0)
    draven_ie.items = [InfinityEdge(), Deathblade(), Guinsoo()]
    draven_ie.traits = [Forgotten(2), Legionnaire(4)]

    draven_gs = Draven(2, 0)
    draven_gs.items = [GiantSlayer(), Deathblade(), Guinsoo()]
    draven_gs.traits = [Forgotten(2), Legionnaire(4)]

    dummy_1 = Dummy(1, 1)
    dummy_1.traits = [Knight(4), Ironclad(3)]
    dummy_2 = Dummy(1, 1)
    dummy_2.traits = [Knight(4), Ironclad(3)]
    dummy_3 = Dummy(1, 1)
    dummy_3.traits = [Knight(4), Ironclad(3)]
    dummy_4 = Dummy(1, 1)
    dummy_4.traits = [Knight(4), Ironclad(3)]

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
    BOARD.champions.append(dummy_3)
    BOARD.champions.append(dummy_4)
    GAME_LOOP.tick_team = 1
    GAME_LOOP.start()

for i in range(1):
    try:
        iteration()
    except:
        times.append(GAME_LOOP.game_time)
    BOARD.reset()
    GAME_LOOP.reset()

print(times)
print('mean: {}'.format(mean(times)))
print('min: {}'.format(min(times)))
print('max: {}'.format(max(times)))
print('median: {}'.format(median(times)))
