import sys
from collections import namedtuple
from pathlib import Path

proj_path = Path(__file__).parents[1].resolve()
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = "2022"
DAY = "04"
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

# Structure the data
SectionAssignment = namedtuple("SectionAssignment", "start end")
section_assignments: list[tuple[SectionAssignment, SectionAssignment]] = []
for line in input_data:
    sa1, sa2 = line.split(",")
    sa1_start, sa1_stop = sa1.split("-")
    sa2_start, sa2_stop = sa2.split("-")
    section_assignments.append(
        (
            SectionAssignment(int(sa1_start), int(sa1_stop)),
            SectionAssignment(int(sa2_start), int(sa2_stop)),
        )
    )

# Find any section assignments which fully contain the other
fully_contained_count: int = 0
for sa_pair in section_assignments:
    sa1, sa2 = sa_pair

    # If sa1 fully contains sa2
    if int(sa1.start) <= int(sa2.start) and int(sa1.end) >= int(sa2.end):
        fully_contained_count += 1
    # If sa2 fully contains sa1
    elif int(sa2.start) <= int(sa1.start) and int(sa2.end) >= int(sa1.end):
        fully_contained_count += 1

print(f"Answer: {fully_contained_count}")
