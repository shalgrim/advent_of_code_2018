import logging
import sys
from collections import defaultdict
from logging import StreamHandler

from day07_1 import parse_lines

logger = logging.getLogger('advent_of_code.2018.day07_2')
logging.basicConfig(
    filename='day07_2.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


class Step(object):
    def __init__(self, letter, extra_time=60):
    # def __init__(self, letter, extra_time=0):
        self.letter = letter
        self.time_spent = 0
        self.time_remaining = extra_time + ord(letter) - 64  # ord('A') == 65
        self.completed = False

    def work_on(self):
        if self.time_remaining == 0:
            return
        self.time_spent += 1
        self.time_remaining -= 1
        if self.time_remaining == 0:
            self.completed = True


class Worker(object):
    def __init__(self):
        self.working_on = None

    def is_free(self):
        return not self.working_on

    def assign(self, step):
        self.working_on = step

    def work(self):
        if not self.working_on:
            return None

        self.working_on.work_on()
        if self.working_on.completed:
            retval = self.working_on
            self.working_on = None
        else:
            retval = None

        return retval


def main(lines, num_workers=5):
    data = parse_lines(lines)
    letters_to_do = set(d[0] for d in data).union(set(d[1] for d in data))
    steps_to_do = {letter: Step(letter) for letter in letters_to_do}

    predecessors = defaultdict(set)
    for datum in data:
        predecessors[datum[1]].add(datum[0])

    workers = [Worker() for i in range(num_workers)]

    steps_done = []
    num_seconds = 0

    # print('Second   Worker 1   Worker 2   Done')
    print('Second   Worker 1   Worker 2   Worker 3   Worker 4   Worker 5   Worker 6   Done')

    while steps_to_do:
        # 0. increment number of seconds
        num_seconds += 1

        # 1. look for available workers
        available_workers = [worker for worker in workers if worker.is_free()]

        # 2. look for available steps
        possible_next_step_letters = set(
            k
            for k, v in steps_to_do.items()
            if (k not in predecessors or not predecessors[k]) and v.time_spent == 0
        )

        # 3. whatever the min is of 1 and 2, assign that many steps to workers
        next_step_letters = sorted(list(possible_next_step_letters))[
            : len(available_workers)
        ]
        assert len(next_step_letters) <= len(
            available_workers
        ), f'{len(next_step_letters)} next steps but {len(available_workers)} available workers'

        for i, step_letter in enumerate(next_step_letters):
            available_workers[i].assign(steps_to_do[step_letter])

        output_string = str(num_seconds - 1).rjust(4, ' ') + '   '
        for worker in workers:
            printable = worker.working_on.letter if worker.working_on else '.'
            output_string += f'    {printable}      '

        output_string += ''.join(steps_done)
        print(output_string)

        # 4. everybody works
        for worker in workers:
            worker.work()

        # 5. figure out which steps were completed
        completed_step_letters = [k for k, v in steps_to_do.items() if v.completed]

        # 6. put completed step letters (alphabetically if tie(?)) into steps_done
        steps_done += sorted(completed_step_letters)

        # 7. remove completed step letters from values of predecessors
        completed_step_letter_set = set(completed_step_letters)
        for v in predecessors.values():
            if v.intersection(completed_step_letter_set):
                v.difference_update(completed_step_letter_set)

        # 8. remove completed step letter keys from steps_to_do
        for letter in completed_step_letters:
            del steps_to_do[letter]

    print(f'took {num_seconds} seconds')


if __name__ == '__main__':
    with open('data/input07.txt') as f:
    # with open('data/test07.txt') as f:
        lines = f.readlines()

    main(lines)
    # main(lines, 2)
