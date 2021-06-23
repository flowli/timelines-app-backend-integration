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
    delivery_status_lines: None  # list of strings, to be set by your backend plugin

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

    # required by most backend plugins
    def project_id(self):
        matches = re.findall('\[([^\]]+)\]', self.timeline)
        return matches[0] if len(matches) >= 1 else None

    def __eq__(self, other):
        return self.id() == other.id()

    def __str__(self):
        lines = ["+- Timelines Event ----------------------------------+", "| User: " + self.user,
                 "| Timeline: " + self.timeline, "| Start: " + self.start, "| Stop: " + self.stop(),
                 "| Title: " + self.title, "| Note: " + self.note, "| Project #: " + self.project_id(),
                 "| Delivery status:\n" + "\n".join(self.delivery_status_lines), ""]
        return "\n".join(lines)
