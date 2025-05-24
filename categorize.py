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

    # Hauptkategorie: Sparen/Altersvorsorge/Sparen Kinder
    elif "ETF" in row["Buchungstext"] or "World" in row["Buchungstext"]:
        hauptkategorie = "Sparen/Altersvorsorge/Sparen Kinder"
        if "Jella" in row["Auftraggeber"]:
            unterkategorie = "ETF Sparen Jella"
        elif "Hanno" in row["Auftraggeber"]:
            unterkategorie = "ETF Sparen Hanno"
        elif "Lenni" in row["Auftraggeber"]:
            unterkategorie = "ETF Sparen Lenni"

    # Hauptkategorie: Variable Ausgaben Lebensmittel etc.
    elif any(store in row["Auftraggeber"].upper() for store in ["ALDI", "EDEKA", "LIDL","REWE", "PENNY", "NETTO","KIK", "DM", "ROSSMANN", "REAL", "DM-DROGERIE", "MUELLER"]):
        hauptkategorie = "Variable Ausgaben Lebensmittel etc."
        unterkategorie = "Lebensmittel inkl Hygiene/Verbrauchsartikel"
    elif "Apotheke" in row["Buchungstext"] or "Arzt" in row["Buchungstext"]:
        hauptkategorie = "Variable Ausgaben Lebensmittel etc."
        unterkategorie = "Gesundheitsausgaben, Apotheke, Arzt, Massage"
    elif "Friseur" in row["Buchungstext"]:
        hauptkategorie = "Variable Ausgaben Lebensmittel etc."
        unterkategorie = "Friseur"


    # Hauptkategorie: Auto+Versicherungen
    elif any(fuel_station in row["Auftraggeber"].upper() for fuel_station in ["RYD", "JET TANKSTELLE", "ARAL", "ESSO", "SHELL"]):
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

    return hauptkategorie, unterkategorie
