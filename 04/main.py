"""AOC 2024 - Day 4: Ceres Search."""

from pathlib import Path


# ----------------------------- support functions ---------------------------- #
def read_data() -> list[str]:
    """Read the data in from the provided file."""
    with Path("./input.txt").open() as file:
        return [line.strip() for line in file]


def part1(grid: list[str]) -> int:
    """Part one - how many ways can we find 'XMAS' in the grid."""

    def is_valid(nr: int, nc: int, char: str) -> bool:
        return 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == char

    count = 0

    rows, cols = len(grid), len(grid[0])

    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ]
    target = "XMAS"
    target_chars = list(target)
    target_len = len(target)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != target_chars[0]:
                continue
            for dr, dc in directions:
                if all(
                    is_valid(r + dr * i, c + dc * i, target_chars[i])
                    for i in range(target_len)
                ):
                    count += 1

    return count


# -------------------------------- do the work ------------------------------- #
data = read_data()

# O(n^2) - answer for me is 2458
print(f"Answer for Part 1 (number of 'XMAS' in the grid) is {part1(data)}")
