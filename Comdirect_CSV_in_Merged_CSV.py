import csv
import re

# Input and output file paths
#input_file = r"c:\Users\dkron\Coding\Python\FinAuto\Comdirect_2025_10052025.csv"
input_file = r"c:\Users\dkron\Coding\Python\umsaetze_9784700399_20250523-2341.csv"
output_file = r"c:\Users\dkron\Coding\Python\merged.csv"

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
    writer = csv.DictWriter(outfile, fieldnames=list(columns_to_extract.values()) + additional_columns, delimiter=";")
    
    # Write header to the output file
    writer.writeheader()
    
    # Extract and write the required columns
    for row in reader:
        # Extract original columns
        extracted_row = {new_col: row[old_col] for old_col, new_col in columns_to_extract.items()}
        
        # Parse Buchungstext for additional columns
        buchungstext = row["Buchungstext"]
        
        # Match Auftraggeber or Empfänger
        auftraggeber_match = re.search(r"(Auftraggeber|Empfänger): (.+?)(?= Buchungstext:| Ref\.|$)", buchungstext)
        buchungstext_match = re.search(r"Buchungstext: (.+?)(?= Ref\.|$)", buchungstext)
        ref_id_match = re.search(r"Ref\. ([^\s]+)", buchungstext)
        
        # Add parsed values to the row
        extracted_row["Auftraggeber"] = auftraggeber_match.group(2).strip() if auftraggeber_match else ""
        extracted_row["Buchungstext"] = buchungstext_match.group(1).strip() if buchungstext_match else ""
        extracted_row["Ref ID"] = ref_id_match.group(1).strip() if ref_id_match else ""

        # Remove unnecessary columns
        if "Typ" in extracted_row:
            del extracted_row["Typ"]
        if "Text" in extracted_row:
            del extracted_row["Text"]

        # Write the row to the output file
        writer.writerow(extracted_row)

# Add Hauptkategorie and Unterkategorie to merged.csv
with open(output_file, mode="r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile, delimiter=";")
    
    # Check if fieldnames are valid
    if reader.fieldnames is None:
        raise ValueError("Die Datei 'merged.csv' ist leer oder enthält keine Kopfzeile.")
    
    fieldnames = reader.fieldnames + ["Hauptkategorie", "Unterkategorie"]
    rows = list(reader)  # Read all rows into memory

# Write updated rows back to the file
with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=";")
    
    # Write updated header
    writer.writeheader()
    
    # Define categorization logic
    def categorize(row):
        hauptkategorie = ""
        unterkategorie = ""
        
        # Hauptkategorie: Einnahmen
        if row["Auftraggeber"] == "Bundesagentur für Arbeit - Familienkasse":
            hauptkategorie = "Einnahmen"
            unterkategorie = "Einkommen Kindergeld"
        elif "Miete" in row["Buchungstext"]:
            hauptkategorie = "Einnahmen"
            unterkategorie = "Mieteinnahmen (Warmmiete)"
        elif "ERTRAEGNISGUTSCHRIFT" in row["Buchungstext"]:
            hauptkategorie = "Einnahmen"
            unterkategorie = "Dividendeneinnahmen"
        elif "E E G Deisslinger Str" in row["Buchungstext"]:
            hauptkategorie = "Einnahmen"
            unterkategorie = "EEG Vergütung"
        elif "Werner Ostheim" in row["Auftraggeber"]:
            hauptkategorie = "Einnahmen"
            unterkategorie = "Steuerrückzahlung/Geschenke"    
        elif False:  # Dummy conditions for other Einnahmen
            if False:
                unterkategorie = "Nettoeinkommen Daniel"
            elif False:
                unterkategorie = "Nettoeinkommen Wiebke"
            elif False:
                unterkategorie = "Steuerrückzahlung/Geschenke/ Kerstin Kredit"


        # Hauptkategorie: Haus
        elif row["Auftraggeber"] == "WEG-T.E.Garagen Rainstrasse Trossingen":
            hauptkategorie = "Haus"
            unterkategorie = "Ausgaben Kaiserstraße"   
        elif row["Auftraggeber"] == "WEG-Kaiserstr. 61-86, Trossingen":
            hauptkategorie = "Haus"
            unterkategorie = "Ausgaben Kaiserstraße"       
        elif row["Auftraggeber"] == "Stadtwerke Duisburg Aktiengesellschaft":
            hauptkategorie = "Haus"
            unterkategorie = "Strom"
        elif "Stadtkasse Trossingen" in row["Auftraggeber"]:
            hauptkategorie = "Haus"
            unterkategorie = "Grundsteuer Kaiserstraße"    


        # Hauptkategorie: Mitgliedschaften/Abos/Verträge
        elif row["Auftraggeber"] == "mobilezone GmbH":
            hauptkategorie = "Mitgliedschaften/Abos/Verträge"
            unterkategorie = "Handyverträge Wiebke+Daniel"
        elif "Spotify" in row["Buchungstext"] or "Netflix" in row["Buchungstext"]:
            hauptkategorie = "Mitgliedschaften/Abos/Verträge"
            unterkategorie = "Spotify / Disney+ / Netflix etc"
        elif row["Auftraggeber"] == "Raz, Tibor":
            hauptkategorie = "Mitgliedschaften/Abos/Verträge"
            unterkategorie = "Vereine / Kurse / Bücherei"
        elif row["Auftraggeber"] == "Kath. Kirchenpflege Weigheim":
            hauptkategorie = "Mitgliedschaften/Abos/Verträge"
            unterkategorie = "Kiga Beiträge Jella + Hanno"
         
        elif False:  # Dummy conditions for other Mitgliedschaften
            if False:
                unterkategorie = "Zwift / Strava"
            elif False:
                unterkategorie = "Amazon Prime"
            elif False:
                unterkategorie = "Vereine / Kurse / Bücherei"
            elif False:
                unterkategorie = "Usenet Account /sonstige Abos/ Online Sachen"
            elif False:
                unterkategorie = "ADAC Mitgliedschaft"
            elif False:
                unterkategorie = "Kiga Beiträge Jella + Hanno"

        # Hauptkategorie: Sparen/Altersvorsorge/Sparen Kinder
        elif "ETF" in row["Buchungstext"] or "World" in row["Buchungstext"]:
            hauptkategorie = "Sparen/Altersvorsorge/Sparen Kinder"
            if "Jella" in row["Auftraggeber"]:
                unterkategorie = "ETF Sparen Jella"
            elif "Hanno" in row["Auftraggeber"]:
                unterkategorie = "ETF Sparen Hanno"
            elif "Lenni" in row["Auftraggeber"]:
                unterkategorie = "ETF Sparen Lenni"
        elif False:  # Dummy conditions for other Sparen
            if False:
                unterkategorie = "LBS BSV"
            elif False:
                unterkategorie = "DEVK"
            elif False:
                unterkategorie = "DWS"
            elif False:
                unterkategorie = "Fidelity Wiebke"
            elif False:
                unterkategorie = "Fidelity Daniel"
            elif False:
                unterkategorie = "VW Bank 1"
            elif False:
                unterkategorie = "VW Bank 2"

        # Hauptkategorie: Variable Ausgaben Lebensmittel etc.
        elif row["Auftraggeber"] in ["ALDI SUED", "LIDL", "EDEKA"]:
            hauptkategorie = "Variable Ausgaben Lebensmittel etc."
            unterkategorie = "Lebensmittel inkl Hygiene/Verbrauchsartikel"
        elif "Apotheke" in row["Buchungstext"] or "Arzt" in row["Buchungstext"]:
            hauptkategorie = "Variable Ausgaben Lebensmittel etc."
            unterkategorie = "Gesundheitsausgaben, Apotheke, Arzt, Massage"
        elif "Friseur" in row["Buchungstext"]:
            hauptkategorie = "Variable Ausgaben Lebensmittel etc."
            unterkategorie = "Friseur"
        elif False:  # Dummy conditions for other Variable Ausgaben
            if False:
                unterkategorie = "Anschaffungen/ Reparaturen Auto/Haus"
            elif False:
                unterkategorie = "Ausgehen, Kino, Eintritte, etc."
            elif False:
                unterkategorie = "Kantine/Essen gehen"
            elif False:
                unterkategorie = "Bekleidung, Accessoires"
            elif False:
                unterkategorie = "Urlaub"
            elif False:
                unterkategorie = "Geschenke und Kids Stuff"
            elif False:
                unterkategorie = "Hobby / Technik / Sport / Dampfen"

        # Hauptkategorie: Auto+Versicherungen
        elif row["Auftraggeber"] == "JET TANKSTELLE XJ05982":
            hauptkategorie = "Auto+Versicherungen"
            unterkategorie = "Tanken"
        elif row["Auftraggeber"] == "SC-LEASING GMBH":
            hauptkategorie = "Auto+Versicherungen"
            unterkategorie = "Leasing Fiat 500e"
        elif row["Auftraggeber"] == "Bundeskasse DO Weiden" and "Kfz-Steuer" in row["Buchungstext"]:
            hauptkategorie = "Autoversteuer"
            unterkategorie = "Kfz-Steuer"
        elif row["Auftraggeber"] == "HUK-COBURG UNTERNEHMENSGRUPPE" and "VS-XK 666" in row["Buchungstext"]:
            hauptkategorie = "Auto+Versicherungen"
            unterkategorie = "Autoversicherung"
        elif row["Auftraggeber"] == "HUK-COBURG UNTERNEHMENSGRUPPE" and "VS-XW 666" in row["Buchungstext"]:
            hauptkategorie = "Auto+Versicherungen"
            unterkategorie = "Autoversicherung"    
        return hauptkategorie, unterkategorie
    
    # Process rows and add categories
    for row in rows:
        hauptkategorie, unterkategorie = categorize(row)
        row["Hauptkategorie"] = hauptkategorie
        row["Unterkategorie"] = unterkategorie
        writer.writerow(row)
