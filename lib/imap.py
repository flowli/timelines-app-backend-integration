import ssl

from imapclient import IMAPClient

from .email_parser import EMailParser


class Mailbox:
    config = None
    client = None

    def __init__(self, config):
        self.config = config
        self.client = None
        self.client = self.get_imap_client_instance()
        self.client.login(self.config.get('imap_username'), self.config.get('imap_password'))
        self.client.select_folder(self.config.get('imap_search_folder'))

    def get_imap_client_instance(self):
        ssl_context = self.get_imap_ssl_context()
        client = IMAPClient(self.config.get('imap_host'), ssl=True, ssl_context=ssl_context, timeout=15, use_uid=True)
        return client

    def get_imap_ssl_context(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED

        # Allow own certificate if configured
        if self.config.get('imap_cert_allow_other') == 'on':
            # other certificate is to be allowed
            if self.config.get('imap_key_file') == '':
                # a certificate with integrated key is provided
                ssl_context.load_cert_chain(certfile=self.config.get('imap_cert_file'))
            else:
                # a separate key file is provided
                ssl_context.load_cert_chain(certfile=self.config.get('imap_cert_file'),
                                            keyfile=self.config.get('imap_key_file'))
        return ssl_context

    def move_to_processed_folder(self, messages):
        # make sure the processed folder exists
        self.client.create_folder(self.config.get('imap_processed_folder'))

        # move messages over
        message_unique_ids = []
        for message in messages:
            message_unique_ids.append(message['id'])
        if len(message_unique_ids):
            self.client.move(message_unique_ids, self.config.get('imap_processed_folder'))

    def messages(self, attachment_suffix_filter=None):
        # search criteria are passed in a straightforward way (nesting is supported)
        message_ids = self.client.search(['NOT', 'DELETED'])

        # fetch selectors are passed as a simple list of strings.
        fetched = self.client.fetch(message_ids, ['FLAGS', 'RFC822.SIZE', 'RFC822', 'BODY[TEXT]'])

        # create a simple, useful list of messages
        messages = []
        email_parser = EMailParser()
        for message_id, data in fetched.items():
            message = email_parser.message_from_fetched_data(message_id, data,
                                                             attachment_suffix_filter=attachment_suffix_filter)
            if attachment_suffix_filter is None or len(message['attachments']) > 0:
                messages.append(message)
            return messages

    def close(self):
        self.client.shutdown()
