"""GUI module for PRIP - handles all Tkinter widget creation and management."""

from typing import Optional, List, Callable, Any
from tkinter import *
from tkinter import ttk

from config import (
    WHITEGRAY, WHITE, LIGHTBLUE, DARKBLUE, BLACK, FONT_NAME,
    FONT_SIZE_NORMAL, WINDOW_WIDTH, WINDOW_HEIGHT
)

# ---------------------------- GUI / Widget skeletons ------------------------------- #

class GuiMaster:
    """Main GUI controller for PRIP application."""
    
    def __init__(self) -> None:
        """Initialize the main window and configure default settings."""
        self.window: Tk = Tk()
        self.window.title("Protein Residue Interaction Parser")
        self.window.config(padx=10, pady=5, bg=WHITEGRAY)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # Configure grid weights
        for i in range(3):
            self.window.columnconfigure(i, weight=1)
        self.window.rowconfigure(1, weight=3)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)

    def clear_page(self) -> None:
        """Destroy all widgets in the main window."""
        for widget in self.window.winfo_children():
            widget.destroy()

    def create_button(
        self, 
        btn_text: str, 
        btn_command: Callable, 
        btn_width: int = 22, 
        btn_height: int = 2, 
        btn_font: tuple = (FONT_NAME, FONT_SIZE_NORMAL, "normal"), 
        btn_columnspan: int = 1,
        btn_fit: str = 'grid', 
        btn_column: int = 0, 
        btn_row: int = 0, 
        btn_sticky: Optional[str] = None, 
        add_padx: int = 1, 
        add_pady: int = 1, 
        btn_state: str = 'normal'
    ) -> Button:
        """Create and place a button widget.
        
        Args:
            btn_text: Button label text
            btn_command: Function to call when button is clicked
            btn_width: Button width in characters
            btn_height: Button height in lines
            btn_font: Tuple of (font_family, size, style)
            btn_columnspan: Number of columns to span
            btn_fit: Layout manager ('grid' or 'pack')
            btn_column: Grid column position
            btn_row: Grid row position
            btn_sticky: Grid sticky direction
            add_padx: Horizontal padding
            add_pady: Vertical padding
            btn_state: Button state ('normal', 'disabled')
            
        Returns:
            The created Button widget
        """
        self.btn = Button(
            text=btn_text, 
            width=btn_width, 
            height=btn_height, 
            font=btn_font, 
            command=btn_command, 
            state=btn_state
        )
        if btn_fit == 'grid':
            self.btn.grid(
                column=btn_column, 
                row=btn_row, 
                sticky=btn_sticky, 
                padx=add_padx, 
                pady=add_pady, 
                columnspan=btn_columnspan
            )
        return self.btn

    def create_label(self, lbl_text, lbl_bg=WHITEGRAY, lbl_fg=BLACK, lbl_font=(FONT_NAME, 12, "normal"), lbl_wraplength=None, lbl_justify="center", 
                     lbl_fit='grid', lbl_column=0, lbl_row=0, lbl_columnspan=1, lbl_sticky=None, add_padx=1, add_pady=1):
        self.lbl = Label(text=lbl_text, bg=lbl_bg, fg=lbl_fg, font=lbl_font, wraplength=lbl_wraplength, justify=lbl_justify)
        if lbl_fit == 'grid':
            self.lbl.grid(column=lbl_column, row=lbl_row, columnspan=lbl_columnspan, stick=lbl_sticky, padx=add_padx, pady=add_pady)
        elif lbl_fit == 'pack':
            pass

    def create_cbo_box(self, cbo_parent, cbo_width=10, cbo_state='readonly', cbo_dropdown_values=['NA'], cbo_default_val=0,
                       cbo_fit='grid', cbo_column=0, cbo_row=0, cbo_sticky=None):
        self.cbo_box = ttk.Combobox(master=cbo_parent, width=cbo_width, state=cbo_state)
        self.cbo_box['values'] = cbo_dropdown_values
        self.cbo_box.set(cbo_default_val)
        if cbo_fit == 'grid':
            self.cbo_box.grid(column=cbo_column, row=cbo_row, sticky=cbo_sticky)
        elif cbo_fit == 'pack':
            pass
        return self.cbo_box

    def create_frame(self, frm_parent, frm_bg=WHITE, frm_width=500, frm_height=320, frm_fit='grid', frm_row=0, frm_column=0, frm_columnspan=1, 
                     frm_sticky = None, add_padx=1, add_pady=1, frm_grid_propagate=False, frm_rowconfigure=0, frm_columnconfigure=0):
        self.frm = Frame(master=frm_parent)
        self.frm.config(bg=frm_bg, width=frm_width, height=frm_height)
        if frm_fit == 'grid':
            self.frm.grid(row=frm_row, column=frm_column, columnspan=frm_columnspan, sticky=frm_sticky, padx=add_padx, pady=add_pady)
            self.frm.grid_propagate(frm_grid_propagate)
            self.frm.rowconfigure(frm_row, weight=frm_rowconfigure)
            self.frm.columnconfigure(frm_column, weight=frm_columnconfigure)
        elif frm_fit == 'pack':
            self.frm.pack(side='left', fill='both', expand=True)
            # self.frm.pack_propagate(frm_grid_propagate)
        return self.frm
    
    def create_canvas(self, can_parent, can_bg=WHITE, can_width=500, can_height=320, can_fit='grid', can_row=0, can_column=0, can_columnspan=1,
                      can_sticky=None, add_padx=1, add_pady=1, can_borderwidth=0):
        self.canv = Canvas(master=can_parent, borderwidth=can_borderwidth)
        if can_fit == 'grid':
            self.canv.grid(row=can_row, column=can_column, columnspan=can_columnspan, sticky=can_sticky, padx=add_padx, pady=add_pady)
            self.canv.grid_propagate(False)
        elif can_fit == 'pack':
            self.canv.pack(side="left", fill="both", expand=True)
            # self.canv.pack_propagate(False)
        return self.canv

    def create_scrollbar(self, scr_parent, scr_orient='vertical', scr_fit='grid', scr_row=0, scr_column=0, scr_sticky='nse', scr_command=None):
        self.scrl_bar = Scrollbar(master=scr_parent, orient=scr_orient, command=scr_command)
        if scr_fit == 'grid':
            self.scrl_bar.grid(row=scr_row, column=scr_column, stick=scr_sticky)
        elif scr_fit == 'pack':
            self.scrl_bar.pack(side="right", fill="y")
        return self.scrl_bar
    
    def create_text(self, txt_parent, txt_text='', txt_yscrollcommand=None, txt_font=(FONT_NAME, 12, "normal"), txt_fit='grid', txt_row=0, txt_column=0, 
                    txt_sticky='w', txt_columnspan=1):
        self.text = Text(master=txt_parent, font=txt_font, yscrollcommand=txt_yscrollcommand)
        self.text.insert(INSERT, txt_text)
        self.text.config(state='disabled') 
        if txt_fit == 'grid':
            self.text.grid(row=txt_row, column=txt_column, sticky=txt_sticky, columnspan=txt_columnspan)
        elif txt_fit == 'pack':
            self.text.pack(anchor='center')
        return self.text
    
    def reweight_rows_cols(self, row_weights, col_weights):
        for row in range(len(row_weights)):
            self.window.rowconfigure(index=row, weight=row_weights[row])
        for col in range(len(col_weights)):
            self.window.columnconfigure(index=col, weight=col_weights[col])
    
    def reweight_frame_rows_cols(self, rew_frame, row_weights, col_weights):
        if row_weights != None:
            for row in range(len(row_weights)):
                rew_frame.rowconfigure(index=row, weight=row_weights[row])
        if col_weights != None:
            for col in range(len(col_weights)):
                rew_frame.columnconfigure(index=col, weight=col_weights[col])
    
    def create_entry(self, ety_parent, ety_bg=WHITE, ety_fg=BLACK, ety_font=(FONT_NAME, 12, "normal"), ety_justify='left', 
                     ety_fit='grid', ety_row=0, ety_column=0, ety_sticky=None, add_padx=1, add_pady=1, ety_width=16, ety_pack=BOTTOM):
        self.entry_string = StringVar()
        self.entry = Entry(master=ety_parent, bg=ety_bg, fg=ety_fg, textvariable=self.entry_string, font=ety_font, justify=ety_justify, width=ety_width)
        if ety_fit == 'grid':
            self.entry.grid(row=ety_row, column=ety_column, sticky=ety_sticky, padx=add_padx, pady=add_pady)
            self.entry.grid_propagate(False)
        elif ety_fit == 'pack':
            self.entry.pack(side=ety_pack)
            self.entry.pack_propagate(False)
        return self.entry