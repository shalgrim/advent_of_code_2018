from water import CLAY, FLOWING, SAND, STANDING, WELL


class Ground(object):
    def __init__(self, clay_coordinates):
        self.clay_coordinates = clay_coordinates
        self.well_coordinate = (500, 0)
        self.flowing_coordinates = set()
        self.standing_coordinates = set()
        self.water = None

    def gimme_char(self, x, y):
        if (x, y) in self.standing_coordinates:
            return STANDING
        elif (x, y) in self.flowing_coordinates:
            return FLOWING
        elif (x, y) in self.clay_coordinates:
            return CLAY
        else:
            return SAND

    @property
    def max_y(self):
        return max(coord[1] for coord in self.clay_coordinates)

    def __str__(self):
        min_x = min(coord[0] for coord in self.clay_coordinates) - 1
        max_x = max(coord[0] for coord in self.clay_coordinates) + 1
        min_y = 0

        # build headers
        lines = [
            '     {}'.format(''.join([str(x // 100) for x in range(min_x, max_x + 1)])),
            '     {}'.format(
                ''.join([str(x // 10 % 10) for x in range(min_x, max_x + 1)])
            ),
            '     {}'.format(''.join([str(x % 10) for x in range(min_x, max_x + 1)])),
        ]

        # build ground level
        line = '   0 '
        for x in range(min_x, max_x + 1):
            if (x, 0) == self.well_coordinate:
                line += WELL
            elif (x, 0) in self.clay_coordinates:
                line += CLAY
            else:
                line += SAND
        lines.append(line)

        # build ground slice
        for y in range(1, self.max_y + 1):
            lines.append(
                '{:>4} {}'.format(
                    y, ''.join([self.gimme_char(x, y) for x in range(min_x, max_x + 1)])
                )
            )

        lines = [''] + lines + ['']

        return '\n'.join(lines)

    @property
    def wet_squares(self):
        return len(self.flowing_coordinates) + len(self.standing_coordinates)

    @property
    def flowing_squares(self):
        return len(self.flowing_coordinates)

    @property
    def standing_squares(self):
        return len(self.standing_coordinates)

    # def tick(self):
    #     if self.water:
    #         self.water = self.water.flow(self)
    #     else:
    #         self.water = Water(
    #             self, self.well_coordinate[0], self.well_coordinate[1] + 1, self, None
    #         )
    #
    #     return True
