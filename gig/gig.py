import os
import git
import pathlib

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
            self._doRemove(parsedArgs)
        elif(parsedArgs.subcommand == "list"):
            self._doList()


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
        # if self._gitignoreExists:
        #     self._gitignoreContent = Gitignore.fromGitignoreFile(self._gitignorePath)

    # handle "init" subcommand
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
            # check args for any gitignore schemas to initialise with
            if len(args.schemas) > 0:
                # generate the fresh gitignore from the given schema files
                Gitignore.fromSchemaFiles(self._getSchemaFilesFromNames(args.schemas)).write(self._gitignorePath)
            else:
                # initialise an empty .gitignore
                Gitignore.createEmpty().write(self._gitignorePath)
        else:
            return

    # handle add subcommand
    def _doAdd(self, args):
        self._setup()
        raise NotImplementedError

    # handle add-untracked subcommand
    def _doAddUntracked(self, args):
        self._setup()
        raise NotImplementedError

    # handle update subcommand
    def _doUpdate(self, args):
        self._setup()
        raise NotImplementedError

    # handle remove subcommand
    def _doRemove(self, args):
        self._setup()
        raise NotImplementedError

    # handle list subcommand
    def _doList(self):
        self._setup()

        print("==================")
        print("Available schemas:")
        print("==================")

        files = []
        for (dirpath, dirnames, filenames) in os.walk(self._schemadir):
            files.extend(filenames)

        files.sort()
        for f in files:
            path = pathlib.Path(f)
            if(path.suffix == ".gitignore"):
                print(path.stem)

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

        # add subparser for the add subcommand
        parser_add = subparsers.add_parser(
            "add",
            help="Add the .gitignore scehma to the .gitignore file")
        parser_add.add_argument("schemas", choices="XYZ", help="schemas help")

        # add subparser for the add-untracked command
        parser_add_untracked = subparsers.add_parser(
            "add-untracked",
            help="Add any currently untracked files in the git repository to .gitignore")

        # add subparser for the update command
        parser_update = subparsers.add_parser(
            "update",
            help="Update any .gitignore schemas in the .gitignore file to their latest versions")

        # add subparser for the remove command
        parser_remove = subparsers.add_parser(
            "remove",
            help="Remove the .gitignore schema from the .gitignore file")

        parser_list = subparsers.add_parser(
            "list",
            help="List available schemas")

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

    def _getSchemaFilesFromNames(self, names):
        output = []
        for n in names:
            output.append(self._schemadir + "/" + n + ".gitignore")
        return output
