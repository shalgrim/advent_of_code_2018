import sys


if __name__ == '__main__':
    with open('data/input02_1.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    for i, first_line in enumerate(lines):
        first_line_rep = {(x, c) for x, c in enumerate(first_line)}
        first_line_len = len(first_line_rep)

        for j, second_line in enumerate(lines[i+1:]):
            second_line_rep = {(y, d) for y, d in enumerate(second_line)}

            if len(first_line_rep.intersection(second_line_rep)) == first_line_len - 1:
                print(i, j, i + j + 1, first_line, second_line)
                sys.exit()
