import sys
from pathlib import Path

# Import the util package
home = Path.home()
proj_path = home.joinpath("Documents/Code/Challenges/AdventOfCode2022")
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = 2023
DAY = 1
PART = 2

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

with open(input_file) as f:
    input_data = f.read().split("\n")
input_data.append("")  # This ensures the last value in data is counted

totals = []
total = 0
for calories in input_data:
    if calories:
        total += int(calories)
    else:
        totals.append(total)
        total = 0

top_three = sorted(totals, reverse=True)[:3]

print(f"Answer = {sum(top_three)}")
