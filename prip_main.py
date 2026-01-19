"""Main module for PRIP (Protein Residue Interaction Parser) application."""

from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from Bio.PDB import PDBParser

from prip_parser import ProteinParser
from prip_parsecriteria import ParserCriteria
from prip_gui import GuiMaster
from config import (
    WHITEGRAY, WHITE, LIGHTBLUE, DARKBLUE, BLACK, FONT_NAME,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, FONT_SIZE_TINY, FONT_SIZE_NORMAL,
    MAX_RULES
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------- Page Navigation and Construction ------------------------------- #

def goto_criteria() -> None:
    """Navigate to the criteria configuration page."""
    gui.clear_page()
    gui.create_button(
        btn_text="Back", 
        btn_command=lambda: on_back_from_criteria(), 
        btn_width=10, 
        add_padx=(10), 
        add_pady=(10), 
        btn_column=0, 
        btn_row=0, 
        btn_sticky='nw', 
        btn_font=(FONT_NAME, FONT_SIZE_TINY, 'normal'), 
        btn_height=1
    )
    gui.create_label(
        lbl_text="Parse criteria", 
        lbl_font=(FONT_NAME, FONT_SIZE_MEDIUM, "bold"), 
        lbl_justify="center", 
        lbl_column=0, 
        lbl_row=0, 
        lbl_columnspan=4, 
        add_pady=(30, 30)
    )
    add_rule_btn = gui.create_button(
        btn_text="Add rule", 
        btn_command=lambda: add_rule(rules_frame, add_rule_btn), 
        btn_column=0, 
        btn_row=1, 
        btn_width=16, 
        btn_sticky='ne', 
        add_pady=(10), 
        btn_height=1, 
        btn_state=parse_criteria.can_add_rule
    )
    gui.create_button(
        btn_text="Import", 
        btn_command=lambda: on_import_rules(), 
        btn_column=1, 
        btn_row=1, 
        btn_width=16, 
        btn_sticky='ne', 
        add_pady=(10), 
        btn_height=1
    )
    gui.create_button(
        btn_text="Save", 
        btn_command=lambda: on_save_rules(), 
        btn_column=2, 
        btn_row=1, 
        btn_width=16, 
        btn_sticky='ne', 
        add_pady=(10), 
        btn_height=1
    )
    gui.create_label(
        lbl_text='Rule name', 
        lbl_column=0, 
        lbl_row=2, 
        lbl_sticky='nw', 
        add_padx=(10), 
        add_pady=(30, 0)
    )
    gui.create_label(
        lbl_text='Group 1', 
        lbl_column=1, 
        lbl_row=2, 
        lbl_sticky='n', 
        add_padx=(10), 
        add_pady=(30, 0)
    )
    gui.create_label(
        lbl_text='Group 2', 
        lbl_column=2, 
        lbl_row=2, 
        lbl_sticky='n', 
        add_padx=(10), 
        add_pady=(30, 0)
    )
    gui.create_label(
        lbl_text='Distance', 
        lbl_column=3, 
        lbl_row=2, 
        lbl_sticky='n', 
        add_padx=(10), 
        add_pady=(30, 0)
    )
    rules_frame = gui.create_frame(
        frm_parent=gui.window, 
        frm_bg=WHITE, 
        frm_row=3, 
        frm_column=0, 
        frm_columnspan=4, 
        frm_sticky='new', 
        frm_height=550
    )
    gui.reweight_rows_cols(row_weights=[2, 1, 1, 7], col_weights=[1, 2, 2, 1])
    initialize_rules(gui_frame=rules_frame)
    gui.reweight_frame_rows_cols(rew_frame=rules_frame, row_weights=None, col_weights=[1, 2, 2, 1])

def goto_mainpage() -> None:
    """Navigate to the main page with file selection and run options."""
    gui.canvas = Canvas(width=350, height=300, bg=WHITEGRAY, highlightthickness=0)
    gui.canvas.grid(column=1, row=0)
    gui.reweight_rows_cols(row_weights=[5, 2, 2, 1], col_weights=[1, 1, 1, 0])
    gui.create_label(
        lbl_text="Protein Residue Interaction Parser", 
        lbl_bg=WHITEGRAY, 
        lbl_fg=LIGHTBLUE, 
        lbl_font=(FONT_NAME, FONT_SIZE_LARGE, "bold"),
        lbl_wraplength=400, 
        lbl_justify="center", 
        lbl_column=0, 
        lbl_row=0, 
        lbl_columnspan=3
    )
    gui.create_button(
        btn_text="Select File", 
        btn_command=lambda: browse_files(), 
        btn_column=0, 
        btn_row=1, 
        btn_sticky='e'
    )
    gui.create_button(
        btn_text="Interaction criteria", 
        btn_command=lambda: goto_criteria(), 
        btn_column=2, 
        btn_row=1, 
        btn_sticky='w'
    )
    
    if not protein_parser.protein_file:
        display_filename = 'No file selected'
        run_button_state = 'disable'
    else:
        display_filename = f'Opened: {protein_parser.protein_name}'
        run_button_state = 'normal'
        model_cbo_box = gui.create_cbo_box(
            cbo_parent=gui.window, 
            cbo_dropdown_values=protein_parser.model_list, 
            cbo_column=0, 
            cbo_row=2, 
            cbo_sticky='e', 
            cbo_default_val=protein_parser.selected_model
        )
        model_cbo_box.bind('<<ComboboxSelected>>', lambda event: protein_parser.update_model(model_cbo_box.get()))
        gui.create_label(lbl_text='Model:', lbl_column=0, lbl_row=2)
        chain_cbo_box = gui.create_cbo_box(
            cbo_parent=gui.window, 
            cbo_dropdown_values=protein_parser.chain_list, 
            cbo_column=0, 
            cbo_row=3, 
            cbo_sticky='e', 
            cbo_default_val=protein_parser.selected_chain
        )
        chain_cbo_box.bind('<<ComboboxSelected>>', lambda event: protein_parser.update_chain(chain_cbo_box.get()))
        gui.create_label(lbl_text='Chain:', lbl_column=0, lbl_row=3)
        
    gui.create_label(
        lbl_text=display_filename, 
        lbl_fg=DARKBLUE, 
        lbl_font=(FONT_NAME, FONT_SIZE_SMALL, "normal"), 
        lbl_column=0, 
        lbl_row=4, 
        lbl_columnspan=3, 
        lbl_sticky='sw', 
        add_pady=(10, 0)
    )
    gui.create_button(
        btn_text="Run", 
        btn_state=run_button_state, 
        btn_command=lambda: run_and_goto_results(), 
        btn_column=1, 
        btn_row=1
    )

def goto_results_page():
    gui.clear_page()
    results_frame = gui.create_frame(frm_parent=gui.window, frm_columnspan=3, frm_sticky="news", add_padx=(5), add_pady=(5, 0), frm_rowconfigure=1, frm_columnconfigure=1)
    results_scrollbar = gui.create_scrollbar(scr_parent=results_frame, scr_row=0, scr_column=2)
    results_text = gui.create_text(txt_parent=results_frame, txt_yscrollcommand=results_scrollbar.set, txt_row=0, txt_column=0, txt_columnspan=3, txt_sticky='n',
                                   txt_text=protein_parser.parse_results.loc[:,['Residue 1', 'Residue 1 id', 'Residue 2', 'Residue 2 id', 'Distance']].head(50))
    results_text.config(highlightthickness=0, borderwidth=0)
    results_scrollbar.config(command=results_text.yview,)
    gui.create_button(btn_text="Go back", btn_command=lambda: [gui.clear_page(), goto_mainpage()], 
                      btn_column=0, btn_row=1, btn_sticky='sw', add_padx=(20, 10))
    gui.create_button(btn_text="Export results", btn_command=lambda: [prompt_save_excel()], btn_column=2, btn_row=1, btn_sticky='se', add_padx=(10, 20))
    criteria_frame = gui.create_frame(frm_parent=gui.window, frm_bg=WHITEGRAY, frm_width=60, frm_height=100, frm_row=1, frm_column=1, frm_sticky="nsew", add_padx=(5),
                                      add_pady=(40, 0), frm_rowconfigure=1, frm_columnconfigure=1)
    criteria_scroll = gui.create_scrollbar(scr_parent=criteria_frame, scr_row=1, scr_column=2)
    criteria_text = gui.create_text(txt_parent=criteria_frame, txt_row=1, txt_column=1, txt_sticky='w', txt_text=protein_parser.rule_summary)
    criteria_scroll.config(command=criteria_text.yview)
    gui.reweight_rows_cols(row_weights=[2, 1], col_weights=[1, 1])

# ---------------------------- General functions ------------------------------- #

def on_back_from_criteria() -> None:
    """Handle back button from criteria page."""
    parse_criteria.cache_rules()
    parse_criteria.reset_entry_widgets()
    gui.clear_page()
    goto_mainpage()

def on_import_rules() -> None:
    """Handle import rules button."""
    if parse_criteria.import_rules():
        parse_criteria.reset_entry_widgets()
        goto_criteria()
    else:
        messagebox.showerror("Import Error", "Failed to import rules file")

def on_save_rules() -> None:
    """Handle save rules button."""
    if parse_criteria.save_rules():
        messagebox.showinfo("Success", f"Rules saved to {parse_criteria.rules_file}")
    else:
        messagebox.showerror("Save Error", "Failed to save rules")

def run_and_goto_results() -> None:
    """Run the parser and navigate to results page."""
    if run_interaction_criteria(cached_rules=parse_criteria.cached_rules):
        goto_results_page()
    else:
        messagebox.showerror("Parse Error", "Failed to parse protein structure")

def browse_files() -> None:
    """Open file dialog to select a PDB file."""
    filename_fullpath = filedialog.askopenfilename(
        initialdir="/", 
        title="Select a File", 
        filetypes=(("PDB File", "*.pdb*"), ("all files", "*.*"))
    )
    
    if filename_fullpath and isinstance(filename_fullpath, str) and filename_fullpath != '':
        try:
            file_path = Path(filename_fullpath)
            filename = file_path.stem
            protein_parser.update_protein_name(filename)
            protein_parser.update_protein_file(file_path)
            if protein_parser.update_protein_structure():
                protein_parser.detect_models_chains()
            else:
                messagebox.showerror("File Error", "Failed to load PDB file")
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            messagebox.showerror("File Error", f"Error loading file: {e}")
    
    gui.clear_page()
    goto_mainpage()

def run_interaction_criteria(cached_rules: Optional[List[Dict[str, Any]]]) -> bool:
    """Run the parser with cached rules.
    
    Args:
        cached_rules: List of rule dictionaries
        
    Returns:
        True if parsing was successful
    """
    return protein_parser.run_parser(rule_cache=cached_rules)

def add_rule(gui_frame: Frame, btn: Button) -> None:
    """Add a new rule entry row to the criteria frame.
    
    Args:
        gui_frame: The parent frame to add widgets to
        btn: The add rule button (to disable when limit reached)
    """
    rule_name = gui.create_entry(
        ety_parent=gui_frame, 
        ety_sticky='w', 
        ety_row=parse_criteria.num_rules_index, 
        add_pady=(20, 0), 
        add_padx=(10, 0), 
        ety_column=0, 
        ety_width=15
    )
    rule_group1 = gui.create_entry(
        ety_parent=gui_frame, 
        ety_sticky='w', 
        ety_row=parse_criteria.num_rules_index, 
        add_pady=(20, 0), 
        add_padx=(60, 20), 
        ety_column=1, 
        ety_width=30
    )
    rule_group2 = gui.create_entry(
        ety_parent=gui_frame, 
        ety_sticky='w', 
        ety_row=parse_criteria.num_rules_index, 
        add_pady=(20, 0), 
        add_padx=(10, 20), 
        ety_column=2, 
        ety_width=30
    )
    rule_distance = gui.create_entry(
        ety_parent=gui_frame, 
        ety_sticky='w', 
        ety_row=parse_criteria.num_rules_index, 
        add_pady=(20, 0), 
        add_padx=(20, 10), 
        ety_column=3, 
        ety_width=5
    )
    parse_criteria.store_new_rule(new_rule_list=[rule_name, rule_group1, rule_group2, rule_distance])
    parse_criteria.num_rules_index += 1
    
    if parse_criteria.num_rules_index >= MAX_RULES:
        parse_criteria.can_add_rule = 'disable'
        btn['state'] = parse_criteria.can_add_rule

def initialize_rules(gui_frame: Frame) -> None:
    """Initialize rule entry widgets from cached rules.
    
    Args:
        gui_frame: The parent frame to add widgets to
    """
    for i in range(parse_criteria.num_rules_index):
        rule_name = gui.create_entry(
            ety_parent=gui_frame, 
            ety_sticky='w', 
            ety_row=i, 
            add_pady=(20, 0), 
            add_padx=(10, 0), 
            ety_column=0, 
            ety_width=15
        )
        rule_group1 = gui.create_entry(
            ety_parent=gui_frame, 
            ety_sticky='w', 
            ety_row=i, 
            add_pady=(20, 0), 
            add_padx=(60, 20), 
            ety_column=1, 
            ety_width=30
        )
        rule_group2 = gui.create_entry(
            ety_parent=gui_frame, 
            ety_sticky='w', 
            ety_row=i, 
            add_pady=(20, 0), 
            add_padx=(10, 20), 
            ety_column=2, 
            ety_width=30
        )
        rule_distance = gui.create_entry(
            ety_parent=gui_frame, 
            ety_sticky='w', 
            ety_row=i, 
            add_pady=(20, 0), 
            add_padx=(20, 10), 
            ety_column=3, 
            ety_width=5
        )
        parse_criteria.store_new_rule(new_rule_list=[rule_name, rule_group1, rule_group2, rule_distance])
        
        # Populate from cached rules if available
        if parse_criteria.cached_rules and i < len(parse_criteria.cached_rules):
            rule_name.insert(0, parse_criteria.cached_rules[i]["name"])
            rule_group1.insert(0, ','.join(parse_criteria.cached_rules[i]["grp1"]))
            rule_group2.insert(0, ','.join(parse_criteria.cached_rules[i]["grp2"]))
            rule_distance.insert(0, parse_criteria.cached_rules[i]["distance"])

def prompt_save_excel() -> None:
    """Prompt user to save results to Excel file."""
    excel_filename = filedialog.asksaveasfilename(
        initialdir="/", 
        title="Save results", 
        filetypes=(("Microsoft Excel", "*.xlsx*"), ("all files", "*.*")),
        defaultextension='.xlsx'
    )
    
    if excel_filename:
        if protein_parser.save_to_excel(excel_name=excel_filename):
            messagebox.showinfo("Success", f"Results saved to {Path(excel_filename).name}")
        else:
            messagebox.showerror("Save Error", "Failed to save results")

# ---------------------------- Program initiation ------------------------------- #

def main() -> None:
    """Initialize and start the PRIP application."""
    global gui, protein_parser, parse_criteria
    
    gui = GuiMaster()
    protein_parser = ProteinParser()
    parse_criteria = ParserCriteria()
    
    goto_mainpage()
    gui.window.mainloop()


if __name__ == "__main__":
    main()
