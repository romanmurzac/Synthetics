import json


class ConfigReader:
    """
    Read and parse a JSON configuration file.
    """

    def __init__(self, config_path: str) -> None:
        """
        Initializes the ConfigReader with the given configuration file path.
        Args:
            config_path (str): Path to the JSON configuration file.
        """
        self.config_file = config_path

    def get_config(self):
        """
        Reads and parses the JSON configuration file.
        Returns:
            A dictionary containing the parsed configuration.
        """
        with open(self.config_file, "r") as f:
            return json.load(f)


if __name__ == "__main__":
    config_file = "../config/config.json"
    config_reader = ConfigReader(config_file)
    print(config_reader.get_config())
