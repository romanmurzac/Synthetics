# Synthetics
Generate synthetic data with all characteristics based on provided data sample.


## Roadmap

- Add dataset size to the config
- Update to use Metadata class
- Write to origin datatype
- Generate based on config
- Support multiple config files


# Synthetic Data Generator

## Overview
The **Synthetic Data Generator** is a Python-based tool designed to generate synthetic multi-table datasets. It allows users to define constraints such as primary keys, foreign keys, regex validation, and numerical ranges. The generated data can be saved in multiple formats, including CSV, JSON, and Parquet.

## Features
- **Automatic metadata detection** for multi-table datasets
- **Custom constraints support**, including:
  - Primary keys
  - Foreign keys
  - Numerical range constraints
  - Regular expression validation
  - Fixed combinations
- **Multi-table data synthesis** using the `HMASynthesizer`
- **Configurable data generation** with a specified number of rows
- **Flexible data export** to CSV, JSON, and Parquet formats

## Installation

Ensure you have Python 3.8+ installed, then install the required dependencies:

```bash
pip install pandas sdv pyarrow
```

## Usage

### 1. Sample Data and Constraints

```python
import pandas as pd
from metadata_processor import MetadataProcessor, SyntheticDataSaver

# Define sample data
data = {
    "users": pd.DataFrame({
        "user_id": [1, 2, 3],
        "email": ["user1@example.com", "user2@example.com", "user3@example.com"]
    }),
    "orders": pd.DataFrame({
        "order_id": [101, 102, 103],
        "user_id": [1, 2, 3],
        "amount": [100.5, 200.0, 150.75]
    })
}

# Define constraints
constraints = {
    "users": {
        "user_id": {"type": "primary_key"},
        "email": {"type": "regex", "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"}
    },
    "orders": {
        "order_id": {"type": "primary_key"},
        "user_id": {"type": "foreign_key", "referenced_table": "users", "referenced_column": "user_id"}
    }
}
```

### 2. Generate Synthetic Data

```python
# Create processor instance and generate synthetic data
processor = MetadataProcessor(data, constraints)
synthetic_data = processor.generate_synthetic_data(num_rows=500)
```

### 3. Save Synthetic Data

```python
# Save to different formats
saver = SyntheticDataSaver(synthetic_data, "synthetic_output")
saver.save_to_csv()
saver.save_to_json()
saver.save_to_parquet()
```

## File Structure
```
synthetic-data-generator/
│── metadata_processor.py  # Core logic for metadata handling
│── constraints.py         # Constraint definitions
│── data_saver.py          # File saving utilities
│── README.md              # Project documentation
```

## License
This project is licensed under the MIT License.

