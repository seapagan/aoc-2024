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


# @timer
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


def parse_data_to_blocks(data: list[tuple[int, int]]) -> list[int | str]:
    """Parse the data into the block layout."""
    blocks: list[int | str] = []
    for file_id, (file_size, free_space) in enumerate(data):
        blocks.extend([file_id] * file_size)  # Add file blocks
        blocks.extend(["."] * free_space)  # Add free space
    return blocks


@timer
def part1(data: list[tuple[int, int]]) -> int:
    """Compact the files then calculate the checksum."""
    blocks = parse_data_to_blocks(data)

    for i in range(len(blocks)):
        if blocks[i] == ".":
            write_ptr = i
            break

    read_ptr = len(blocks) - 1
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
    return sum(index * int(block) for index, block in enumerate(blocks) if block != ".")


@timer
def part2(data: list[tuple[int, int]]) -> int:
    """Compact whole files by moving to leftmost free space.

    I'm really not happy with this answer as it takes 4s on my beast of a CPU,
    I'll revisit it later I think.
    """
    blocks = parse_data_to_blocks(data)

    # Precompute file locations in a single pass
    files: list[tuple[int, int, int]] = []
    current_file_id: int = -1
    current_file_start: int = -1

    for i, block in enumerate(blocks):
        if isinstance(block, int):
            if current_file_id == -1:
                current_file_id = block
                current_file_start = i
            elif block != current_file_id:  # New file starts
                files.append((current_file_id, current_file_start, i - 1))
                current_file_id = block
                current_file_start = i
        elif current_file_id != -1:  # End of current file
            files.append((current_file_id, current_file_start, i - 1))
            current_file_id = -1
            current_file_start = -1

    # Handle last file if it exists
    if current_file_id != -1:
        files.append((current_file_id, current_file_start, len(blocks) - 1))

    # Sort files by descending ID
    files.sort(reverse=True, key=lambda x: x[0])

    def find_leftmost_free_space(
        blocks: list[int | str],
        file_length: int,
        max_position: int,
    ) -> int | None:
        start = None
        for i in range(max_position):
            if blocks[i] == ".":
                if start is None:
                    start = i
                if i - start + 1 == file_length:
                    return start
            else:
                start = None
        return None

    # Process each file in descending ID order
    for file_id, file_start, file_end in files:
        file_length = file_end - file_start + 1

        # Find leftmost free space
        free_start = find_leftmost_free_space(blocks, file_length, file_start)

        if free_start is not None:
            # Move file
            blocks[free_start : free_start + file_length] = [file_id] * file_length
            blocks[file_start : file_end + 1] = ["."] * file_length

    # Calculate the checksum
    return sum(index * int(block) for index, block in enumerate(blocks) if block != ".")


def main() -> None:
    """Run the AOC problems for Day 9."""
    data = get_data("2333133121414131402")
    # data = get_data()

    # Part 1 - answer for me is 6259790630969
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is 6289564433984
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
