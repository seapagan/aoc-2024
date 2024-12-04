"""AOC 2024 - Day 3: 'Mull It Over'.

We will do this using a regex.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Generator

# This regex will find each proper 'mul(x,y)' string and return a list of each
# pair as a tuple. It will also match the `do()` and `don't()` for the second
# part
REGEX = r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)"


# get the data in from file
def get_data() -> str:
    """Read the data in from a file and return as a single string."""
    with Path("input.txt").open() as file:
        return file.read()


def get_pairs(
    input_data: str,
    *,
    use_toggle: bool = False,
) -> Generator[tuple[int, int], None, None]:
    """Process input sequentially.

    Optionally, use the toggle marks whether to handle or ignore `mul` pairs."""
    toggle = True
    for match in re.finditer(REGEX, input_data):
        if use_toggle:
            if match.group(0) == "do()":
                toggle = True
                continue
            elif match.group(0) == "don't()":
                toggle = False
                continue

        if match.group(1) and toggle:
            yield int(match.group(1)), int(match.group(2))


def calculate(data: str, *, use_toggle: bool = False) -> int:
    """Return the total for each 'mul()' pair.

    Optionally, pay attention to the toggle commands.
    """
    return sum(x * y for x, y in get_pairs(data, use_toggle=use_toggle))


data = get_data()
part1_result = calculate(data)
part2_result = calculate(data, use_toggle=True)

print(f"Result for part1 is {part1_result}")  # for me is 159833790
print(f"Result for part2 is {part2_result}")  # for me is 89349241
