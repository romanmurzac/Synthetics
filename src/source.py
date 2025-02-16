import pandas as pd
import json
import re
from sdv.metadata import MultiTableMetadata
from sdv.multi_table import HMASynthesizer
from sdv.constraints import ScalarRange, FixedCombinations, Constraint


def load_data(folder_path):
    """
    Load multiple CSV files from a folder as a dictionary of DataFrames.
    """
    tables = {}
    for file in ["users.csv", "orders.csv"]:
        tables[file.split(".")[0]] = pd.read_csv(f"{folder_path}/{file}")
    return tables


def detect_metadata(data):
    """
    Detect metadata for multi-table data.
    """
    metadata = MultiTableMetadata()
    metadata.detect_from_dataframes(data)
    return metadata


class RegexConstraint(Constraint):
    """
    Custom constraint to enforce regex validation on a column.
    """

    def __init__(self, column_name, pattern):
        self.column_name = column_name
        self.pattern = re.compile(pattern)

    def is_valid(self, table_data):
        return table_data[self.column_name].astype(str).str.match(self.pattern)


def apply_constraints(metadata, constraints_config):
    """
    Apply constraints from config.json to the metadata.
    """
    constraints = []

    for table, columns in constraints_config.items():
        for column, rule in columns.items():
            if isinstance(rule, dict) and "type" in rule:
                constraint_dict = {"table_name": table, "constraint_class": None, "constraint_parameters": {}}

                if rule["type"] == "range":
                    constraint_dict["constraint_class"] = "ScalarRange"
                    constraint_dict["constraint_parameters"] = {
                        "column_name": column,
                        "low_value": rule["low"],
                        "high_value": rule["high"],
                        "strict_boundaries": rule.get("strict", False)
                    }

                elif rule["type"] == "fixed_combinations":
                    print(f"META: {metadata}")
                    constraint_dict["constraint_class"] = "FixedCombinations"
                    constraint_dict["constraint_parameters"] = {
                        "column_names": rule["columns"]
                    }

                elif rule["type"] == "regex":
                    constraint_dict["constraint_class"] = "RegexConstraint"
                    constraint_dict["constraint_parameters"] = {
                        "column_name": column,
                        "pattern": rule["pattern"]
                    }

                elif rule["type"] == "primary_key":
                    # metadata.set_primary_key(table_name=table, column_name=column)
                    ...

                elif rule["type"] == "foreign_key":
                    metadata.update_column(column_name=column, sdtype='id', table_name="users")
                    metadata.update_column(column_name=column, sdtype='id', table_name=table)
                    metadata.set_primary_key(table_name=table, column_name=column)
                    metadata.add_relationship(table, rule["referenced_table"], column, rule["referenced_column"])

                if constraint_dict["constraint_class"]:
                    constraints.append(constraint_dict)

    return constraints


def generate_synthetic_data(data, metadata, constraints):
    """
    Generate synthetic multi-table data.
    """
    synthesizer = HMASynthesizer(metadata)
    synthesizer.add_constraints(constraints)
    synthesizer.fit(data)
    return synthesizer.sample()


def save_synthetic_data(synthetic_data, folder_path):
    """
    Save synthetic data to CSV format.
    """
    for table, df in synthetic_data.items():
        df.to_csv(f"{folder_path}/{table}.csv", index=False)


def main(data_folder, config_file, output_folder):
    """
    Main execution function.
    """
    data = load_data(data_folder)
    metadata = detect_metadata(data)

    with open(config_file, "r") as f:
        constraints_config = json.load(f)

    constraints = apply_constraints(metadata, constraints_config)
    synthetic_data = generate_synthetic_data(data, metadata, constraints)

    save_synthetic_data(synthetic_data, output_folder)
    print("Synthetic data saved successfully!")


if __name__ == "__main__":
    main("../data/input_data", "../config/config.json", "../data/output_data")
