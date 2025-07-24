
"""
debug_data_files.py

This script explores the contents of the 'data/' directory to provide a
quick overview of each file. It lists all files and attempts to read and
print the first few lines of each to help understand their structure and content.

This is useful for debugging and initial data exploration.

Usage:
    uv run debug_data_files.py
"""

import os
import pandas as pd

# Directory path
DATA_DIR = 'data/'

def preview_files_in_directory(directory):
    """
    Lists all files in a directory and prints a preview of their content.
    """
    print(f"--- Exploring files in '{directory}' directory ---")
    
    try:
        # Get the list of files
        files = sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    except FileNotFoundError:
        print(f"Error: Directory not found at '{directory}'")
        return

    if not files:
        print("No files found in the directory.")
        return

    for filename in files:
        file_path = os.path.join(directory, filename)
        print(f"\n{'='*50}")
        print(f"File: {filename}")
        print(f"{'='*50}")
        
        try:
            # Handle different file types for preview
            if filename.endswith('.tsv'):
                # Preview TSV using pandas for a nice format
                df = pd.read_csv(file_path, sep='\t', nrows=5)
                print("File Type: TSV (first 5 rows shown)")
                print(df)
            elif filename.endswith(('.fasta', '.txt', '.json')):
                # Preview other text-based files by reading the first few lines
                print(f"File Type: {filename.split('.')[-1].upper()} (first 5 lines shown)")
                with open(file_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if i >= 5:
                            break
                        print(line.strip())
            elif filename.endswith('.tar.bz2'):
                print("File Type: Compressed Archive (tar.bz2)")
                print("Content preview is not available for compressed files.")
            else:
                print("File Type: Other/Binary")
                print("Content preview is not available for this file type.")

        except Exception as e:
            print(f"Could not read or preview file. Reason: {e}")

if __name__ == "__main__":
    preview_files_in_directory(DATA_DIR)
