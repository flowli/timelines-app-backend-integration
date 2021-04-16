from io import StringIO
import csv
from lib.entities.timelines_event import TimelinesEvent


class AttachmentTimespanReader:
    processed = None
    timespans = []

    def __init__(self, processed=None):
        self.processed = processed

    def add(self, message, attachment_payload):
        iterable = StringIO(attachment_payload.decode('utf-8'))
        reader = csv.reader(iterable, delimiter=',')
        i = 0
        for row in reader:
            i = i + 1
            if i == 1:  # skip header row
                continue
            timespan = TimelinesEvent()
            timespan.user = message['from']
            timespan.timeline = row[0]
            timespan.start = row[1]
            timespan.stop = row[2]
            timespan.title = row[4]
            timespan.note = row[5]
            processed_marking_active = self.processed is not None
            if processed_marking_active:
                if self.processed.not_yet(timespan):
                    self.timespans.append(timespan)
            else:
                self.timespans.append(timespan)
