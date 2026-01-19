"""Configuration constants for PRIP (Protein Residue Interaction Parser)."""

from typing import Final

# Color scheme
WHITEGRAY: Final[str] = "#F0F4EF"
WHITE: Final[str] = "#FFFFFF"
LIGHTBLUE: Final[str] = "#5C80BC"
DARKBLUE: Final[str] = "#011936"
BLACK: Final[str] = "#000000"

# Font settings
FONT_NAME: Final[str] = "Courier"
FONT_SIZE_LARGE: Final[int] = 22
FONT_SIZE_MEDIUM: Final[int] = 16
FONT_SIZE_NORMAL: Final[int] = 12
FONT_SIZE_SMALL: Final[int] = 10
FONT_SIZE_TINY: Final[int] = 8

# Application settings
WINDOW_WIDTH: Final[int] = 1200
WINDOW_HEIGHT: Final[int] = 750
MAX_RULES: Final[int] = 12
STARTING_RULES: Final[int] = 5

# File paths
DEFAULT_RULES_FILE: Final[str] = "saved_rules.json"

# Accepted amino acid abbreviations (3-letter and 1-letter codes)
ACCEPTED_AMINO_ACIDS: Final[tuple] = (
    'ALA', 'A', 'ARG', 'R', 'ASN', 'N', 'ASP', 'D', 'CYS', 'C', 
    'GLU', 'E', 'GLN', 'Q', 'GLY', 'G', 'HIS', 'H', 'ILE', 'I',
    'LEU', 'L', 'LYS', 'K', 'MET', 'M', 'PHE', 'F', 'PRO', 'P', 
    'SER', 'S', 'THR', 'T', 'TRP', 'W', 'TYR', 'Y', 'VAL', 'V'
)
