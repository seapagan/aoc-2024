"""AOC 2024 - Day 9: Disk Fragmenter."""

from __future__ import annotations

import time
from functools import wraps
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class FileInfo:
    """Structure to hold info for each file."""

    id: int
    length: int
    free_space: int


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
def get_data(test_data: str | None = None) -> list[tuple[int, int]]:
    """Process the input file, return in a suitable format."""
    if test_data:
        data = test_data
    else:
        with Path("./input.txt").open() as file:
            data = file.read().strip()

    return [
        (int(data[i]), int(data[i + 1])) if i + 1 < len(data) else (int(data[i]), 0)
        for i in range(0, len(data), 2)
    ]


@timer
def part1(data: list[tuple[int, int]]) -> int:
    """Compact the files then calculate the checksum."""
    # Parse the data into the block layout
    blocks: list[int | str] = []
    for file_id, (file_size, free_space) in enumerate(data):
        blocks.extend([file_id] * file_size)  # Add file blocks
        blocks.extend(["."] * free_space)  # Add free space

    # Two-pointer solution
    for i in range(len(blocks)):
        if blocks[i] == ".":
            write_ptr = i
            break

    read_ptr = len(blocks) - 1  # Start from the end of the list
    while read_ptr >= write_ptr:
        if blocks[read_ptr] != ".":  # Found a file block
            blocks[write_ptr] = blocks[read_ptr]  # Move block to free space
            blocks[read_ptr] = "."  # Mark original position as free

            # Update write_ptr to the next free space
            write_ptr += 1
            while write_ptr < len(blocks) and blocks[write_ptr] != ".":
                write_ptr += 1

        read_ptr -= 1  # Move read pointer backward

    # Calculate the checksum
    checksum = sum(
        index * int(block) for index, block in enumerate(blocks) if block != "."
    )

    return checksum


@timer
def part2(data) -> int:
    """Solve Part 2."""
    total = 0

    return total


def main() -> None:
    """Run the AOC problems for Day 9."""
    # data = get_data("2333133121414131402")
    data = get_data()

    # Part 1 - answer for me is 6259790630969
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is ?
    # result2 = part2(data)
    # print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
