import os
import git

from gigparser import GigParser
from gitignore import Gitignore

# define some error
class GigError(Exception):
    pass

class Gig:
    # the default url for the schemas
    _schemaurl = "https://github.com/github/gitignore"  # ???
    _configdir = os.path.expanduser("~/.config/gitignore")
    _configpath = _configdir + "/config"
    _schemadir = _configpath + "/schemas"

    def __init__(self):
        # first check that git is installed
        if not git.isInstalled():
            raise GigError("E: Git must be installed to use gitignore")
        # first check that we are in an git repository before going any further
        elif not git.isRepo():
            raise GigError("E: Must be in a git repository to use gitignore")

        # create argument parser and parse the args
        self._parser = self._getParser()
        # self._parser.parse_args(sys.argv[1:])

    def execute(self, args):
        parsedArgs = self._parser.parse_args(args)

        # get the subcommand and go from there
        if(parsedArgs.subcommand == "init"):
            self._doInit(parsedArgs)
        elif(parsedArgs.subcommand == "add"):
            self._doAdd(parsedArgs)
        elif(parsedArgs.subcommand == "add-untracked"):
            self._doAddUntracked(parsedArgs)
        elif(parsedArgs.subcommand == "update"):
            self._doUpdate(parsedArgs)
        elif(parsedArgs.subcommand == "remove"):
            self._doUpdate(parsedArgs)


    def _setup(self):
        # check that the schemas exist
        if not (self._schemasExist() or self._initSchemaDir()):
            raise GigError("E: Gitignore schemas are not available")
        elif not self._pullSchemas():  # should this be an error
            print("W: Gitignore schemas could not be updated")

        # path information for the git repository
        self._gitroot = git.getRoot()
        self._gitignorePath = git.getIgnore()
        self._gitignoreExists = os.path.exists(self._gitignorePath)

        # set the initial gitignore content based on whether the gitignore
        # exidsts or not
        if self._gitignoreExists:
            self._gitignoreContent = Gitignore(self._gitignorePath)


    def _doInit(self, args):
        self._setup()

        overwrite = False
        if self._gitignoreExists:
            # prompt user to overwrite the git ignore
            print(".gitignore already exists. Overwrite? [yn]")

            choice = input().lower()
            while choice not in ("y", "n"):
                choice = input.lower()

            if(choice == "y"):
                # overwrite the file
                overwrite = True

        if(overwrite or not self._gitignoreExists):
            # check args fo

            raise NotImplementedError
        else:
            return

    def _doAdd(self, args):
        self._setup()
        raise NotImplementedError

    def _doAddUntracked(self, args):
        self._setup()
        raise NotImplementedError

    def _doUpdate(self, args):
        self._setup()
        raise NotImplementedError

    def _doRemove(self, args):
        self._setup()
        raise NotImplementedError

    # construct the argument parser for gitignore
    def _getParser(self):
        parser = GigParser(
            description="Gig: A tool for managing .gitignore",
        )

        subparsers = parser.add_subparsers(
            title="subcommands",
            description="valid subcommands",
            dest="subcommand",
            help="additional help")

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
        # parser_init.set_defaults(func=self._doInit)

        # add subparser for the add subcommand
        parser_add = subparsers.add_parser(
            "add",
            help="Add the .gitignore scehma to the .gitignore file")
        parser_add.add_argument("schemas", choices="XYZ", help="schemas help")
        # parser_add.set_defaults(func=self._doAdd)

        # add subparser for the add-untracked command
        parser_add_untracked = subparsers.add_parser(
            "add-untracked",
            help="Add any currently untracked files in the git repository to .gitignore")
        # parser_add_untracked.set_defaults(func=self._doAddUntracked)

        # add subparser for the update command
        parser_update = subparsers.add_parser(
            "update",
            help="Update any .gitignore schemas in the .gitignore file to their latest versions")
        # parser_update.set_defaults(func=self._doUpdate)

        # add subparser for the remove command
        parser_remove = subparsers.add_parser(
            "remove",
            help="Remove the .gitignore schema from the .gitignore file")
        # parser_remove.set_defaults(func=self._doRemove)

        return parser

    # initialise the configuration directory structure and clone the schemas
    # from the github directory
    def _initSchemaDir(self):
        try:
            os.makedirs(self._schemadir, exist_ok=True)
            return self._cloneSchemas()
        except FileExistsError:
            return False

    # check that the schemadir exists
    def _schemasExist(self):
        return os.path.exists(self._schemadir)

    # clone the schemaurl to the schemadir
    def _cloneSchemas(self):
        return git.clone(self._schemaurl, self._schemadir)

    # pull updates for the git reposotory in the schema dir
    def _pullSchemas(self):
        return git.pull(branch="main", gitDir=self._schemadir)
