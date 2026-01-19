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

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

2. Install system dependencies (Linux):
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

3. Install Python dependencies:
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

## Recent Improvements (2026-01-18)

### Code Quality Enhancements

1. **Type Hints**: Added comprehensive type hints throughout all modules for better IDE support and type checking
2. **Docstrings**: Added detailed docstrings to all classes and functions explaining parameters and return values
3. **Error Handling**: Implemented try/except blocks around file I/O, PDB parsing, and data operations with logging
4. **Input Validation**: Added validation for distance values and amino acid codes before processing

### Architecture Improvements

5. **Shared Configuration**: Created `config.py` with centralized constants (colors, fonts, limits)
6. **Path Handling**: Replaced string splitting with `pathlib.Path` for cross-platform file path handling
7. **BioPython Integration**: Using proper BioPython methods (`get_resname()`, `get_id()`) instead of string parsing
8. **Main Guard**: Added `if __name__ == "__main__"` pattern with proper initialization
9. **Logging**: Integrated Python logging framework for better debugging and error tracking

### Code Organization

10. **Separation of Concerns**: Extracted business logic from GUI callbacks into dedicated functions
11. **Error Messages**: Added user-friendly message boxes for errors and confirmations
12. **Magic Numbers**: Replaced hardcoded values with named constants (MAX_RULES, FONT_SIZES, etc.)
13. **Function Extraction**: Broke down complex lambda expressions into named functions

## Project Structure

```
PRIP/
├── config.py                  # Shared constants and configuration
├── prip_main.py              # Main application entry point
├── prip_gui.py               # GUI widget creation and management
├── prip_parser.py            # Protein structure parsing logic
├── prip_parsecriteria.py     # Rule management and validation
└── saved_rules.json          # Saved interaction rules (generated)
```

## Configuration

Edit `config.py` to customize:
- Color scheme
- Font sizes
- Window dimensions
- Maximum number of rules
- Default rules file location
- Accepted amino acid abbreviations

## Dependencies

- Python 3.8+
- tkinter (usually included with Python)
- biopython
- pandas
- xlsxwriter
- numpy

## License

This project is provided as-is for educational and research purposes.

## TODO

- Add delete button for individual rules
- Implement rule validation before running parser
- Add progress bar for long-running analyses
- Package as standalone executable
- Add unit tests
- Support additional file formats (mmCIF)
