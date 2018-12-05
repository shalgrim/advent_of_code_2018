from day04_1 import build_elf_tracker


def main(lines):
    elf_tracker = build_elf_tracker(lines)
    most_slept_at = 0
    sleepiest_elf_minute = None
    for elf_id, counter in elf_tracker.items():
        sleepiest_minute, times_slept = sorted(
            counter.items(), key=lambda x: x[1], reverse=True
        )[0]
        if times_slept > most_slept_at:
            sleepiest_elf_minute = (elf_id, sleepiest_minute)
            most_slept_at = times_slept

    print(
        f'Elf #{sleepiest_elf_minute[0]} slept {most_slept_at} times at {sleepiest_elf_minute[1]}'
    )
    print(f'answer: {int(sleepiest_elf_minute[0]) * int(sleepiest_elf_minute[1])}')

    # 11911 is too low


if __name__ == '__main__':
    with open('data/input04.txt') as f:
        lines = f.readlines()

    main(sorted(lines))
