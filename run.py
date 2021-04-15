#!/usr/bin/env python

from lib.config import Config
from lib.imap import Mailbox

config = Config().read('.env')
mailbox = Mailbox(config)
messages = mailbox.messages(attachment_suffix_filter='csv')

# iterate over fetched mails
for message in messages:
    print(message)
