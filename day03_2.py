import sys
from collections import defaultdict

from day03_1 import get_claimed_squares, parse_line


def main(lines):
    print(f'len(lines): {len(lines)}')
    known_elfs = set()
    claims_on_squares = defaultdict(set)

    for line in lines:
        claim = parse_line(line)
        known_elfs.add(claim.elf_id)
        claimed_squares = get_claimed_squares(claim)

        for square in claimed_squares:
            claims_on_squares[square].add(claim.elf_id)

    print(f'len(known_elfs): {len(known_elfs)}')
    print(f'len(claims_on_squares): {len(claims_on_squares)}')

    overlapping_squares = {k: v for k, v in claims_on_squares.items() if len(v) > 1}
    print(f'len(overlapping_squares): {len(overlapping_squares)}')
    overlapping_claim_ids = set()
    for square, ids in overlapping_squares.items():
        overlapping_claim_ids.update(ids)

    print(f'len(overlapping_claim_ids): {len(overlapping_claim_ids)}')

    for elf in known_elfs:
        if elf not in overlapping_claim_ids:
            print(f'answer: {elf}')
            break
    else:
        print('no answer found')


if __name__ == '__main__':
    with open('data/input03.txt') as f:
        lines = f.readlines()

    main(lines)
