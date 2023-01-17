import sys
from collections import namedtuple
from pathlib import Path

proj_path = Path(__file__).parents[1].resolve()
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = "2022"
DAY = "04"
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

# Find any overlaps and count them
overlaps_count: int = 0
for sa_pair in section_assignments:
    sa1, sa2 = sa_pair

    # If the start or end of section assignment 1 is between the start and end of
    # section assignment 2, there is an overlap
    if sa1.start in range(sa2.start, sa2.end + 1) or sa1.end in range(
        sa2.start, sa2.end + 1
    ):
        overlaps_count += 1
    # If the start or end of section assignment 2 is between the start and end of
    # section assignment 1, there is an overlap
    elif sa2.start in range(sa1.start, sa1.end + 1) or sa2.end in range(
        sa1.start, sa1.end + 1
    ):
        overlaps_count += 1

print(f"Answer: {overlaps_count}")
