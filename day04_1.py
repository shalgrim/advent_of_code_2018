"""
NB: I verified that every guard is awake at the end of their shift:
for i, line in enumerate(lines):
    if i == 0:
        continue
    if 'begins shift' in line:
        if 'wakes up' not in lines[i-1] and 'begins shift' not in lines[i-1]:
            print(i)
            break

Data structure:
elf_tracker = {}  # keys = elf_id, values = dictionary; so this is defaultdict(Counter)
inner_dictionary = {} # keys = four-digit representation of minute, values = number of times asleep at that minute;
so this is Counter
"""
import re
from collections import Counter, defaultdict
from enum import Enum

START_LINE_REGEX = r'^\[(?P<year>\d{4})\-(?P<month>\d{2})\-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\] '
NEW_SHIFT_REGEX = r'Guard #(?P<elf_id>\d+) begins shift\n$'
STATE_CHANGE_REGEX = r'\D+\n$'

NEW_SHIFT_PATTERN = re.compile(START_LINE_REGEX + NEW_SHIFT_REGEX)
STATE_CHANGE_PATTERN = re.compile(START_LINE_REGEX + STATE_CHANGE_REGEX)


class State(Enum):
    AWAKE = 0
    ASLEEP = 1


def update_sleep_times(elf_tracker, elf_id, sleep_time, awake_time):

    if int(sleep_time) > 2259:  # assumption
        if int(awake_time) > int(sleep_time):
            for minute in range(int(sleep_time), int(awake_time)):
                elf_tracker[elf_id][minute] += 1
        else:
            for minute in range(int(sleep_time), 2400):
                elf_tracker[elf_id][minute] += 1
            for minute in range(int(awake_time)):
                elf_tracker[elf_id][minute] += 1
    else:
        for minute in range(int(sleep_time), int(awake_time)):
            elf_tracker[elf_id][minute] += 1


def calculate_total_minutes_by_elf(elf_tracker):
    total_minutes_by_elf = {}
    for elf_id, counter in elf_tracker.items():
        total_minutes_by_elf[elf_id] = sum(counter.values())

    return total_minutes_by_elf


def main(lines):
    elf_tracker = defaultdict(Counter)
    state = State.AWAKE
    for line in lines:
        match = NEW_SHIFT_PATTERN.match(line)

        if match:
            state = State.AWAKE  # assumption
            current_elf = match.group('elf_id')
        else:
            match = STATE_CHANGE_PATTERN.match(line)
            state_change_time = match.group('hour') + match.group('minute')

            if state == State.AWAKE:
                sleep_time = state_change_time
                state = State.ASLEEP
            else:
                awake_time = state_change_time
                update_sleep_times(elf_tracker, current_elf, sleep_time, awake_time)
                state = State.AWAKE

    total_minutes_by_elf = calculate_total_minutes_by_elf(elf_tracker)
    elves_sorted_by_sleepiness = sorted(
        total_minutes_by_elf.items(), key=lambda x: x[1], reverse=True
    )
    sleepiest_elf_id, sleepiest_elf_minutes = elves_sorted_by_sleepiness[0]
    print(
        f'The sleepiest elf is #{sleepiest_elf_id}, who slept for a total of {sleepiest_elf_minutes} minutes'
    )
    sleepiest_elfs_log = elf_tracker[sleepiest_elf_id]
    sleepiest_minute, num_times_slept = sorted(
        sleepiest_elfs_log.items(), key=lambda x: x[1], reverse=True
    )[0]
    print(
        f"That elf's sleepiest minute was {sleepiest_minute}, which they slept at {num_times_slept} times"
    )
    print(f'answer: {int(sleepiest_minute) * int(sleepiest_elf_id)}')


if __name__ == '__main__':
    with open('data/input04.txt') as f:
        lines = f.readlines()

    main(sorted(lines))
