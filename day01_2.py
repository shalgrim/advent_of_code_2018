from day01_1 import get_val_from_line

if __name__ == '__main__':
    current_frequency = 0
    seen_frequencies = set()

    with open('data/input01_1.txt') as f:
        values = [get_val_from_line(line) for line in f.readlines()]

    dup_found = False

    while not dup_found:
        for value in values:
            if current_frequency in seen_frequencies:
                print('breaking')
                # print(f'seen_frequencies: {seen_frequencies}')
                dup_found = True
                break
            seen_frequencies.add(current_frequency)
            current_frequency += value
            # print(len(seen_frequencies))

    print(f'first frequency seen twice: {current_frequency}')
