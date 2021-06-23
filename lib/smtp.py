import smtplib


class smtp:
    server = None

    # set debug_level to 1 to see more
    def __init__(self, config, debug_level=0):
        self.server = smtplib.SMTP_SSL(config.get('smtp_host'))
        self.server.set_debuglevel(debug_level)
        self.server.login(config.get('smtp_username'), config.get('smtp_password'))

    def __del__(self):
        self.server.quit()

    def send(self, sender, recipients, subject, messageText):
        recipient_list = recipients.split()
        message = '''Subject: {subject}

{messageText}
'''.format(subject=subject, messageText=messageText)
        self.server.sendmail(sender, recipient_list, message)
