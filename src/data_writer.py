import os
import pandas as pd


class DataWriter:
    """
    Save synthetic data to specific file formats.
    """

    def __init__(
        self, synthetic_data: dict, folder_path: str, file_format: str
    ) -> None:
        """
        Initializes the DataWriter with synthetic data and output folder path.
        Args:
            synthetic_data (dict): Dictionary containing table names as keys and Pandas DataFrames as values.
            folder_path (str): Path to the folder where output files will be saved.
            file_format (str): File format to save the output.
        """
        self.synthetic_data = synthetic_data
        self.folder_path = folder_path
        self.format = file_format

    def save_file(self) -> None:
        """
        Saves the synthetic data to CSV files in the specified folder.
        """
        os.makedirs(self.folder_path, exist_ok=True)
        for table, df in self.synthetic_data.items():
            if self.format == "csv":
                df.to_csv(os.path.join(self.folder_path, f"{table}.csv"), index=False)
            elif self.format == "json":
                df.to_json(
                    os.path.join(self.folder_path, f"{table}.json"),
                    orient="records",
                    lines=True,
                )
            elif self.format == "parquet":
                df.to_parquet(
                    os.path.join(self.folder_path, f"{table}.parquet"), index=False
                )


if __name__ == "__main__":
    synthetic_data_example = {
        "users": pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]}),
        "orders": pd.DataFrame(
            {"order_id": [101, 102], "user_id": [1, 2], "amount": [250, 125]}
        ),
    }
    output_folder = "../data/output_data"
    output_format = "csv"
    data_writer = DataWriter(synthetic_data_example, output_folder, output_format)
    data_writer.save_file()
