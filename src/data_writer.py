import os
import pandas as pd


class DataWriter:
    def __init__(self, synthetic_data, folder_path):
        self.synthetic_data = synthetic_data
        self.folder_path = folder_path

    def save_to_csv(self):
        os.makedirs(self.folder_path, exist_ok=True)
        for table, df in self.synthetic_data.items():
            df.to_csv(os.path.join(self.folder_path, f"{table}.csv"), index=False)
