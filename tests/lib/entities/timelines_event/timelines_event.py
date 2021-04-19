import unittest
from lib.entities.timelines_event import TimelinesEvent


class TimelinesEventTest(unittest.TestCase):
    def test_id_extraction_from_timeline(self):
        event = TimelinesEvent()
        # shortest case
        event.timeline = '[13]'
        self.assertEqual('13', event.project_id())
        # with text around
        event.timeline = 'some timeline [#AZ-1] more text'
        self.assertEqual('#AZ-1', event.project_id())
