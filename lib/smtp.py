import smtplib


class smtp:
    server = None

    def __init__(self):
        self.server = smtplib.SMTP('localhost')
        self.server.set_debuglevel(1)

    def __del__(self):
        self.server.quit()

    def send(self, sender, recipients, subject, messageText):
        recipient_list = recipients.split()
        message = '''
            Subject: {subject}
    
            {messageText}
            '''.format(subject=subject, messageText=messageText)
        self.server.sendmail(sender, recipient_list, messageText)
        return
