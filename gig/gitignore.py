import re
import os
from pathlib import Path
from schemaentry import SchemaEntry

# markers to show in .gitignore where portion of file managed by this
# begins and ends
_begintag = "# <<<GIGBEGIN>>>"
_endtag = "# <<<GIGEND>>>"

# message that is shown after the begin message to inform the reader
# that the content between the tags is managed by this program
_infomessage = (
    "# Content between <<<GIGBEGIN>>> and <<<GIGEND>>> managed by gig DO NOT MODIFY"
)

# markers to show in .gitignore where a specific schema begins and ends
# includes information about the shemas that the content in between the
# markers is from.
# "name" is the name of the schema
# "url" is the url of the git repository that the schema came from
# "commit" is the git hash of the commit that the file in the git repo
#          was last modified
#
# NOTE: url will not be utilised in the first version but I'm putting
# it here in case I decide to later allow for additional configuration
# regarding which git repository the schemas come from
_beginschematagregex = "# <<<GIGSCHEMABEGIN name=\"()\" url=\"()\" commit=\"()\">>>"
_beginschematag = "# <<<GIGSCHEMABEGIN name=\"%s\" url=\"%s\" commit=\"%s\">>>"
_endschematag = "# <<<GIGSCHEMAEND>>>"

def _getSchemaDataFromFile(file):
    name = Path(file).stem
    beginTag = _beginschematag % (name, "someurl", "somecommit")

    data = []

    data.extend(beginTag)
    data.append("\n")
    with open(file, 'r') as f:
        data.extend(f.read())
    data.extend(_endschematag)
    data.append("\n")

    return data


class Gitignore():
    _schemadir = ""

    _preGigLines = []
    _gigLines = []
    _postGigLines = []

    def __init__(self, data):
        self._data = data
        # print(self._data)
        self._process()

    # initialise from a gitignore file
    @classmethod
    def fromGitignoreFile(cls, file):
        with open(file, 'r') as f:
            data = f.read()
            return cls(data)

    # initialise from schema files
    @classmethod
    def fromSchemaFiles(cls, schemaFiles):
        # read all lines from each of the schema dirs and pass to __init__
        # this will create a fresh gitignore file with only gig data inside

        data = []
        data.extend(_begintag)
        data.append("\n")
        data.extend(_infomessage)
        data.append("\n\n")

        for file in schemaFiles:
            if os.path.exists(file):
                data.extend(_getSchemaDataFromFile(file))
            else:
                print("W: %s does not exist" % file)

        data.append("\n")
        data.extend(_endtag)
        data.append("\n")

        return cls(''.join(str(x) for x in data))


    # write the data to the given file
    def write(self, file):
        # write the data back to the file
        # with open(file, 'w') as f:
            # write _preGigLines followed by _gigLines followed by _posGigLines
        return


    def _process(self):
        # read the data into the structure
        lines = self._data.split('\n')
        lines = [line.rstrip() for line in lines]

        (found, self._gigStart, self._gigEnd) = self._findGigTags(lines)

        if found:
            self._sortData(lines)
            self._processGigData()
            # sort the data into non gig managed and 
        else:
            raise Exception("No gig tags")


    def _findGigTags(self, lines):
        found = False

        startFound = False
        start = 0
        end = 0

        for index, line in enumerate(lines):
            if not startFound and re.match(_begintag, line):
                start = index
                startFound = True
            elif re.match(_endtag, line):
                end = index

        if start != 0 and end > start:
            found = True

        return (found, start, end)

    def _sortData(self, lines):
        self._preGigLines = []
        self._gigLines = []
        self._postGigLines = []

        for i in range(0, self._gigStart):
            self._preGigLines.append(lines[i])

        for i in range(self._gigStart, self._gigEnd + 1):
            self._gigLines.append(lines[i])

        for i in range(self._gigEnd + 1, len(lines)):
            self._postGigLines.append(lines[i])

    def _processGigData(self):
        matchFound = False
        matchStartLine = 0
        matchEndLine = 0
        matchName = ""
        matchURL = ""
        matchCommit = ""

        schemaEntries = []
        for index, line in enumerate(self._gigLines):
            if not matchFound:
                m = re.match(_beginschematag, line)
                if m:
                    print("Found entry: %s" % line)
                    matchStartLine = index
                    matchName = m.group(1)
                    matchURL = m.group(2)
                    matchCommit = m.group(3)
            else:
                # searching for a close tag
                m = re.match(_endschematag, line)
                if m:
                    matchEndLine = index
                    schemaEntries.append(
                        SchemaEntry(
                            matchStartLine,
                            matchEndLine,
                            matchName,
                            matchURL,
                            matchCommit
                        )
                    )

        if matchFound:
            raise Exception("No closing tag found for {}")
        else:
            # closing tag was not found
            # print("%u entries found\n" % len(schemaEntries))
            for entry in schemaEntries:
                print(entry)

    # check that the schemadir exists
    def _schemasExist(self):
        return os.path.exists(self._schemadir)

    # check that the specified schema exists
    def _schemaExists(self, name):
        return self._schemasExist() and os.path.exists(self._getSchemaFile(name))

    # get the schema file path from the name of the schema
    def _getSchemaFile(self, name):
        return self._schemadir + "/" + name + ".gitignore"
