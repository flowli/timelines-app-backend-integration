from imapclient import IMAPClient
import ssl
from .email_parser import EMailParser


class Mailbox:
    config = None
    client = None

    def __init__(self, config):
        self.config = config
        self.client = None
        self.client = self.get_imap_client_instance()
        self.client.login(self.config['imap_username'], self.config['imap_password'])
        self.client.select_folder(self.config['imap_search_folder'])

    def get_imap_client_instance(self):
        ssl_context = self.get_imap_ssl_context()
        client = IMAPClient(self.config['imap_host'], ssl=True, ssl_context=ssl_context, timeout=15, use_uid=True)
        return client

    def get_imap_ssl_context(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED

        # Allow own certificate if configured
        if self.config['imap_cert_allow_other'] == 'on':
            # other certificate is to be allowed
            if self.config['imap_key_file'] == '':
                # a certificate with integrated key is provided
                ssl_context.load_cert_chain(certfile=self.config['imap_cert_file'])
            else:
                # a separate key file is provided
                ssl_context.load_cert_chain(certfile=self.config['imap_cert_file'],
                                            keyfile=self.config['imap_key_file'])
        return ssl_context

    def messages(self):
        # search criteria are passed in a straightforward way (nesting is supported)
        messageIds = self.client.search(['NOT', 'DELETED'])
        # fetch selectors are passed as a simple list of strings.
        fetched = self.client.fetch(messageIds, ['FLAGS', 'RFC822.SIZE', 'RFC822', 'BODY[TEXT]'])

        # create a simple, useful list of messages
        messages = []
        for message_id, data in fetched.items():
            message = EMailParser.message_from_fetched_data(data)
            messages.append(message)
            return messages
