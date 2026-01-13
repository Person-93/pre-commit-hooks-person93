"""Forbid binary files
pre-commit uses the "identify" python library to detect binary files
"""

import sys
import subprocess


def main():
    binary_files = sys.argv[1:]

    if len(binary_files) == 0:
        sys.exit()

    try:
        output = subprocess.run(
            args=["git", "check-attr", "filter", "--", *binary_files],
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
        ).stdout.decode()
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

    found_untracked = False

    for line in output.splitlines():
        [file, _, filter] = line.split(":")
        if filter.strip() == "lfs":
            continue
        found_untracked = True
        sys.stdout.write(f"[ERROR] {file} appears to be a binary file\n")

    if found_untracked:
        sys.exit(1)


if __name__ == "__main__":
    main()
