import sys
from collections import namedtuple
from enum import Enum, auto
from pathlib import Path

proj_path = Path(__file__).parents[1].resolve()
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = "2023"
DAY = "02"
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

# Store the possible moves
class Moves(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


# Store what move each letter represents
move_map = {
    "A": Moves.ROCK,
    "B": Moves.PAPER,
    "C": Moves.SCISSORS,
}

# Store what move beats what
winning_moves = {
    Moves.ROCK: Moves.SCISSORS,
    Moves.PAPER: Moves.ROCK,
    Moves.SCISSORS: Moves.PAPER,
}
# Stores what move loses to what
losing_moves = {
    Moves.ROCK: Moves.PAPER,
    Moves.PAPER: Moves.SCISSORS,
    Moves.SCISSORS: Moves.ROCK,
}

# Store how much points each move earns when it wins
move_points = {Moves.ROCK: 1, Moves.PAPER: 2, Moves.SCISSORS: 3}

# Stores how much points are earned for a win, draw and loss
result_points = {"win": 6, "draw": 3, "lose": 0}

# Get the game data
with open(input_file) as f:
    rounds = f.readlines()

# Structure the data
Move = namedtuple("Move", "opp res")
moves: list[Move] = []
for round in rounds:
    round_moves = round.split(" ")
    opp = round_moves[0].strip()  # Opposition moves
    res = round_moves[1].strip()  # Response
    moves.append(Move(opp=opp, res=res))

total_points: list[int] = []
for move in moves:
    opp_move = move_map[move.opp]
    # X: Lose | Y: Draw | Z: Win
    if move.res == "X":
        res_move = winning_moves[opp_move]
    if move.res == "Y":
        res_move = opp_move
    if move.res == "Z":
        res_move = losing_moves[opp_move]

    points = 0

    # Win
    if winning_moves[res_move] == opp_move:
        points += result_points["win"]

    # Draw
    if opp_move == res_move:
        points += result_points["draw"]

    points += move_points[res_move]
    total_points.append(points)

print(f"Answer: {sum(total_points)}")
