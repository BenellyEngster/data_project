import re
import sqlite3
import pandas as pd

# 1. Connect to the database created by Selenium
connection = sqlite3.connect("tjpr_data.db")

# 2. Read the raw text from the table
df = pd.read_sql_query("SELECT full_text FROM raw_lawsuits", connection)

# EXTRACTION FUNCTIONS (The Regex "Scissors")
def extract_number(text):
    match = re.search(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", str(text))
    return match.group(0) if match else "Not found"


def extract_decision_type(text):
    # Captures the text inside parentheses, e.g.: (Judgment) or (Single-Judge Decision)
    match = re.search(
        r"\((Acórdão|Decisão Monocrática[^\)]*)\)",
        str(text),
        re.IGNORECASE,
    )
    return match.group(1).strip() if match else "Not informed"


def extract_judicial_secrecy(text):
    # Captures 'Sim' (Yes) or 'Não' (No) after "Under Seal:"
    match = re.search(
        r"Segredo de Justiça:\s*(Sim|Não)", str(text), re.IGNORECASE
    )
    return match.group(1).strip() if match else "Not informed"


def extract_rapporteur(text):
    # Captures after "Rapporteur" until it finds the word "Appellate Judge" or "Adjudicating Body"
    match = re.search(
        r"Relator(?:a)?:\s*(.*?)(?=Desembargad|Órgão Julgador:|\n|$)",
        str(text),
        re.IGNORECASE,
    )
    return match.group(1).strip() if match else "Not informed"


def extract_judging_body(text):
    # Captures after "Adjudicating Body" until the word "Judicial District:""
    match = re.search(
        r"Órgão Julgador:\s*(.*?)(?=Comarca:|\n|$)", str(text), re.IGNORECASE
    )
    return match.group(1).strip() if match else "Not informed"


def extract_district(text):
    # Captures after "judicial district:" until "Date of Judgment:"
    match = re.search(
        r"Comarca:\s*(.*?)(?=Data do Julgamento:|\n|$)",
        str(text),
        re.IGNORECASE,
    )
    return match.group(1).strip() if match else "Not informed"


def extract_judgment_date(text):
    # Captures the date (DD/MM/YYYY) after "Date of Judgment:"
    match = re.search(
        r"Data do Julgamento:\s*(\d{2}/\d{2}/\d{4})",
        str(text),
        re.IGNORECASE,
    )
    return match.group(1) if match else "No date"


def extract_publication_source(text):
    # Captures the date (DD/MM/YYYY) after "Source/Publication Date:"
    match = re.search(
        r"Fonte/Data da Publicação:\s*(\d{2}/\d{2}/\d{4})",
        str(text),
        re.IGNORECASE,
    )
    return match.group(1) if match else "No date"


# 3. APPLYING THE FUNCTIONS TO CREATE PANDAS COLUMNS
df["lawsuit_number"] = df["full_text"].apply(extract_number)
df["decision_type"] = df["full_text"].apply(extract_decision_type)
df["judicial_secrecy"] = df["full_text"].apply(extract_judicial_secrecy)
df["rapporteur"] = df["full_text"].apply(extract_rapporteur)
df["judging_body"] = df["full_text"].apply(extract_judging_body)
df["district"] = df["full_text"].apply(extract_district)
df["judgment_date"] = df["full_text"].apply(extract_judgment_date)
df["publication_source_date"] = df["full_text"].apply(extract_publication_source)

# Organizes the exact order of the columns in the final table
ordered_columns = [
    "lawsuit_number",
    "decision_type",
    "judicial_secrecy",
    "rapporteur",
    "judging_body",
    "district",
    "judgment_date",
    "publication_source_date",
    "full_text",
]
clean_df = df[ordered_columns]

# 4. Displays the first few rows in the terminal for visualization
print(clean_df.head())

# 5. Saves to the CSV file
clean_df.to_csv("clean_tjpr_data.csv", index=False, encoding="utf-8-sig")
print(
    "-> Success! 'clean_tjpr_data.csv' file created with ALL columns separated!"
)

# 6. Closes the database connection
connection.close()