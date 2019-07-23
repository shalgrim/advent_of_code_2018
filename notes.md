## Day 15

### Part One

#### Test Case Two

I think I see the problem here. After 33 rounds there is an elf with two HP that has a goblin above and below it. So in round 34, the goblin above it kills it, so when it comes to the goblin below's turn, that goblin should attack the elf that is to its left but it doesn't seem to be doing that.

The issue seems to be when `attackables` gets defined in `attack()` it doesn't check for attackables to have hp > 0
