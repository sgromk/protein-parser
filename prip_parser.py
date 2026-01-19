"""Parser module for analyzing protein structures and residue interactions."""

from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import logging

from Bio.PDB import PDBParser, Structure, Model, Chain
from Bio.PDB.PDBExceptions import PDBConstructionException
import pandas as pd
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProteinParser:
    """Parses PDB files and analyzes residue-residue interactions."""
    
    def __init__(self) -> None:
        """Initialize the ProteinParser with default values."""
        self.protein_name: Optional[str] = None
        self.protein_file: Optional[Path] = None
        self.parser: PDBParser = PDBParser(QUIET=True)
        self.protein_structure: Optional[Structure.Structure] = None

        self.model_list: List[int] = []
        self.chain_list: List[str] = []
        self.selected_model: Union[int, float] = 0
        self.selected_chain: Union[str, int, float] = 0
        self.parse_results: Optional[pd.DataFrame] = None
        self.protein_file_selected: bool = False
        self.rule_results: List[Dict[str, Any]] = []
        self.rule_summary: str = ''

    def detect_models_chains(self) -> None:
        """Detect available models and chains in the loaded protein structure."""
        if not self.protein_structure:
            logger.warning("No protein structure loaded")
            return
            
        try:
            self.model_list = [model.serial_num for model in self.protein_structure]
            self.chain_list = [chain.get_id() for chain in self.protein_structure[0]]
            self.selected_model = self.model_list[0] if self.model_list else 0
            self.selected_chain = self.chain_list[0] if self.chain_list else 0
        except (IndexError, KeyError) as e:
            logger.error(f"Error detecting models/chains: {e}")
            self.model_list = []
            self.chain_list = []

    def update_model(self, new_model: Union[str, int, float]) -> None:
        """Update the selected model.
        
        Args:
            new_model: The new model identifier (can be string, int, or float)
        """
        if isinstance(new_model, str) and new_model.isdigit():
            new_model = float(new_model)
        self.selected_model = new_model

    def update_chain(self, new_chain: Union[str, int, float]) -> None:
        """Update the selected chain.
        
        Args:
            new_chain: The new chain identifier (can be string, int, or float)
        """
        if isinstance(new_chain, str) and new_chain.isdigit():
            new_chain = float(new_chain)
        self.selected_chain = new_chain

    def update_protein_name(self, new_protein_name: str) -> None:
        """Update the protein name.
        
        Args:
            new_protein_name: The new name for the protein
        """
        self.protein_name = new_protein_name

    def update_protein_file(self, new_protein_file: Union[str, Path]) -> None:
        """Update the protein file path.
        
        Args:
            new_protein_file: Path to the PDB file
        """
        self.protein_file = Path(new_protein_file) if isinstance(new_protein_file, str) else new_protein_file

    def update_protein_structure(self) -> bool:
        """Parse and load the protein structure from the file.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.protein_file or not self.protein_name:
            logger.error("Protein name or file not set")
            return False
            
        try:
            self.protein_structure = self.parser.get_structure(self.protein_name, str(self.protein_file))
            logger.info(f"Successfully loaded structure: {self.protein_name}")
            return True
        except (FileNotFoundError, PDBConstructionException) as e:
            logger.error(f"Error loading PDB file: {e}")
            self.protein_structure = None
            return False

    def run_parser(self, rule_cache: Optional[List[Dict[str, Any]]]) -> bool:
        """Parse protein residues and identify interactions based on rules.
        
        Args:
            rule_cache: List of rule dictionaries containing interaction criteria
            
        Returns:
            True if parsing was successful, False otherwise
        """
        if not self.protein_structure:
            logger.error("No protein structure loaded")
            return False
            
        try:
            final_result_list: List[List[Any]] = []
            self.rule_results = []
            chain: Chain.Chain = self.protein_structure[self.selected_model][self.selected_chain]
            parsable_rules: List[Dict[str, Any]] = []
            df_columns = ['Residue 1', 'Residue 1 id', 'Residue 2', 'Residue 2 id', 'Distance']
            
            # Prepare parsable rules
            if rule_cache:
                for cache in rule_cache:
                    if cache.get('parsable') == 'yes':
                        cache_copy = cache.copy()
                        cache_copy['results'] = []
                        cache_copy['counter'] = 0
                        parsable_rules.append(cache_copy)
                        df_columns.append(cache['name'])
            
            # Iterate through all residue pairs
            for residue1 in chain:
                for residue2 in chain:
                    if residue1 != residue2 and residue1 < residue2:
                        try:
                            # Calculate CA-CA distance
                            distance = residue1['CA'] - residue2['CA']
                        except KeyError:
                            # Skip if CA atom not found
                            continue
                        
                        # Extract residue information using BioPython methods
                        res_1_name = residue1.get_resname()
                        res_2_name = residue2.get_resname()
                        res_1_id = str(residue1.get_id()[1])
                        res_2_id = str(residue2.get_id()[1])
                        
                        line_data = [res_1_name, res_1_id, res_2_name, res_2_id, distance]
                        
                        # Check against each rule
                        for rule in parsable_rules:
                            if self._matches_rule(res_1_name, res_2_name, distance, rule):
                                rule['counter'] += 1
                                rule['results'].append(line_data[:5])
                                line_data.append('X')
                            else:
                                line_data.append(np.nan)
                        
                        final_result_list.append(line_data)
            
            # Create results DataFrame
            self.parse_results = pd.DataFrame(final_result_list, columns=df_columns)
            self.parse_results.index += 1
            
            # Generate rule summary
            intermediate_rule_summary = 'Matches:\n'
            for rule in parsable_rules:
                results_df = pd.DataFrame(rule['results'], columns=df_columns[:5])
                rule['results'] = results_df
                self.rule_results.append(rule)
                intermediate_rule_summary += f'{rule["name"]}: {rule["counter"]}\n'
            
            self.rule_summary = intermediate_rule_summary
            logger.info(f"Parsing complete. Found {len(final_result_list)} residue pairs")
            return True
            
        except (KeyError, IndexError) as e:
            logger.error(f"Error during parsing: {e}")
            return False
    
    def _matches_rule(self, res1: str, res2: str, distance: float, rule: Dict[str, Any]) -> bool:
        """Check if a residue pair matches a given rule.
        
        Args:
            res1: First residue name
            res2: Second residue name
            distance: Distance between residues
            rule: Rule dictionary with groups and distance threshold
            
        Returns:
            True if the pair matches the rule, False otherwise
        """
        grp1 = rule.get('grp1', [])
        grp2 = rule.get('grp2', [])
        max_distance = rule.get('distance', float('inf'))
        
        return (
            (res1 in grp1 and res2 in grp2 and distance < max_distance) or
            (res1 in grp2 and res2 in grp1 and distance < max_distance)
        )


    def save_to_excel(self, excel_name: Union[str, Path]) -> bool:
        """Save parsing results to an Excel file.
        
        Args:
            excel_name: Path to the output Excel file
            
        Returns:
            True if save was successful, False otherwise
        """
        if self.parse_results is None:
            logger.error("No results to save")
            return False
        
        if not excel_name:
            logger.error("No filename provided")
            return False
            
        try:
            excel_path = Path(excel_name)
            writer = pd.ExcelWriter(
                excel_path, 
                engine='xlsxwriter', 
                engine_kwargs={'options': {'strings_to_numbers': True}}
            )
            
            # Write comprehensive results
            self.parse_results.to_excel(
                excel_writer=writer, 
                sheet_name='Comprehensive', 
                freeze_panes=(1, 0), 
                index=False
            )
            
            # Write individual rule results
            for result in self.rule_results:
                result['results'].to_excel(
                    excel_writer=writer, 
                    sheet_name=result['name'][:31],  # Excel sheet name limit is 31 chars
                    freeze_panes=(1, 0), 
                    index=False
                )
            
            writer.close()
            logger.info(f"Results saved to {excel_path}")
            return True
            
        except (IOError, PermissionError) as e:
            logger.error(f"Error saving Excel file: {e}")
            return False