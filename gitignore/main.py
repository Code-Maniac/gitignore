#!/usr/bin/env python3

import sys

from argparse import ArgumentError
from gitignore import GitIgnore, GitIgnoreError

def main():
    try:
        gi = GitIgnore()
        gi.execute(sys.argv)
    except GitIgnoreError as err:
        print(err)
        sys.exit(1)
    except ArgumentError as err:
        print(err)
        sys.exit(2)
    except NotImplementedError:
        print("Hit not implemented")
        sys.exit(1)


if __name__ == "__main__":
    main()
