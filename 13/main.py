"""AOC 2024 - Day 13: Claw Contraption."""

from __future__ import annotations

import re
import time
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeAlias, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

Pair: TypeAlias = tuple[int, int]
Button = Pair
Prize = Pair
GameInfo: TypeAlias = dict[Prize, tuple[Button, Button]]

REGEX = (
    r"Button A: X\+(\d+), Y\+(\d+)\s*"
    r"Button B: X\+(\d+), Y\+(\d+)\s*"
    r"Prize: X=(\d+), Y=(\d+)"
)

PART2_OFFSET = 10_000_000_000_000


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
        print(f"{func.__name__}() took {elapsed_time_ms:.3f} ms")
        return result

    return wrapper


@timer
def get_data() -> GameInfo:
    """Process the input file, return in a suitable format."""
    with Path("./input.txt").open() as file:
        data = file.read()

    matches = re.findall(REGEX, data)

    return {
        (int(match[4]), int(match[5])): (  # Prize tuple as key
            (int(match[0]), int(match[1])),  # Button A tuple
            (int(match[2]), int(match[3])),  # Button B tuple
        )
        for match in matches
    }


def play_claw_machine(
    prize: Prize, button_a: Button, button_b: Button
) -> int | None:
    """Solve the claw machine using Cramer's Rule."""
    prize_x, prize_y = prize
    a_x, a_y = button_a
    b_x, b_y = button_b

    # Compute determinants
    D = a_x * b_y - a_y * b_x  # noqa: N806
    if D == 0:
        return None  # No unique solution

    D_a = prize_x * b_y - prize_y * b_x  # noqa: N806
    D_b = a_x * prize_y - a_y * prize_x  # noqa: N806

    # Check if solutions are integers
    if D_a % D != 0 or D_b % D != 0:
        return None  # No integer solution

    count_a = D_a // D
    count_b = D_b // D

    # Ensure non-negative solutions
    if count_a < 0 or count_b < 0:
        return None  # No valid solution

    return count_a * 3 + count_b


@timer
def part1(data: GameInfo) -> int:
    """Solve Part 1.

    My original part 1 was a brute-force since I'd not sussed out that 'Cramer's
    Rule' would help here and part 2. This is the re-written solution using
    Cramer.
    """
    total_tokens = 0

    # Iterate over each prize and button configuration
    for prize, (button_a, button_b) in data.items():
        min_cost = play_claw_machine(prize, button_a, button_b)
        if min_cost is not None:
            total_tokens += min_cost

    return total_tokens


@timer
def part2(data: GameInfo) -> int:
    """Solve Part 2, applying the PART2_OFFSET.

    Was totally stumped here, until I got the hint about 'Cramer's Rule'. It's
    Been 30+ years since i learned maths :D.
    """
    total_tokens = 0

    # Apply the offset to all prize coordinates
    data = {
        (prize_x + PART2_OFFSET, prize_y + PART2_OFFSET): buttons
        for (prize_x, prize_y), buttons in data.items()
    }

    # Iterate over each prize and button configuration
    for prize, (button_a, button_b) in data.items():
        min_cost = play_claw_machine(prize, button_a, button_b)
        if min_cost is not None:
            total_tokens += min_cost

    return total_tokens


@timer
def main() -> None:
    """Run the AOC problems for Day 13."""
    data = get_data()

    # Part 1 - answer for me is 28059
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is 102255878088512
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()

# ---------------------------------- timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ------------------------------- Python 3.13.1 ------------------------------ #
# ---------------------------------------------------------------------------- #
# get_data :  0.358 ms
#    part1 : 0.065 ms
#    part2 : 0.152 ms
#    Total : 0.602 ms
