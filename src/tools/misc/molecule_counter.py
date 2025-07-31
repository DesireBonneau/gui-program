import os
import sys
from tqdm import tqdm

def main(input_file):
    # Usage: python script.py <fichier.smi | fichier.sdf | fichier.mol2>
    # Check if the file exists
    if not os.path.isfile(input_file):
        print(f"The file {input_file} does not exist.")
        sys.exit(1)

    # Get the file extension
    file_extension = input_file.split('.')[-1]

    # Process based on file extension
    if file_extension == "smi":
        # If the file is a .smi, extract and display the SMILES
        print("The file is a .smi file.")
        with open(input_file, "r") as f:
            smiles_input = [line.split()[0] for line in tqdm(f, desc="Processing SMILES")]
        print(f"SMILES extracted from the file {input_file}:")
        print("\n".join(smiles_input))
        print(f"SMILES extracted from the file {input_file}:")
        print("\n".join(smiles_input))

    elif file_extension == "sdf":
        # If the file is a .sdf, count the number of molecules
        print("The file is a .sdf file.")
        with open(input_file, "r") as f:
            # Count the number of occurrences of the $$$$ separator
            content = f.read()
            num_molecules = sum(1 for _ in tqdm(content.split("$$$$"), desc="Counting molecules") if _)
        print(f"The file {input_file} contains {num_molecules} molecules.")

    elif file_extension == "mol2":
        # If the file is a .mol2, count the number of molecules
        print("The file is a .mol2 file.")
        with open(input_file, "r") as f:
            # Count the number of occurrences of the @<TRIPOS>MOLECULE tag
            content = f.read()
            num_molecules = sum(1 for _ in tqdm(content.split("@<TRIPOS>MOLECULE"), desc="Counting molecules") if _)
        print(f"The file {input_file} contains {num_molecules} molecules.")

    else:
        print("Unsupported format. Please provide a .smi, .sdf, or .mol2 file.")
        sys.exit(1)