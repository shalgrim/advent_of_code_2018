from day11_1 import calc_all_powers, find_best_subgrid

# SERIAL_NUMBER = 18
# SERIAL_NUMBER = 42
SERIAL_NUMBER = 7672


def main():
    all_powers = calc_all_powers(300, 300, SERIAL_NUMBER)
    high_val = 0
    best_coord = None
    best_subgrid_size = None

    for subgrid_size in range(1, 301):
        if subgrid_size % 20 == 0:
            print(f'subgrid_size: {subgrid_size}')
        coord, val = find_best_subgrid(all_powers, subgrid_size, subgrid_size)
        if val > high_val:
            high_val = val
            best_coord = coord
            best_subgrid_size = subgrid_size

            print(f'best_coord: {best_coord}')
            print(f'best_subgrid_size: {best_subgrid_size}')
            print(f'high_val: {high_val}')


if __name__ == '__main__':
    main()
