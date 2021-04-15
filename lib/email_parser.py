import email


class EMailParser:
    def message_from_fetched_data(self, message_id, data, attachment_suffix_filter=None):
        if attachment_suffix_filter is not None:
            attachment_suffix_filter = attachment_suffix_filter.lower()
        this_email = email.message_from_bytes(data[b'RFC822'])
        parts = this_email.walk()
        message = {
            'id': message_id,
            'subject': '',
            'from': '',
            'attachments': []
        }
        # look at all email parts
        for part in parts:
            # detect subject in part
            if part['from'] is not None:
                message['from'] = EMailParser.extract_email_address(part['from'])
            if part['subject'] is not None:
                message['subject'] = part['subject']
            # detect attachment in part
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                payload = part.get_payload(decode=True)
                attachment_suffix = filename.split('.').pop().lower()
                if attachment_suffix_filter is None or attachment_suffix_filter == attachment_suffix:
                    message['attachments'].append({'filename': filename, 'payload': payload})
        return message

    def extract_email_address(sender):
        (name, address) = email.utils.parseaddr(sender)
        return address
