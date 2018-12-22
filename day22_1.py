ROCKY = 'rocky'
WET = 'wet'
NARROW = 'narrow'

RISK_FACTORS = {
    ROCKY: 0,
    WET: 1,
    NARROW: 2,
}

def calc_risk_level(target_x, target_y, depth):
    risk_level = 0
    for x in range(target_x+1):
        for y in range(target_y+1):
            risk_level += RISK_FACTORS[cave[(x, y)].type]

    pass


if __name__ == '__main__':
    print(f'answer: {calc_risk_level(12, 757, 3198)}')