from day13_1 import parse_input


def locate_last_cart(game):
    while len([cart for cart in game.carts if cart.active]) > 1:
        # print(game)
        game.tick(remove_crashed_carts=True)

    for cart in game.carts:
        if cart.active:
            return cart.x, cart.y
    return 0, 0


if __name__ == '__main__':
    game = parse_input('data/input13.txt')
    answer = locate_last_cart(game)
    print(answer)
