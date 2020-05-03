import logging
import sys
from logging import StreamHandler

logger = logging.getLogger('advent_of_code_2018.day21_alternate')
logging.basicConfig(filename='day21_alternate.log',
                    level=logging.INFO,
                    format='%(levelname) -10s %(asctime)s %(module)s line %(lineno)d: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger.addHandler(StreamHandler(sys.stdout))

REG0 = 4_682_012
ONE_THEN_16_ZEROS = 65536  # 2^16
EIGHT_ONES = 255  # 2^8 - 1
TWENTY_FOUR_ONES = 16_777_215  # 2^24 - 1
BIG_RANDO = 8_725_355
SMALL_RANDO = 65899


def mod(x, y):
    return x & y - 1


def big_fat_one(r1, r2):
    return mod(
        mod(mod(r2, EIGHT_ONES + 1) + r1, TWENTY_FOUR_ONES + 1) * SMALL_RANDO,
        TWENTY_FOUR_ONES + 1,
    )


def main():
    reg0 = REG0  # This never changes after it's set
    reg1 = 0
    reg2 = 0
    reg3 = 0
    reg4 = -1  # IP...don't really need this
    reg5 = 0

    while reg0 != reg1:  # I06 loop
        logger.info(f'{(reg0, reg1, reg2, reg3, reg4, reg5)}')
        # I06 - addition except when the 2^16 bit is turned on in reg1 then it's the original number
        reg2 = (
            reg1 | ONE_THEN_16_ZEROS
        )
        logger.info(f'{(reg0, reg1, reg2, reg3, reg4, reg5)}')
        reg1 = BIG_RANDO  # I07
        logger.info(f'{(reg0, reg1, reg2, reg3, reg4, reg5)}')

        # do part of do-while loop
        reg1 = big_fat_one(reg1, reg2)
        logger.info(f'{(reg0, reg1, reg2, reg3, reg4, reg5)}')

        while EIGHT_ONES < reg2:  # I08 loop...i.e., while reg2 > 256
            # invariant 256 < reg2

            # I17 - I27
            reg5 = 0  # don't need this except for logging below
            reg3 = 256  # don't need this except for logging below
            reg2 = reg2 // 256
            logger.info(f'{(reg0, reg1, reg2, reg3, reg4, reg5)}')

            # something about the number of times we did that (big_fat_one?) combined with where reg1 was
            # and putting that back in reg1
            reg1 = big_fat_one(reg1, reg2)
            logger.info(f'{(reg0, reg1, reg2, reg3, reg4, reg5)}')

    return reg0, reg1, reg2, reg3, reg4, reg5


if __name__ == '__main__':
    print(main())
