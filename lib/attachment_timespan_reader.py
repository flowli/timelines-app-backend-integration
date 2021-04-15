from io import StringIO
import csv
from lib.entities.timespan import Timespan


class AttachmentTimespanReader:
    timespans = []

    def add(self, message, attachment_payload):
        iterable = StringIO(attachment_payload.decode('utf-8'))
        reader = csv.reader(iterable, delimiter=',')
        i = 0
        for row in reader:
            i = i + 1
            if i == 1:  # skip header row
                continue
            timespan = Timespan()
            timespan.user = message['from']
            timespan.timeline = row[0]
            timespan.start = row[1]
            timespan.stop = row[2]
            timespan.title = row[4]
            timespan.note = row[5]
            self.timespans.append(timespan)
