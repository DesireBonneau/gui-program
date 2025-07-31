# Importing necessary libraries
import tkinter as tk
from tkinter import ttk
# Importing custom window classes
from home_window import HomeWindow
from pre_docking_window import PreDockingWindow
from post_docking_window import PostDockingWindow
from misc_window import MiscellaneousWindow
from credits_window import CreditsWindow
from tools.prototype_tool_window import ToolWindowPrototype
from tools.pre_docking.try1 import HERGPredictorWindow
from tools.pre_docking.try2 import FAKEPredictorWindow
# Set DPI awareness for high DPI displays on Windows
# IMPORTANT: Also need to account for Macs and Linux
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # for per-monitor DPI awareness
except AttributeError:
    pass


class MainApp(tk.Tk):
    def __init__(self):
        """
        Since I'm using the Frame-Swapping Method, this class is simply to host the main window.

        Have more docstrings later.
        """
        super().__init__()
        # Importing the theme file
        self.tk.call('source', "tkinter_theme/forest-light.tcl")
        ttk.Style().theme_use('forest-light')
        # To change the font size of the TLabelframe.Label
        style = ttk.Style()
        style.configure("TLabelframe.Label", font=("Helvetica Black", 10, "bold"))

        # Window configuration
        self.title("Program")
        self.geometry("1200x800")

        # ADD THE TOOL NAMES (FOR PRE/POST-DOCKING/MISC WINDOWS) HERE
        self.pre_docking_button_texts = self.wrap_and_pad_tool_names([
            "",
            "TOOL 1",               # index=1
            "TOOL 2",               # index=2
            "TOOL 3",               # index=3
            "TOOL 4",               # index=4
            "TOOL 5",               # index=5
            "TOOL 6",               # index=6
            "TOOL 7",               # index=7
            "TOOL 8",               # index=8
            "TOOL 9",               # index=9
        ])

        self.post_docking_button_texts = self.wrap_and_pad_tool_names([
            "",
            "RESIDUE TARGETING",    # index=1
            "TOOL 2",               # index=2
            "TOOL 3",               # index=3
            "TOOL 4",               # index=4
            "TOOL 5",               # index=5
            "TOOL 6",               # index=6
            "TOOL 7",               # index=7
            "TOOL 8",               # index=8
            "TOOL 9",               # index=9
        ])

        self.misc_button_texts = self.wrap_and_pad_tool_names([
            "",
            "MOLECULE COUNTER",                     # index=1
            "TRUNCATE LONG MOLECULE NAMES/IDs",     # index=2
            "SDF/MOL2 FILE SPLITTER",               # index=3
            "FILE MERGER: SDF/MOL2/SMI",            # index=4
            "SMILES TO SDF CONVERTER",              # index=5
            "MOL2/SDF TO SMILES CONVERTER",         # index=6
            "SDF DOCKING SCORE FILTER",             # index=7
            "MOLECULE VIEWER AND MANUAL FILTERING", # index=8
            "SDF TO MOLECULE IMAGE GRID",           # index=9
        ])


        # Create a container frame
        self.frames = {}
        for class_name, name, kwargs in [
            # Add more frames here as needed
            (HomeWindow, "home", {}),

            (PreDockingWindow, "pre_docking", {"tool_list": self.pre_docking_button_texts, "max_tool_width": self.get_max_tool_width(self.pre_docking_button_texts)}),
            (PostDockingWindow, "post_docking", {"tool_list": self.post_docking_button_texts, "max_tool_width": self.get_max_tool_width(self.post_docking_button_texts)}),
            (MiscellaneousWindow, "misc", {"tool_list": self.misc_button_texts, "max_tool_width": self.get_max_tool_width(self.misc_button_texts)}),

            (CreditsWindow, "credits", {}),

            # PRE-DOCKING TOOLS

            # POST-DOCKING TOOLS
            (ToolWindowPrototype, "residue_targeting",{"tool_name": "RESIDUE TARGETING", "tool_category": "post_docking", "tool_inputs": "residue_targeting_inputs.txt", "path_to_code": "tools/post_docking/residue_targeting_david.py"}),

            # MISC TOOLS
            (ToolWindowPrototype, "molecule_counter", {"tool_name": "Molecule Counter", "tool_category": "misc", "tool_inputs": "molecule_counter_inputs.txt", "path_to_code": "tools/misc/molecule_counter.py"}),
            (ToolWindowPrototype, "truncate_long_molecule_names", {"tool_name": "Truncate Long Molecule Names/IDs", "tool_category": "misc", "tool_inputs": "truncate_long_molecule_names_inputs.txt", "path_to_code": "tools/misc/truncate_long_molecule_names.py"}),
            (ToolWindowPrototype, "sdf_mol2_file_splitter", {"tool_name": "SDF/MOL2 File Splitter", "tool_category": "misc", "tool_inputs": "sdf_mol2_file_splitter_inputs.txt", "path_to_code": "tools/misc/sdf_mol2_file_splitter.py"}),
            (ToolWindowPrototype, "file_merger_sdf_mol2_smi", {"tool_name": "File Merger: SDF/MOL2/SMI", "tool_category": "misc", "tool_inputs": "file_merger_sdf_mol2_smi_inputs.txt", "path_to_code": "tools/misc/file_merger_sdf_mol2_smi.py"}),
            (ToolWindowPrototype, "smiles_to_sdf_converter", {"tool_name": "SMILES to SDF Converter", "tool_category": "misc", "tool_inputs": "smiles_to_sdf_converter_inputs.txt", "path_to_code": "tools/misc/smiles_to_sdf_converter.py"}),
            (ToolWindowPrototype, "mol2_or_sdf_to_smiles_converter", {"tool_name": "MOL2/SDF to SMILES Converter", "tool_category": "misc", "tool_inputs": "mol2_or_sdf_to_smiles_converter_inputs.txt", "path_to_code": "tools/misc/mol2_or_sdf_to_smiles_converter.py"}),
            (ToolWindowPrototype, "sdf_docking_score_filter", {"tool_name": "SDF Docking Score Filter", "tool_category": "misc", "tool_inputs": "sdf_docking_score_filter_inputs.txt", "path_to_code": "tools/misc/sdf_docking_score_filter.py"}),
            (ToolWindowPrototype, "molecule_viewer_and_manual_filtering", {"tool_name": "Molecule Viewer and Manual Filtering", "tool_category": "misc", "tool_inputs": "molecule_viewer_and_manual_filtering_inputs.txt", "path_to_code": "tools/misc/molecule_viewer_and_manual_filtering.py"}),
            (ToolWindowPrototype, "sdf_to_molecule_image_grid", {"tool_name": "SDF to Molecule Image Grid", "tool_category": "misc", "tool_inputs": "sdf_to_molecule_image_grid_inputs.txt", "path_to_code": "tools/misc/sdf_to_molecule_image_grid.py"}),

        ]:
            if kwargs:
                frame = class_name(self, self.show_screen, **kwargs)
            else:
                frame = class_name(self, self.show_screen)
            self.frames[name] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            frame.place_forget()  # Hides the frame until you show it

            # replaced by the conditional statements above
            # frame = class_name(self, self.show_screen)
        self.show_screen("home")  # Show this window by default

        # Menubar setup
        # CHANGE THE DESIGN OF THE MENUBAR
        self.menubar = tk.Menu(self)

        # Create the File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        # Perhaps edit the name of the new file option
        self.file_menu.add_command(label="New File")
        self.file_menu.add_command(label="Previous Page")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Settings")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        # Add this sub-menu to the menubar
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # Create the Edit menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label="Undo")
        self.edit_menu.add_command(label="Redo")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut")
        self.edit_menu.add_command(label="Copy")
        self.edit_menu.add_command(label="Paste")
        self.edit_menu.add_command(label="Select All")
        # Add this sub-menu to the menubar
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)

        # Create the View menu
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_command(label="Appearance")
        self.view_menu.add_command(label="Fullscreen")
        # Add this sub-menu to the menubar
        self.menubar.add_cascade(label="View", menu=self.view_menu)

        # Create the Default menu
        self.default_menu = tk.Menu(self.menubar, tearoff=0)
        self.default_menu.add_command(label="Default setting for ...")
        self.default_menu.add_command(label="Default setting for ...")
        self.default_menu.add_command(label="Default setting for ...")
        # Add this sub-menu to the menubar
        self.menubar.add_cascade(label="Default", menu=self.default_menu)

        # Create the Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="About")
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Getting Started")
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Contact")
        # Add this sub-menu to the menubar
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        self.config(menu=self.menubar)


    def show_screen(self, name):
        for fname, frame in self.frames.items():
            if fname == name:
                frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            else:
                frame.place_forget()


    def get_pre_docking_tool_list(self):
        """
        Returns the list of tools available in the pre-docking window.
        """
        return self.pre_docking_button_text


    def get_post_docking_tool_list(self):
        """
        Returns the list of tools available in the post-docking window.
        """
        return self.post_docking_button_text


    def get_misc_tool_list(self):
        """
        Returns the list of tools available in the miscellaneous window.
        """
        return self.misc_button_text

    def get_max_tool_width(self, tool_list):
        """
        Given a list of possibly multi-line button labels,
        return the length of the longest line among all labels.
        """
        max_width = 0
        for label in tool_list:
            # Split each label into its lines and get the max length line
            lines = label.split('\n')
            width = max(len(line) for line in lines)
            if width > max_width:
                max_width = width
        return max_width


    def wrap_and_pad_tool_names(self, tool_names, max_chars=20):
        def wrap_text(text, max_chars):
            words = text.split()
            lines = []
            current = ""
            for word in words:
                if len(current + " " + word) <= max_chars:
                    if current:
                        current += " " + word
                    else:
                        current = word
                else:
                    lines.append(current)
                    current = word
            lines.append(current)
            return lines

        # Wrap all tool names
        wrapped_lists = [wrap_text(name, max_chars) for name in tool_names]
        # Find the max number of lines
        max_lines = max(len(lines) for lines in wrapped_lists)
        # Pad all to same number of lines
        padded_names = [
            "\n".join(lines + [""] * (max_lines - len(lines))) for lines in wrapped_lists
        ]
        return padded_names


if __name__ == "__main__":
    MainApp().mainloop()