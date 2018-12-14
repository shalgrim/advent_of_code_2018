def score_elves(first_n_recipes):
    scores = [3, 7]
    elf_locations = [0, 1]

    while len(scores) < first_n_recipes + 10:
        elf_scores = [scores[i] for i in elf_locations]
        # this is where a line would get printed
        new_score = sum(elf_scores)
        new_recipes = [int(c) for c in str(new_score)]
        scores += new_recipes

        elf_moves = [1 + score for score in elf_scores]
        elf_locations = [
            (location + move) % len(scores)
            for location, move in zip(elf_locations, elf_moves)
        ]

    return int(
        ''.join([str(c) for c in scores[first_n_recipes : first_n_recipes + 10]])
    )


if __name__ == '__main__':
    print(score_elves(793061))
