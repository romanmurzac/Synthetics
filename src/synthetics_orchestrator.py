from src.synthetic_logger import logger


class SyntheticOrchestrator:

    def __init__(self, tables) -> None:
        self.tables = tables

    def run(self):
        tables = self.tables
        logger.info("Started synthetic data generator...")
        ...


if __name__ == "__main__":
    synthetic_orchestrator = SyntheticOrchestrator(["tables"])
    synthetic_orchestrator.run()
