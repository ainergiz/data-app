"""
resistance_breakdown.py

This script analyzes and visualizes the breakdown of antibiotic resistance
mechanisms for a specific drug class, distinguishing between gene-based
resistance and SNP-based resistance.

It performs the following steps:
1.  Loads data from 'aro_index.tsv' (gene information) and 'snps.txt' (mutation information).
2.  Focuses on a specified drug class (e.g., 'fluoroquinolone antibiotic').
3.  Correlates the two datasets using ARO Accession numbers to identify which
    resistance determinants are caused by SNPs.
4.  Calculates the total counts for gene-based vs. SNP-based resistance.
5.  Generates and displays a pie chart visualizing this breakdown.

Dependencies:
- pandas
- plotly

Usage:
    uv run resistance_breakdown.py
"""

import pandas as pd
import plotly.express as px

# File paths
ARO_INDEX_PATH = 'data/aro_index.tsv'
SNPS_PATH = 'data/snps.txt'

def analyze_resistance_breakdown(aro_df, snp_df, drug_class):
    """
    Analyzes the breakdown of resistance mechanisms for a given drug class.

    Args:
        aro_df (pd.DataFrame): DataFrame from aro_index.tsv.
        snp_df (pd.DataFrame): DataFrame from snps.txt.
        drug_class (str): The drug class to analyze.

    Returns:
        pd.DataFrame: A DataFrame with the counts of gene-based and SNP-based resistance.
    """
    # --- 1. Process ARO Index Data ---
    # Handle multi-valued 'Drug Class' column
    aro_df_exploded = aro_df.assign(**{'Drug Class': aro_df['Drug Class'].str.split(';')}).explode('Drug Class')
    aro_df_exploded['Drug Class'] = aro_df_exploded['Drug Class'].str.strip()
    
    # Filter for the specified drug class
    drug_class_df = aro_df_exploded[aro_df_exploded['Drug Class'] == drug_class]
    
    if drug_class_df.empty:
        print(f"No data found for drug class: '{drug_class}'")
        return None
        
    total_resistance_determinants = drug_class_df['ARO Accession'].nunique()
    
    # --- 2. Process SNP Data ---
    # Get unique ARO accessions from the SNP data
    # The 'Accession' column in snps.txt is just the number, so we prepend 'ARO:'
    snp_aro_accessions = set('ARO:' + snp_df['Accession'].astype(str))
    
    # --- 3. Correlate Data ---
    # Find which of the drug class determinants are SNP-based
    drug_class_aro_accessions = set(drug_class_df['ARO Accession'])
    snp_based_accessions = drug_class_aro_accessions.intersection(snp_aro_accessions)
    
    snp_count = len(snp_based_accessions)
    gene_count = total_resistance_determinants - snp_count
    
    # --- 4. Prepare DataFrame for plotting ---
    breakdown_data = {
        'Mechanism Type': ['Gene-based', 'SNP-based'],
        'Count': [gene_count, snp_count]
    }
    breakdown_df = pd.DataFrame(breakdown_data)
    
    return breakdown_df

def plot_resistance_breakdown(df, drug_class):
    """
    Generates and displays a pie chart of the resistance mechanism breakdown.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Mechanism Type' and 'Count' columns.
        drug_class (str): The drug class being plotted.
    """
    if df is None or df.empty:
        print("No data to plot.")
        return
        
    fig = px.pie(
        df,
        names='Mechanism Type',
        values='Count',
        title=f"Resistance Mechanism Breakdown for<br>'{drug_class}'",
        hole=0.3
    )
    fig.update_traces(textinfo='percent+label', pull=[0, 0.05])
    fig.show()

def main():
    """
    Main function to load data and run the analysis.
    """
    try:
        aro_df = pd.read_csv(ARO_INDEX_PATH, sep='\t')
        
        # The snps.txt file has a complex, irregular format.
        # We only need the first column (Accession), so we'll parse it manually
        # to avoid the errors caused by the inconsistent structure.
        snp_accessions = []
        with open(SNPS_PATH, 'r') as f:
            # Skip the two header lines
            next(f)
            next(f)
            for line in f:
                # Split by whitespace and take the first element
                parts = line.strip().split()
                if parts:
                    snp_accessions.append(parts[0])
        
        # Create a DataFrame from the extracted accessions
        snp_df = pd.DataFrame(snp_accessions, columns=['Accession'])

    except FileNotFoundError as e:
        print(f"Error: Could not find a required data file. {e}")
        return
    except Exception as e:
        print(f"An error occurred during file loading: {e}")
        return

    # Analyze a specific drug class
    target_drug_class = 'fluoroquinolone antibiotic'
    print(f"Analyzing resistance breakdown for: '{target_drug_class}'...")
    
    breakdown_df = analyze_resistance_breakdown(aro_df, snp_df, target_drug_class)
    
    if breakdown_df is not None:
        print("\nAnalysis Results:")
        print(breakdown_df)
        
        print("\nGenerating plot...")
        plot_resistance_breakdown(breakdown_df, target_drug_class)
        print("Plot has been generated.")

if __name__ == "__main__":
    main()
