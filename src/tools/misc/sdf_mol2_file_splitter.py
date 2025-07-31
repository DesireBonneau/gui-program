import os
from rdkit import Chem
from tqdm import tqdm

def add_formal_charges(mol):
    """Add formal charges to nitrogens with 4 bonds, boron with 4 bonds, and oxygens with single bond."""
    mol.UpdatePropertyCache(strict=False)

    for at in mol.GetAtoms():
        if at.GetAtomicNum() == 7 and at.GetExplicitValence() == 4:
            at.SetFormalCharge(1)
        elif at.GetAtomicNum() == 5 and at.GetExplicitValence() == 4:
            at.SetFormalCharge(-1)
        elif at.GetAtomicNum() == 8 and at.GetExplicitValence() == 1:
            at.SetFormalCharge(-1)

def main(input_file, molecules_per_file):
    """
    Split an SDF or MOL2 file into smaller files based on a molecule count.

    Parameters:
    input_file (str): Path to the input file (.sdf or .mol2).
    molecules_per_file (int): Number of molecules per output file.
    """
    ext = os.path.splitext(input_file)[1].lower()
    input_dir = os.path.dirname(input_file)
    input_basename = os.path.basename(input_file).rsplit('.', 1)[0]

    if ext == '.sdf':
        supplier = Chem.SDMolSupplier(input_file)
        i = 0  # molecule counter
        j = 0  # file index
        current_mol_limit = molecules_per_file
        out_path = os.path.join(input_dir, f'{input_basename}_{j}.sdf')
        f_out = open(out_path, 'w')

        for mol in tqdm(supplier, desc="Processing SDF", unit="mol"):
            if mol is not None:
                add_formal_charges(mol)
                f_out.write(Chem.MolToMolBlock(mol))
                f_out.write('$$$$\n')
                i += 1

                if i >= current_mol_limit:
                    f_out.close()
                    j += 1
                    current_mol_limit += molecules_per_file
                    out_path = os.path.join(input_dir, f'{input_basename}_{j}.sdf')
                    f_out = open(out_path, 'w')

        f_out.close()
        print(f"Completed. Split {i} molecules into {j + 1} SDF files.")

    elif ext == '.mol2':
            file_count = 0
            molecule_count = 0
            with open(input_file, 'r') as infile:
                lines = []
                total_molecules = sum(1 for line in open(input_file) if line.startswith('@<TRIPOS>MOLECULE'))
                with tqdm(total=total_molecules, desc="Processing MOL2", unit="mol") as pbar:
                    for line in infile:
                        if line.startswith('@<TRIPOS>MOLECULE'):
                            if molecule_count % molecules_per_file == 0:
                                if lines:
                                    with open(os.path.join(input_dir, f'{input_basename}_{file_count}.mol2'), 'w') as f_out:
                                        f_out.writelines(lines)
                                    lines = []
                                    file_count += 1
                            molecule_count += 1
                            pbar.update(1)
                        lines.append(line)

                    if lines:
                        with open(os.path.join(input_dir, f'{input_basename}_{file_count}.mol2'), 'w') as f_out:
                            f_out.writelines(lines)
                        file_count += 1

            print(f"Completed. Split {molecule_count} molecules into {file_count} MOL2 files.")

    else:
        raise ValueError("Unsupported file format. Use .sdf or .mol2")