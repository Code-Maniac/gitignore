#!/bin/env python3

import sys
import argparse


def getParser():
    parser = argparse.ArgumentParser(
        description="A tool for managing .gitignore",
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        help="sub-command help")

    # add subparser for the init subcommand
    parser_init = subparsers.add_parser(
        "init",
        help="Initialise the .gitignore file for the git repo. If no schema is specified then init as empty")
    parser_init.add_argument(
        "-f", "--force",
        help="Force overwrite of existing .gitignore")
    parser_init.add_argument(
        "schemas",
        metavar="schemas",
        nargs="*",
        help="A schema or set of schemas to initialise the .gitignore with")

    # add subparser for the add subcommand
    parser_add = subparsers.add_parser(
        "add",
        help="Add the .gitignore scehma to the .gitignore file")
    parser_add.add_argument("schemas", choices="XYZ", help="baz help")

    # add subparser for the add-untracked command
    parser_add_untracked = subparsers.add_parser(
        "add-untracked",
        help="Add any currently untracked files in the git repository to .gitignore")

    # add subparser for the update command
    parse_update = subparsers.add_parser(
        "update",
        help="Update any .gitignore schemas in the .gitignore file to their latest versions")

    # add subparser for the remove command
    parser_remove = subparsers.add_parser(
        "remove",
        help="Remove the .gitignore schema from the .gitignore file")

    return parser


def usage():
    print("HELP")


def main():
    # first argument is the subcommand

    try:
        parser = getParser()
        parser.parse_args()
    except argparse.ArgumentError as err:
        print(err)
        usage()
        sys.exit(2)


if __name__ == "__main__":
    main()
