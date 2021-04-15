from dotenv import load_dotenv
import os


class Config:
    def read(self, env_filename):
        load_dotenv(env_filename)
        keys_with_defaults = {
            'imap_host': 'imap.example.com',
            'imap_username': 'username',
            'imap_password': 'password',
            'imap_search_folder': 'INBOX',
            'imap_cert_allow_other': 'off',
            'imap_cert_file': '',
            'imap_key_file': '',
            'imap_delete_mail_when_processed': True
        }
        config = {}
        # assign
        for key, defaultValue in keys_with_defaults.items():
            config[key] = os.getenv(key.upper()) or defaultValue
        # transform data types as expected by consumers
        config['imap_cert_allow_other'] = config['imap_cert_allow_other'].lower()
        config['imap_delete_mail_when_processed'] = config['imap_delete_mail_when_processed'].lower() != 'false'
        # provide the config dict
        return config
