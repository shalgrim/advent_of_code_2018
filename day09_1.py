from collections import Counter


class Marble(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, to_right_of):
        self.left = to_right_of
        self.right = to_right_of.right
        to_right_of.right.left = self
        to_right_of.right = self

    def __str__(self):
        return str(self.value)


class Circle(object):
    def __init__(self):
        self.current = Marble(0)
        self.first = self.current
        self.current.left = self.current
        self.current.right = self.current

    def insert(self, marble):
        if marble.value % 23 != 0:
            marble.insert(self.current.right)
            self.current = marble
            return 0
        else:
            new_current = self.current
            for i in range(6):
                new_current = new_current.left
            to_remove = new_current.left
            self._remove(to_remove)
            self.current = new_current
            return marble.value + to_remove.value

    def _remove(self, marble):
        marble.left.right = marble.right
        marble.right.left = marble.left
        marble.right = None
        marble.left = None

    def __str__(self):
        if self.current is self.first:
            s = f' ({self.first.value})'
        else:
            s = f' {self.first.value}'

        printing = self.first.right
        while printing is not self.first:
            if printing is self.current:
                s += f' ({printing.value})'
            else:
                s += f' {printing.value}'
            printing = printing.right

        return s


def play_marble_game(num_players, last_marble_value):
    scores = Counter()
    circle = Circle()

    # print(f'[-]{circle}')

    for i in range(1, last_marble_value + 1):
        marble = Marble(i)
        player = i % num_players
        if player == 0:
            player = num_players
        scores[player] += circle.insert(marble)
        # print(f'[{player}]{circle}')

    winner, highest_score = scores.most_common(1)[0]

    return highest_score


if __name__ == '__main__':
    print(play_marble_game(462, 71938))
