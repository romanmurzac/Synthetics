from src.synthetic_logger import logger
from src.config_reader import ConfigReader
from src.data_loader import DataLoader
from src.data_generator import SyntheticDataGenerator
from src.data_writer import DataWriter

CONFIG_FILE = "../config/config.json"
INPUT_DATA_PATH = "../data/input_data"
OUTPUT_DATA_PATH = "../data/output_data"
DATASET_SIZE = 1_000
OUTPUT_FORMAT = "csv"


class SyntheticOrchestrator:
    """
    Orchestrates the synthetic data generation process by reading configuration,
    loading input data, generating synthetic data, and saving the output.
    """

    def __init__(
        self,
        input_path: str,
        output_path: str,
        config_file: str,
        dataset_size: int,
        file_format: str,
    ) -> None:
        """
        Initializes the SyntheticOrchestrator with paths, configuration file, and dataset size.
        Args:
        input_path (str): Path to the input data directory.
        output_path (str): Path to the output data directory.
        config_file (str): Path to the configuration JSON file.
        dataset_size (int): Number of synthetic records to generate.
        file_format (str): Format of the file to save.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.config_file = config_file
        self.dataset_size = dataset_size
        self.file_format = file_format

    def run(self) -> None:
        """
        Executes the synthetic data generation pipeline.
        """
        logger.info("Started synthetic data generation.")

        config_reader = ConfigReader(self.config_file)
        config = config_reader.get_config()

        data_loader = DataLoader(self.input_path, config)
        source_data = data_loader.load_data()

        processor = SyntheticDataGenerator(source_data, config, self.dataset_size)
        synthetic_data = processor.generate_synthetic_data()

        data_writer = DataWriter(synthetic_data, self.output_path, self.file_format)
        data_writer.save_file()

        logger.info("Finished synthetic data generation.")


if __name__ == "__main__":
    synthetic_orchestrator = SyntheticOrchestrator(
        INPUT_DATA_PATH, OUTPUT_DATA_PATH, CONFIG_FILE, DATASET_SIZE, OUTPUT_FORMAT
    )
    synthetic_orchestrator.run()
