import csv
import re
from categorize import categorize

# Input and output file paths
input_file = r"c:\Users\dkron\Coding\Python\FinAuto\Comdirect_2025_10052025.csv"
#input_file = r"c:\Users\dkron\Coding\Python\FinAuto\umsaetze_9784700399_20250523-2341.csv"

output_file = r"c:\Users\dkron\Coding\Python\FinAuto\merged.csv"

# Column mappings: input column -> output column
columns_to_extract = {
    "Buchungstag": "Datum",
    "Vorgang": "Typ",
    "Buchungstext": "Text",
    "Umsatz in EUR": "Umsatz"
}

# Additional columns to extract from Buchungstext
additional_columns = ["Auftraggeber", "Buchungstext", "Ref ID"]

# Read and process the input CSV
with open(input_file, mode="r", encoding="latin-1") as infile, open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
    reader = csv.DictReader(infile, delimiter=";")
    writer = csv.DictWriter(outfile, fieldnames=list(columns_to_extract.values()) + additional_columns + ["Hauptkategorie", "Unterkategorie"], delimiter=";")
    
    # Write header to the output file
    writer.writeheader()
    
    # Extract and write the required columns
    for row in reader:
        # Extract original columns
        extracted_row = {new_col: row[old_col].strip() for old_col, new_col in columns_to_extract.items()}
        
        # Parse Buchungstext for additional columns
        buchungstext = row["Buchungstext"]
        auftraggeber_match = re.search(r"(Auftraggeber|Empfänger): (.+?)(?= Buchungstext:| Ref\.|$)", buchungstext)
        buchungstext_match = re.search(r"Buchungstext: (.+?)(?= Ref\.|$)", buchungstext)
        ref_id_match = re.search(r"Ref\. ([^\s]+)", buchungstext)
        
        # Add parsed values to the row
        extracted_row["Auftraggeber"] = auftraggeber_match.group(2).strip() if auftraggeber_match else ""
        extracted_row["Buchungstext"] = buchungstext_match.group(1).strip() if buchungstext_match else ""
        extracted_row["Ref ID"] = ref_id_match.group(1).strip() if ref_id_match else ""

        # Categorize the row
        hauptkategorie, unterkategorie = categorize(extracted_row)
        extracted_row["Hauptkategorie"] = hauptkategorie
        extracted_row["Unterkategorie"] = unterkategorie

        # Write the row to the output file
        writer.writerow(extracted_row)
