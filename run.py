#!/usr/bin/env python

import os
import sys
import importlib
from lib.config import Config
from lib.imap import Mailbox
from lib.attachment_events_reader import AttachmentEventsReader
from lib.processed import Processed

app_path = os.path.dirname(os.path.realpath(__file__))

# 1. connect to mailbox
config = Config(app_path + '/.env').read()
mailbox = Mailbox(config)

# 2. fetch emails with a csv attachment
messages = mailbox.messages(attachment_suffix_filter='csv')
if messages is None:
    sys.exit(0)

# 3. turn attachments into timelines events
db_dir = app_path + '/storage/processed'
if config['timelines_events_add_each_id_only_once']:
    processed = Processed('timelines_events', db_dir)
    reader = AttachmentEventsReader(processed)
else:
    processed = None
    reader = AttachmentEventsReader()
for message in messages:
    for attachment in message['attachments']:
        reader.add(message, attachment_payload=attachment['payload'])

# 4. deliver events to backend
backend_module = importlib.import_module(config['backend_module'])
backend_class = getattr(backend_module, config['backend_class'])
backend = backend_class()
for event in reader.events:
    backend.deliver_timelines_event(event)
    if processed is not None:
        processed.now(event)

# 5. move successfully processed emails to processed folder
if config['imap_move_processed_messages']:
    mailbox.move_to_processed_folder(messages)

# 6. disconnect from mailbox
mailbox.close()
