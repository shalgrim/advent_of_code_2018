class State(object):
    def __init__(self, x, y, distance_from_start):
        self.x = x
        self.y = y
        self.distance = distance_from_start
        self.north = None
        self.south = None
        self.east = None
        self.west = None

    def add_state(self, other, direction):
        if direction == 'N':
            self.north = other
        if direction == 'S':
            self.south = other
        if direction == 'E':
            self.east = other
        if direction == 'W':
            self.west = other


def find_matching_rparen(s, lparen_index):
    count = 1
    i = lparen_index
    while count > 0:
        i += 1
        if s[i] == ')':
            count -= 1
        elif s[i] == '(':
            count += 1
        else:
            continue

    return i


ALL_STATES = {}


def get_next_coords(state, direction):
    if direction == 'N':
        return state.x, state.y - 1
    if direction == 'S':
        return state.x, state.y + 1
    if direction == 'E':
        return state.x + 1, state.y
    if direction == 'W':
        return state.x - 1, state.y


def process_direction(current_state, direction):
    next_x, next_y = get_next_coords(current_state, direction)
    if (next_x, next_y) in ALL_STATES:
        next_state = ALL_STATES[(next_x, next_y)]
        next_state.distance = min(
            next_state.distance, current_state.distance + 1
        )
    else:
        next_state = State(next_x, next_y, current_state.distance + 1)
        ALL_STATES[(next_x, next_y)] = next_state
    current_state.add_state(next_state, direction)
    return next_state


def find_furthest_room_helper(regex, start_state=None):
    if not start_state:
        current_states = [State(0, 0, 0)]
        ALL_STATES[(0, 0)] = current_states[0]
    else:
        current_states = [start_state]
    end_states = {}
    i = 0

    while i < len(regex):
        char = regex[i]
        if char == '^':
            assert i == 0, 'Unexpected carat'
        elif char == '$':
            assert i == len(regex) - 1, 'Unexpected dollar'
            for cs in current_states:
                end_states[(cs.x, cs.y)] = cs
        elif char in 'NSEW':
            for j in range(len(current_states)):
                current_states[j] = process_direction(current_states[j], char)
        elif char == '(':
            lparen_index = i
            rparen_index = find_matching_rparen(regex, lparen_index)
            substring = f'^{regex[lparen_index+1:rparen_index]}$'
            new_current_states = []
            for cs in current_states:
                new_current_states += list(find_furthest_room_helper(substring, cs).values())
            current_states = list(set(new_current_states))  # make unique
            i = rparen_index
        elif char == '|':
            # assert len(current_states) == 1, 'Unexpected precedence'
            for cs in current_states:
                end_states[(cs.x, cs.y)] = cs
            current_states = [start_state]
        else:
            raise Exception('Unexpected character')
        i += 1

    return end_states


def find_furthest_room(regex):
    ALL_STATES.clear()
    output = find_furthest_room_helper(regex)
    end_states_from_furthest_to_nearest = sorted(
        output.values(), key=lambda x: x.distance, reverse=True
    )
    return end_states_from_furthest_to_nearest[0].distance


if __name__ == '__main__':
    with open('data/input20.txt') as f:
        data = f.read().strip()
    answer = find_furthest_room(data)
    print(f'answer: {answer}')
