"""AOC 2024 - Day 7: Bridge Repair."""

from pathlib import Path
from typing import Optional


def get_data(
    test_data: Optional[str] = None,
) -> list:
    """Get the input data."""
    if test_data:
        data = test_data.split()
    else:
        with Path("./input.txt").open() as file:
            data = file.readlines()

    # pre-process if needed.

    return data


def part1(data) -> int:
    """Solve part 1 of the puzzle."""
    result = 0

    return result


def part2(data) -> int:
    """Solve part 2 of the puzzle."""
    result = 0

    return result


test_data = """
"""


def main() -> None:
    """Run the AOC problems for Day 6."""
    data = get_data()

    # Part 1 - answer for me is 5129
    result1 = part1(data)
    print(f"Part 1: {result1}.")

    # Part 2 - answer for me is 1888
    result2 = part2(data)
    print(f"Part 2: {result2}.")


if __name__ == "__main__":
    main()
