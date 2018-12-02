def get_val_from_line(line):
    if line[0] == '+':
        return int(line[1:-1])

    return int(line[:-1])


if __name__ == '__main__':
    total = 0
    with open('data/input01_1.txt') as f:
        for line in f:
            total += get_val_from_line(line)
    print(f'total: {total}')