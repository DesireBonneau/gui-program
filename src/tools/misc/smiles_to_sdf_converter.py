import os
import re
import pandas as pd
from rdkit import Chem
from rdkit.Chem import PandasTools
from tqdm import tqdm

def clean_smiles(smiles):
    """Remove unwanted characters from SMILES."""
    return re.sub(r'[^A-Za-z0-9@+\-\[\]\(\)\\\/%=#$&*~`.,!?\'\":;_]', '', smiles)

def add_formal_charges(mol):
    """Add missing formal charges to nitrogen, boron, and oxygen atoms."""
    mol.UpdatePropertyCache(strict=False)
    for at in mol.GetAtoms():
        if at.GetAtomicNum() == 7 and at.GetExplicitValence() == 4:
            mol.GetAtomWithIdx(at.GetIdx()).SetFormalCharge(1)
        if at.GetAtomicNum() == 5 and at.GetExplicitValence() == 4:
            mol.GetAtomWithIdx(at.GetIdx()).SetFormalCharge(-1)
        if at.GetAtomicNum() == 8 and at.GetExplicitValence() == 1:
            mol.GetAtomWithIdx(at.GetIdx()).SetFormalCharge(-1)
    return mol

def read_smiles_file(input_file):
    """Read SMILES from .smi, .csv, or .txt file into a DataFrame."""
    ext = os.path.splitext(input_file)[1].lower()
    if ext == '.smi':
        df = pd.read_csv(input_file, sep=r'\s+', header=None, names=['Smiles'], engine='python')
    elif ext == '.csv':
        df = pd.read_csv(input_file)
        smiles_col = next((col for col in df.columns if col.lower() == 'smiles'), None)
        if smiles_col is None:
            raise ValueError("CSV must contain a 'smiles' column.")
        df = df.rename(columns={smiles_col: 'Smiles'})
    elif ext == '.txt':
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        df = pd.DataFrame({'Smiles': lines})
    else:
        raise ValueError("Unsupported file format. Use .smi, .csv, or .txt")
    return df

def main(input_file):
    """Main function to convert SMILES to SDF with formal charges applied."""
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"File not found: {input_file}")

    df = read_smiles_file(input_file)
    df['Smiles'] = df['Smiles'].apply(clean_smiles)

    # Convert SMILES to RDKit molecules and apply charge fixes
    mols = []
    valid_smiles = []
    for smi in tqdm(df['Smiles'], desc="Processing SMILES", unit="SMILES"):
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            mol = add_formal_charges(mol)
            mols.append(mol)
            valid_smiles.append(smi)

    if not mols:
        raise ValueError("No valid SMILES found in the input file after cleaning and processing.")

    # Prepare output DataFrame
    output_df = pd.DataFrame({'Smiles': valid_smiles})
    output_df['Molecule'] = mols

    # Create output path in the same folder, using input filename + .sdf
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_path = os.path.join(os.path.dirname(input_file), f"{base_name}.sdf")

    PandasTools.WriteSDF(output_df, output_path, molColName='Molecule', properties=list(output_df.columns))

    return output_path

