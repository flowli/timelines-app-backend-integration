import unittest
from lib.attachment_events_reader import AttachmentEventsReader


class AttachmentEventsReaderTest(unittest.TestCase):
    # TODO: write this test
    def test_reader(self):
        reader = AttachmentEventsReader()
        message = {
            'from': 'user1@example.com'
        }
        attachment_payload_lines = [
            'Timeline,Start,Stop,Title,Note',
            '"Project A","2021-04-17 13:50:00","","2021-04-17 16:30","Task 57","Done with bells and whistles."',
            '"Project B","2021-04-16 06:00:00","","2021-04-16 08:00","Task 13","Almost done, but still WiP."',
        ]
        attachment_payload = attachment_payload_lines
        reader.add(message, bytes("\n".join(attachment_payload), 'utf-8'))

        # expect two timespans
        self.assertEqual(2, len(reader.events))
