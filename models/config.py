import os

from singleton import singleton
from utils.constants import *
from utils.file_helpers import select_folder
from utils.helper import get_app_directory
from utils.string_helpers import string_list_to_json

from .config_manager import ConfigManager


@singleton
class Config(ConfigManager):
    key_values = SEPARATOR.join(KEY_VALUES)
    input_folder = os.path.join(os.getcwd(), "receipts")
    output_folder = os.path.join(os.getcwd(), "receipts", DEFAULT_OUTPUT_DIR_NAME)
    bank_acronyms = SEPARATOR.join([f"{key}{SEPARATOR}{value}" for key, value in BANK_ACRONYMS.items()])
    config_file = os.path.join(get_app_directory(), CONFIG_FILE)

    def __init__(self):
        super().__init__(self.config_file)
        self.read_config()
        try:
            self.get_section("App")
        except:
            self.__default_values()

    def __default_values(self):
        input_folder_title = select_folder("Selecione a pasta contendo os comprovantes (PDF)")
        output_folder_title = select_folder("Selecione a pasta onde serão salvos os arquivos (PDF)")

        self.set_value("App", "title", APP_TITLE)
        self.set_value("App", "key_values", self.key_values)
        self.set_value("App", "bank_acronyms", self.bank_acronyms)
        self.set_value("Folder", "input_folder", input_folder_title)
        self.set_value("Folder", "output_folder", output_folder_title)
        self.set_value("Folder", "output_filename", FILENAME)
        self.save_config()

    def get_title(self):
        return self.get_value("App", "title", APP_TITLE)

    def get_key_values(self):
        key_values = self.get_value("App", "key_values", self.key_values)
        return key_values.split(SEPARATOR)

    def get_bank_acronyms(self):
        bank_acronyms = self.get_value("App", "bank_acronyms", self.bank_acronyms)
        return string_list_to_json(bank_acronyms, separator=SEPARATOR)

    def get_input_folder(self):
        return self.get_value("Folder", "input_folder", self.input_folder)

    def get_output_folder(self):
        return self.get_value("Folder", "output_folder", self.output_folder)

    def get_output_filename(self):
        return self.get_value("Folder", "output_filename", FILENAME)
