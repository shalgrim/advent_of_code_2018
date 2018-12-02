from collections import Counter


if __name__ == '__main__':
    num_twos = 0
    num_threes = 0

    with open('data/input02_1.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    for line in lines:
        counts = Counter(line)
        if 2 in counts.values():
            num_twos += 1
        if 3 in counts.values():
            num_threes += 1

    answer = num_twos * num_threes
    print(f'answer: {answer}')
