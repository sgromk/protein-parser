# PRIP - Protein Residue Interaction Parser

A desktop application for analyzing protein structures from PDB files to identify residue-residue interactions based on distance criteria and amino acid types.

## Features

- **PDB File Loading**: Opens and parses Protein Data Bank files using BioPython
- **Model/Chain Selection**: Select specific models and chains from multi-model PDB structures
- **Custom Interaction Rules**: Define rules specifying amino acid groups and distance thresholds
- **Rule Management**: Save/import rule sets as JSON files for reuse
- **Interaction Detection**: Parses all residue pairs, calculating CA-CA distances
- **Results Display**: Shows matching residue pairs with distances and rule matches
- **Excel Export**: Exports results with comprehensive and per-rule sheets

## Installation

Install Python dependencies:
```bash
pip install biopython pandas xlsxwriter numpy
```

## Usage

Run the application:
```bash
python prip_main.py
```

1. Click "Select File" to load a PDB file
2. Select the desired model and chain
3. Click "Interaction criteria" to configure rules
4. Define rules with amino acid groups and distance thresholds
5. Click "Run" to analyze the protein
6. Export results to Excel
