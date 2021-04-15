#!/usr/bin/env python

from lib.config import Config
from lib.imap import Mailbox
from lib.attachment_timespan_reader import AttachmentTimespanReader
import sys

# Left TODO:
# - remember which ids were processed and do not repeat them (see git history for removed code)
# - identify user by sender email
# - identify project by timeline substring matching
# - …and write to log for when any of the above fails

# 1. connect to mailbox
config = Config().read('.env')
mailbox = Mailbox(config)

# 2. fetch emails with a csv attachment
messages = mailbox.messages(attachment_suffix_filter='csv')

# 3. turn attachments into timespans
reader = AttachmentTimespanReader()
if messages is None:
    sys.exit(0)

for message in messages:
    for attachment in message['attachments']:
        reader.add(message, attachment_payload=attachment['payload'])

# 4. process timespans - TODO: add your backend communication here
successful_so_far = True
for timespan in reader.timespans:
    print("👉 Processing timespan:")
    print(timespan)
    successful_so_far = True  # TODO: set success depending on your backend module

# 5. move successfully processed emails to processed folder
if config['imap_move_processed_messages'] and successful_so_far:
    mailbox.move_to_processed_folder(messages)

# 6. disconnect from mailbox
mailbox.close()
