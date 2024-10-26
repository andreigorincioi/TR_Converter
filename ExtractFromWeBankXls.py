"""This library is used to convert data from xls file to csv"""
import pathlib
import xlrd
from utils import convert_to_csv_text

MAPPING_XLS = {
    "DATA":0,
    "Data Valuta":1,
    "IN ENTRATA/IN USCITA":2,
    "VALUTA":3,
    "DESCRIZIONE":4,
    "TIPO":5}
COLUMNS = ("DATA", "TIPO", "DESCRIZIONE", "IN ENTRATA/IN USCITA", "SALDO")
cwd = pathlib.Path.cwd()
FROM_FOLDER = cwd / 'ToConvert'  
TO_FOLDER = cwd / 'Converted'

def main():
    for path in FROM_FOLDER.iterdir():
        if path.name.lower().find("webank") == -1: continue
        vals = process_file(path)
        save_to_csv(path, vals)

def process_file(path_file:pathlib.Path):
    wb = xlrd.open_workbook_xls(path_file)
    sheet = wb.sheet_by_index(0)
    for row_index in range(sheet.nrows):
        for col_index in range(sheet.ncols):
            
    for row_number in sheet:
        line_vals = []
        for col in COLUMNS:
            match col:
                case "DATA"|"DESCRIZIONE"|"TIPO":
                    value = ws[f"{MAPPING_XLS.get(col)}{row_number}"].value
                    line_vals.append(value)
                case "IN ENTRATA/IN USCITA":
                    value = ws[f"{MAPPING_XLS.get(col)}{row_number}"].value
                    value = ws[f"{MAPPING_XLS.get("VALUTA")}{row_number}"].value
                    line_vals.append(value)
        vals.append(line_vals)
    return vals

def save_to_csv(path:pathlib.Path, values:list[list[str]]):
    text_vals = convert_to_csv_text(values)
    file_name = path.name.removesuffix(".xls") + ".csv"
    file_path = TO_FOLDER / file_name
    with file_path.open("wt", encoding="utf-8") as fw:
        fw.write(text_vals)

if __name__ == "__main__":
    main()
