#!/usr/bin/env python

from lib.config import Config
from lib.imap import Mailbox
from lib.attachment_timespan_reader import AttachmentTimespanReader
from lib.processed import Processed
import os

# 1. connect to mailbox
config = Config().read('.env')
mailbox = Mailbox(config)

# 3. fetch emails with a csv attachment
messages = mailbox.messages(attachment_suffix_filter='csv')

# 4. turn attachments into timespans
reader = AttachmentTimespanReader()
for message in messages:
    for attachment in message['attachments']:
        reader.add(attachment_payload=attachment['payload'])

# 5. process new timespans
db_dir = os.path.dirname(os.path.realpath(__file__)) + '/db'
processed = Processed('timespans', db_dir)
for timespan in reader.timespans:
    if processed.not_yet(timespan):
        print(timespan.id())
        processed.now(timespan)

# 6. delete processed emails emails


# 7. disconnect from mailbox
# mailbox.client.disconnect?
