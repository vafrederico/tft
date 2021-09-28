Hobby implementation of best effort simulator for TFT fights with hard assumptions made for easier development, after getting tired of making different spreadsheets when wanting to compare different builds.

Assumptions may change at any time.

Calculations and logic may be wrong.

### Some current assumptions: 
- Pieces are always in range to each other
- Fights end when a new target can't be found
- Order of calculations for damage (eg: Giant Slayer calculated on pre-knight mitigation)


### Implemented:
- Basic item / trait system
- Ticking game loop for attacking / casting
- Simplified Mana-lock (mana may be gained for certain cases like blue buff, but mana lock also locks casting)


### To Do:
- Testing
- Mana-generation from damge taken
- Debuffs (stun, shred, burn, etc)
- Items as necessary for specific simulations
- Proper statistics and comparison between different solutions
- Move out of global game loop and board (easily done, but not high pri)
- Item knowledge of components for base stats
- Maybe: movement and grid positioning (eg:for simluating advantages of RFC)


### Non-goal:
- Achieve perfect simulation
- 100% coverage of all items/traits/effects
- Multi-threading/processing (might change if more comparisons are done in parallel)
- Easy-to-use GUI / web app