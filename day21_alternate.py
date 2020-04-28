REG0 = 4_682_012
ONE_THEN_16_ZEROS = 65_536  # 2^16
EIGHT_ONES = 255  # 2^8 - 1
TWENTY_FOUR_ONES = 16_777_215  # 2^24 - 1
BIG_RANDO = 8_725_355
SMALL_RANDO = 65_899


def main():
    reg0 = REG0  # This never changes
    reg1 = 0
    reg2 = 0
    reg3 = 0
    reg4 = -1  # Don't really need this
    reg5 = 0

    while reg0 != reg1:  # I06 loop
        # I06 - addition except when the 2^16 bit is turned on in reg1 then it's the original number
        reg2 = reg1 | ONE_THEN_16_ZEROS  # I06 - addition except when the 2^16 bit is turned on in reg1 then it's
        reg1 = BIG_RANDO  # I07

        # do part of do-while loop
        reg5 = reg2 & EIGHT_ONES  # I08
        reg1 += reg5  # I09

        # Can these lines be concisified?
        reg1 = reg1 & TWENTY_FOUR_ONES  # I10
        reg1 *= SMALL_RANDO  # I11
        reg1 = reg1 & TWENTY_FOUR_ONES  # I12

        while EIGHT_ONES < reg2:  # I08 loop
            # invariant 256 <= reg2

            # I17 - I27
            reg5 = 0
            reg3 = 256

            # Count how many times reg3 has to go up by 512 before it's > reg2 (I think)
            while reg3 <= reg2:
                reg5 += 1
                reg3 = reg5 + 1
                reg3 *= 256  # so this is like reg3 going up by 512 each time until it's bigger than reg2?

            reg2 = reg5  # I26; and then set the number of times it had to increase to reg2

            # Back to that Do part but conciser
            # So something about the number of times we did that combined with where reg1 was
            # and putting that back in reg1
            reg1 = ((((reg2 & EIGHT_ONES) + reg1) & TWENTY_FOUR_ONES) * SMALL_RANDO) & TWENTY_FOUR_ONES

    return reg0, reg1, reg2, reg3, reg4, reg5


if __name__ == '__main__':
    print(main())
