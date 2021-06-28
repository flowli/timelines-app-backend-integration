import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class smtp:
    server = None

    # set debug_level to 1 to see more
    def __init__(self, config, debug_level=0):
        self.server = smtplib.SMTP_SSL(config.get('smtp_host'))
        self.server.set_debuglevel(debug_level)
        self.server.login(config.get('smtp_username'), config.get('smtp_password'))

    def __del__(self):
        self.server.quit()

    def send(self, mail_sender, recipients, subject, text, html):
        mail_recipients = recipients.split()
        message = MIMEMultipart('alternative')  # messageText.encode('utf8'), _charset="UTF-8"
        message['From'] = mail_sender
        message['Subject'] = Header(subject, "utf-8")
        message.attach(MIMEText(text, 'plain'))
        message.attach(MIMEText(html, 'html'))
        self.server.sendmail(mail_sender, mail_recipients, message.as_string())
