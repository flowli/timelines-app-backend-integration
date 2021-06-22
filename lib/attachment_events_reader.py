import csv
from io import StringIO

from lib.entities.timelines_event import TimelinesEvent


class AttachmentEventsReader:
    processed = None
    events = []

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
            if len(row) < 6:  # skip rows with less than 6 columns
                raise Exception('CSV has only ' + str(len(row)) + ' columns, 6 expected')
            event = TimelinesEvent()
            event.user = message['from']
            event.timeline = row[0]
            event.start = row[1]
            event.duration = row[3]
            event.title = row[4]
            event.note = row[5]
            processed_marking_active = self.processed is not None
            if processed_marking_active:
                if self.processed.not_yet(event):
                    self.events.append(event)
            else:
                self.events.append(event)
