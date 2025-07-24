
"""
snp_analyzer.py

This script loads and analyzes the 'snps.txt' file to identify and
visualize the genes most frequently affected by resistance-conferring
Single Nucleotide Polymorphisms (SNPs).

It performs the following steps:
1.  Loads the 'snps.txt' data into a pandas DataFrame.
2.  Counts the occurrences of each gene (using 'CARD Short Name').
3.  Identifies the top 10 most frequently mutated genes.
4.  Generates and displays a bar chart of these top 10 genes.

Dependencies:
- pandas
- plotly

Usage:
    uv run snp_analyzer.py
"""

import pandas as pd
import plotly.express as px

# File path
SNPS_PATH = 'data/snps.txt'

def analyze_snp_data(file_path):
    """
    Loads SNP data, identifies the most frequently mutated genes,
    and returns a DataFrame of the top 10.
    
    Args:
        file_path (str): The path to the snps.txt file.
        
    Returns:
        pd.DataFrame: A DataFrame containing the top 10 mutated genes
                      and their mutation counts.
    """
    try:
        # Load the data using tab as a separator
        df = pd.read_csv(file_path, sep='\t')
        
        # Check if the required column exists
        if 'CARD Short Name' not in df.columns:
            print("Error: 'CARD Short Name' column not found.")
            return None
            
        # Count mutations per gene
        snp_counts = df['CARD Short Name'].value_counts().reset_index()
        snp_counts.columns = ['CARD Short Name', 'count']
        
        return snp_counts.head(10)

    except FileNotFoundError:
        print(f"Error: The file was not found at '{file_path}'")
        return None
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return None

def plot_top_mutated_genes(df):
    """
    Generates and displays a sorted bar chart of the top 10
    most frequently mutated genes.
    
    Args:
        df (pd.DataFrame): DataFrame with 'CARD Short Name' and 'count' columns.
    """
    if df is None or df.empty:
        print("No data available to plot.")
        return
        
    fig = px.bar(
        df,
        x='CARD Short Name',
        y='count',
        title='Top 10 Genes with Resistance-Conferring SNPs',
        labels={'CARD Short Name': 'Gene (CARD Short Name)', 'count': 'Number of SNPs'}
    )
    fig.update_xaxes(categoryorder='total descending')
    fig.update_layout(xaxis_tickangle=45)
    fig.show()

def main():
    """
    Main function to run the SNP analysis and plotting.
    """
    print(f"Analyzing SNP data from '{SNPS_PATH}'...")
    top_snps_df = analyze_snp_data(SNPS_PATH)
    
    if top_snps_df is not None:
        print("\nTop 10 Genes with Resistance-Conferring SNPs:")
        print(top_snps_df)
        
        print("\nGenerating plot...")
        plot_top_mutated_genes(top_snps_df)
        print("Plot has been generated.")

if __name__ == "__main__":
    main()
