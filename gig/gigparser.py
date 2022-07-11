import argparse
import sys

class GigParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(2)
