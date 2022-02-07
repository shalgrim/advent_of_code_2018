"""An unconventional naming strategy for me. I want to put random stuff to try here, but it's definitely part 2"""
import math

from day22_1 import Cave, Region, build_cave, RegionType, Equipment, POSSIBLE_EQUIPMENT

# input
DEPTH = 3198
TARGET = 12, 757

# toy with these if your answer is wrong...maybe going a bit wide and deep around will help
EXTRA_X = 0
EXTRA_Y = 0

cave = build_cave(TARGET[0], TARGET[1], DEPTH, EXTRA_X, EXTRA_Y)


class Node:
    def __init__(self, x, y, equipment, initial_distance):
        self.x = x
        self.y = y
        self.equipment = equipment
        self.visited = False
        self.distance = initial_distance
        self.distance = 0 if x == 0 and y == 0 and equipment == 'whatever' else math.inf
        self.neighbors = []


def create_dijkstra_nodes(cave, target_x, target_y, extra_x, extra_y):
    """The trickiest part is going to be setting neighbors"""
    nodes = {}  # key is (x, y, equipment) for easier neighbor calculation
    for y in range(target_y + extra_y):
        for x in range(target_x + extra_x):
            region = cave[(x, y)]
            if x == 0 and y == 0:
                nodes[(0, 0, Equipment.TORCH)] = Node(x, y, Equipment.TORCH, 0)
                if region.tipe == RegionType.ROCKY:
                    nodes[(0, 0, Equipment.CLIMB)] = Node(
                        x, y, Equipment.CLIMB, math.inf
                    )
                else:
                    assert region.tipe == RegionType.NARROW
                    nodes[(0, 0, Equipment.NO)] = Node(x, y, Equipment.NO, math.inf)
            elif region.tipe == RegionType.ROCKY:
                torch_node = Node(x, y, Equipment.TORCH, math.inf)
                climb_node = Node(x, y, Equipment.CLIMB, math.inf)
                torch_node.neighbors.append((climb_node, 7))
                climb_node.neighbors.append((torch_node, 7))
                nodes[(x, y, Equipment.TORCH)] = torch_node
                nodes[(x, y, Equipment.CLIMB)] = climb_node
                torch_node.neighbors.append((climb_node, 7))
                climb_node.neighbors.append((torch_node, 7))
            elif region.type == RegionType.NARROW:
                torch_node = Node(x, y, Equipment.TORCH, math.inf)
                nodes[(x, y, Equipment.TORCH)] = torch_node
                no_node = Node(x, y, Equipment.NO, math.inf)
                nodes[(x, y, Equipment.NO)] = no_node
                torch_node.neighbors.append((no_node, 7))
                no_node.neighbors.append((torch_node, 7))
            else:  # wet
                climb_node = Node(x, y, Equipment.CLIMB, math.inf)
                no_node = Node(x, y, Equipment.NO, math.inf)
                nodes[(x, y, Equipment.CLIMB)] = climb_node
                nodes[(x, y, Equipment.NO)] = no_node
                climb_node.neighbors.append((no_node, 7))
                no_node.neighbors.append((climb_node, 7))

    for key, node in nodes.items():
        x, y, equipment = key
        west_neighbor = nodes.get((x - 1, y, equipment))
        if west_neighbor:
            node.neighbors.append((west_neighbor, 1))  # 1 is the path cost

        east_neighbor = nodes.get((x + 1, y, equipment))
        if east_neighbor:
            node.neighbors.append((east_neighbor, 1))

        north_neighbor = nodes.get((x, y - 1, equipment))
        if north_neighbor:
            node.neighbors.append((north_neighbor, 1))

        south_neighbor = nodes.get((x, y + 1, equipment))
        if south_neighbor:
            node.neighbors.append((south_neighbor, 1))

    return nodes


unvisited_nodes = create_dijkstra_nodes(cave, TARGET[0], TARGET[1], EXTRA_X, EXTRA_Y)
current_node = unvisited_nodes[(0, 0, Equipment.TORCH)]
current_node.distance = 0
visited_nodes = {}
target_key = (TARGET[0], TARGET[1], Equipment.TORCH)

while unvisited_nodes and target_key not in unvisited_nodes:
    current_key = (current_node.x, current_node.y, current_node.equipment)
    for neighbor, edge_distance in current_node.neighbors:
        if neighbor.visited:
            continue
        neighbor.distance = min(
            neighbor.distance, current_node.distance + edge_distance
        )

    current_node.visited = True
    visited_nodes[current_key] = current_node
    del unvisited_nodes[current_key]
    if unvisited_nodes:
        current_node = sorted(
            list(unvisited_nodes.values()), key=lambda node: node.distance
        )[0]
    else:
        current_node = None

print(visited_nodes[target_key].distance)
