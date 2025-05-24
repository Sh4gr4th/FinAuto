import csv
import re
import os
from datetime import datetime

# Input and output file paths
input_file = r"c:\Users\dkron\Coding\Python\FinAuto\Amex_2025_csv_including_details.csv"
output_file = r"c:\Users\dkron\Coding\Python\merged.csv"

# Column mappings: input column -> output column
columns_to_extract = {
    "Datum": "Datum",
    "Beschreibung": "Auftraggeber",
    "Betrag": "Umsatz",
    "Erscheint auf Ihrer Abrechnung als": "Buchungstext"
}

# Check if the merged.csv file already exists
file_exists = os.path.exists(output_file)

# Open the output file in append mode if it exists, otherwise in write mode
with open(output_file, mode="a" if file_exists else "w", encoding="utf-8", newline="") as outfile:
    reader = csv.DictReader(open(input_file, mode="r", encoding="utf-8"))
    
    # Read existing fieldnames from merged.csv if it exists
    if file_exists:
        with open(output_file, mode="r", encoding="utf-8") as existing_file:
            existing_reader = csv.DictReader(existing_file, delimiter=";")
            fieldnames = existing_reader.fieldnames
    else:
        # Define fieldnames for a new file
        fieldnames = list(columns_to_extract.values())
    
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=";")
    
    # Write header only if the file is being created
    if not file_exists:
        writer.writeheader()
    
    # Extract and write the required columns
    for row in reader:
        # Extract original columns
        extracted_row = {new_col: row[old_col] for old_col, new_col in columns_to_extract.items()}
        
        # Convert date format from dd/mm/yyyy to dd.mm.yyyy
        try:
            extracted_row["Datum"] = datetime.strptime(extracted_row["Datum"], "%d/%m/%Y").strftime("%d.%m.%Y")
        except ValueError:
            pass  # Keep the original value if conversion fails
        
        # Write the row to the output file
        writer.writerow(extracted_row)

# Add categorization logic (if needed, similar to Comdirect_CSV_in_Merged_CSV.py)
# ...existing code for categorization logic...
