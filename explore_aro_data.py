"""
explore_aro_data.py

This script provides an initial exploration of the data in 'aro_index.tsv' and 'aro_categories.tsv'.
It loads each file as a pandas DataFrame and prints:
- Shape (rows, columns)
- Column names and data types
- First 5 rows (head)
- DataFrame info (including nulls and dtypes)
- Descriptive statistics (where appropriate)
- Missing value counts per column

Dependencies:
- pandas

Usage:
    uv run explore_aro_data.py

Author: (your name here)
"""

import pandas as pd

# File paths
ARO_INDEX_PATH = 'data/aro_index.tsv'
ARO_CATEGORIES_PATH = 'data/aro_categories.tsv'

def explore_file(path, name):
    """
    Loads a TSV file and prints basic exploratory information.
    Args:
        path (str): Path to the TSV file.
        name (str): Descriptive name for the file.
    """
    print(f"\n{'='*40}\nExploring {name}\n{'='*40}")
    df = pd.read_csv(path, sep='\t')
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nData types:")
    print(df.dtypes)
    print("\nInfo:")
    df.info()
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nDescriptive statistics:")
    print(df.describe(include='all', datetime_is_numeric=True))
    print("\nMissing values per column:")
    print(df.isnull().sum())

if __name__ == "__main__":
    explore_file(ARO_INDEX_PATH, 'ARO Index')
    explore_file(ARO_CATEGORIES_PATH, 'ARO Categories') 