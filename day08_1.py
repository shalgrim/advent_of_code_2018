import sys


def get_metadata_sum(tree):
    if not tree:
        return 0, ''

    data = tree.split()
    num_children = int(data[0])
    num_metadata = int(data[1])
    metadata_sum = 0
    remaining_tree = ' '.join(data[2:])

    for i in range(num_children):
        child_sum, remaining_tree = get_metadata_sum(remaining_tree)
        metadata_sum += child_sum

    data = remaining_tree.split()

    for i in range(num_metadata):
        metadata_sum += int(data[i])

    remaining_tree = ' '.join(data[num_metadata:])

    return metadata_sum, remaining_tree


if __name__ == '__main__':
    # filename = 'data/test08.txt'
    filename = 'data/input08.txt'
    with open(filename) as f:
        text = f.read()

    answer, _ = get_metadata_sum(text.strip())
    print(answer)
