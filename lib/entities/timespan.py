class Timespan:
    timeline = None
    start = None
    stop = None
    title = None
    note = None

    def id(self):
        return hash(frozenset({'timeline': self.timeline, 'start': self.start}))

    def __eq__(self, other):
        return self.id() == other.id()

    def __repr__(self):
        lines = [
            "+-----------------------------------------------------------+",
            "Timeline: " + self.timeline,
            "Start: " + self.start,
            "Stop: " + self.stop,
            "Title: " + self.title,
            "Note: " + self.note,
            "+-----------------------------------------------------------+",
        ]
        return "\n".join(lines)
