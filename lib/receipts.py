from lib.smtp import smtp


class receipts:
    def __init__(self):
        self.smtp = smtp()

    def send(self, messages, receipt_to_sender, receipt_copy_to_addresses):
        print(messages)
        self.smtp.send()
