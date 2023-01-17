import re
import sys
from pathlib import Path

proj_path = Path(__file__).parents[1].resolve()
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = "2022"
DAY = "05"
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

# Hard coded the stack to avoid having to parse the stack from the input file
# Each crate stack is TOP -> BOTTOM
stack: dict[int, list[str]] = {
    1: ["V", "J", "B", "D"],
    2: ["F", "D", "R", "W", "B", "V", "P"],
    3: ["Q", "Q", "C", "D", "L", "F", "G", "R"],
    4: ["B", "D", "N", "L", "M", "P", "J", "W"],
    5: ["Q", "S", "C", "P", "B", "N", "H"],
    6: ["G", "N", "S", "B", "D", "R"],
    7: ["H", "S", "F", "Q", "M", "P", "B", "Z"],
    8: ["F", "L", "W"],
    9: ["R", "M", "F", "V", "S"],
}


def move_crate(
    num: int, stack_from: list[str], stack_to: list[str]
) -> tuple[list[str], list[str]]:
    # Get the crates to move
    crates_to_move: list[str] = stack_from[:num]

    # Move the crates one at a time
    new_stack_to: list[str] = stack_to
    for crate in crates_to_move:
        new_stack_to.insert(0, crate)

    # Remove the moved crates from the previous stack
    new_stack_from: list[str] = stack_from
    del new_stack_from[:num]

    return (new_stack_from, new_stack_to)


def main() -> None:
    # Input data
    with open(input_file) as f:
        input_data = f.read().split("\n")

    # Rearrange of the crates
    for moves in input_data:
        move = re.findall(r"\b\d+\b", moves)
        quantity = int(move[0])  # Number of crates to move
        stack_from = int(move[1])  # Where to move crates from
        stack_to = int(move[2])  # Where to move crates to

        # Move the crates
        new_stack_from, new_stack_to = move_crate(
            quantity, stack[stack_from], stack[stack_to]
        )
        stack[stack_from] = new_stack_from
        stack[stack_to] = new_stack_to

    # List the crates on top of each crate stack
    crates_on_top: list[str] = []
    for crate_stack in stack.values():
        crates_on_top.append(crate_stack[0])

    print(f"Answer: {''.join(crates_on_top)}")


if __name__ == "__main__":
    main()
