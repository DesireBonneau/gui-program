# Importing necessary libraries
import tkinter as tk
from tkinter import ttk
# Importing custom window classes
from home_window import HomeWindow
from progress_patch import apply_patch
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
        style.configure("Accent.TButton", anchor="center")

        # Window configuration
        self.title("Program")
        self.geometry("1200x800")

        # Tool button texts
        pre_docking_tools = [
            {
                "button_label": "TRY 1",
                "window_name": "try_1",
                "toolwindow_kwargs": {
                    "tool_name": "Not sure",
                    "tool_category": "pre_docking",
                    "tool_inputs": "try1_inputs.txt",
                    "path_to_code": "tools/pre_docking/try1.py"
                },
                "description": "Prototype pre-docking step (placeholder)."
            },
            {
                "button_label": "TRY 2",
                "window_name": "try_2",
                "toolwindow_kwargs": {
                    "tool_name": "Not quite sure",
                    "tool_category": "pre_docking",
                    "tool_inputs": "try2_inputs.txt",
                    "path_to_code": "tools/pre_docking/try2.py"
                },
                "description": "Prototype pre-docking step (placeholder)."
            },
            {
                "button_label": "TRY 3",
                "window_name": "try_3",
                "toolwindow_kwargs": {
                    "tool_name": "Not quite sure again",
                    "tool_category": "pre_docking",
                    "tool_inputs": "try3_inputs.txt",
                    "path_to_code": "tools/pre_docking/try3.py"
                },
                "description": "Prototype pre-docking step (placeholder)."
            },
            # ... more tools
        ]

        post_docking_tools = [
            {
                "button_label": "GLOBAL COUNTER",
                "window_name": "global_counter",
                "toolwindow_kwargs": {
                    "tool_name": "Global Counter",
                    "tool_category": "post_docking",
                    "tool_inputs": "global_counter_inputs.txt",
                    "path_to_code": "tools/post_docking/global_counter.py"
                },
                "description": "Compute global stats over docking results: ligands, poses, and score distributions; quick sanity checks at a glance."
            },
            {
                "button_label": "RESIDUE TARGETING",
                "window_name": "residue_targeting",
                "toolwindow_kwargs": {
                    "tool_name": "Residue Targeting",
                    "tool_category": "post_docking",
                    "tool_inputs": "residue_targeting_inputs.txt",
                    "path_to_code": "tools/post_docking/residue_targeting.py"
                },
                "description": "Analyze pose–residue contacts/clashes vs a target residue set; flag ligands that best engage specified residues."
            },
            # ... more tools
        ]

        misc_tools = [
            {
                "button_label": "MOLECULE COUNTER",
                "window_name": "molecule_counter",
                "toolwindow_kwargs": {
                    "tool_name": "Molecule Counter",
                    "tool_category": "misc",
                    "tool_inputs": "molecule_counter_inputs.txt",
                    "path_to_code": "tools/misc/molecule_counter.py"
                },
                "description": "Count molecules across SDF/MOL2/SMI files (optionally per-file and unique IDs); outputs a tidy summary for quick QC"
            },
            {
                "button_label": "TRUNCATE LONG MOLECULE NAMES/IDs",
                "window_name": "truncate_long_molecule_names",
                "toolwindow_kwargs": {
                    "tool_name": "Truncate Long Molecule Names/IDs",
                    "tool_category": "misc",
                    "tool_inputs": "truncate_long_molecule_names_inputs.txt",
                    "path_to_code": "tools/misc/truncate_long_molecule_names.py"
                },
                "description": "Shorten over-long names/IDs to a safe length for downstream tools and UIs while keeping an unmangled copy in a new field."
            },
            {
                "button_label": "SDF/MOL2 FILE SPLITTER",
                "window_name": "sdf_mol2_file_splitter",
                "toolwindow_kwargs": {
                    "tool_name": "SDF/MOL2 File Splitter",
                    "tool_category": "misc",
                    "tool_inputs": "sdf_mol2_file_splitter_inputs.txt",
                    "path_to_code": "tools/misc/sdf_mol2_file_splitter.py"
                },
                "description": "Split a large SDF/MOL2 into evenly sized chunks (N molecules per file) for parallel docking or easier review."
            },
            {
                "button_label": "FILE MERGER: SDF/MOL2/SMI",
                "window_name": "file_merger_sdf_mol2_smi",
                "toolwindow_kwargs": {
                    "tool_name": "File Merger: SDF/MOL2/SMI",
                    "tool_category": "misc",
                    "tool_inputs": "file_merger_sdf_mol2_smi_inputs.txt",
                    "path_to_code": "tools/misc/file_merger_sdf_mol2_smi.py"
                },
                "description": "Merge multiple SDF/MOL2/SMI files into one, optionally deduplicating by ID or canonical SMILES and preserving fields."
            },
            {
                "button_label": "MOL2/SDF TO SMILES CONVERTER",
                "window_name": "mol2_or_sdf_to_smiles_converter",
                "toolwindow_kwargs": {
                    "tool_name": "MOL2/SDF to SMILES Converter",
                    "tool_category": "misc",
                    "tool_inputs": "mol2_or_sdf_to_smiles_converter_inputs.txt",
                    "path_to_code": "tools/misc/mol2_or_sdf_to_smiles_converter.py"
                },
                "description": "Extract canonical SMILES (and InChIKey) from MOL2/SDF; writes SMI/CSV for modeling or curation."
            },
            {
                "button_label": "SDF DOCKING SCORE FILTER",
                "window_name": "sdf_docking_score_filter",
                "toolwindow_kwargs": {
                    "tool_name": "SDF Docking Score Filter",
                    "tool_category": "misc",
                    "tool_inputs": "sdf_docking_score_filter_inputs.txt",
                    "path_to_code": "tools/misc/sdf_docking_score_filter.py"
                },
                "description": "Keep only top-N or thresholded poses based on a chosen score tag (e.g., Vina/Glide score); outputs filtered SDF+CSV."
            },
            {
                "button_label": "MOLECULE VIEWER AND MANUAL FILTERING",
                "window_name": "molecule_viewer_and_manual_filtering",
                "toolwindow_kwargs": {
                    "tool_name": "Molecule Viewer and Manual Filtering",
                    "tool_category": "misc",
                    "tool_inputs": "molecule_viewer_and_manual_filtering_inputs.txt",
                    "path_to_code": "tools/misc/molecule_viewer_and_manual_filtering.py"
                },
                "description": "Review structures and metadata, mark keep/remove by hand, and export selections for downstream steps."
            },
            {
                "button_label": "SDF TO MOLECULE IMAGE GRID",
                "window_name": "sdf_to_molecule_image_grid",
                "toolwindow_kwargs": {
                    "tool_name": "SDF to Molecule Image Grid",
                    "tool_category": "misc",
                    "tool_inputs": "sdf_to_molecule_image_grid_inputs.txt",
                    "path_to_code": "tools/misc/sdf_to_molecule_image_grid.py"
                },
                "description": "Render 2D depictions into a printable image grid (PNG/SVG), optionally annotated with name/score/ID."
            },
        ]


        # Create a container frame
        self.frames = {}


        # 1. First, dynamically add each misc tool's ToolWindowPrototype frame
        for tool in misc_tools:
            tool_window = ToolWindowPrototype(self, self.show_screen, **tool["toolwindow_kwargs"])
            self.frames[tool["window_name"]] = tool_window

        # Then the pre-docking tools
        for tool in pre_docking_tools:
            tool_window = ToolWindowPrototype(self, self.show_screen, **tool["toolwindow_kwargs"])
            self.frames[tool["window_name"]] = tool_window

        # Then the post-docking tools
        for tool in post_docking_tools:
            tool_window = ToolWindowPrototype(self, self.show_screen, **tool["toolwindow_kwargs"])
            self.frames[tool["window_name"]] = tool_window


        # 2. Now create the MiscellaneousWindow, passing the *whole* tool config list
        self.frames["misc"] = MiscellaneousWindow(
            self, self.show_screen, tool_configs=misc_tools
        )
        self.frames["pre_docking"] = PreDockingWindow(
            self, self.show_screen, tool_configs=pre_docking_tools
        )
        self.frames["post_docking"] = PostDockingWindow(
            self, self.show_screen, tool_configs=post_docking_tools
        )
        # 3. Keep the rest (credits, etc.) as before:
        for class_name, name, kwargs in [
            (HomeWindow, "home", {}),
            (CreditsWindow, "credits", {}),
            # etc. for other core windows
        ]:
            if kwargs:
                frame = class_name(self, self.show_screen, **kwargs)
            else:
                frame = class_name(self, self.show_screen)
            self.frames[name] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            frame.place_forget() # Hides the frame until you show it


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
                # Rebind tqdm to this frame’s progress bar if it has one
                if hasattr(frame, "progress_bar"):
                    apply_patch(frame.progress_bar)
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