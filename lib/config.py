from dotenv import load_dotenv
import os


class Config:
    env_filename = None
    read_cache = None

    def __init__(self, env_filename):
        self.env_filename = env_filename

    # returns all config options as a dict. transforms on/off to Python bool.
    def read(self):
        config_defaults = {
            'IMAP_HOST': 'imap.example.com',
            'IMAP_USERNAME': 'username',
            'IMAP_PASSWORD': 'password',
            'IMAP_SEARCH_FOLDER': 'INBOX',
            'IMAP_MOVE_PROCESSED_MESSAGES': True,
            'IMAP_PROCESSED_FOLDER': 'PROCESSED',
            'IMAP_CERT_ALLOW_OTHER': 'off',
            'IMAP_CERT_FILE': '',
            'IMAP_KEY_FILE': '',
            'TIMELINES_EVENTS_ADD_EACH_ID_ONLY_ONCE': True,
            'BACKEND_MODULE': 'lib.backends.printer_example',
            'BACKEND_CLASS': 'PrinterExample',
        }

        # make .env override environment variables
        load_dotenv(self.env_filename)

        # write environment variables to config (use defaults if not env var is not set)
        config = {}
        env_vars = os.environ
        for env_key, env_val in env_vars.items():
            config[env_key] = env_vars[env_key] or config_defaults[env_key]

        # transform data types as expected by consumers
        config['IMAP_CERT_ALLOW_OTHER'] = config['IMAP_CERT_ALLOW_OTHER'].lower()
        config['IMAP_MOVE_PROCESSED_MESSAGES'] = Config.on_off_to_bool(config['IMAP_MOVE_PROCESSED_MESSAGES'])
        config['TIMELINES_EVENTS_ADD_EACH_ID_ONLY_ONCE'] = Config.on_off_to_bool(
            config['TIMELINES_EVENTS_ADD_EACH_ID_ONLY_ONCE'])

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
