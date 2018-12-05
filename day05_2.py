import math
import logging
import sys
from logging import StreamHandler
from day05_1 import reduce

logger = logging.getLogger('advent_of_code.2018.day05_2')
logging.basicConfig(filename='day05_2.log',
                    level=logging.INFO,
                    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger.addHandler(StreamHandler(sys.stdout))


if __name__ == '__main__':
    most_problematic = None
    shortest_len = math.inf

    with open('data/input05.txt') as f:
        text = f.read().strip()

    for i in range(65, 91):
        logger.info(f'stripping {chr(i)}/{chr(i+32)}')
        replaced = text.replace(chr(i), '')
        replaced = replaced.replace(chr(i + 32), '')
        logger.info(f'len(replaced): {len(replaced)}')
        reduced = reduce(replaced)

        if len(reduced) < shortest_len:
            shortest_len = len(reduced)
            most_problematic = i
            logger.info(f'current most problematic: {chr(i)}; gives length of {shortest_len}')
