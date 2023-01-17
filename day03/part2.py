import string
import sys
from pathlib import Path

proj_path = Path(__file__).parents[1].resolve()
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = "2022"
DAY = "03"
PART = "02"

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

# Get a list of the groups
groups: list[list[str]] = []
for i in range(0, len(input_data), 3):
    group = input_data[i : i + 3]
    groups.append(group)

# Calculate the priority for each group and sum it
sum: int = 0
for i, group in enumerate(groups):
    # Get the unique items from each set and store them
    fr, sr, tr = (set(group[0]), set(group[1]), set(group[2]))
    # Loop over the items in the first rucksack
    for item in fr:
        # If the item also appears in the second and third rucksacks,
        # get the priority for that item and add it to the sum
        if item in sr and item in tr:
            sum += priority[item]

print(f"Answer: {sum}")
