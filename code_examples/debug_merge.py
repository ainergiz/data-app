"""
debug_merge.py

Debug script to investigate why the merge between aro_index.tsv and aro_categories.tsv
is only returning 1 row instead of thousands.
"""

import pandas as pd

# Load the files
aro_index_df = pd.read_csv('data/aro_index.tsv', sep='\t')
aro_categories_df = pd.read_csv('data/aro_categories.tsv', sep='\t')

print("aro_index.tsv shape:", aro_index_df.shape)
print("aro_categories.tsv shape:", aro_categories_df.shape)

print("\naro_index.tsv columns:", list(aro_index_df.columns))
print("aro_categories.tsv columns:", list(aro_categories_df.columns))

print("\nFirst 5 ARO Accessions in aro_index.tsv:")
print(aro_index_df['ARO Accession'].head())

print("\nFirst 5 ARO Accessions in aro_categories.tsv:")
print(aro_categories_df['ARO Accession'].head())

# Check for unique values
print(f"\nUnique ARO Accessions in aro_index.tsv: {aro_index_df['ARO Accession'].nunique()}")
print(f"Unique ARO Accessions in aro_categories.tsv: {aro_categories_df['ARO Accession'].nunique()}")

# Check overlap
aro_index_accessions = set(aro_index_df['ARO Accession'])
aro_categories_accessions = set(aro_categories_df['ARO Accession'])

overlap = aro_index_accessions.intersection(aro_categories_accessions)
print(f"\nOverlap between files: {len(overlap)}")

print("\nSample overlapping accessions:")
print(list(overlap)[:10])

# Try the merge
merged = pd.merge(aro_index_df, aro_categories_df, on='ARO Accession', how='inner')
print(f"\nMerged DataFrame shape: {merged.shape}")

if merged.shape[0] > 0:
    print("\nFirst few rows of merged DataFrame:")
    print(merged[['ARO Accession', 'Drug Class', 'Resistance Mechanism', 'Protein Accession']].head()) 