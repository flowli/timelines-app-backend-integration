from dotenv import load_dotenv
import os


class Config:
    env_filename = None

    def __init__(self, env_filename):
        self.env_filename = env_filename

    # returns all config options as a dict. transforms on/off to Python bool.
    def read(self):
        load_dotenv(self.env_filename)
        keys_with_defaults = {
            'imap_host': 'imap.example.com',
            'imap_username': 'username',
            'imap_password': 'password',
            'imap_search_folder': 'INBOX',
            'imap_move_processed_messages': True,
            'imap_processed_folder': 'PROCESSED',
            'imap_cert_allow_other': 'off',
            'imap_cert_file': '',
            'imap_key_file': '',
            'timelines_events_add_each_id_only_once': True,
            'backend_module': 'lib.backends.printer_example',
            'backend_class': 'PrinterExample',
        }
        config = {}
        # assign
        for key, defaultValue in keys_with_defaults.items():
            config[key] = os.getenv(key.upper()) or defaultValue
        # transform data types as expected by consumers
        config['imap_cert_allow_other'] = config['imap_cert_allow_other'].lower()
        config['imap_move_processed_messages'] = Config.on_off_to_bool(config['imap_move_processed_messages'])
        config['timelines_events_add_each_id_only_once'] = Config.on_off_to_bool(config['timelines_events_add_each_id_only_once'])

        # provide the config dict
        return config

    # returns config value from read() if found, else returns environment variable value
    def get(self, key):
        standard_config = self.read()
        if standard_config.get(key):
            return standard_config[key]
        else:
            return os.getenv(key.upper())

    def on_off_to_bool(string):
        return string.lower() != 'off'
