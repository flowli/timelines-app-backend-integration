# Timelines App: Backend Integration

Started in 2021 by [Florian Arndt](https://arweb.de/imprint/) out of 💜 for 🕰.

## Technical Concept

*TL;DR: [Timelines App](https://timelines.app) 👉 Share detailed CSV via E-Mail 👉 Collect using IMAP 👉 Deliver time
spans to your backend*

1. **Track time in Timelines App**
    - Time tracked in the [Timelines App](https://timelines.app) can be exported to CSV
    - We need the CSV format "Detailed" that requires a "Pro" subscription (currently costs around 20 € per year and
      user)
    - That CSV format can - at any point in time - be manually shared to an e-mail address. This should be done before
      reasonable invoicing can take place.
2. **Deliver tracked time to your backend**
    - With the aforementioned mechanism this integration can automatically determine important fields of tracked time spans:
        - The user can be identified by the e-mail's sender address
        - [Not coded yet] security can be enhanced with a required, short smtp relaying path, e-mail encryption or a simple
          passphrase somewhere in e-mails can be required for each user
        - The project identifier can be encoded in the timeline name (using square brackets like `[backend project id]`).
          This identifier can then be used to match the project in your backend.
3. **Get Receipts**
    - Any user who reported his time can be informed about the state and stats of the import process via a report e-mail

## User Guide

### Caveats

1. This tool identifies time spans using their timeline name and the starting time. So whenever one or both of the two
   change it counts as a new event and gets re-imported. This could be fixed by Timelines App providing a unique
   identifier for events in the CSV data and this tool using that as the new identifier.
2. The *project identifier* needs to be part of the Timeline name like `Project XYZ [123] …`. This could be automated if
   the Timelines app supported syncing project metadata with a backend.

### Install and run

1. Using Docker
    1. Install [Docker](https://www.docker.com/products/docker-desktop)
    2. Run `./docker-run --build`
2. Without Docker
    1. Ensure python3 is installed
    2. Install the dependencies with `pip3 install python-dotenv==0.17.0 imapclient==2.2.0 pickledb==0.9.2 requests==2.25.1`
    3. Your backend plugin's dependencies like [requests](https://docs.python-requests.org/en/master/)
    4. Run `python3 run.py`

### Configuration

1. Set environment variables. You can:
    - set environment variables (see `example.env` for a list) in your machine or container
    - copy `example.env` to `.env` and customize it to your needs
    - it's likely wise to make sure your imap server has a valid certificate
    - feel encouraged to write your own backend plugin - check out printer_example.py for a trivial example

### Deployment

1. Clone this repo
2. Install and configure as described in paragraph "Install and run"
3. Run this tool whenever needed (i. e. using a cronjob or scheduled task)
4. Monitoring:
    - make sure you get informed if the `run.py` exit code is not zero
    - you can log/append start+end date of runs as well as std{out,err} somewhere for reference
5. Happy + want to support this project? You could paypal a donation to `florian.arndt@gmail.com` 🥳
6. Unhappy? Open an issue or a fork 😄
