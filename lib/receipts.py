from lib.smtp import smtp


class receipts:
    def __init__(self, config):
        self.smtp = smtp(config)

    def send(self, messages, receipt_to_sender, receipt_copy_to_addresses):
        for message in messages:
            print(message['from'])
            print(message)
            print('[⏱ Receipt] ' + message['subject'])
    # if receipt_to_sender or receipt_copy_to_addresses:
    #    self.smtp.send('fa@arweb.de', 'yolo', 'wow, a message body')
    # if receipt_copy_to_addresses != '':
    #    self.smtp.send('fa@arweb.de', 'yolo', 'wow, a message body')
