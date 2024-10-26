"""utils functions"""

from tkinter import N


VALUTE_MAPPING = {
    "USD":"$",
    "EUR":"€"
}

def get_valuta_symbol(acronym:str) -> str:
    return VALUTE_MAPPING.get(acronym, None)