#!/usr/bin/env python3

import sys

from argparse import ArgumentError
from gig import Gig, GigError

def main():
    try:
        gi = Gig()
        gi.execute(sys.argv)
    except GigError as err:
        print(err)
        sys.exit(1)
    except ArgumentError as err:
        print(err)
        sys.exit(2)
    except NotImplementedError:
        print("Not implemented")
        sys.exit(1)


if __name__ == "__main__":
    main()
