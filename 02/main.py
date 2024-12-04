"""AOC 2024 - Day 2: 'Red-Nosed Reports'."""


def get_data() -> list[list[int]]:
    with open("./input.txt", "r") as file:
        # Read and process all lines, splitting into two sorted arrays
        data = [list(map(int, line.strip().split())) for line in file]
    if not data:
        raise ValueError("Failed: Input data is empty or invalid")

    return data


def is_safe(report: list[int]) -> bool:
    """Returns True if a report is safe.

    A report is safe if:
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.
    """
    if len(report) < 2:
        return True  # A single-element report is inherently safe

    last_direction = None
    for index in range(len(report) - 1):
        difference = report[index + 1] - report[index]
        if not (1 <= abs(difference) <= 3):
            return False  # not a safe report
        direction = 1 if difference > 0 else -1

        if last_direction is not None and direction != last_direction:
            return False

        last_direction = direction

    return True


def dampened_is_safe(report: list[int]) -> bool:
    """Returns True if a report is safe.

    We have more information!

    A report is safe if:
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.
    - Using the 'problem dampener', we can remove ONE level from each report
    """
    if is_safe(report):
        return True

    # remove one level each time and test again:
    for i in range(len(report)):
        dampened_report = report[:i] + report[i + 1 :]
        if is_safe(dampened_report):
            return True

    return False  # meh we tried!


def part1(reports: list[list[int]]) -> int:
    """Return the number of safe reports."""
    return sum(1 for report in reports if is_safe(report))


def part2(reports: list[list[int]]) -> int:
    """Return the number of safe reports after dampening."""
    return sum(1 for report in reports if dampened_is_safe(report))


data = get_data()
safe_reports = part1(data)
dampened_safe_reports = part2(data)

print(f"Original Number of safe reports : {safe_reports}")  # 224 for me
print(f"After Dampening, we have {dampened_safe_reports} safe reports!")  # ?
