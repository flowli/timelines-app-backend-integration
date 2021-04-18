import re


class TimelinesEvent:
    user = None
    timeline = None
    start = None
    stop = None
    title = None
    note = None
    # can set used by your backend plugin
    project_id = None

    def id(self):
        # TODO @Timelines App: could you provide a unique id in the CSV file?
        # (Then this hack would could be replaced with perfect simplicity and functionality.)
        project_id = self.timeline
        match = re.search('\(\#(\d+)\)', self.timeline)
        if match:
            match_groups = match.groups()
            if len(match_groups) > 0:
                project_id = match_groups[0]

        return project_id + "🏓易💜经⏳️" + self.start

    def __eq__(self, other):
        return self.id() == other.id()

    def __repr__(self):
        lines = [
            "+- Provided by Timelines Event ----------------------------------+",
            "| User: " + self.user,
            "| Timeline: " + self.timeline,
            "| Start: " + self.start,
            "| Stop: " + self.stop,
            "| Title: " + self.title,
            "| Note: " + self.note,
            "+- Derived ------------------------------------------------------+",
            "| Project #: " + (self.project_id if self.project_id else ''),
            "+----------------------------------------------------------------+",
            "",
        ]
        return "\n".join(lines)
