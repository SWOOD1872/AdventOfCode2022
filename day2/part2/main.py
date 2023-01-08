from collections import namedtuple
from enum import Enum, auto

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
with open("input.txt") as f:
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
