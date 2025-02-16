import os
import json
import pandas as pd


class DataLoader:

    def __init__(self, folder_path: str, config_path: dict) -> None:
        self.folder_path = folder_path
        self.config_file = config_path
        self.tables = {}

    def _get_table_names(self) -> list:
        table_names = list(self.config_file.keys())
        return table_names

    def _get_file_path(self, table):
        for ext in ["csv", "json", "parquet"]:
            file_path = os.path.abspath(os.path.join(self.folder_path, f"{table}.{ext}"))
            file_path = file_path.replace("\\", "/")
            if os.path.exists(file_path):
                return file_path
        return None

    def _read_file(self, file_path):
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            return pd.read_json(file_path)
        elif file_path.endswith(".parquet"):
            return pd.read_parquet(file_path)
        return None

    def load_data(self):
        for table in self._get_table_names():
            file_path = self._get_file_path(table)
            if file_path:
                self.tables[table] = self._read_file(file_path)
        return self.tables


if __name__ == "__main__":
    data_path = "../data/input_data"
    config_file = {'users': {'user_id': {'type': 'primary_key'}}, 'orders': {'order_id': {'type': 'primary_key'}}}
    data_loader = DataLoader(data_path, config_file)
    print(data_loader.load_data())
