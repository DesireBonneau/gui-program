import os
import pandas as pd
from tqdm import tqdm
from rdkit import Chem
from rdkit.Chem import MolFromMol2Block, SanitizeMol


def add_formal_charges(mol):
    """Add formal charges to nitrogens with 4 bonds, borons with 4 bonds, and oxygens with 1 bond."""
    mol.UpdatePropertyCache(strict=False)

    for at in mol.GetAtoms():
        if at.GetAtomicNum() == 7 and at.GetExplicitValence() == 4:
            mol.GetAtomWithIdx(at.GetIdx()).SetFormalCharge(1)
        elif at.GetAtomicNum() == 5 and at.GetExplicitValence() == 4:
            mol.GetAtomWithIdx(at.GetIdx()).SetFormalCharge(-1)
        elif at.GetAtomicNum() == 8 and at.GetExplicitValence() == 1:
            mol.GetAtomWithIdx(at.GetIdx()).SetFormalCharge(-1)


def mol2_block_generator(file_path):
    """Yield mol2 blocks one at a time from a large file."""
    with open(file_path, 'r') as f:
        block = []
        for line in f:
            if line.startswith("@<TRIPOS>MOLECULE"):
                if block:
                    yield ''.join(block)
                    block = []
            block.append(line)
        if block:
            yield ''.join(block)


def mol2_block_to_mol(block):
    try:
        mol = MolFromMol2Block(block, sanitize=False)
        if mol:
            SanitizeMol(mol)
        return mol
    except Exception:
        return None


def count_mol2_blocks(file_path):
    """Count number of molecules in mol2 file to set tqdm length."""
    count = 0
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("@<TRIPOS>MOLECULE"):
                count += 1
    return count


def convert_mol2_to_csv(input_file, output_file):
    data = []
    total = count_mol2_blocks(input_file)
    for i, block in enumerate(tqdm(mol2_block_generator(input_file), total=total, desc="Processing mol2"), 1):
        mol = mol2_block_to_mol(block)
        if mol:
            try:
                add_formal_charges(mol)
                mol_id = mol.GetProp("_Name") if mol.HasProp("_Name") else f"mol_{i}"
                smiles = Chem.MolToSmiles(mol)
                data.append((smiles, mol_id))
            except Exception as e:
                print(f"[mol_{i}] Conversion error: {e}")
        else:
            print(f"[mol_{i}] Invalid molecule")

    df = pd.DataFrame(data, columns=["SMILES", "ID"])
    df.to_csv(output_file, index=False)
    print(f"\nDone: {len(data)} valid molecules processed.")
    print(f"Output file: {output_file}")


def convert_sdf_to_csv(input_file, output_file):
    suppl = Chem.SDMolSupplier(input_file)
    total = sum(1 for _ in suppl)
    suppl = Chem.SDMolSupplier(input_file)  # reload after count
    data = []

    for i, mol in enumerate(tqdm(suppl, total=total, desc="Processing SDF"), 1):
        if mol is not None:
            try:
                add_formal_charges(mol)
                custom_id = f"POP_KI_{i}"
                smiles = Chem.MolToSmiles(mol)
                data.append((smiles, custom_id))
            except Exception as e:
                print(f"[POP_KI_{i}] Conversion error: {e}")
        else:
            print(f"[POP_KI_{i}] Invalid molecule")

    df = pd.DataFrame(data, columns=['SMILES', 'ID'])
    df.to_csv(output_file, index=False)
    print(f"\nDone: {len(data)} valid molecules processed.")
    print(f"Output file: {output_file}")


def main(input_file, output_file):
    ext = os.path.splitext(input_file)[1].lower()
    if ext == ".mol2":
        convert_mol2_to_csv(input_file, output_file)
    elif ext == ".sdf":
        convert_sdf_to_csv(input_file, output_file)
    else:
        print("Unsupported file format. Please provide a .mol2 or .sdf file.")


