"""AOC 2024 - Day 1: 'Historian Hysteria'."""

from collections import Counter


# ------------------------ read in and return the data ----------------------- #
def get_data() -> tuple[list[int], list[int]]:
    with open("input.txt", "r") as file:
        # Read and process all lines, splitting into two sorted arrays
        data = [tuple(map(int, line.strip().split())) for line in file]

    # Unzip and sort
    array1, array2 = zip(*data)
    return sorted(array1), sorted(array2)


# ---------------------- calculate the answer for part 1 --------------------- #
def part1(array1, array2):
    running_total = sum(abs(a - b) for a, b in zip(array1, array2))
    return running_total


# ---------------------- calculate the answer for part 2 --------------------- #
def part2(array1, array2):
    similarity = 0
    array2_counts = Counter(array2)

    for num in array1:
        similarity += num * array2_counts[num]

    return similarity


first, second = get_data()  # O(n)
part1_answer = part1(first, second)  # O(n) since both arrays are the same size
part2_answer = part2(first, second)  # O(n + m)

print(f"Answer to Part 1 is {part1_answer}")  # for me it is 1388114
print(f"Answer to Part 2 is {part2_answer}")  # for me it is 23529853
