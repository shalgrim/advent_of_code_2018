import logging
import sys
from logging import StreamHandler

logger = logging.getLogger('avent_of_code.2018.day17_1')
logging.basicConfig(filename='day17_1.log',
                    level=logging.INFO,
                    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger.addHandler(StreamHandler(sys.stdout))


def calc_wettable_squares_from_file(filename):
    answer = 0
    return answer


if __name__ == '__main__':
    print(calc_wettable_squares_from_file('data/input17.txt'))
