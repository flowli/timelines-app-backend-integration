#!/usr/bin/env python

import sys
import importlib
from lib.config import Config
from lib.imap import Mailbox
from lib.attachment_timespan_reader import AttachmentTimespanReader

# Left TODO:
# 1. remember which ids were processed and do not repeat them (see git history for removed code)
#     - use processed.py
# 2. backend implementation for 安龙's invoicing system


# 1. connect to mailbox
config = Config().read('.env')
mailbox = Mailbox(config)

# 2. fetch emails with a csv attachment
messages = mailbox.messages(attachment_suffix_filter='csv')
if messages is None:
    sys.exit(0)

# 3. turn attachments into timespans
reader = AttachmentTimespanReader()
for message in messages:
    for attachment in message['attachments']:
        reader.add(message, attachment_payload=attachment['payload'])

# 4. deliver timespans to backend
backend_module = importlib.import_module(config['backend_module'])
backend_class = getattr(backend_module, config['backend_class'])
backend = backend_class()
for timespan in reader.timespans:
    backend.deliver_timespan(timespan)

# 5. move successfully processed emails to processed folder
if config['imap_move_processed_messages']:
    mailbox.move_to_processed_folder(messages)

# 6. disconnect from mailbox
mailbox.close()
