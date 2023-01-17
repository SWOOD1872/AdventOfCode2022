import string
import sys
from pathlib import Path

proj_path = Path(__file__).parents[1].resolve()
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = "2022"
DAY = "03"
PART = "01"

# Create a parser with a boolean flag to toggle test mode
parser = util.parser.default_parser(year=YEAR, day=DAY, part=PART)
args = parser.parse_args()

# Core or "base" input file name
input_file = "input.txt"

# If test mode (-t | --test) was used, prepend "test_" to the input file name
# to run against a test file instead
if args.test:
    input_file = f"test_{input_file}"

# Get the absolute path of the input file
input_file = str(Path(f"day{DAY}", input_file).resolve())

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
