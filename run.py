#!/usr/bin/env python

from lib.config import Config
from lib.imap import Mailbox
import csv

config = Config().read('.env')
mailbox = Mailbox(config)
messages = mailbox.messages()

# iterate over fetched mails
for message in messages:
    print(message)
