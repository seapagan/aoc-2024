"""AOC 2024 - Day 8: Resonant Collinearity."""

from __future__ import annotations

import time
from collections import defaultdict
from functools import wraps
from pathlib import Path
from typing import (
    Callable,
    ParamSpec,
    TypeAlias,
    TypedDict,
    TypeVar,
)

P = ParamSpec("P")
R = TypeVar("R")

AntennaMap: TypeAlias = defaultdict[str, list[tuple[int, int]]]
Bounds: TypeAlias = tuple[int, int]


class DataDict(TypedDict):
    """Define typing for the get_data() function."""

    antennas: AntennaMap
    bounds: Bounds


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure the execution time of a function in milliseconds.

    This is a decorator that can be added to any function.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time_ms = (end_time - start_time) * 1000
        print(f" [ {func.__name__}() took {elapsed_time_ms:.3f} ms ]")
        return result

    return wrapper


@timer
def get_data(input_file: str = "input.txt") -> DataDict:
    """Process the input file and return in a usable format."""
    with Path(input_file).open() as file:
        antennas: AntennaMap = defaultdict(list)
        rows = 0
        cols = 0

        for line_index, line in enumerate(file):
            stripped_line = line.strip()
            rows += 1
            cols = max(cols, len(stripped_line))
            for pos_index, position in enumerate(stripped_line):
                if position != ".":
                    antennas[position].append((line_index, pos_index))

    bounds: Bounds = rows, cols

    return {"antennas": antennas, "bounds": bounds}


@timer
def part1(data: DataDict) -> int:
    """Solve Part 1 count the number of valid antinodes."""
    antennas = data["antennas"]
    rows, cols = data["bounds"]
    unique_antinodes = set()

    for positions in antennas.values():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                a1 = positions[i]
                a2 = positions[j]

                dx, dy = a2[0] - a1[0], a2[1] - a1[1]

                # find potential canditates
                candidates = [
                    (a2[0] + dx, a2[1] + dy),
                    (a1[0] - dx, a1[1] - dy),
                ]

                for candidate in candidates:
                    if 0 <= candidate[0] < rows and 0 <= candidate[1] < cols:
                        d1 = abs(candidate[0] - a1[0]) + abs(candidate[1] - a1[1])
                        d2 = abs(candidate[0] - a2[0]) + abs(candidate[1] - a2[1])

                        if d1 == 2 * d2 or d2 == 2 * d1:
                            unique_antinodes.add(candidate)

    return len(unique_antinodes)


@timer
def part2(data: DataDict) -> int:
    """
    Solve Part 2 by finding all valid antinodes based on in-line points between antennas.
    """
    from math import gcd

    antennas = data["antennas"]
    rows, cols = data["bounds"]
    antinodes = set()

    for positions in antennas.values():
        if len(positions) < 2:
            continue

        # Include all antennas as antinodes
        for position in positions:
            antinodes.add(position)

        # Process all unique pairs of antennas
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                a1 = positions[i]
                a2 = positions[j]

                dx, dy = a2[0] - a1[0], a2[1] - a1[1]
                step_x, step_y = dx // gcd(dx, dy), dy // gcd(dx, dy)

                # Generate all points between the antennas
                x, y = a1
                while (x, y) != a2:
                    antinodes.add((x, y))
                    x += step_x
                    y += step_y

                # Add the second antenna
                antinodes.add(a2)

                # Extend the line beyond both antennas
                # Forward direction
                x, y = a2[0] + step_x, a2[1] + step_y
                while 0 <= x < rows and 0 <= y < cols:
                    antinodes.add((x, y))
                    x += step_x
                    y += step_y

                # Backward direction
                x, y = a1[0] - step_x, a1[1] - step_y
                while 0 <= x < rows and 0 <= y < cols:
                    antinodes.add((x, y))
                    x -= step_x
                    y -= step_y

    return len(antinodes)


@timer
def main() -> None:
    """Run the AOC problems for Day 8."""

    data = get_data()

    # Part 1 - answer for me is 293
    result1 = part1(data)
    print(f"Part 1: Number of unique antinodes is {result1}")

    # Part 2 - answer for me is 934
    result2 = part2(data)
    print(f"Part 2: Taking into account resonance, we have {result2} unique antinodes")


if __name__ == "__main__":
    main()

# Timing on my machine:
# -> get_data() took 0.085 ms
# -> part1() took 0.104 ms
# -> part2() took 0.204 ms
#
# -> In total: 0.414 ms
