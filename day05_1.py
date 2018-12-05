import logging
import sys
from copy import copy
from logging import StreamHandler

logger = logging.getLogger('advent_of_code.2018.day05_1')
logging.basicConfig(
    filename='day05_1.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


def reduce(text):
    reduced = copy(text)
    done = False
    while not done:
        for i, char in enumerate(reduced[:-1]):
            if abs(ord(char) - ord(reduced[i + 1])) == 32:
                try:
                    reduced = reduced[:i] + reduced[i + 2 :]
                except IndexError:
                    done = True
                    reduced = reduced[:i]
                finally:
                    break
        else:
            done = True

    return reduced


if __name__ == '__main__':
    with open('data/input05.txt') as f:
        text = f.read().strip()

    logger.info(f'input length: {len(text)}')
    reduced = reduce(text)
    logger.info(f'output length: {len(reduced)}')
