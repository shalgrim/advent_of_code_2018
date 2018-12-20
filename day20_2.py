from day20_1 import ALL_STATES, find_furthest_room_helper


def find_num_rooms_beyond_distance(regex, distance):
    ALL_STATES.clear()
    output = find_furthest_room_helper(regex)
    end_states_beyond_distance = [
        es for es in output.values() if es.distance >= distance
    ]
    return len(set(end_states_beyond_distance))


if __name__ == '__main__':
    with open('data/input20.txt') as f:
        data = f.read().strip()
    print(f'answer: {find_num_rooms_beyond_distance(data, 1000)}')
    # 630 is too small
