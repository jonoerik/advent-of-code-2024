# Advent of Code 2024
Solutions by jonoerik \
[https://adventofcode.com/2024/](https://adventofcode.com/2024/)

| Day | Solved |
| --- | --- |
| 1 | ✔✔ |
| 2 | ✔✔ |
| 3 | ✔✔ |
| 4 | ✔✔ |
| 5 | ✔✔ |
| 6 | ✔✔ |
| 7 | ✔✔ |
| 8 | ✔✔ |
| 9 | ✔✔ |
| 10 | ✔✔ |
| 11 | ✔✔ |
| 12 | ✔✔ |
| 13 | ✔✔ |
| 14 | ✔✔ |
| 15 | ✔✔ |
| 16 | ✔✔ |
| 17 | ✔✔ |
| 18 | ✔✔ |
| 19 | ✔✔ |
| 20 | ✔✔ |
| 21 | ✔✔ |
| 22 | ✔✔ |
| 23 | ✔✔ |
| 24 | ✔❌ |
| 25 | ❌❌ |

## Setup
```
cd advent-of-code-2024
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running
`python3 aoc2024.py --help` \
Show program usage and arguments \
`python3 aoc2024.py 05 --part2 day05/data/input` \
Run puzzle solution for day 05, part 2, with puzzle input from file `day05/data/input` \
`python3 aoc2024.py 11 -1 day11/data/sample2 -e blinks=6` \
Run puzzle solution for day 11, part 1, with input file `day11/data/sample2`, and the `blinks` keyword argument set to 6.

## Unit Tests
To use pytest unit tests, add files to the data directory of each day following this pattern:
| filename | content |
| --- | --- |
| sample1 | Input data for the first example given in the puzzle. |
| sample1.answer1 | Expected answer for part 1, when given sample1 as input. |
| sample1.answer2 | Expected answer for part 2, when given sample1 as input. |
| sample2 | Input data for the second example. Follow the same pattern for all additional examples. |
| input | Main puzzle input file. |
| input.answer1 | Expected answer for part 1. |
| input.answer2 | Expected answer for part 2. |

For puzzle parts that have keyword arguments, answer files can be either just the expected answer for the default argument values, or:
```
keyword_1=value,keyword_2=value: answer
keyword_1=other_value,keyword_2=other_value: other_answer
...etc...
```
With one line per set of different keyword argument values.

### Usage:
`pytest -v` \
Run all tests, showing the name and result of each. \
`pytest -v -k day13` \
Run all tests for day13. \
`pytest -v -k 'main and part2'` \
Run tests for the second part of all puzzles, only on the main input file. \
`pytest -v -k 'sample' --durations=0` \
Run all sample tests (examples given in the puzzle descriptions), and report test duration for longer-running tests.
