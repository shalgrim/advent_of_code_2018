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
- It correctly finds many shortests
- Including as close as 7,12climb...with a distance of 12
- But then it goes and assigns 6,11climb a distance of 28
- Which this gets by switching to torch then going to 7,11 torch where the distance is 20
- notably there's not a single exploration of (6, 12), regardless of equipment
- distances is only [28, 33]...I'm not surprised that left would come back with nothing
- but why does Down return nothing?
- it gets 28 from RIGHT and 33 from UP
- so going down...
  - it gets to 8,12 and finds a shortest of 11 so returns 14...that's correct
  - and 12 gets assigned as the shortest for 7,12climb...that's correct
  - and then it _returns_ 12, which I think might be a problem
- boy, i should never be returning final cost
- ugh, but it still breaks in the same place
- somehow from 6,11climb it gets as distances for right, up, down, and left [66, 100, 71, 95]
- it goes right first, does some stuff, then assigns 7 as shortest for 10,11climb (but it should be 8)
- fixed that bug and it _still_ breaks in the same place, coming back with an answer of 33 when it should be 14

```py
problem:
self.shortest_froms['(10, 11),Equipment.CLIMB']
8
self.shortest_froms['(10, 12),Equipment.CLIMB']
42
```

- fixed that, but having the same problem
- getting frustrated
- well now self.shortest_froms['(6, 11),Equipment.CLIMB'] is the correct answer, and it's returning the right answer
- but it's not storing the right answer in self.shortest_known_path
- (and i checked if i could just ignore that and still be good by using the return value for the test for the whole thing and that wasn't the case)
- (but it was correct for the minus 8 test case too)
- this bug is happening b/c it only calculates the shortest_known when it's in the terminal position
- and it can really also calculate it if current cost plus known shortest from is less
- new failure: test_base_case_minus_10
- again it's where the happy path move is DOWN
- going that direction it comes back with 36 (should be 16 like previous test case)
- and '(4, 11),Equipment.CLIMB' is not in self.shortest_froms, which is weird
- 5,11climb is in there but it's 34 (at which point 36 makes sense)
- 10,11climb and 10,12climb aren't in shortest_froms
- the closest you ever get on the happy path is 7,12climb
- so why does that one not make it to 8,12climb
- (there is an 8,12torch in there (and 7,12torch))
- i believe it is because it takes the "wrong" way to get there and then runs out of room before getting longer than the known shortest path so it gives up
- so it should only record shortest_from if it gets all four distances back? either that or stop terminating if we've searched more than the known shortest path
- If I try the latter I get max recursion depth
- And trying the former makes things take too long...test_base_case_minus_04 takes 26 seconds
  - and _06 doesn't seem to want to stop
- Two ideas:
  1) Solve above directly by storing four shortests, one for each direction...then you'd have to
     1a) only stop searching if all four shortests are filled in
     1b) only bother searching those where you don't have shortests
  2) New idea entirely...fill in the surrounding values of shortest_from, like cycle around it...uff, but you wouldn't know if the shortest would actually be to go away from the target
- okay new idea, you track shortest by incoming cost
- so then if you come in with a lower cost, then you can re-search, else just take whatever is equal to or the next higher than your current cost for the known shortest
- i implemented that, now to test it
- that broke everything from test_base_case_minus_01 on
- fixed that but now test_base_case_minus_02 takes 11s and still witing on test_base_case_minus_03
- got overwhelmed, decided to create BFS search
- it is ready to "test" (i.e., walkthrough)
- tho it might be good to try to set up some happy path tets for that as well
- yeah just trying to get base case working now
- frig, I also can't get the damned base-case minus 3 to terminate for bfs
- oh there it took 25 seconds, christ
- let's try basecase6
- that don't work
- basecase4 also don't
- but i'm getting some exception that I can't get PyCharm to stop on
- nor can I get PyCharm to stop on the condition that the test is bailing on
- why doesn't PyCharm do the thing I'm telling it to
- fine, I think I'm giving up on this...for now...I wish PyCharm would do what it says it does
