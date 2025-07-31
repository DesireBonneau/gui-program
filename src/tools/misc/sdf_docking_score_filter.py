# Import necessary libraries
from rdkit import Chem
from rdkit.Chem import SDWriter
from tqdm import tqdm
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

# Function to filter molecules based on a specific score property and threshold
def main(input_file, score_property, threshold):
    """
    Filter molecules from an SDF file based on a specific score property and threshold.

    Parameters:
    input_file (str): Path to the input SDF file.
    output_file (str): Path to the output SDF file where filtered molecules will be saved.
    score_property (str): The property name that holds the score to filter on.
    ex : 'FR_FITTED_HybridScore' / 'FR_FITTED_MScore' / 'FR_FITTED_Energy' / 'FR_FITTED_Score'
    threshold (float): The threshold value for filtering the molecules.
    """
    # Open the input SDF file
    supplier = Chem.SDMolSupplier(input_file)

    # Create a writer for the output SDF file
    # The output file name is the input file name with "_filtered" appended
    input_file = input_file[:input_file.rfind('.')]  # Remove the file extension
    output_file = input_file + "_filtered.sdf"
    writer = SDWriter(output_file)

    # Filter and write the molecules that meet the criteria
    for mol in tqdm(supplier, desc="Processing molecules", unit="molecule"):
        if mol is not None:  # Check if the molecule was read correctly
            try:
                add_formal_charges(mol)
                # Retrieve the value of the score property
                score = mol.GetProp(score_property)
                if float(score) <= threshold:
                    writer.write(mol)
            except:
                # Ignore molecules where the property is missing or the value is invalid
                continue

    # Close the writer
    writer.close()
    # Print a message indicating completion
    print(f'Molecules that meet the criteria have been written to {output_file}')

