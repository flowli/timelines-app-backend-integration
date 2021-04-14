# Timelines iOS App

## Technical concept for backend integration via IMAP accounts

### Idea (last change: Apr 13, 2021)
1. Track time
    - Time tracked in the Timelines App (available for iOS) can be exported to CSV
    - We need the CSV format "Detailed" that requires a "Pro" subscription (currently costs around 20 € per year and user)
    - That CSV format can - at any point in time - be manually shared to an e-mail address. This should be done before invoicing takes place.
2. With this mechanism this processor can automatically determine important fields of tracked time spans:
    - The user is identified by the e-mail's sender address
    - Security can be enhanced with a required, short smtp relaying path, e-mail encryption or a simple passphrase somewhere in e-mails can be required for each user
    - The project identifier needs to be encoded in the timeline name (using the characters `#<company-wide project id>`)
3. Any user who reported his time can be informed about the state and stats of the import process via a report e-mail

## Implementation
### Installation of dependencies
1. ensure python3 is installed
2. run
````
pip3 install imapclient python-dotenv
````

### Configuration
1. Set environment variables. You can:
    - set environment variables (see `.env.example` for a list) in your machine or container
    - copy `.env.example` to `.env` and customize it to your needs
    - in case of GMail, you'll probably need to run two steps to access IMAP:
        - Allow "less secure apps" on https://myaccount.google.com/lesssecureapps?pli=1
        - GMail ➡ All Settings ➡ Forwarding and POP / IMAP ➡ Enable IMAP access

2. Define a CA Bundle. You could follow https://stackoverflow.com/questions/39356413/how-to-add-a-custom-ca-root-certificate-to-the-ca-store-used-by-pip-in-windows

### Deployment
#### TODO: write this (like "run run.py as cron as often as needed")
