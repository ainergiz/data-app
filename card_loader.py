"""
card_loader.py

This script loads 'aro_index.tsv' as a pandas DataFrame, prints its shape, and provides summary statistics.
It also generates a bar chart of the top Drug Classes using Plotly Express.

Dependencies:
- pandas
- plotly

Usage:
    uv run card_loader.py

"""

import pandas as pd
import plotly.express as px

# File paths
ARO_INDEX_PATH = 'data/aro_index.tsv'

def merge_card():
    """
    Loads 'aro_index.tsv' and returns a DataFrame with the following columns:
        - 'ARO Accession'
        - 'Drug Class'
        - 'Resistance Mechanism'
        - 'Protein Accession'
    Returns:
        pd.DataFrame: DataFrame with selected columns.
    """
    aro_index_df = pd.read_csv(ARO_INDEX_PATH, sep='\t')
    selected_cols = [
        'ARO Accession',
        'Drug Class',
        'Resistance Mechanism',
        'Protein Accession'
    ]
    # Only keep columns that exist in the DataFrame
    selected_cols = [col for col in selected_cols if col in aro_index_df.columns]
    return aro_index_df[selected_cols]

def top_drug_classes(df, n=10):
    """
    Returns a DataFrame of the n most frequent Drug Class values, sorted descending.
    Handles semicolon-separated values.
    Args:
        df (pd.DataFrame): DataFrame containing a 'Drug Class' column.
        n (int): Number of top drug classes to return.
    Returns:
        pd.DataFrame: DataFrame with columns 'Drug Class' and 'count'.
    """
    if 'Drug Class' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'Drug Class' column.")
    # Split semicolon-separated values and explode the DataFrame
    split_df = df.assign(**{'Drug Class': df['Drug Class'].str.split(';')})
    exploded_df = split_df.explode('Drug Class')
    # Trim whitespace
    exploded_df['Drug Class'] = exploded_df['Drug Class'].str.strip()
    counts = exploded_df['Drug Class'].value_counts().reset_index()
    counts.columns = ['Drug Class', 'count']
    return counts.head(n)

def top_resistance_mechanisms(df, n=10):
    """
    Returns a DataFrame of the n most frequent Resistance Mechanism values, sorted descending.
    Handles semicolon-separated values.
    Args:
        df (pd.DataFrame): DataFrame containing a 'Resistance Mechanism' column.
        n (int): Number of top resistance mechanisms to return.
    Returns:
        pd.DataFrame: DataFrame with columns 'Resistance Mechanism' and 'count'.
    """
    if 'Resistance Mechanism' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'Resistance Mechanism' column.")
    # Split semicolon-separated values and explode the DataFrame
    split_df = df.assign(**{'Resistance Mechanism': df['Resistance Mechanism'].str.split(';')})
    exploded_df = split_df.explode('Resistance Mechanism')
    # Trim whitespace
    exploded_df['Resistance Mechanism'] = exploded_df['Resistance Mechanism'].str.strip()
    counts = exploded_df['Resistance Mechanism'].value_counts().reset_index()
    counts.columns = ['Resistance Mechanism', 'count']
    return counts.head(n)

def plot_drug_class_resistance_mechanisms(df, top_n_drug_classes=5, top_n_mechanisms=5):
    """
    Generates a grouped bar chart showing the relationship between top drug classes
    and their most common resistance mechanisms.
    """
    if 'Drug Class' not in df.columns or 'Resistance Mechanism' not in df.columns:
        raise ValueError("Input DataFrame must contain 'Drug Class' and 'Resistance Mechanism' columns.")

    # Create a clean, exploded DataFrame for both columns
    df_exploded = df.assign(
        **{
            'Drug Class': df['Drug Class'].str.split(';'),
            'Resistance Mechanism': df['Resistance Mechanism'].str.split(';')
        }
    ).explode('Drug Class').explode('Resistance Mechanism')
    df_exploded['Drug Class'] = df_exploded['Drug Class'].str.strip()
    df_exploded['Resistance Mechanism'] = df_exploded['Resistance Mechanism'].str.strip()

    # Find top N drug classes
    top_drug_classes_list = df_exploded['Drug Class'].value_counts().nlargest(top_n_drug_classes).index.tolist()

    # Filter the DataFrame to include only top drug classes
    df_filtered = df_exploded[df_exploded['Drug Class'].isin(top_drug_classes_list)]

    # Group by drug class and resistance mechanism and count occurrences
    grouped_counts = df_filtered.groupby(['Drug Class', 'Resistance Mechanism']).size().reset_index(name='count')

    # For each drug class, find the top N mechanisms
    top_mechanisms_per_class = grouped_counts.groupby('Drug Class').apply(
        lambda x: x.nlargest(top_n_mechanisms, 'count')
    ).reset_index(drop=True)

    # Create the plot
    fig = px.bar(
        top_mechanisms_per_class,
        x="Drug Class",
        y="count",
        color="Resistance Mechanism",
        title=f"Top {top_n_mechanisms} Resistance Mechanisms for Top {top_n_drug_classes} Drug Classes",
        barmode='group',
        labels={"Drug Class": "Drug Class", "count": "Count", "Resistance Mechanism": "Resistance Mechanism"},
        category_orders={"Drug Class": top_drug_classes_list}
    )
    fig.update_layout(xaxis_tickangle=45)
    fig.show()


def main():
    """
    Loads the TSV file and prints its shape.
    """
    aro_index_df = pd.read_csv(ARO_INDEX_PATH, sep='\t')
    print(f"aro_index.tsv shape: {aro_index_df.shape}")

    # Demonstrate merge_card usage
    merged_df = merge_card()
    print("\nSelected DataFrame (first 5 rows):")
    print(merged_df.head())

    # Show top 10 most frequent Drug Class values
    print("\nTop 10 Drug Classes (Corrected):")
    top_dc_df = top_drug_classes(merged_df, n=10)
    print(top_dc_df)

    # Generate a bar chart of the top Drug Classes
    fig_dc = px.bar(
        top_dc_df,
        x="Drug Class",
        y="count",
        title="Top 10 Drug Classes",
        labels={"Drug Class": "Drug Class", "count": "Count"}
    )
    fig_dc.update_xaxes(categoryorder='total descending')
    fig_dc.update_layout(xaxis_tickangle=45)
    fig_dc.show()

    # Show top 10 most frequent Resistance Mechanism values
    print("\nTop 10 Resistance Mechanisms:")
    top_rm_df = top_resistance_mechanisms(merged_df, n=10)
    print(top_rm_df)

    # Generate a bar chart of the top Resistance Mechanisms
    fig_rm = px.bar(
        top_rm_df,
        x="Resistance Mechanism",
        y="count",
        title="Top 10 Resistance Mechanisms",
        labels={"Resistance Mechanism": "Resistance Mechanism", "count": "Count"}
    )
    fig_rm.update_xaxes(categoryorder='total descending')
    fig_rm.update_layout(xaxis_tickangle=45)
    fig_rm.show()

    # Generate the combined plot
    print("\nGenerating plot for Drug Class vs. Resistance Mechanism...")
    plot_drug_class_resistance_mechanisms(merged_df)


if __name__ == "__main__":
    main()