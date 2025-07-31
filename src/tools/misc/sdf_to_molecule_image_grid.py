from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from tqdm import tqdm  # For progress bar
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

def add_formal_charges(mol):
    """This  function adds a formal charge to nitrogens with 4 bonds and to oxygens with single bond
    if not provided in the sdf file"""
    mol.UpdatePropertyCache(strict=False)

    for at in mol.GetAtoms():
        if at.GetAtomicNum() == 7:
            if at.GetExplicitValence() == 4:
                mol.GetAtomWithIdx(at.GetIdx()).SetFormalCharge(1)
        if at.GetAtomicNum() == 5:
            if at.GetExplicitValence() == 4:
                mol.GetAtomWithIdx(at.GetIdx()).SetFormalCharge(-1)
        if at.GetAtomicNum() == 8:
           if at.GetExplicitValence() == 1:
               mol.GetAtomWithIdx(at.GetIdx()).SetFormalCharge(-1)

def main(sdf_file):
    """
    Convert an SDF file to an image of the molecules, ensuring they are "flattened" to 2D.

    Parameters:
    sdf_file (str): Path to the input SDF file.
    output_image_file (str): Path to save the output image file.
    """
    # Read the molecules from the SDF file
    suppl = Chem.SDMolSupplier(sdf_file)
    molecules = []
    for mol in suppl:
        if mol is not None:
            add_formal_charges(mol)
            molecules.append(mol)

    if not molecules:
        print("No valid molecules found in the SDF file.")
        return

    # Compute 2D coordinates for each molecule and flatten them
    for i, mol in tqdm(enumerate(molecules), total=len(molecules), desc="Processing molecules"):
        if mol is not None:
            # Remove any 3D coordinates by removing the conformer
            mol.RemoveAllConformers()

            # Compute 2D coordinates for the molecule
            success = AllChem.Compute2DCoords(mol)
            if not success:
                print(f"Failed to generate 2D coordinates for molecule {i}")
            else:
                print(f"2D coordinates successfully computed for molecule {i}")
        else:
            print(f"Molecule {i} is None and was skipped.")

    # Draw the molecules in a grid
    img = Draw.MolsToGridImage(molecules, molsPerRow=4, subImgSize=(500, 500))

    # Save the image
    output_image_file = sdf_file.replace('.sdf', '_molecules.png')
    img.save(output_image_file)
    print(f"Image saved as {output_image_file}")

