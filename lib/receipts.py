from lib.smtp import smtp


class receipts:
    config = None
    smtp = None

    def __init__(self, config):
        self.config = config
        self.smtp = smtp(config)

    def send(self, messages, receipt_to_sender, receipt_copy_to_addresses):
        send_any = receipt_to_sender or receipt_copy_to_addresses != ''
        if not send_any:
            return
        sender_address = self.config.get('receipt_sender_address')
        for message in messages:
            messageText = '''
The following Timeline Events were received:
'''
        if receipt_to_sender:
            subject = '[Timelines Receipt] ' + message['subject']
            print('Sending receipt "' + subject + ' to ' + message['from'])
            self.smtp.send(message['from'], message['from'], subject, messageText)
        if receipt_copy_to_addresses != '':
            subject = '[Copy of Timlines Receipt for ' + message['from'] + '] ' + message['subject']
            print('Sending receipt "' + subject + ' to ' + receipt_copy_to_addresses)
            self.smtp.send(sender_address, receipt_copy_to_addresses, subject, messageText)
