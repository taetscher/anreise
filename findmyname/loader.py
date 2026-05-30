import csv
import os

def load_names_from_csv(csv_filename):
    names_list = []
    original_hyphen_names = {}  # speichert das saubere mapping
    
    if os.path.exists(csv_filename):
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # skip empty rows
                    name_raw = row[0].strip()
                    if name_raw:
                        # umlaute umwandeln und bindestriche entfernen für den generator
                        name_clean = name_raw.lower()
                        name_clean = name_clean.replace("ä", "ae")
                        name_clean = name_clean.replace("ö", "oe")
                        name_clean = name_clean.replace("ü", "ue")
                        name_clean = name_clean.replace("-", "")
                        
                        names_list.append(name_clean)
                        original_hyphen_names[name_clean] = name_raw
        return names_list, original_hyphen_names
    else:
        print(f"Error: Could not find '{csv_filename}'. Bitte zuerst erstellen.")
        exit()
