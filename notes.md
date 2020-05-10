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

- Working through it from `test_base_case_minus_7`
- The happy path will be taking Down as the first direction
- But that will be the third direction it tries, after Right and Up
- It gets there okay and drills down into a state of (6, 12), CLIMB, and the previous test case found the shortest path from there fine
- So what goes wrong
- I feel like it has to be a `shortest_from` gets set wrong
- Yep, `shortest_froms['(8, 12),Equipment.CLIMB']` is set to 137
- So next in to test this test case and figure out why that gets set the way it does even though `test_case_base_minus_4` succeeds
- setting breakpoints and testing `test_case_base_minus_7`
- The first time through the four direction loop where the String is `'(8, 12),Equipment.CLIMB'`, distances is a list of four Nones so no shortest gets sent
- The second time through distances is a list of 137 and then three Nones
- The first direction, the one where it finds 137, is UP
- So I could either explore the problem the first time through or the second time through
- The first time problem: Why does it find no path when going RIGHT?
- The second time problem: Why does it find such a long path when going UP but only that one?
- I think it's better to deal with the first time problem, since, I think, it should find a path there
- Looking into that now
- (9, 12) is not in the visited path
- well, just the first time it gets to a state of '(8, 12),Equipment.CLIMB', the value of self.shortest_froms['(10, 11),Equipment.CLIMB'] is 39
- which is nuts (should be eight)
- so let's see what happens the first time it gets to that state
- It goes up to (10, 10) first thing
- And there it sets final_cost to 33 and returns final_cost
- And so then the shortest from for the state gets set to 33 (must get reset to 39 later)
  - Also curious here is how it also finds no path going DOWN...i guess it's just longer than longest_known path
- So I still have an unruly mix of final cost and incremental cost messing me up
- Consider `distances.append(self.find_quickest_path(nextstate) - state.cost)`
- I'll try that and see what test cases it messes up
- Hm, it's still that `test_case_base_minus_7` breaks, so keep looking into that
