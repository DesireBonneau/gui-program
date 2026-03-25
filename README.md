# GUI Program Platform
A desktop application designed to provide a unified, user-friendly graphical interface (GUI) for computational chemistry and cheminformatics tools.



## Description
This program serves as an extensible "dashboard" or "launcher" for molecular data processing scripts. It targets computational chemistry workflows, specifically those involving molecular docking. It provides graphical tools to manipulate, analyze, and visualize molecular data files (like SDF, MOL2, and SMILES formats), allowing researchers to easily perform complex file conversions, filtering, and post-docking analysis without operating the command line.

The application uses the **Prototype design pattern** via the `ToolWindowPrototype` class. This abstracts the Tkinter GUI implementation away from the underlying scientific tools, enabling non-computational chemists to seamlessly integrate and run their own custom Python scripts.



## Tool Categories
The tools are organized into three primary categories:
- **Pre-Docking Tools**: For preparing ligands and making early predictions prior to docking.
- **Post-Docking Tools**: For computing global statistics over docking results and analyzing pose-residue interactions.
- **Miscellaneous Tools**: Utility scripts for counting, merging, splitting, converting, and filtering data files, as well as visualizing 2D molecular structures.



## How to Add a New Tool
Adding a new tool to the UI requires no GUI programming. Developers simply need to focus on the logic and configuration.

### 1. Create the Tool's Execution Script
Write your standalone Python script and place it in the appropriate folder (e.g., `src/tools/misc/my_custom_tool.py`).
Your script must contain a `main(**kwargs)` function as the entry point, which will receive the parameters collected from the UI.
```python
def main(input_file_path="", target_residue="", **kwargs):
    print(f"Running tool with {input_file_path} and {target_residue}")
    # ... your tool's logic ...
```

### 2. Define the UI Inputs
Create a text file in the corresponding `inputs` directory (e.g., `src/tools/misc/inputs/my_custom_tool_inputs.txt`). Each line in this file corresponds to an input field in the GUI.

Lines are formatted using `|||` as a delimiter:
`argument_name|||argument_type|||description|||browse_file(True/False)|||browse_dir(True/False)|||default_value`

Example:
```text
input_file|||string|||Path to the SDF file|||True|||False|||
score_threshold|||float|||Minimum docking score|||False|||False|||-8.0
```
*Note: The `argument_name` here exactly matches the keyword arguments passed to your `main()` function.*

### 3. Register the Tool in the Dashboard
Open `src/main.py` and assign your tool to the appropriate tool list (e.g., `misc_tools`). Append a dictionary configuration for your new tool:
```python
{
    "button_label": "MY CUSTOM TOOL",
    "window_name": "my_custom_tool",
    "toolwindow_kwargs": {
        "tool_name": "My Custom Tool",
        "tool_category": "misc", 
        "tool_inputs": "my_custom_tool_inputs.txt", 
        "path_to_code": "tools/misc/my_custom_tool.py"
    },
    "description": "A brief description of the tool to show in the UI menu.",
    "credits": "Author details, lab names, and paper citations (optional)."
}
```

By providing a `"credits"` string, the application will automatically list your attribution in the global Credits window alongside the core project team.

Once registered, clicking the tool's button will automatically parse your inputs text file, generate the necessary labels and entry widgets, and dynamically launch your script through the application's unified interface and built-in terminal.



## How to Start / Launch
To run the UI dashboard, open your terminal, navigate to the `src` directory, and execute the `main.py` file:
```bash
cd src
python main.py
```
*(Ensure you have your virtual environment or Conda environment activated before running this command).*



## Distributing the Application
To learn how to compile this project into a standalone `.exe` file for non-programmers, or to understand how updates are published and distributed to end-users, please read [DISTRIBUTION.md](DISTRIBUTION.md).



## Requirements
The project relies on a few external libraries for its UI and backend tools:
- `customtkinter` and `pillow` (for the UI)
- `rdkit`, `matplotlib`, `pandas`, `numpy`, `tqdm` (for backend tools)

*(Note: `tkinter` and `ttk` are included with standard Python 3.x installations).*

### Installation
You can install the dependencies using either **Conda** or **Pip**.

#### Option 1: Using Conda (Recommended)
You can create an isolated environment with all dependencies installed using the provided `environment.yml` file:
```bash
conda env create -f environment.yml
conda activate ui-program-env
```

#### Option 2: Using Python Pip
If you prefer not to use Conda, it is highly recommended to create a Python virtual environment first to isolate your dependencies:
```bash
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 3. Install the required dependencies
pip install -r requirements.txt
```
