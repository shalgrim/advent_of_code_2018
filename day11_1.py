SERIAL_NUMBER = 7672
# SERIAL_NUMBER = 18
# SERIAL_NUMBER = 42
# SERIAL_NUMBER = 8


def keep_only_hundreds_digit(power_level):
    quotient = power_level // 100
    return quotient % 10


def calc_cell_power(x, y, serial_number=SERIAL_NUMBER):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    power_level = keep_only_hundreds_digit(power_level)
    power_level -= 5
    return power_level


def calc_all_powers(width, height):
    output = []
    for y in range(1, height + 1):
        output.append([calc_cell_power(x, y) for x in range(1, width + 1)])

    return output


def find_best_subgrid(all_powers, subgrid_width, subgrid_height):
    grid_height = len(all_powers)
    grid_width = len(all_powers[0])
    high_val = 0
    best_coord = None

    for y in range(grid_height - subgrid_height + 1):
        for x in range(grid_width - subgrid_width + 1):
            coord = (x + 1, y + 1)
            val = 0

            for suby in range(y, y + subgrid_height):
                val += sum(all_powers[suby][x : x + subgrid_width])
            if val > high_val:
                best_coord = coord
                high_val = val
    return best_coord, high_val


def main():
    all_powers = calc_all_powers(300, 300)
    answer = find_best_subgrid(all_powers, 3, 3)
    print(f'answer; {answer}')


if __name__ == '__main__':
    main()
