import re
from datetime import datetime, timedelta


class TimelinesEvent:
    user = None  # email address (sender who shared the event)
    timeline = None  # timeline name
    start = None  # event start, datetime
    duration = None  # event duration, measured in minutes
    title = None  # event title
    note = None  # event note
    date_format = '%Y-%m-%d %H:%M:%S'

    def id(self):
        # TODO @Timelines App: could you provide a unique id in the CSV file?
        # (Then this hack would could be replaced with perfect simplicity and functionality.)

        # use extracted id as timeline input to event id if possible, else use entire timeline name
        extracted_id = self.project_id()
        project_id = extracted_id if extracted_id else self.timeline

        return str(project_id) + "🏓易💜经⏳️" + self.start

    def stop(self):
        start = datetime.strptime(self.start, self.date_format)
        duration = timedelta(minutes=float(self.duration))
        stop = datetime.strftime(start + duration, self.date_format)
        return stop

    # can be useful for a backend plugin
    def project_id(self):
        project_id = None
        match = re.search('\[([^\]]+)\]', self.timeline)
        if match:
            match_groups = match.groups()
            if len(match_groups) > 0:
                project_id = match_groups[0]
        return project_id

    def __eq__(self, other):
        return self.id() == other.id()

    def __repr__(self):
        lines = [
            "+- Provided by Timelines Event ----------------------------------+",
            "| User: " + self.user,
            "| Timeline: " + self.timeline,
            "| Start: " + self.start,
            "| Stop: " + self.stop(),
            "| Title: " + self.title,
            "| Note: " + self.note,
            "+- Derived ------------------------------------------------------+",
            "| Project #: " + (self.project_id() if self.project_id() else ''),
            "+----------------------------------------------------------------+",
            "",
        ]
        return "\n".join(lines)
