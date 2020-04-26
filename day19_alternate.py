PART1_REG3 = 888
PART2_REG3 = 10_551_241


def main():
    reg0 = 0
    reg1 = 1
    reg3 = PART1_REG3
    # reg3 = PART2_REG3
    reg4 = 1

    while reg4 <= reg3:
        reg1 = 1

        while reg3 >= reg1:
            reg5 = reg1 * reg4
            if reg3 == reg5:
                reg0 += reg4
            reg1 += 1

        reg4 += 1
        print(reg4)

    return reg0


if __name__ == '__main__':
    print(main())
