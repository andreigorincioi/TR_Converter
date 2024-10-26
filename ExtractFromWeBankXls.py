"""This library is used to convert data from xls file to csv"""
import openpyxl as xl
import pathlib

MAPPING_XLS = {
    "DATA":"A",
    "Data Valuta":"B",
    "Importo":"C",
    "Divisa":"D",
    "Causale/Descrizione":"E",
    "Canale":"F"}
COLUMNS = ("DATA", "TIPO", "DESCRIZIONE", "IN ENTRATA/IN USCITA", "SALDO")
MAPPING_CSV = ("A", "E", "", "C", "")
cwd = pathlib.Path.cwd()
FROM_FOLDER = cwd / 'ToConvertTRR'  
TO_FOLDER = cwd / 'Converted'

def main():
    for path in FROM_FOLDER.iterdir():
        if path.name.lower().find("webank") == -1: continue
        process_file(path)

def process_file(path_file:pathlib.Path):
    wb = xl.open(path_file, read_only=True, data_only=True)
    ws = wb.active
    vals = []
    for row in ws.iter_rows():
        for val in MAPPING_CSV:
            if not val: vals.append("")
            else: vals.append(val)

def save_to_csv(path:pathlib.Path, values:list[list[str]]):
    pass


