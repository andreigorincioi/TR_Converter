import pathlib
from datetime import datetime as dt
from PyPDF2 import PdfReader
 

cwd = pathlib.Path.cwd()
FROM_FOLDER = cwd / 'ToConvertTRR'  
TO_FOLDER = cwd / 'Converted'

if not FROM_FOLDER.is_dir() or not TO_FOLDER.is_dir():
    raise Exception("Folder \"ToConverted\" and \"Converted\" not found.")

DIVIDER = "§§"
COLUMNS = ("DATA", "TIPO", "DESCRIZIONE", "IN ENTRATA", "IN USCITA", "SALDO")
TIPO_TRANSAZIONI = ("Transazione con carta", "Trasferimento", "Pagamento degli interessi")
  
def main() -> list[list[str]]:
    for path in FROM_FOLDER.iterdir():
        reader = PdfReader(path)
        first_page_text = reader.pages[0].extract_text()
        year = get_year(first_page_text)
        vals = [list(COLUMNS)]
        for page in reader.pages:
            text = page.extract_text()
            data = extract_data(text, year)
<<<<<<< HEAD:ExtractFromTRRPdf.py
            vals.extend(data)                
        sanitize_data(vals)

def save_to_csv(vals:list[list[str]]):
    pass
=======
            vals.extend(data)
        create_workbook_from_tr_converter_data(vals, year)        
>>>>>>> b41610d3c605c5a18286dd80e7dc27f3988d648a:main.py

def sanitize_data(data:list[list])->list[list]:
    for i in range(len(data)-1):
        if to_float(data[i][-1]) - to_float(data[i+1][-2]) == to_float(data[i+1][-1]):
            data[i+1][-2] = "-" + data[i+1][-2]
    
def to_float(val:str)-> float:
    val = val[:-1]
    val = val.replace(".","")
    val = val.replace(",",".")
    return float(val)
            
def get_year(first_page_text:str) -> str:
    line = first_page_text.split("\n")[1]
    text_finder = "Trade Republic Bank GmbHDATA"
    start = line.find(text_finder) + len(text_finder) + 8
    end = start + 4
    return line[start:end]

def extract_data(text:str, year:str) -> list[list[str]]:
    data = []
    text = text.replace("\xa0","")
    ltext = text.split("\n")
    for i in range(len(ltext)):
        if ltext[i].find(year) == 0:
            complete_text = ltext[i-1] + ltext[i] + ltext[i+1] 
            data.append(extract_from_text(complete_text))
    return data

def extract_from_text(text:str):
    def extract_euro_val():
        for i in reversed(range(len(text))):  
            if text[i] == "€":
                break
        for k in reversed(range(i)):
            if not text[k].isnumeric() and text[k] != "." and text[k] != ",":
                break
        return text[k:i+1]
    
    DATA = text[:11]
    
    if text.find("Commercio") != -1:
        TIPO = "Commercio"
        text = text.replace(DATA, "")
        text = text.replace(TIPO, "")
        DESCRIPTION = text[:text.find("quantity:") + 9 + 9]
        text = text.replace(DESCRIPTION, "")
        SALDO = extract_euro_val().strip()
        text = text.replace(SALDO, "")
        IN_OUT = extract_euro_val().strip()
        text = text.replace(IN_OUT, "")
    else:
        TIPO = [i for i in TIPO_TRANSAZIONI if text.find(i) != -1][0]
        text = text.replace(DATA, "")
        text = text.replace(TIPO, "")
        SALDO = extract_euro_val().strip()
        text = text.replace(SALDO, "")
        IN_OUT = extract_euro_val().strip()
        text = text.replace(IN_OUT, "")
        DESCRIPTION = text.strip()
    return [DATA, TIPO, DESCRIPTION, IN_OUT, SALDO]    
<<<<<<< HEAD:ExtractFromTRRPdf.py
=======

if __name__ == '__main__':
    cwd = pathlib.Path.cwd()
    PATH_FROM = cwd / 'ToConvert'
    PATH_TO = cwd / 'Converted'
    YEAR = str(datetime.now().year)

    if PATH_FROM.is_dir() and PATH_TO.is_dir():
        main()
    else:
        print("Folder \"ToConverted\" and \"Converted\" not found.")
>>>>>>> b41610d3c605c5a18286dd80e7dc27f3988d648a:main.py
