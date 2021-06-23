import os

from dotenv import load_dotenv


class Config:
    env_filename = None
    read_cache = None

    def __init__(self, env_filename):
        self.env_filename = env_filename

    # returns all config options as a dict. transforms on/off to Python bool.
    def read(self):
        config_defaults = {
            'IMAP_HOST': 'imap.example.com',
            'IMAP_USERNAME': 'imap-username',
            'IMAP_PASSWORD': 'imap-password',
            'IMAP_SEARCH_FOLDER': 'INBOX',
            'IMAP_MOVE_PROCESSED_MESSAGES': True,
            'IMAP_PROCESSED_FOLDER': 'PROCESSED',
            # 'TIMELINES_EVENTS_ADD_EACH_ID_ONLY_ONCE': True,
            'BACKEND_MODULE': 'lib.backends.printer_example',
            'BACKEND_CLASS': 'PrinterExample',
            'SMTP_HOST': 'smtp.example.com',
            'SMTP_USERNAME': 'smtp-username',
            'SMTP_PASSWORD': 'smtp-password',
            'RECEIPT_TO_SENDER': False,
            'RECEIPT_SENDER_ADDRESS': 'timelines@example.com',
            'RECEIPT_COPY_TO_ADDRESSES': ''
        }

        # make .env override environment variables
        load_dotenv(self.env_filename)

        # write environment variables to config (use defaults if not env var is not set)
        config = {}
        env_vars = os.environ

        # add all env values to config
        for env_key, env_val in env_vars.items():
            config[env_key] = env_vars[env_key] or config_defaults[env_key]

        # add defaults for keys which were not in env
        for default_key in config_defaults:
            if config.get(default_key) is None:
                config[default_key] = config_defaults[default_key]

        # transform data types as expected by consumers
        config['IMAP_MOVE_PROCESSED_MESSAGES'] = Config.on_off_to_bool(config['IMAP_MOVE_PROCESSED_MESSAGES'])
        config['RECEIPT_TO_SENDER'] = Config.on_off_to_bool(config['RECEIPT_TO_SENDER'])
        config['RECEIPT_COPY_TO_ADDRESSES'] = config['RECEIPT_COPY_TO_ADDRESSES'].strip()
        config['RECEIPT_SENDER_ADDRESS'] = config['RECEIPT_SENDER_ADDRESS'].strip()
        # config['TIMELINES_EVENTS_ADD_EACH_ID_ONLY_ONCE'] = Config.on_off_to_bool(
        #    config['TIMELINES_EVENTS_ADD_EACH_ID_ONLY_ONCE'])

        # provide the config dict
        return config

    # returns config value from read() if found, else returns environment variable value
    def get(self, key):
        if self.read_cache is None:
            self.read_cache = self.read()
        if self.read_cache[key.upper()] is not None:
            return self.read_cache[key.upper()]
        else:
            return os.getenv(key.upper())

    def on_off_to_bool(string):
        return string.lower() != 'off'
