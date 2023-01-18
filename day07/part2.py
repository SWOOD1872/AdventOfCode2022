import os
import string
import sys
from pathlib import Path
from typing import Any, Dict
import re

proj_path = Path(__file__).parents[1].resolve()
sys.path.append(str(proj_path))
import util

# Basic metadata
YEAR = "2022"
DAY = "07"
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


class FS:
    """A very basic filesystem representation and associated functionality."""

    def __init__(self) -> None:
        self.fs = {
            "/": {"parent": "/", "files": [], "directories": [], "total_size": 0}
        }
        self.current_dir = "/"

    def touch(self, file: str, size: int = 0) -> None:
        """Create a new file."""

        # Full path to the file
        file_path: str = ""
        # Full path to the parent dir of the file
        file_path_dir: str = ""

        # If the file is a fully qualified path
        if file.startswith("/"):
            file_path = file
            file_path_dir = os.path.dirname(file)

            file_dir = self.fs[os.path.dirname(file)]
            file_dir["files"].append({"name": os.path.basename(file), "size": size})
        # Otherwise create the file in the current directory
        else:
            file_path = os.path.join(self.current_dir, file)
            file_path_dir = self.current_dir
            self.fs[self.current_dir]["files"].append({"name": file, "size": size})

        # Update all file sizes
        # Update the size of directory where we created the file
        self.fs[file_path_dir]["total_size"] += size
        # If it was the root directory, simply return
        if file_path_dir == "/":
            return
        # Otherwise, go through each parent directory, until we reach the root directory
        # and update the total size
        file_path_dirs_to_update = os.path.dirname(file_path_dir)
        while file_path_dirs_to_update != "/":
            self.fs[file_path_dirs_to_update]["total_size"] += size
            file_path_dirs_to_update = os.path.dirname(file_path_dirs_to_update)
        # Finally, update the root directory total size
        self.fs["/"]["total_size"] += size

    def mkdir(self, dir_name: str) -> None:
        """Create a new directory."""

        # If the directory is a fully qualified path
        if dir_name.startswith("/"):
            # Can't create a directory if it already exists
            if dir_name in self.fs.keys():
                print(f"Directory '{dir_name}' already exists")
                return

            # Get the parent directory
            parent_dir: str = os.path.dirname(dir_name)

            # Create the directory
            self.fs[dir_name] = {
                "parent": parent_dir,
                "files": [],
                "directories": [],
                "total_size": 0,
            }

            # Update the parent directory
            self.fs[parent_dir]["directories"].append(os.path.basename(dir_name))

        # Otherwise create the directory in the current directory
        else:
            # Dir names can't contain any punctuation
            if any(p in dir_name for p in string.punctuation):
                print("Illegal character in directory name")
                return

            # Get the parent directory
            parent_dir: str = self.current_dir

            # Create the directory
            self.fs[os.path.join(parent_dir, dir_name)] = {
                "parent": parent_dir,
                "files": [],
                "directories": [],
                "total_size": 0,
            }

            # Update the parent directory
            self.fs[parent_dir]["directories"].append(dir_name)

    def ls(self, dir_name: str = None) -> None:
        """List the content of a directory."""

        if dir_name is None:
            dir_name = ""

        # If the directory is a fully qualified path
        if dir_name.startswith("/"):
            # Can't create a directory if it already exists
            if dir_name not in self.fs.keys():
                print(f"Directory '{dir_name}' doesn't exist")
                return
            directory = self.fs[dir_name]
        # Otherwise create the directory in the current directory
        else:
            if dir_name == "":
                dir_name = self.current_dir
                directory = self.fs[dir_name]
            else:
                target_dir = os.path.join(self.current_dir, dir_name)
                if target_dir not in self.fs.keys():
                    print(f"Directory '{target_dir}' doesn't exist")
                    return
                dir_name = target_dir
                directory = self.fs[target_dir]

        print(dir_name)

        # Print files
        for file in directory["files"]:
            filesize = file["size"]
            filename = file["name"]
            print(f"f  {filesize:<12}  {filename}")

        # Print directories
        for directory in directory["directories"]:
            print(f"d  {'0':<12}  {directory}")

    def cd(self, dir_name: str) -> None:
        """Change to a different directory."""

        # ".." means go up one directory, to the parent of the current directory
        if dir_name == "..":
            dir_name = os.path.dirname(self.current_dir)

        # If the directory is a fully qualified path
        if dir_name.startswith("/"):
            # The directory must first exist
            if dir_name not in self.fs.keys():
                print(f"Directory '{dir_name}' doesn't exist")
                return
            self.current_dir = dir_name
        # Otherwise the directory must be in the current directory
        else:
            if any(p in dir_name for p in string.punctuation):
                print("Illegal character in directory name")
                return
            if os.path.join(self.current_dir, dir_name) not in self.fs.keys():
                print(f"Directory '{dir_name}' doesn't exist")
                return
            self.current_dir = os.path.join(self.current_dir, dir_name)


def new_fs() -> FS:
    return FS()


def main() -> None:
    fs = new_fs()

    for line in input_data:
        # If the line is a command
        if line.startswith("$"):
            command = line.strip()
            # We only care about cd commands, not ls commands
            if command.startswith("$ cd"):
                directory = command.split("$ cd")[1].strip()
                fs.cd(directory)
        # Otherwise it's the output of an ls command
        else:
            file_pattern = re.compile(r"^\d+ [\w\.]+$")
            dir_pattern = re.compile(r"^dir [\w0-9]+$")
            listing = line.strip()
            # If it's a file, create the file
            if file_pattern.match(listing):
                file_size, file_name = listing.split(" ")
                fs.touch(file_name, size=int(file_size))
            # If it's a directory, create the directory
            if dir_pattern.match(listing):
                dir_name = listing.split(" ")[1]
                fs.mkdir(dir_name)

    # Calculate the size of the directory to be deleted in order
    # to install the update
    space_available: int = 70_000_000
    update_size: int = 30_000_000
    space_used: int = fs.fs["/"]["total_size"]
    unused_space: int = space_available - space_used
    dirs_with_space: list[int] = []
    for dir_info in fs.fs.values():
        dir_size = dir_info["total_size"]
        if (unused_space + dir_size) >= update_size:
            dirs_with_space.append(dir_size)
    answer: int = sorted(dirs_with_space)[0]
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
