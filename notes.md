## Day 15

### Part One

#### Test Case Two

I think I see the problem here. After 33 rounds there is an elf with two HP that has a goblin above and below it. So in round 34, the goblin above it kills it, so when it comes to the goblin below's turn, that goblin should attack the elf that is to its left but it doesn't seem to be doing that.

The issue seems to be when `attackables` gets defined in `attack()` it doesn't check for attackables to have hp > 0

## Day 22

### Part Two

Working on the test case

The first time a Happy State shortest_from (line 252) gets recorded, it's (5, 8)
Which is clearly a problem
So next let's look at what happens when state is (10, 10) or (10, 11)...heck, x==10 would be fine

Problem:
  - line 245
    - state: (9, 10),Equipment.NO
    - nextstate: (10,10),Equipment.CLIMB
    - value appended to distances is 83 (should be 15...switch to CLIMB, move, switch to TORCH)
    - because line 221 returns total cost for that visitation path
    - which probably made sense somewhere but now I've got a mix of doing that plus doing incremental costs
    - oof
    - and the reason I wanted to do that was to record a global known_shortest_path
    - and that's nice, but it doesn't jibe with the distances/actual_distances/shortest_froms work I'm doing in lines 245-253
