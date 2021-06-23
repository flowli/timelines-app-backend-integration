from lib.entities.timelines_event import TimelinesEvent
from lib.smtp import smtp


class receipts:
    config = None
    smtp = None

    def __init__(self, config):
        self.config = config
        self.smtp = smtp(config)

    def send(self, message, events: list[TimelinesEvent]):
        receipt_to_sender = self.config.get('receipt_to_sender')
        receipt_copy_to_addresses = self.config.get('receipt_copy_to_addresses')
        send_any = receipt_to_sender or receipt_copy_to_addresses != ''
        if not send_any:
            return

        lines = []
        for event in events:
            lines.append(str(event) + "\n")

        message_text = "\n".join(lines)
        sender_address = self.config.get('receipt_sender_address')
        if receipt_to_sender:
            subject = '[Timelines Receipt] ' + message['subject']
            self.smtp.send(sender_address, message['from'], subject, message_text)
        if receipt_copy_to_addresses != '':
            subject = '[Copy of Timlines Receipt for ' + message['from'] + '] ' + message['subject']
            self.smtp.send(sender_address, receipt_copy_to_addresses, subject, message_text)
