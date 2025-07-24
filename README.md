# AMR Data Analysis Project

## Project Overview

This project is designed to analyze and visualize Antibiotic Resistance (AMR) data from the Comprehensive Antibiotic Resistance Database (CARD). It includes a series of Python scripts to explore, analyze, and visualize different aspects of AMR, including resistance genes, drug classes, resistance mechanisms, and Single Nucleotide Polymorphisms (SNPs).

The primary goal is to understand the prevalence of different resistance mechanisms and the relationships between drug classes and the genes or mutations that confer resistance to them.

## Getting Started

### Prerequisites

This project uses `uv` for environment and dependency management.

### Installation & Setup

1. **Install `uv`:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

### Running the Analyses

Each analysis can be run using the `uv run` command:

-   **Explore Drug Classes & Mechanisms:**
    ```bash
    uv run card_loader.py
    ```
-   **Analyze SNP-based Resistance:**
    ```bash
    uv run snp_analyzer.py
    ```
-   **See Resistance Breakdown for Fluoroquinolones:**
    ```bash
    uv run resistance_breakdown.py
    ```

## Scripts

- `card_loader.py`: Analyzes and visualizes the most common drug classes and resistance mechanisms from the main `aro_index.tsv` dataset.
- `snp_analyzer.py`: Focuses on SNP-based resistance, identifying and visualizing the top 10 genes most frequently affected by resistance-conferring mutations from `snps.txt`.
- `resistance_breakdown.py`: Combines data from the gene and SNP datasets to provide a complete picture of resistance mechanisms for a specific drug class (e.g., fluoroquinolones), showing the breakdown between acquired genes and point mutations.
- `debug_data_files.py`: A utility script to quickly inspect and preview the content of all files in the `data/` directory.

## Data Directory Overview

The `data/` directory contains the complete dataset from CARD. Here is a breakdown of the key files:

- **`aro_index.tsv`**: The main data file. Each row represents an AMR gene or mutation, detailing its ARO Accession, the drug class it confers resistance to, the resistance mechanism, and the AMR gene family.

- **`aro_categories.tsv`**: A data dictionary (ontology) that defines the terms and categories used in `aro_index.tsv`. It provides official names for `Drug Class`, `Resistance Mechanism`, etc.

- **`card.json`**: A comprehensive, structured JSON file that contains all the information from the various TSV files in a hierarchical format. It is likely the primary source from which the other files are derived.

- **`snps.txt`**: Contains detailed information on Single Nucleotide Polymorphisms (SNPs) that confer antibiotic resistance. This file is crucial for analyzing resistance that arises from mutations rather than the acquisition of new genes.

- **`*.fasta` files**: A collection of FASTA files containing the nucleotide and protein sequences for the various AMR gene models (e.g., `protein_fasta_protein_homolog_model.fasta`).

- **`CARD-Download-README.txt`**: Documentation providing context and information about the downloaded dataset.

- **`PMID.tsv`**: Contains PubMed IDs, linking the AMR data to the corresponding scientific literature.

- **`shortname_antibiotics.tsv` & `shortname_pathogens.tsv`**: Reference files that provide convenient abbreviations for antibiotic and pathogen names.
