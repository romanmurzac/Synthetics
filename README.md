# Synthetics

## Overview
The **Synthetic** is a Python-based tool designed to generate synthetic multi-table datasets. It allows users to define constraints such as primary keys, foreign keys, regex validation, and numerical ranges. The generated data can be saved in multiple formats, including CSV, JSON, and Parquet.

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


Clone the repository.
```bash
git clone https://github.com/romanmurzac/PyProcData.git
```

Create virtual environment and activate it.
```bash
python3 -m venv venv
.venv/Scripts/activate
```

Install dependencies.
```bash
pip install -r requirements.txt
```

Tests run:
```bash
pytest tests/  
```

## Usage
In the `data/input_data` directory upload sample data files. Accepted formats are: CSV, JSON, and Parquet.\
In the `config.config.json` file define for each table properties for each column that should be restricted.

### Restriction options
`primary_key` --> define the primary key in the table.\
`foreign_key` --> define the foreign key in the table. Provide the `reference` table and column.\
`range` --> define the numeric range that values in the column should fit in.\
`regex` --> define the regex pattern to be followed by the values in the column.\
`fixed_combinations` --> define columns that are interdependent.

***Example***
```json
{
  "users": {
    "user_id": {
      "type": "primary_key"
    },
    "age": {
      "type": "range",
      "low": 18,
      "high": 80
    },
    "email": {
      "type": "regex",
      "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    }
  },
  "orders": {
    "order_id": {
      "type": "primary_key"
    },
    "user_id": {
      "type": "foreign_key",
      "referenced_table": "users",
      "referenced_column": "user_id"
    },
    "amount": {
      "type": "range",
      "low": 0.01,
      "high": 10000.00
    },
    "status": {
      "type": "fixed_combinations",
      "columns": ["status", "orig"]
    }
  }
}

```

## File Structure
```
synthetic/
│── config/           
│  │── config.json 
│── data/           
│  │── input_data/
│  │── output_data/
│── src/  
│── tests/
│── .gitignore  
│── LICENSE         
│── README.md
│── requirements.txt           
```

## ChangeLogs

- Add dataset size to the config
- Update to use Metadata class
- Write to origin datatype
- Generate based on config
- Support multiple config files

## License
This project is licensed under the MIT License.