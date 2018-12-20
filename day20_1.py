class State(object):
    def __init__(self, x, y, distance_from_start):
        self.x = x
        self.y = y
        self.distance = distance_from_start
        self.north = None
        self.south = None
        self.east = None
        self.west = None


def find_furthest_room(regex):
    start_state = State(0, 0, 0)
    current_state = start_state
    all_states = {(0, 0): start_state}
    end_states = {}

    for i, char in enumerate(regex):
        if char == '^':
            assert i == 0, 'Unexpected carat'
        elif char == '$':
            assert i == len(regex) - 1, 'Unexpected dollar'
            end_states[(current_state.x, current_state.y)] = current_state
        elif char == 'N':
            next_x = current_state.x
            next_y = current_state.y + 1
            if (next_x, next_y) in all_states:
                next_state = all_states[next_x, next_y]
                next_state.distance = min(
                    next_state.distance, current_state.distance + 1
                )
                current_state.north = next_state
            else:
                next_state = State(next_x, next_y, current_state.distance + 1)
                all_states[(next_x, next_y)] = next_state
                current_state.north = next_state
            current_state = next_state
        elif char == 'S':
            next_x = current_state.x
            next_y = current_state.y - 1
            if (next_x, next_y) in all_states:
                next_state = all_states[next_x, next_y]
                next_state.distance = min(
                    next_state.distance, current_state.distance + 1
                )
                current_state.south = next_state
            else:
                next_state = State(next_x, next_y, current_state.distance + 1)
                all_states[(next_x, next_y)] = next_state
                current_state.south = next_state
            current_state = next_state
        elif char == 'E':
            next_x = current_state.x + 1
            next_y = current_state.y
            if (next_x, next_y) in all_states:
                next_state = all_states[next_x, next_y]
                next_state.distance = min(
                    next_state.distance, current_state.distance + 1
                )
                current_state.east = next_state
            else:
                next_state = State(next_x, next_y, current_state.distance + 1)
                all_states[(next_x, next_y)] = next_state
                current_state.east = next_state
            current_state = next_state
        elif char == 'W':
            next_x = current_state.x - 1
            next_y = current_state.y
            if (next_x, next_y) in all_states:
                next_state = all_states[next_x, next_y]
                next_state.distance = min(
                    next_state.distance, current_state.distance + 1
                )
                current_state.west = next_state
            else:
                next_state = State(next_x, next_y, current_state.distance + 1)
                all_states[(next_x, next_y)] = next_state
                current_state.west = next_state
            current_state = next_state
        elif char == '(':
            pass
        elif char == '|':
            pass
        elif char == ')':
            pass
        else:
            raise Exception('Unexpected character')

    end_states_from_furthest_to_nearest = sorted(
        end_states.values(), key=lambda x: x.distance, reverse=True
    )
    return end_states_from_furthest_to_nearest[0].distance


if __name__ == '__main__':
    with open('data/input20.txt') as f:
        data = f.read().strip()
    print(f'answer: {find_furthest_room(data)}')
