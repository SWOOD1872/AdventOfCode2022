import string
import sys
from pathlib import Path

# Import the util package
home = Path.home()
proj_path = home.joinpath("Documents/Code/Challenges/AdventOfCode2022")
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = 2023
DAY = 3
PART = 1

# Core or 'base' input file name
input_file = "input.txt"

# Create a parser with a boolean flag to toggle test mode
parser = util.parser.default_parser(year=YEAR, day=DAY, part=PART)
args = parser.parse_args()

# If test mode (-t | --test) was used, prepend "test_" to the input file name
# to run against a test file instead
if args.test:
    input_file = f"test_{input_file}"

# ========================================== SOLUTION START ==========================================

# Input data
with open(input_file) as f:
    input_data = f.read().split("\n")

# Stores each letter and an associated priority
priority: dict[str, int] = {}
for i, char in enumerate(list(string.ascii_lowercase + string.ascii_uppercase)):
    priority[char] = i + 1

# Loop over each rucksack
sum: int = 0
for rucksack in input_data:
    # Store a list of the items in the rucksack
    items = list(rucksack)
    mid = len(items) // 2
    # Split the rucksack in to two compartments
    c1, c2 = (set(items[:mid]), set(items[mid:]))
    # Loop over the items in the first compartment
    for item in c1:
        # If the item in the first compartment is also found in the
        # second compartment, get the priority for that item and add
        # it to the sum
        if item in c2:
            sum += priority[item]

print(f"Answer: {sum}")
