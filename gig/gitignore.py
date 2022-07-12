import re
from schemaentry import SchemaEntry

class Gitignore():
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
    _beginschematag = "# <<<GIGSCHEMABEGIN name=\"()\" url=\"()\" commit=\"()\">>>"
    _endschematag = "# <<<GIGSCHEMAEND>>>"

    def __init__(self, file):
        self._file = file
        self._read()


    def write(self):
        # write the data back to the file
        return


    def _read(self):
        # read the data into the structure
        with open(self._file) as f:
            lines = f.readlines()
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
            if not startFound and re.match(self._begintag, line):
                start = index
                startFound = True
            elif re.match(self._endtag, line):
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
                m = re.match(self._beginschematag, line)
                if m:
                    print("Found entry: %s" % line)
                    matchStartLine = index
                    matchName = m.group(1)
                    matchURL = m.group(2)
                    matchCommit = m.group(3)
            else:
                # searching for a close tag
                m = re.match(self._endschematag, line)
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
            print("%u entries found\n" % len(schemaEntries))
            for entry in schemaEntries:
                print(entry)


