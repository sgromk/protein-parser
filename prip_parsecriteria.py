"""Module for managing and validating parsing criteria/rules for protein interactions."""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from tkinter import Entry

from config import ACCEPTED_AMINO_ACIDS, STARTING_RULES, MAX_RULES, DEFAULT_RULES_FILE

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParserCriteria:
    """Manages parsing rules for protein residue interactions."""
    
    def __init__(self, rules_file: str = DEFAULT_RULES_FILE) -> None:
        """Initialize ParserCriteria with default values.
        
        Args:
            rules_file: Path to the JSON file for saving/loading rules
        """
        self.num_rules_index: int = STARTING_RULES
        self.can_add_rule: str = 'normal'
        self.saved_rules: Dict[str, Any] = {"numRules": 0, "ruleList": []}
        self.rule_entry_widgets: List[Dict[str, Entry]] = []
        self.cached_rules: Optional[List[Dict[str, Any]]] = None
        self.accepted_abbrev: tuple = ACCEPTED_AMINO_ACIDS
        self.rules_file: Path = Path(rules_file)

    def store_new_rule(self, new_rule_list: List[Entry]) -> None:
        """Store a new rule's entry widgets for later retrieval.
        
        Args:
            new_rule_list: List of Entry widgets [name, group1, group2, distance]
        """
        if len(new_rule_list) != 4:
            logger.warning(f"Expected 4 widgets, got {len(new_rule_list)}")
            return
            
        entry_widget = {
            "name": new_rule_list[0],
            "grp1": new_rule_list[1],
            "grp2": new_rule_list[2],
            "distance": new_rule_list[3]
        }
        self.rule_entry_widgets.append(entry_widget)

    def save_rules(self) -> bool:
        """Save current rules to a JSON file.
        
        Returns:
            True if save was successful, False otherwise
        """
        self.cache_rules()
        
        if not self.cached_rules:
            logger.warning("No rules to save")
            return False
            
        try:
            with open(self.rules_file, 'w') as saving_file:
                json.dump(self.cached_rules, saving_file, indent=4)
            logger.info(f"Rules saved to {self.rules_file}")
            return True
        except (IOError, PermissionError) as e:
            logger.error(f"Error saving rules: {e}")
            return False

    def import_rules(self) -> bool:
        """Import rules from a JSON file.
        
        Returns:
            True if import was successful, False otherwise
        """
        try:
            if not self.rules_file.exists():
                logger.warning(f"Rules file not found: {self.rules_file}")
                return False
                
            with open(self.rules_file, 'r') as import_file:
                self.cached_rules = json.load(import_file)
                
            if isinstance(self.cached_rules, list):
                self.num_rules_index = len(self.cached_rules)
            else:
                logger.warning("Unexpected rules format")
                return False
                
            logger.info(f"Rules imported from {self.rules_file}")
            return True
            
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error importing rules: {e}")
            return False

    def cache_rules(self) -> None:
        """Cache current rules from entry widgets, validating format and content."""
        self.cached_rules = []
        
        for rule in self.rule_entry_widgets:
            rule_to_cache: Dict[str, Any] = {}
            parsable = 'yes'
            
            # Get rule name
            try:
                rule_to_cache["name"] = rule["name"].get().strip()
                if not rule_to_cache["name"]:
                    rule_to_cache["name"] = f"Rule {len(self.cached_rules) + 1}"
            except Exception as e:
                logger.warning(f"Error getting rule name: {e}")
                rule_to_cache["name"] = f"Rule {len(self.cached_rules) + 1}"
                parsable = 'no'
            
            # Get and validate distance
            try:
                distance_str = rule["distance"].get().strip()
                rule_to_cache["distance"] = float(distance_str)
                if rule_to_cache["distance"] <= 0:
                    logger.warning(f"Distance must be positive: {rule_to_cache['distance']}")
                    parsable = 'no'
            except (ValueError, AttributeError) as e:
                logger.warning(f"Invalid distance value: {e}")
                rule_to_cache["distance"] = rule["distance"].get()
                parsable = 'no'
            
            # Get and validate amino acid groups
            for group in ["grp1", "grp2"]:
                try:
                    current_group = rule[group].get().strip()
                    if not current_group:
                        rule_to_cache[group] = []
                        parsable = 'no'
                        continue
                        
                    split_rule = current_group.split(sep=",")
                    stripped_rule = [protein.strip().upper() for protein in split_rule]
                    rule_to_cache[group] = stripped_rule
                    
                    # Validate all abbreviations
                    for abbrev in stripped_rule:
                        if abbrev and abbrev not in self.accepted_abbrev:
                            logger.warning(f"Invalid amino acid abbreviation: {abbrev}")
                            parsable = 'no'
                            break
                            
                except (AttributeError, Exception) as e:
                    logger.warning(f"Error processing group {group}: {e}")
                    rule_to_cache[group] = rule[group].get() if hasattr(rule[group], 'get') else []
                    parsable = 'no'
            
            rule_to_cache['parsable'] = parsable
            self.cached_rules.append(rule_to_cache)
        
        logger.info(f"Cached {len(self.cached_rules)} rules")

    def reset_entry_widgets(self) -> None:
        """Clear all stored entry widget references."""
        self.rule_entry_widgets = []
        logger.debug("Entry widgets reset")

    def validate_rule_input(self, name: str, grp1: str, grp2: str, distance: str) -> tuple[bool, str]:
        """Validate rule input before adding.
        
        Args:
            name: Rule name
            grp1: Comma-separated amino acid codes for group 1
            grp2: Comma-separated amino acid codes for group 2
            distance: Maximum distance threshold
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate name
        if not name or not name.strip():
            return False, "Rule name cannot be empty"
        
        # Validate distance
        try:
            dist_val = float(distance)
            if dist_val <= 0:
                return False, "Distance must be positive"
        except ValueError:
            return False, "Distance must be a number"
        
        # Validate amino acid groups
        for group_name, group_value in [("Group 1", grp1), ("Group 2", grp2)]:
            if not group_value or not group_value.strip():
                return False, f"{group_name} cannot be empty"
            
            amino_acids = [aa.strip().upper() for aa in group_value.split(",")]
            for aa in amino_acids:
                if aa and aa not in self.accepted_abbrev:
                    return False, f"Invalid amino acid code in {group_name}: {aa}"
        
        return True, ""
