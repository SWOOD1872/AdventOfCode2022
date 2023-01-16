import argparse


def default_parser(year: int, day: int, part: int) -> argparse.ArgumentParser:
    # Create the parser
    parser = argparse.ArgumentParser(
        description=f"Advent of Code {year} Day {day} Part {part}"
    )

    # Add the boolean test flag to the parser
    parser.add_argument(
        "-t", "--test", action="store_true", help="Use the test input file"
    )

    return parser
