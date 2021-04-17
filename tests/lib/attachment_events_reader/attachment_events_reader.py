import unittest
from lib.attachment_events_reader import AttachmentEventsReader
from lib.processed import Processed


class AttachmentEventsReaderTest(unittest.TestCase):
    # TODO: write this test
    def test_idempotent_import_of_multiple_attachments(self):
        processed = Processed('events')
        reader = AttachmentEventsReader(processed)
