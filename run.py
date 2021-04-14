#!/usr/bin/env python
import sys

import config
from imapclient import IMAPClient
import ssl

# Read config
config = config.get()

# Define ssl context for the IMAP connection
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Allow own certificate if configured
if config['imap_cert_allow_other'] == 'on':
    # other certificate is to be allowed
    if config['imap_key_file'] == '':
        # a certificate with integrated key is provided
        ssl_context.load_cert_chain(certfile=config['imap_cert_file'])
    else:
        # a separate key file is provided
        ssl_context.load_cert_chain(certfile=config['imap_cert_file'], keyfile=config['imap_key_file'])

# Connect to e-mail account and process messages
with IMAPClient(config['imap_host']) as client:
    client.login(config['imap_username'], config['imap_password'])
    client.select_folder(config['imap_search_folder'])

    # search criteria are passed in a straightforward way (nesting is supported)
    messages = client.search(['NOT', 'DELETED'])

    # fetch selectors are passed as a simple list of strings.
    response = client.fetch(messages, ['FLAGS', 'RFC822.SIZE'])

    # `response` is keyed by message id and contains parsed,
    # converted response items.
    for message_id, data in response.items():
        print('{id}: {size} bytes, flags={flags}'.format(
            id=message_id,
            size=data[b'RFC822.SIZE'],
            flags=data[b'FLAGS']))
