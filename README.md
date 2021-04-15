# Timelines App Backend Integration

## Technical concept for backend integration via IMAP accounts

### Idea (last change: Apr 13, 2021)
1. Track time
    - Time tracked in the [Timelines App](https://timelines.app) can be exported to CSV
    - We need the CSV format "Detailed" that requires a "Pro" subscription (currently costs around 20 € per year and user)
    - That CSV format can - at any point in time - be manually shared to an e-mail address. This should be done before invoicing takes place.
2. With this mechanism this processor can automatically determine important fields of tracked time spans:
    - The user is identified by the e-mail's sender address
    - Security can be enhanced with a required, short smtp relaying path, e-mail encryption or a simple passphrase somewhere in e-mails can be required for each user
    - The project identifier needs to be encoded in the timeline name (using the characters `#<company-wide project id>`)
3. Any user who reported his time can be informed about the state and stats of the import process via a report e-mail

## Implementation
### Installation
1. ensure python3 is installed
2. install the following python3 modules:
    - python-dotenv
    - imapclient
    - pickledb

### Configuration
1. Set environment variables. You can:
    - set environment variables (see `.env.example` for a list) in your machine or container
    - copy `.env.example` to `.env` and customize it to your needs
    - it's likely wise to make sure your imap server has a valid certificate
    - feel encouraged to write your own backend plugin - check out printer_example.py for a trivial example

### Deployment
1. clone this repo
2. configure as described above
3. call run.py as often as needed, i. e. using a cronjob
4. sent donations or complaints ;-)
