"""AOC 2024 - Day 3: 'Mull It Over'.

We will do this using a regex.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Generator

# This regex will find each proper 'mul(x,y)' string and return a list of each
# pair as a tuple
REGEX = r"mul\((\d{1,3}),(\d{1,3})\)"


# get the data in from file
def get_data() -> str:
    """Read the data in from a file and return as a single string."""
    with Path("input.txt").open() as file:
        return file.read()


def get_pairs(input_data: str) -> Generator[tuple[int, int], None, None]:
    """Return a GENERATOR with tuple(int,int)."""
    for match in re.finditer(REGEX, input_data):
        yield (int(match.group(1)), int(match.group(2)))


def part1(data: str) -> int:
    """Return the total for each 'mul()' pair."""
    return sum(x * y for x, y in get_pairs(data))


data = get_data()
part1_result = part1(data)

print(f"Result for part1 is {part1_result}")  # for me is 159833790
