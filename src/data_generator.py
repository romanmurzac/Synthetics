import pandas as pd
import re
from sdv.metadata import MultiTableMetadata
from sdv.multi_table import HMASynthesizer
from sdv.constraints import Constraint


class SyntheticDataGenerator:
    """
    Generating synthetic data based on given constraints and metadata.
    """

    def __init__(self, data: dict, constraints_config: dict, dataset_size: int) -> None:
        """
        Initializes the synthetic data generator.
        Args:
            data (dict): Dictionary containing Pandas DataFrames representing the tables.
            constraints_config (dict): Dictionary defining constraints for data generation.
            dataset_size (int): Number of synthetic records to generate.
        """
        self.data = data
        self.size = dataset_size
        self.constraints_config = constraints_config
        self.metadata = self.detect_metadata()
        self.constraints = self.apply_constraints()

    def detect_metadata(self) -> MultiTableMetadata:
        """
        Detects metadata from the provided dataframes.
        Returns:
            MultiTableMetadata object.
        """
        metadata = MultiTableMetadata()
        metadata.detect_from_dataframes(self.data)
        return metadata

    class RegexConstraint(Constraint):
        """
        Custom constraint for enforcing regex patterns on column values.
        """

        def __init__(self, column_name: str, pattern: str) -> None:
            """
            Initializes the regex constraint.
            Args:
                column_name: Name of the column to apply the regex pattern.
                pattern: Regex pattern to enforce.
            """
            self.column_name = column_name
            self.pattern = re.compile(pattern)

        def is_valid(self, table_data: pd.DataFrame) -> bool:
            """
            Checks if the table data matches the regex pattern.
            Args:
                table_data (pd.DataFrame): DataFrame containing the column data.
            Returns
                Boolean Series indicating validity.
            """
            return table_data[self.column_name].astype(str).str.match(self.pattern)

    def apply_constraints(self) -> list:
        """
        Applies the defined constraints to the metadata.
        Returns:
            List of constraint dictionaries.
        """
        constraints = []
        for table, columns in self.constraints_config.items():
            for column, rule in columns.items():
                if isinstance(rule, dict) and "type" in rule:
                    constraint_dict = {
                        "table_name": table,
                        "constraint_class": None,
                        "constraint_parameters": {},
                    }

                    if rule["type"] == "range":
                        constraint_dict["constraint_class"] = "ScalarRange"
                        constraint_dict["constraint_parameters"] = {
                            "column_name": column,
                            "low_value": rule["low"],
                            "high_value": rule["high"],
                            "strict_boundaries": rule.get("strict", False),
                        }

                    elif rule["type"] == "fixed_combinations":
                        print(f"META: {self.metadata}")
                        constraint_dict["constraint_class"] = "FixedCombinations"
                        constraint_dict["constraint_parameters"] = {
                            "column_names": rule["columns"]
                        }

                    elif rule["type"] == "regex":
                        constraint_dict["constraint_class"] = "RegexConstraint"
                        constraint_dict["constraint_parameters"] = {
                            "column_name": column,
                            "pattern": rule["pattern"],
                        }

                    elif rule["type"] == "primary_key":
                        self.metadata.update_column(
                            column_name=column, sdtype="id", table_name=table
                        )

                    elif rule["type"] == "foreign_key":
                        self.metadata.update_column(
                            column_name=column, sdtype="id", table_name=table
                        )
                        self.metadata.set_primary_key(
                            table_name=table, column_name=column
                        )
                        self.metadata.add_relationship(
                            table,
                            rule["referenced_table"],
                            column,
                            rule["referenced_column"],
                        )

                    if constraint_dict["constraint_class"]:
                        constraints.append(constraint_dict)

        return constraints

    def generate_synthetic_data(self) -> dict:
        """
        Generates synthetic data based on the metadata and constraints.
        Returns:
            Dictionary containing synthetic data tables as Pandas DataFrames.
        """
        synthesizer = HMASynthesizer(self.metadata)
        synthesizer.add_constraints(self.constraints)
        synthesizer.fit(self.data)
        return synthesizer.sample(self.size)


if __name__ == "__main__":
    sample_data = {
        "users": pd.DataFrame(
            {
                "user_id": [1, 2, 3],
                "email": [
                    "user1@example.com",
                    "user2@example.com",
                    "user3@example.com",
                ],
            }
        ),
        "orders": pd.DataFrame(
            {
                "order_id": [101, 102, 103],
                "user_id": [1, 2, 3],
                "amount": [100.5, 200.0, 150.75],
            }
        ),
    }
    sample_constraints = {
        "users": {
            "user_id": {"type": "primary_key"},
            "email": {
                "type": "regex",
                "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
            },
        },
        "orders": {
            "order_id": {"type": "primary_key"},
            "user_id": {
                "type": "foreign_key",
                "referenced_table": "users",
                "referenced_column": "user_id",
            },
        },
    }
    size = 10
    processor = SyntheticDataGenerator(sample_data, sample_constraints, size)
    synthetic_data = processor.generate_synthetic_data()
    print(synthetic_data)
