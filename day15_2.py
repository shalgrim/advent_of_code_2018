from day15_1 import parse_cave_input, run_cave_game

if __name__ == '__main__':
    cave = parse_cave_input('data/input15.txt')
    outcome = -1
    elf_power = 3
    while outcome == -1:
        elf_power += 1
        for elf in cave.elves:
            elf.power = elf_power
        print(f'running with elf power: {elf_power}')
        outcome = run_cave_game(cave, abort_on_elf_death=True)

    print(f'No elves died with power {elf_power} for an outcome of {outcome}')


