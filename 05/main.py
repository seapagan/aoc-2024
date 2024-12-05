"""AOC 2024 - Day 5: Print Queue."""

from collections import defaultdict
from pathlib import Path


# ------------------------------ get the data in ----------------------------- #
def get_data() -> tuple[list[tuple[int, ...]], list[list[int]]]:
    """Read in the input data and return.

    The data is in 2 sections separated by an empty line. We will return a tuple
    that can be unpacked with both sections separate.

    Section 1 will be the 'page ordering rules' as a list of tuples each
    containing 2 integers.

    Section 2 will be the 'page numbers of each update' as a list of Sets, each
    set containing only integers.
    """
    rules: list[tuple[int, ...]] = []
    updates: list[list[int]] = []

    first_section = True

    with Path("./input.txt").open() as file:
        for line in file:
            line = line.strip()
            if not line:
                first_section = False
                continue

            if first_section:
                rules.append(tuple(map(int, line.split("|"))))
            else:
                updates.append(list(map(int, line.split(","))))

    return rules, updates


def preprocess_rules() -> defaultdict[int, set[int]]:
    """Convert rules into a defaultdict for faster lookups."""
    rule_dict = defaultdict(set)
    for x, y in rules:
        rule_dict[x].add(y)
    return rule_dict


def part1() -> int:
    """Identify which updates are in the correct order."""
    rule_dict = preprocess_rules()
    count = 0

    for update in updates:
        valid = True
        for page in update:
            # Check if this page has any constraints
            if page in rule_dict:
                for after_page in rule_dict[page]:
                    if after_page in update:
                        # Validate the order
                        if update.index(page) > update.index(after_page):
                            valid = False
                            break
            if not valid:
                break

        if valid:
            # This is a valid update
            middle_number = update[len(update) // 2]
            count += middle_number

    return count


# -------------------------------- do the work ------------------------------- #
rules, updates = get_data()

part1_result = part1()  # 6949 for my data

print(f"Updates in the Correct Order are: {part1_result}")  # 6949 for me.
