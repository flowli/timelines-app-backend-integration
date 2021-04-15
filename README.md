# Timelines App Backend Integration

## Technical Concept

### Idea
*TL;DR: App 👉 Share Detailed CSV via E-Mail 👉 Collect using IMAP 👉 Deliver to Backend*

1. Track time
    - Time tracked in the [Timelines App](https://timelines.app) can be exported to CSV
    - We need the CSV format "Detailed" that requires a "Pro" subscription (currently costs around 20 € per year and user)
    - That CSV format can - at any point in time - be manually shared to an e-mail address. This should be done before reasonable invoicing can take place.
2. With this mechanism this integration can automatically determine important fields of tracked time spans:
    - The user can be identified by the e-mail's sender address
    - [Not coded yet] security can be enhanced with a required, short smtp relaying path, e-mail encryption or a simple passphrase somewhere in e-mails can be required for each user
    - The project identifier can to be encoded in the timeline name (using the characters `#<company-wide project id>`) and interpreted in your backend plugin
3. [Not coded yet] Any user who reported his time can be informed about the state and stats of the import process via a report e-mail

## User Guide
### Installation
1. Ensure python3 is installed
2. Install the following python3 modules, i. e. with pip3:
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
4. 🥳? buy me a ☕️ (paypal einkauf@arweb.de) or 😤? open an issue
