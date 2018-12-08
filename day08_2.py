def get_root_node_value(tree):
    if not tree:
        return 0, ''

    data = tree.split()
    num_children = int(data[0])
    num_metadata = int(data[1])
    child_node_values = []
    remaining_tree = ' '.join(data[2:])

    for i in range(num_children):
        child_node_value, remaining_tree = get_root_node_value(remaining_tree)
        child_node_values.append(child_node_value)

    data = remaining_tree.split()
    root_node_value = 0
    if num_children == 0:
        for i in range(num_metadata):
            root_node_value += int(data[i])
    else:
        for i in range(num_metadata):
            metadata_value = int(data[i])
            try:
                root_node_value += child_node_values[metadata_value - 1]
            except IndexError:
                root_node_value += 0

    remaining_tree = ' '.join(data[num_metadata:])

    return root_node_value, remaining_tree


if __name__ == '__main__':
    # filename = 'data/test08.txt'
    filename = 'data/input08.txt'
    with open(filename) as f:
        text = f.read()

    answer, _ = get_root_node_value(text.strip())
    print(answer)
