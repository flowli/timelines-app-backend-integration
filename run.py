#!/usr/bin/env python

from lib.config import Config
from lib.imap import Mailbox
from lib.attachment_timespan_reader import AttachmentTimespanReader
from lib.processed import Processed
import os

# Left TODO:
# - better Exception handling?


# 1. connect to mailbox
config = Config().read('.env')
mailbox = Mailbox(config)

# 2. fetch emails with a csv attachment
messages = mailbox.messages(attachment_suffix_filter='csv')

# 3. turn attachments into timespans
reader = AttachmentTimespanReader()
for message in messages:
    for attachment in message['attachments']:
        reader.add(attachment_payload=attachment['payload'])

# 4. process new (=previously unprocessed) timespans
db_dir = os.path.dirname(os.path.realpath(__file__)) + '/db'
processed = Processed('timespans', db_dir)
for timespan in reader.timespans:
    if processed.has_been(timespan):
        print('⏭ Skipping timespan "' + timespan.id() + '"')
    if processed.not_yet(timespan):
        print("👉 Processing timespan")
        processed.now(timespan)

# 5. delete successfully processed emails
if config['imap_delete_mail_when_processed']:
    print("deleting")

# 6. disconnect from mailbox
# mailbox.client.disconnect?
