"""AOC 2024 - Day 9: Disk Fragmenter."""

from __future__ import annotations

import time
from bisect import bisect_left
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
        (int(data[i]), int(data[i + 1]))
        if i + 1 < len(data)
        else (int(data[i]), 0)
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

    return sum(
        index * int(block) for index, block in enumerate(blocks) if block != "."
    )


def merge_free_spans(
    spans: list[tuple[int, int]],
    new_span: tuple[int, int],
) -> list[tuple[int, int]]:
    """Merge free spans into sorted order."""
    start, end = new_span
    if not spans:
        return [new_span]

    insert_pos = bisect_left(spans, (start, end))

    merged = spans[:insert_pos]  # All spans before the insertion point
    if merged and merged[-1][1] + 1 >= start:
        # Merge with the last span in the merged list if adjacent/overlapping
        merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    else:
        # Add the new span if no merge is needed
        merged.append((start, end))

    # Add remaining spans, merging if necessary
    for span_start, span_end in spans[insert_pos:]:
        if merged[-1][1] + 1 >= span_start:
            # Merge overlapping/adjacent spans
            merged[-1] = (merged[-1][0], max(merged[-1][1], span_end))
        else:
            # Append non-overlapping spans
            merged.append((span_start, span_end))

    return merged


@timer
def part2(data: list[tuple[int, int]]) -> int:
    """Compact whole files by moving to leftmost free space."""

    def find_leftmost_free_span(
        file_length: int,
        max_position: int,
    ) -> tuple[int, tuple[int, int]] | None:
        """Find the leftmost free span that can fit the file."""
        for index, (span_start, span_end) in enumerate(free_spans):
            if span_start >= max_position:
                break
            if span_end - span_start + 1 >= file_length:
                return index, (span_start, span_end)
        return None

    blocks = parse_data_to_blocks(data)

    # Pre-calculate the file locations
    files: list[tuple[int, int, int]] = []
    current_file_id = -1
    current_file_start = -1

    for i, block in enumerate(blocks):
        if isinstance(block, int):
            if current_file_id == -1:
                current_file_id = block
                current_file_start = i
            elif block != current_file_id:
                files.append((current_file_id, current_file_start, i - 1))
                current_file_id = block
                current_file_start = i
        elif current_file_id != -1:
            files.append((current_file_id, current_file_start, i - 1))
            current_file_id = -1

    if current_file_id != -1:
        files.append((current_file_id, current_file_start, len(blocks) - 1))

    # Sort files by descending ID
    files.sort(reverse=True, key=lambda x: x[0])

    # Initialize free spans
    free_spans: list[tuple[int, int]] = []
    current_free_start = -1

    for i, block in enumerate(blocks):
        if block == ".":
            if current_free_start == -1:
                current_free_start = i
        elif current_free_start != -1:
            free_spans.append((current_free_start, i - 1))
            current_free_start = -1

    if current_free_start != -1:
        free_spans.append((current_free_start, len(blocks) - 1))

    for file_id, file_start, file_end in files:
        file_length = file_end - file_start + 1

        found_span = find_leftmost_free_span(file_length, file_start)

        if found_span is not None:
            span_index, (span_start, span_end) = found_span
            free_start = span_start

            # Move file
            blocks[free_start : free_start + file_length] = [
                file_id
            ] * file_length
            blocks[file_start : file_end + 1] = ["."] * file_length

            # Update free spans
            del free_spans[span_index]
            if free_start + file_length <= span_end:
                free_spans = merge_free_spans(
                    free_spans,
                    (
                        free_start + file_length,
                        span_end,
                    ),
                )

    return sum(
        index * int(block) for index, block in enumerate(blocks) if block != "."
    )


def main() -> None:
    """Run the AOC problems for Day 9."""
    data = get_data()

    # Part 1 - answer for me is 6259790630969
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is 6289564433984
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()

# ---------------------------------- Timings --------------------------------- #
# part1() : 7.860 ms
# part2() : 224.828 ms
