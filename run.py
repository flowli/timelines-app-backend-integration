#!/usr/bin/env python

import importlib
import os
import sys
import datetime

from lib.attachment_events_reader import AttachmentEventsReader
from lib.config import Config
from lib.imap import Mailbox
# from lib.processed import Processed
from lib.processed import Processed
from lib.receipts import receipts

# 0. error handling: add date+time to output
def exception_add_datetime(exctype, value, traceback):
    sys.stderr.write("[ERROR][" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] \n")
    sys.__excepthook__(exctype, value, traceback)
sys.excepthook = exception_add_datetime

app_path = os.path.dirname(os.path.realpath(__file__))

# 1. connect to mailbox
config = Config(app_path + '/.env')
mailbox = Mailbox(config)

# 2. fetch emails with a csv attachment
messages = mailbox.messages(attachment_suffix_filter='csv')
if messages is None:
    sys.exit(0)

# 3. turn attachments into timelines events
db_dir = app_path + '/storage/processed'
if config.get('timelines_events_duplicate_detection'):
    processed = Processed('timelines_events', db_dir)
    reader = AttachmentEventsReader(processed)
else:
    processed = None

# 4. process messages
backend_module = importlib.import_module(config.get('backend_module'))
backend_class = getattr(backend_module, config.get('backend_class'))
backend = backend_class()
for message in messages:
    # try:
    reader = AttachmentEventsReader()
    # read all relevant attachments
    for attachment in message['attachments']:
        reader.add(message, attachment_payload=attachment['payload'])
    # deliver events to backend
    delivery_status_lines_list = []
    for event in reader.events:
        project_id = event.project_id()
        if project_id is not None and project_id != '':
            event.delivery_status_lines = backend.deliver_timelines_event(event)
        if processed is not None:
            processed.now(event)
    # send configured receipts
    if config.get('receipt_to_sender') or config.get('receipt_copy_to_addresses') != '':
        receipts(config).send(message, reader.events)

# 5. move successfully processed emails to processed folder
if config.get('imap_move_processed_messages'):
    mailbox.move_to_processed_folder(messages)

# 6. disconnect from mailbox
mailbox.close()
