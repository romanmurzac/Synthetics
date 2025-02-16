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
To be added.

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