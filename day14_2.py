import logging
import sys
from logging import StreamHandler
from math import floor, log10

logger = logging.getLogger('advent_of_code.2018.day14_2')
logging.basicConfig(filename='day14_2.log',
                    level=logging.INFO,
                    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger.addHandler(StreamHandler(sys.stdout))


def score_elves_backwards(string_to_find):
    scores = [3, 7]
    scores_to_find = [int(c) for c in string_to_find]
    lookback = len(scores_to_find)
    elf_locations = [0, 1]
    last_power = 0

    while scores_to_find != scores[-lookback:] and scores_to_find != scores[-lookback-1:-1]:
        # print(scores)
        if floor(log10(len(scores))) > last_power:
            logger.info(f'len(scores): {len(scores)}')
            last_power = floor(log10(len(scores)))
        elf_scores = [scores[i] for i in elf_locations]
        scores += [int(c) for c in str(sum(elf_scores))]

        elf_moves = [1 + score for score in elf_scores]
        elf_locations = [
            (location + move) % len(scores)
            for location, move in zip(elf_locations, elf_moves)
        ]

    # print(scores)
    # print(scores_to_find)
    if scores_to_find == scores[-lookback:]:
        score_index = len(scores) - lookback
    else:
        score_index = len(scores) - lookback - 1
    # print(f'score_index: {score_index}')
    return score_index


if __name__ == '__main__':
    print(score_elves_backwards('793061'))
