"""AOC 2024 - Day x: xxxx."""

from __future__ import annotations

import time
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeVar

from rich import box
from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

timing_results = []


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure the execution time of a function in milliseconds."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time_ms = (time.perf_counter() - start_time) * 1000
        timing_results.append((func.__name__, elapsed_time_ms))
        return result

    return wrapper


def print_timings() -> None:
    """Pretty-print the timing results for all decorated functions."""
    console = Console()
    table = Table(show_header=False, title="Timing Results", box=box.ROUNDED)

    table.add_column(justify="left", style="cyan", no_wrap=True)
    table.add_column(justify="right", style="green")

    for idx, (func_name, elapsed_time) in enumerate(timing_results):
        is_last = idx == len(timing_results) - 1
        is_second_to_last = idx == len(timing_results) - 2

        display_name = (
            "Total Runtime" if is_last and func_name == "main" else func_name
        )

        table.add_row(
            display_name,
            f"{elapsed_time:.3f} ms",
            end_section=is_second_to_last and timing_results[-1][0] == "main",
        )

    console.print()
    console.print(table, style="grey50")


@timer
def get_data() -> list[str]:
    """Process the input file, return in a suitable format."""
    with Path("./input.txt").open() as file:
        return file.readlines()


@timer
def part1(
    data: list[str],
) -> int:
    """Solve Part 1."""
    total = 0

    return total


@timer
def part2(
    data: list[str],
) -> int:
    """Solve Part 2."""
    total = 0

    return total


@timer
def main() -> None:
    """Run the AOC problems for Day x."""
    data = get_data()

    # Part 1 - answer for me is ?
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is ?
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
    print_timings()

# ---------------------------------- Timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ------------------------------- Python 3.13.1 ------------------------------ #
# ---------------------------------------------------------------------------- #
# get_data : x.xxx ms
#    part1 : x.xxx ms
#    part2 : x.xxx ms
#    Total : x.xxx ms
