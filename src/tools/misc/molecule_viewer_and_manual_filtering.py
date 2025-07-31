import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk
from rdkit import Chem
from rdkit.Chem import AllChem, Draw
import csv
import os
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

# Fonction pour extraire les SMILES et les noms depuis un fichier SDF
def get_smiles_list_from_sdf(sdf_path):
    suppl = Chem.SDMolSupplier(sdf_path)
    smiles_list = []
    for mol in suppl:
        if mol is not None:
            smi = Chem.MolToSmiles(mol)
            name = mol.GetProp("_Name") if mol.HasProp("_Name") else "Unknown"
            smiles_list.append((name, smi))
    return smiles_list


class MolViewerApp:
    def __init__(self, root, smiles_list, output_file_path):
        self.root = root
        self.root.title("Molecule Viewer")

        # Convert SMILES to RDKit mols
        self.mol_list = []
        for name, smi in smiles_list:
            mol = Chem.MolFromSmiles(smi)
            if mol is not None:
                mol.SetProp("_Name", name)
                self.mol_list.append(mol)

        self.total_molecules = len(self.mol_list)
        if self.total_molecules == 0:
            messagebox.showinfo("No Molecules", "No valid molecules found.")
            self.root.destroy()
            return

        self.current_index = 0
        self.decision_count = 0
        self.decisions = []

        # Image display
        self.image_label = ttk.Label(root)
        self.image_label.pack(padx=10, pady=10)

        self.label_counter = ttk.Label(root, text="")
        self.label_counter.pack(padx=10, pady=5)

        self.label_decision_counter = ttk.Label(root, text=f"Decisions: {self.decision_count}")
        self.label_decision_counter.pack(padx=10, pady=5)

        # Buttons
        frame_buttons = ttk.Frame(root)
        frame_buttons.pack(padx=10, pady=10)

        ttk.Button(frame_buttons, text="Yes", command=self.on_yes_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="No", command=self.on_no_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Maybe", command=self.on_maybe_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Previous", command=self.show_previous_molecule).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Next", command=self.show_next_molecule).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Delete", command=self.delete_last_decision).pack(side=tk.LEFT, padx=5)

        # Output file
        self.output_file_path = output_file_path
        try:
            self.output_file = open(self.output_file_path, "w", newline='')
            writer = csv.writer(self.output_file)
            writer.writerow(["Name", "SMILES", "Decision"])  # New header with SMILES
            self.output_file.flush()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the output file: {e}")
            self.root.destroy()
            return

        # Display first molecule
        self.display_molecule()

    def write_response(self, response):
        mol = self.mol_list[self.current_index]
        mol_name = mol.GetProp("_Name")
        mol_smi = Chem.MolToSmiles(mol)
        writer = csv.writer(self.output_file)
        writer.writerow([mol_name, mol_smi, response])
        self.output_file.flush()
        self.decisions.append((mol_name, mol_smi, response))

    def display_molecule(self):
        if self.current_index < self.total_molecules:
            mol = self.mol_list[self.current_index]
            AllChem.Compute2DCoords(mol)
            img = Draw.MolToImage(mol, size=(300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

            self.label_counter.config(text=f"Molecule {self.current_index + 1}/{self.total_molecules}")
        else:
            messagebox.showinfo("End of Molecules", "All molecules have been displayed.")
            self.output_file.close()
            self.root.destroy()

    def show_next_molecule(self):
        if self.current_index < self.total_molecules - 1:
            self.current_index += 1
            self.display_molecule()

    def show_previous_molecule(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_molecule()

    def on_yes_clicked(self):
        self.write_response("yes")
        self.decision_count += 1
        self.label_decision_counter.config(text=f"Decisions: {self.decision_count}")
        self.show_next_molecule()

    def on_no_clicked(self):
        self.write_response("no")
        self.decision_count += 1
        self.label_decision_counter.config(text=f"Decisions: {self.decision_count}")
        self.show_next_molecule()

    def on_maybe_clicked(self):
        self.write_response("maybe")
        self.decision_count += 1
        self.label_decision_counter.config(text=f"Decisions: {self.decision_count}")
        self.show_next_molecule()

    def write_response(self, response):
        mol = self.mol_list[self.current_index]
        mol_name = mol.GetProp("_Name")
        mol_smi = Chem.MolToSmiles(mol)
        writer = csv.writer(self.output_file)
        writer.writerow([mol_name, mol_smi, response])
        self.output_file.flush()
        self.decisions.append((mol_name, mol_smi, response))

    def delete_last_decision(self):
        if self.decisions:
            last_decision = self.decisions.pop()
            lines = []
            with open(self.output_file_path, "r") as file:
                lines = file.readlines()
            with open(self.output_file_path, "w") as file:
                for line in lines:
                    if not line.strip() == f"{last_decision[0]},{last_decision[1]}":
                        file.write(line)
            self.decision_count -= 1
            self.label_decision_counter.config(text=f"Decisions: {self.decision_count}")
        else:
            messagebox.showinfo("No Decisions", "There are no decisions to delete.")


def display_molecules_from_smiles(smiles_list, output_file):
    root = tk.Tk()
    app = MolViewerApp(root, smiles_list, output_file)
    root.mainloop()


def main(input_file, output_folder):
    # Vérification d'existence
    if not os.path.isfile(input_file):
        print(f"Input file not found: {input_file}")
        return
    if not os.path.isdir(output_folder):
        print(f"Output folder does not exist. Creating: {output_folder}")
        os.makedirs(output_folder, exist_ok=True)

    # Génération du nom de fichier de sortie
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_folder, f"{base_name}_filter.csv")

    # Extraction des données
    smiles_list = get_smiles_list_from_sdf(input_file)

    # Lancement de l'application
    root = tk.Tk()
    app = MolViewerApp(root, smiles_list, output_file)
    root.mainloop()


