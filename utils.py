"""utils functions"""

from tkinter import N


VALUTE_MAPPING = {
    "USD":"$",
    "EUR":"€"
}

def get_valuta_symbol(acronym:str) -> str:
    return VALUTE_MAPPING.get(acronym, None)

def convert_to_csv_text(vals:list[list[str]]) -> str:
    text_vals = "\n".join([";".join(v) for v in vals])
    return text_vals