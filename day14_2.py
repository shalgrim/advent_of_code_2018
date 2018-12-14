def score_elves_backwards(string_to_find):
    scores = [3, 7]
    string_scores = '37'
    elf_locations = [0, 1]

    while string_to_find not in string_scores:
        elf_scores = [scores[i] for i in elf_locations]
        new_string_score = str(sum(elf_scores))
        string_scores += new_string_score
        scores += [int(c) for c in new_string_score]

        elf_moves = [1 + score for score in elf_scores]
        elf_locations = [
            (location + move) % len(scores)
            for location, move in zip(elf_locations, elf_moves)
        ]

    score_index = string_scores.index(string_to_find)
    return score_index


if __name__ == '__main__':
    print(score_elves_backwards('793061'))
