import unittest
from lib.attachment_events_reader import AttachmentEventsReader


class AttachmentEventsReaderTest(unittest.TestCase):
    def test_reader(self):
        reader = AttachmentEventsReader()
        # set user
        message = {
            'from': 'user1@example.com'
        }
        # add three events
        attachment_payload_lines = [
            'Timeline,Start,Stop,Title,Note',
            '"Project A (#1)","2021-04-17 13:50:00","","2021-04-17 16:30","Task 57","Done with bells and whistles."',
            '"Project B (#2)","2021-04-16 06:00:00","","2021-04-16 08:00","Task 13","Almost done, but still WiP."',
            '"Project C","2021-04-16 06:00:00","","2021-04-16 08:00","Task 13","Almost done, but still WiP."',
        ]
        attachment_payload = attachment_payload_lines
        reader.add(message, bytes("\n".join(attachment_payload), 'utf-8'))

        # expect the events read from the CSV above
        self.assertEqual(3, len(reader.events))
