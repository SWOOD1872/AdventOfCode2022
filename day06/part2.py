import re
import sys
from pathlib import Path

proj_path = Path(__file__).parents[1].resolve()
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = "2022"
DAY = "06"
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

# Input data
with open(input_file) as f:
    input_data = f.read().split("\n")

# ========================================== SOLUTION START ==========================================


def start_of_marker(stream_buffer: str, marker_size: int) -> int:
    for i, _ in enumerate(stream_buffer):
        marker_end: int = i + marker_size
        chars = stream_buffer[i:marker_end]
        if len(chars) == len(set(chars)):
            return marker_end
    return -1


markers: list[int] = []
for stream_buffer in input_data:
    marker = start_of_marker(stream_buffer=stream_buffer, marker_size=14)
    markers.append(marker)

print(f"Answers: {markers}")
