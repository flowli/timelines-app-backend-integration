#!/usr/bin/env python

import config
from lib.imap import Mailbox

config = config.get()
mailbox = Mailbox(config)
messages = mailbox.messages()

# iterate over fetched mails
for message_id, data in messages:
    print(data)
