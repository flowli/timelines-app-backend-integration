import unittest
from lib.config import Config
import os

this_dir = os.path.dirname(os.path.realpath(__file__))


class ConfigTest(unittest.TestCase):
    def test_overriding_an_option_with_env_var(self):
        os.environ['IMAP_SEARCH_FOLDER'] = "OTHER"
        config = Config(this_dir + "/.env.test")  # has "INBOX"
        config_dict = config.read()
        # read entry 'IMAP_SEARCH_FOLDER' from .env.test which *was* overridden using os.environ
        self.assertEqual("OTHER", config.get('IMAP_SEARCH_FOLDER'))
        self.assertEqual("OTHER", config_dict['imap_search_folder'])

    def test_reading_an_option_from_env_file(self):
        config = Config(this_dir + "/.env.test")  # has "INBOX"
        config_dict = config.read()
        self.assertEqual('PrinterExample', config.get('BACKEND_CLASS'))
        self.assertEqual('PrinterExample', config_dict['backend_class'])

    def test_reading_an_options_default_set_in_config_class(self):
        config = Config(this_dir + "/.env.test")  # has "INBOX"
        config_dict = config.read()
        self.assertEqual("lib.backends.printer_example", config_dict['backend_module'])
        self.assertEqual("lib.backends.printer_example", config.get('BACKEND_MODULE'))
