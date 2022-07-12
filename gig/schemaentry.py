class SchemaEntry():
    def __init__(self, lineStart, lineEnd, name, url, commit):
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.name = name
        self.url = url
        self.commit = commit
