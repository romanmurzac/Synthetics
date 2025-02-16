from src.synthetic_logger import logger
from src.config_reader import ConfigReader
from src.data_loader import DataLoader
from src.data_generator import SyntheticDataGenerator
from src.data_writer import DataWriter

CONFIG_FILE = "../config/config.json"
INPUT_DATA_PATH = "../data/input_data"
OUTPUT_DATA_PATH = "../data/output_data"
DATASET_SIZE = 1_000

class SyntheticOrchestrator:

    def __init__(self, input_path, output_path, config_file, dataset_size) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.config_file = config_file
        self.dataset_size = dataset_size

    def run(self):
        logger.info("Started synthetic data generator...")

        config_reader = ConfigReader(self.config_file)
        config = config_reader.get_config()

        data_loader = DataLoader(self.input_path, config)
        source_data = data_loader.load_data()

        processor = SyntheticDataGenerator(source_data, config, self.dataset_size)
        synthetic_data = processor.generate_synthetic_data()

        data_writer = DataWriter(synthetic_data, self.output_path)
        data_writer.save_to_csv()



if __name__ == "__main__":
    synthetic_orchestrator = SyntheticOrchestrator(INPUT_DATA_PATH, OUTPUT_DATA_PATH, CONFIG_FILE, DATASET_SIZE)
    synthetic_orchestrator.run()
