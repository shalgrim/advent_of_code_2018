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
    string_scores = '37'
    elf_locations = [0, 1]
    last_power = 0

    while string_to_find not in string_scores:
        if floor(log10(len(scores))) > last_power:
            logger.info(f'len(scores): {len(scores)}')
            last_power = floor(log10(len(scores)))
        elf_scores = [scores[i] for i in elf_locations]
        new_string_score = str(sum(elf_scores))
        string_scores += new_string_score
        scores += [int(c) for c in new_string_score]

        elf_moves = [1 + score for score in elf_scores]
        elf_locations = [
            (location + move) % len(scores)
            for location, move in zip(elf_locations, elf_moves)
        ]

    score_index = string_scores.index(string_to_find)
    return score_index


if __name__ == '__main__':
    print(score_elves_backwards('793061'))
