import configparser


class ConfigManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config = configparser.ConfigParser()

    def read_config(self):
        self.config.read(self.file_path)

    def get_value(self, section: str, option: str, fallback=None):
        return self.config.get(section, option, fallback=fallback)

    def set_value(self, section: str, option: str, value: str = None):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def get_section(self, section):
        if not self.config.has_section(section):
            raise ValueError(f"Seção '{section}' não encontrada no arquivo de configuração.")
        return dict(self.config.items(section))

    def save_config(self):
        with open(self.file_path, "w") as configfile:
            self.config.write(configfile)
