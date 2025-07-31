import os
import pandas as pd
from tqdm import tqdm
import csv


def main(file_path, name_length=50):
    # Déterminer l'extension et le dossier d'entrée
    ext = os.path.splitext(file_path)[1].lower()
    input_dir = os.path.dirname(file_path)

    # Construire le chemin du fichier de sortie dans le même dossier
    output_file_path = os.path.join(input_dir, os.path.splitext(os.path.basename(file_path))[0] + "_namefix" + ext)

    if ext == ".sdf":
        marker = "$$$$"
        with open(file_path, "r") as input_file, open(output_file_path, "w") as output_file:
            for line in tqdm(input_file, desc="Processing SDF", unit="line"):
                if line.startswith(marker):
                    output_file.write(line)
                    continue
                if len(line.strip()) > name_length:
                    output_file.write(line[:name_length].strip() + "\n")
                else:
                    output_file.write(line)
        print("Processing complete. Total lines processed:", sum(1 for _ in open(file_path)))

    elif ext == ".mol2":
        marker = "@<TRIPOS>MOLECULE"
        with open(file_path, "r") as input_file, open(output_file_path, "w") as output_file:
            molecule_started = False
            name_processed = False
            for line in tqdm(input_file, desc="Processing MOL2", unit="line"):
                if line.strip() == marker:
                    molecule_started = True
                    name_processed = False
                    output_file.write(line)
                    continue

                if molecule_started and not name_processed:
                    name_processed = True
                    if len(line.strip()) > name_length:
                        output_file.write(line[:name_length].strip() + "\n")
                    else:
                        output_file.write(line)
                    continue

                output_file.write(line)
        print("Processing complete. Total lines processed:", sum(1 for _ in open(file_path)))

    elif ext in [".csv", ".smi", ".txt"]:
        with open(file_path, newline="") as csvfile, open(output_file_path, "w", newline="") as output_file:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            for i, row in tqdm(enumerate(reader, 1), desc="Processing CSV/SMI", unit="row"):
                if "ID" in row:
                    if len(row["ID"].strip()) > name_length:
                        row["ID"] = row["ID"][:name_length].strip()
                writer.writerow(row)
        print("Processing complete. Total rows processed:", i)

    else:
        print("Unsupported file format.")
