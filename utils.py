"""utils functions"""
from pathlib import Path
import pathlib
import win32com.client as win32


VALUTE_MAPPING = {
    "USD":"$",
    "EUR":"€"
}

def get_valuta_symbol(acronym:str) -> str:
    return VALUTE_MAPPING.get(acronym, None)

def convert_to_csv_text(vals:list[list[str]]) -> str:
    text_vals = "\n".join([";".join(v) for v in vals])
    return text_vals
    
def convert_xls_to_xlsx(path: Path) -> Path:
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(path.absolute())
    # FileFormat=51 is for .xlsx extension
    new_path_file = str(path.absolute().with_suffix(".xlsx")) 
    wb.SaveAs(new_path_file, FileFormat=51)
    wb.Close()
    excel.Application.Quit()
    new_path = pathlib.Path(new_path_file)
    path.unlink()
    return new_path

def convert_b_format_month(data:str) -> str:
    """converts the string data like '01 ago 2024' to '01/08/2024'"""
    ita_b = ("gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic")
    if len(data) != 11: raise Exception(f"Can't process provided string {data}")
    month = data[3:6]
    n_month = str(ita_b.index(month) + 1)
    data = f"{data[0:2]}/{ '0' + n_month if len(n_month) == 1 else n_month}/{data[7:]}"
    return data