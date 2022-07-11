import os
import sys
import git
# import argparse
# import argparse.ArgumentError
from gigparser import GigParser

# define some error
class GigError(Exception):
    pass

class Gig:
    # the default url for the schemas
    _shemaurl = "https://github.com/github/gitignore"  # ???
    _configdir = "~/.config/gitignore"
    _configpath = _configdir + "/config"
    _schemadir = _configpath + "/schemas"

    # markers to show in .gitignore where portion of file managed by this
    # begins and ends
    _begintag = "# <<<GIGBEGIN>>>"
    _endtag = "# <<<GIGEND>>>"
    # message that is shown after the begin message to inform the reader
    # that the content between the tags is managed by this program
    _infomessage = (
        "# Content between <<<GIGBEGIN>>> and <<<GIGEND>>> managed by gig"
        "DO NOT MODIFY"
    )

    # markers to show in .gitignore where a specific schema begins and ends
    # includes information about the shemas that the content in between the
    # markers is from.
    # "name" is the name of the schema
    # "from" is the url of the git repository that the schema came from
    # "commit" is the git hash of the commit that the file in the git repo
    #          was last modified
    #
    # NOTE: from will not be utilised in the first version but I'm putting
    # it here in case I decide to later allow for additional configuration
    # regarding which git repository the schemas come from
    _beginschematag = "# <<<GIGSCHEMABEGIN name=\"()\" from=\"\" commit=\"()\">>>"
    _endschematag = "# <<<GIGSCHEMAEND>>>"

    def __init__(self):
        # first check that git is installed
        if not git.isInstalled():
            raise GigError("E: Git must be installed to use gitignore")
        # first check that we are in an git repository before going any further
        elif not git.isRepo():
            raise GigError("E: Must be in a git repository to use gitignore")

        # check that the schemas exist
        if not (self._schemasExist() or self._initSchemaDir()):
            raise GigError("E: Gitignore schemas are not available")
        elif not self._pullSchemas(): # should this be an error
            print("W: Gitignore schemas could not be updated")

        # path information for the git repository
        self._gitroot = git.getRoot()
        self._gitignorePath = git.getIgnore()
        self._gitignoreExists = os.path.exists(self._gitignorePath)

        # set the initial gitignore content based on whether the gitignore
        # exidsts or not
        if self._gitignoreExists:
            self._gitignoreContent = self._readGitignore()
        else:
            self._gitignoreContent = "\n\n\n%s\n%s\n\n\n%s" % (
                self._begintag,
                self._infomessage,
                self._endtag)

        #  finaly create argument parser
        self._parser = self._getParser()

        # parse the arguments
        self._parser.parse_args(sys.argv[1:])


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


    def _doInit(self, args):
        overwrite = False
        if self._gitignoreExists:
            # prompt user to overwrite the git ignore
            msg = ".gitignore already exists. Overwrite? [yn]"
            print(msg)
            choice = input().lower()
            while choice not in ("y", "n"):
                choice = input.lower()

            if(choice == "y"):
                # overwrite the file
                overwrite = True
            else:
                return

        # if there are schemas then gather schema information


        if(overwrite or not self._gitignoreExists):
            #     ret
            # initoialise .gitignore as empty
            raise NotImplementedError


        raise NotImplementedError

    def _doAdd(self, args):
        raise NotImplementedError

    def _doAddUntracked(self, args):
        raise NotImplementedError

    def _doUpdate(self, args):
        raise NotImplementedError

    def _doRemove(self, args):
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
        parse_update = subparsers.add_parser(
            "update",
            help="Update any .gitignore schemas in the .gitignore file to their latest versions")

        # add subparser for the remove command
        parser_remove = subparsers.add_parser(
            "remove",
            help="Remove the .gitignore schema from the .gitignore file")

        return parser

    # initialise the configuration directory structure and clone the schemas
    # from the github directory
    def _initSchemaDir(self):
        try:
            os.makedirs(self._schemadir)
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
        return git.pull(gitDir=self._schemadir)

    # get the contents of the current git ignore file
    def _readGitignore(self):
        with open(self._gitignorePath, 'r') as file:
            self._gitignoreContent = file.read()
            return True
        return False

    # write the current data within _gitignoreContent to the .gitignore file
    def _writeGitignore(self):
        with open(self._gitignorePath, 'w') as file:
            file.write(self._gitignoreContent)
            return True
        return False
