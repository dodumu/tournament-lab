# TournamentLab

A Python command-line league manager: register teams, generate a round-robin
schedule, enter scores, and get a league table and champion recomputed from
the match records. Standard library only.

## Run it

    python3 main.py

## Run the tests

    python3 -m unittest -v

## Menu

1 register team, 2 list teams, 3 generate schedule, 4 list fixtures,
5 record result, 6 standings, 7 save, 8 load, 9 champion,
10 simulate demo fixtures (asks you to type YES), 0 quit.

## Rules

- 4-8 teams; names are 2-30 characters after trimming, unique ignoring case.
- Single round-robin: every pair meets once, N*(N-1)/2 fixtures.
- Win 3 points, draw 1 each, loss 0.
- A score is a whole number >= 0 (booleans, floats and negatives are rejected).
- A fixture accepts a result once; there is no edit operation.
- The schedule is generated once and teams cannot be added afterwards.

## Tie-breakers (in order)

1. points, highest first
2. goal difference, highest first
3. goals for, highest first
4. team name A-Z (trimmed, casefolded)

There is no head-to-head rule.

## Example season

(Write your own: the two-result table from Step 10d, and the final champion.)