from html import escape

from lib.smtp import smtp


class receipts:
    config = None
    smtp = None

    def __init__(self, config):
        self.config = config
        self.smtp = smtp(config)

    def send(self, message, events):
        receipt_to_sender = self.config.get('receipt_to_sender')
        receipt_copy_to_addresses = self.config.get('receipt_copy_to_addresses')
        send_any = receipt_to_sender or receipt_copy_to_addresses != ''
        if not send_any:
            return

        # calculate total hours
        hours_total = 0
        for event in events:
            hours = float(event.duration) / 60
            hours_total += hours

        text = []
        html = [
            '<h2>🎉 Thank you for submitting ' + self.html_hours(hours_total) + ' hours!</h2>',
            '            ',
            '<table>',
            '<tr>',
            '<th>Timeline</th>',
            '<th>Start</th>',
            '<th>Duration</th>',
            '<th>Title</th>',
            '<th>Note</th>',
            '<th>Status</th>',
            '</tr>'
        ]
        for event in events:
            text.append(str(event) + "\n")
            html.append('<tr>')
            html.append('<td>' + escape(event.timeline) + '</td>')
            html.append('<td>' + escape(event.start) + '</td>')
            hours = float(event.duration) / 60
            html.append('<td align="right">' + self.html_hours(hours) + 'h</td>')
            html.append('<td>' + escape(event.title) + '</td>')
            html.append('<td>' + escape(event.note) + '</td>')
            delivery_status_lines = map(escape, event.delivery_status_lines)
            html.append('<td>' + "<br/>".join(delivery_status_lines) + '</td>')
            html.append('</tr>')
        html.append("".join([
            '<tr>',
            '<th></th>',
            '<th></th>',
            '<th align="right">' + self.html_hours(hours_total) + 'h</th>',
            '<th></th>',
            '<th></th>',
            '<th></th>',
            '</tr>'
        ]));
        html.append('</table>')

        sender_address = self.config.get('receipt_sender_address')
        if receipt_to_sender:
            subject = 'Re: ' + message['subject']
            self.smtp.send(sender_address, message['from'], subject, "\n".join(text), "".join(html))
        if receipt_copy_to_addresses != '':
            subject = 'Fwd [' + message['from'] + ']: ' + message['subject']
            self.smtp.send(sender_address, receipt_copy_to_addresses, subject, "\n".join(text), "".join(html))

    # rs = rounded string
    def html_hours(self, hrs):
        return str(round(hrs * 100) / 100)
