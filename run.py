#!/usr/bin/env python

import os
import sys
import importlib
from lib.config import Config
from lib.imap import Mailbox
from lib.attachment_timespan_reader import AttachmentTimespanReader
from lib.processed import Processed

# 1. connect to mailbox
config = Config('.env').read()
mailbox = Mailbox(config)

# 2. fetch emails with a csv attachment
messages = mailbox.messages(attachment_suffix_filter='csv')
if messages is None:
    sys.exit(0)

# 3. turn attachments into timespans
db_dir = os.path.dirname(os.path.realpath(__file__)) + '/storage/processed'
if config['timelines_events_add_each_id_only_once']:
    processed = Processed('timespans', db_dir)
    reader = AttachmentTimespanReader(processed)
else:
    processed = None
    reader = AttachmentTimespanReader()
for message in messages:
    for attachment in message['attachments']:
        reader.add(message, attachment_payload=attachment['payload'])

# 4. deliver timespans to backend
backend_module = importlib.import_module(config['backend_module'])
backend_class = getattr(backend_module, config['backend_class'])
backend = backend_class()
for timespan in reader.timespans:
    backend.deliver_timelines_event(timespan)
    if processed is not None:
        processed.now(timespan)

# 5. move successfully processed emails to processed folder
if config['imap_move_processed_messages']:
    mailbox.move_to_processed_folder(messages)

# 6. disconnect from mailbox
mailbox.close()
