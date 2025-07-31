# Import necessary libraries
import tkinter as tk
from tkinter import filedialog
import os
from tqdm import tqdm  # For progress bar

# Function to combine SDF, MOL2, and SMILES files
def main():
    # Open a file dialog to select multiple files (SDF, MOL2, SMILES)
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    file_list = filedialog.askopenfilenames(
        filetypes=[("SDF Files", "*.sdf"), ("MOL2 Files", "*.mol2"), ("SMILES Files", "*.smi")])
    # Check if any files were selected
    if file_list:
        # Use the current working directory as the save directory
        save_directory = os.getcwd()

        combined_content = ""
        sdf_separator = "\n$$$$\n"  # Standard separator for SDF files
        mol2_separator = "\n@<TRIPOS>MOLECULE\n"  # Standard separator for MOL2 files

        # Combine the content of all selected files
        for file in tqdm(file_list, desc="Combining files", unit="file"):
            with open(file, "r") as f:
                content = f.read().strip()

                # If it's an SDF file, use the $$$$ separator.
                if file.endswith(".sdf"):
                    if combined_content:
                        combined_content += sdf_separator + content
                    else:
                        combined_content = content
                elif file.endswith(".mol2"):
                    # For MOL2 files, use the @<TRIPOS>MOLECULE separator
                    if combined_content:
                        combined_content += mol2_separator + content
                    else:
                        combined_content = content
                elif file.endswith(".smi"):
                    # For SMILES files, just append them as a single line
                    if combined_content:
                        combined_content += "\n" + content
                    else:
                        combined_content = content

        # Define the output file path
        output_path = os.path.join(save_directory, "Combined-Results.sdf")

        # Write the combined content to the output file
        with open(output_path, "w") as out_file:
            out_file.write(combined_content)
        # Provide feedback to the user
        print(f"Combined file saved at '{output_path}'")