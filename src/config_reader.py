import json


class ConfigReader:

    def __init__(self, config_path):
        self.config_file = config_path

    def get_config(self):
        with open(self.config_file, 'r') as f:
            return json.load(f)


if __name__ == "__main__":
    config_file = "../config/config.json"
    config_reader = ConfigReader(config_file)
    print(config_reader.get_config())
