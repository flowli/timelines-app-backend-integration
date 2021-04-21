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

        # prefer the extracted project_id but use the entire timeline name if not extractable
        project_id = self.project_id()

        if project_id is None:
            return None

        return project_id + "🏓易💜经⏳️" + self.start

    def stop(self):
        start = datetime.strptime(self.start, self.date_format)
        duration = timedelta(minutes=float(self.duration))
        stop = datetime.strftime(start + duration, self.date_format)
        return stop

    # can be useful for a backend plugin
    def project_id(self):
        project_id = None
        matches = re.findall('\[([^\]]+)\]', self.timeline)
        if len(matches) >= 1:
            return matches[0]
        return None


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
    ]
    project_id = self.project_id()
    if project_id is not None:
        lines.append("+- Derived ------------------------------------------------------+")
        lines.append("| Project #: " + project_id)
        lines.append("+----------------------------------------------------------------+")
    lines.append("")
    return "\n".join(lines)
