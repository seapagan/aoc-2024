"""AOC 2024 - Day 3: 'Mull It Over'.

We will do this using a regex.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Generator, Literal

# This regex will find each proper 'mul(x,y)' string and return a list of each
# pair as a tuple
REGEX_PART1 = r"mul\((\d{1,3}),(\d{1,3})\)"
REGEX_PART2 = r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)"


# get the data in from file
def get_data() -> str:
    """Read the data in from a file and return as a single string."""
    with Path("input.txt").open() as file:
        return file.read()


def get_pairs(input_data: str, regex: str) -> Generator[tuple[int, int], None, None]:
    """Return a GENERATOR with tuple(int,int)."""
    for match in re.finditer(regex, input_data):
        yield (int(match.group(1)), int(match.group(2)))


def get_pairs_with_toggle(
    input_data: str, regex: str
) -> Generator[tuple[int, int], None, None]:
    """Process input sequentially, toggling whether to handle `mul` pairs."""
    toggle = True  # Start with handling enabled
    for match in re.finditer(regex, input_data):
        if match.group(0) == "do()":
            toggle = True
        elif match.group(0) == "don't()":
            toggle = False
        elif match.group(1) and toggle:  # A `mul(x, y)` and toggle is enabled
            yield int(match.group(1)), int(match.group(2))


def part1(data: str) -> int:
    """Return the total for each 'mul()' pair."""
    return sum(x * y for x, y in get_pairs(data, REGEX_PART1))


def part2(data: str) -> int:
    """Return the total for each 'mul()' pair."""
    return sum(x * y for x, y in get_pairs_with_toggle(data, REGEX_PART2))


data = get_data()
part1_result = part1(data)
part2_result = part2(data)

print(f"Result for part1 is {part1_result}")  # for me is 159833790
print(f"Result for part2 is {part2_result}")
