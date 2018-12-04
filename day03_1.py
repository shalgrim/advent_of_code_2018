import re
from collections import namedtuple, defaultdict

LINE_PATTERN = re.compile(
    r'#(?P<elf_id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)\n'
)

Claim = namedtuple('Claim', ['elf_id', 'x', 'y', 'w', 'h'])


def parse_line(line):
    match = LINE_PATTERN.match(line)
    claim = Claim(
        int(match.group('elf_id')),
        int(match.group('x')),
        int(match.group('y')),
        int(match.group('w')),
        int(match.group('h')),
    )
    return claim


def get_claimed_squares(claim):
    squares = []
    for i in range(claim.w):
        x = claim.x + i
        for j in range(claim.h):
            squares.append((x, claim.y + j))

    return squares


def main(lines):
    claims_on_squares = defaultdict(set)
    for line in lines:
        claim = parse_line(line)
        claimed_squares = get_claimed_squares(claim)

        for square in claimed_squares:
            claims_on_squares[square].add(claim.elf_id)

    print(f'len(claims_on_squares): {len(claims_on_squares)}')
    squares_sharing_claims = [k for k, v in claims_on_squares.items() if len(v) > 1]
    print(f'answer: {len(squares_sharing_claims)}')


if __name__ == '__main__':
    with open('data/input03.txt') as f:
        lines = f.readlines()

    main(lines)
