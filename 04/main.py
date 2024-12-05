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


def part2(grid: list[str]) -> int:
    """Count the number of X-MAS patterns in the grid."""
    rows, cols = len(grid), len(grid[0])
    count = 0

    if rows < 3 or cols < 3:
        return 0  # anything less than 3x3 grid wont work anyway.

    # Check if we can form two 'MAS' segments in the X
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Center must be 'A'
            if grid[r][c] != "A":
                continue

            # Check all possible diagonal configurations
            top_left = grid[r - 1][c - 1]
            top_right = grid[r - 1][c + 1]
            bottom_left = grid[r + 1][c - 1]
            bottom_right = grid[r + 1][c + 1]

            if (top_left + bottom_right in {"MS", "SM"}) and (
                top_right + bottom_left in {"MS", "SM"}
            ):
                count += 1

    return count


# -------------------------------- do the work ------------------------------- #
data = read_data()


# O(n^2) for square grid - answer for me is 2458
print(f"Answer for Part 1 (number of 'XMAS' in the grid) is {part1(data)}")

# O(n^2) for square grid - answer for me is 1737
print(f"Answer for Part 2 (number of 'X-MAS' in the grid) is {part2(data)}")
