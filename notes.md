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
- and basecase-6 works it just takes 20 m 45 s =(
- ... oh not letting paths re-visit nodes has gotten things down under 3 s
- well now BFS is going muuuuch better
- but still basecase-13 took 2.5 minutes
- so i still might put it down for a while
- the only other idea i have at this point is to have paths wait, or tick, for seven passes after they move and change equipment
- the benefit of that is the terminating condition is finding a single solution
- i'm skeptical it will improve anything, but it might be worth a try
- something has to give, because basecase-19 hasn't terminated in over 20 minutes
- I'll put in some interim cases there to try to rule out bug or just taking too long
- ...
- So my counting ticks version in this branch seems a little faster than exhausting bfs in the master branch
- but it's still pretty slow
- i have one more idea
- as soon as any path has a position at the target position, you cull anything not with a manhattan distance of ticks remaining
- and actually there may be some other culling to be going on...e.g., if any path is within one of target position, cull everything that's not within ticksremaing + 7
- and if one is two away then ticksremaining + 14, ticksremaining + 21, etc.
- so cut a new branch and try that kind of culling
- ...
- I'm getting close to taking a pause on day 22
- So a guide:
  - `day22_2.py` is DFS
  - `day22_2_2.py` is BFS
  - in `master` I calculated cost and did an exhaustive BFS
  - in `try-changing-over-ticks` I had paths wait seven ticks before moving if changing equipment and terminating condition was path arriving at destination with TORCH
  - in `now-try-culling` I'm going to try one more thing where, once any path reaches destination, regardless of equipment, we cull out anybody more than a manhattan distance of 7 away
- Well culling went quite well
- But I believe it's still too slow for the real problem
- Though maybe consider the more aggressive culling where you find the closest one by manhattan distance with fewest ticks_remaining
- and then cull anything further than that manhattan_distance*7 + ticks_remaining
- I think I should try that before taking a break
- All the tests in the culling branch took about 42 minutes and I exported the results [here](file:///Users/scotthalgrim/advent_of_code_2018/Test%20Results%20Day%2022%20-%20.html)
- ...
- kicked off `python day22_2.py` on the `now-try-culling` branch at 15:59 on 2022-01-29
  - still running 16 hours later =(

## Day 23

### Part 2

Note that these notes are not on the main branch, they're on a branch where I'm working on day 22

It occurs to me that it should be easy for any two nanobots to figure out if they have any overlap.

And it shouldn't be too hard to figure it out then for three, four, etc.

So let's start by trying to find all combinations of two that have any overlap, then try to find all combinations of three that have any overlap, and so on

...

[This](https://www.reddit.com/r/adventofcode/comments/rd4tah/2018_day_23_part_2_need_some_pointers/hnzfejt/?utm_source=reddit&utm_medium=web2x&context=3) is the thing I want to think about next

I don't feel like that would necessarily get me to a global optimum, but if they say it does there's probably a proof somewhere.

So then I guess the subproblems are:
  - figuring out how to define a cube (I mean, I guess with eight points)
  - figuring out how to determine how many bots' ranges overlap with that cube
  - how to subdivide the cube then
    - I guess find the "center" point (that's one subproblem)
    - and then using that and the opposite corner you can calculate the remaining six points for each child
 
^ That's a good list

First, then, is figuring out how to define the initial cube from the input. You'll need the minmax for x, y, and z. That's six values...how do you go from that to eight points?

1. (minx, maxy, maxz)
2. (maxx, maxy, maxz)
3. (minx, maxy, minz)
4. (maxx, maxy, minz)
5. (minx, miny, maxz)
6. (maxx, miny, maxz)
7. (minx, miny, minz)
8. (maxx, miny, minz)

Binary, duh

Okay, next, how do you find the "center"? I guess take the average of each dimension

And you should be able to determine if a cube is a point by checking if all eight points are the same

So then the next thing is figuring out if cube is in the range of nanobot. I think this comes down to two subproblems as well:

1. Finding the corner that is closest to the bot
2. Figuring out if that corner is within the bot's range

Okay, I think I have enough to go then

...

I've tried BFS and DFS but both have some serious flaws that make it take forever.

The problem with DFS is that spend a ton of time early on going down paths you have no business going down. Like, the first point is always the upper left corner, and there are just so many subprisms to go through before you get to a reasonable answer where you can start to go through fewer subprisms. This is bad enough in the test case where it takes 16 seconds to resolve, but in the actual problem it runs for a long time before even finding the first "best" solution...I haven't seen it get there yet.

The problem with BFS is that you get ties and so have to consider lots of potential subprisms.

I think a reasonable solution might be:
  
1. Get a baseline: do a dumb BFS where, in the case of a tie, you just pick the first one
2. Do a DFS where you've already set the baseline

And on that front I know I've found one that gives me 856 overlaps, so I can do a DFS where I ignore anything less than that number...

Wait a minute...what about a tie where, in the case of a tie, you choose the prism that is closest to the origin. Hm, that might be assailable.

I also think, on the basis of the logging I added today, that running it overnight might give me an answer.

Or, how about this, when you have a tie, you define your new prism as the minx, maxx, miny, etc. of all the prisms that are tied. That would work great, though I think there will be cases where that new prism will equal the existing prism, but maybe then and only then I could add those subprisms to the prisms under consideration.

So right now my ideas are:

1. DFS but seed it with us not being willing to consider prisms with a number of overlaps < 156 and a known starting point that is too low so we won't consider any prism where all points are closer to the origin than what we have there
2. Run the BFS overnight
3. BFS but instead of considering all subprisms in the case of a tie, turn that into a prism using the minx, maxx, miny, etc. available and only creating a list in the cases where that creates a prism that is equal in size to the original prism

I'm cool doing those three in different branches, with `main` as is being a good candidate for #2. First I should maybe double check all my tests are still successful now that I've merged my branches and resolved conflicts
