from water import CLAY, FLOWING, SAND, STANDING, WELL


class Ground(object):
    def __init__(self, clay_coordinates):
        self.clay_coordinates = clay_coordinates
        self.well_coordinate = (500, 0)
        self.flowing_coordinates = set()
        self.standing_coordinates = set()
        self.water = None
        self.completed_coordinates = set()

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

    def check_square(self, square):
        x, y = square
        # print(f'checking {x}, {y}')
        # print(f'{self.flowing_squares} flowing squares and {self.standing_squares} standing squares')
        # print(self)

        # Check 1: If we are at the max depth then we flow off and we're done
        if y == self.max_y:
            self.completed_coordinates.add(square)
            return []

        # Check 2: If below is FLOWING and completed, we're done
        below_coord = (x, y+1)
        below_char = self.gimme_char(*below_coord)
        if below_char == FLOWING and below_coord in self.completed_coordinates:
            self.completed_coordinates.add(square)
            return []

        # Check 3: Try to flow down, push this square and below to stack
        if below_coord not in self.completed_coordinates and below_char not in (CLAY, STANDING):
            self.flowing_coordinates.add(below_coord)
            return [square, below_coord]

        # Check 4: Try to flow left, push this square and left to stack
        left_coord = (x-1, y)
        if self.gimme_char(*left_coord) == SAND and self.gimme_char(*below_coord) in (CLAY, STANDING):
            self.flowing_coordinates.add(left_coord)
            return [square, left_coord]

        # Check 5: Try to flow right, push this square and right to stack
        right_coord = (x+1, y)
        if self.gimme_char(*right_coord) == SAND and self.gimme_char(*below_coord) in (CLAY, STANDING):
            self.flowing_coordinates.add(right_coord)
            return [square, right_coord]

        # I can't flow down, left, or right
        # if self.gimme_char(*left_coord) in (CLAY, STANDING) or self.gimme_char(*right_coord) in (CLAY, STANDING):
        if self._can_i_stand(square):
            self.standing_coordinates.add(square)
            self.flowing_coordinates.remove(square)
        self.completed_coordinates.add(square)

        return []

    @property
    def wet_squares(self):
        return len(self.flowing_coordinates) + len(self.standing_coordinates)

    @property
    def flowing_squares(self):
        return len(self.flowing_coordinates)

    @property
    def standing_squares(self):
        return len(self.standing_coordinates)

    def _is_below_firm(self, square):
        below_coord = (square[0], square[1]+1)
        below_char = self.gimme_char(*below_coord)
        return below_char in (CLAY, STANDING)

    def _can_i_stand(self, square):
        if not self._is_below_firm(square):
            return False

        # check to the left
        square_to_check = (square[0]-1, square[1])
        while self.gimme_char(*square_to_check) != CLAY:
            if not self._is_below_firm(square_to_check):
                return False
            square_to_check = (square_to_check[0]-1, square_to_check[1])

        # check to the right
        square_to_check = (square[0]+1, square[1])
        while self.gimme_char(*square_to_check) != CLAY:
            if not self._is_below_firm(square_to_check):
                return False
            square_to_check = (square_to_check[0]+1, square_to_check[1])

        return True
