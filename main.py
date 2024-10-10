import pathlib
from PyPDF2 import PdfReader
from datetime import datetime
from table_creator import create_workbook_from_tr_converter_data

DIVIDER = "§§"
COLUMNS = ["DATA", "TIPO", "DESCRIZIONE", "IN ENTRATA", "IN USCITA", "SALDO"]

def main():
    for path in PATH_FROM.iterdir():
        reader = PdfReader(path)
        year = get_year(reader.pages[0].extract_text())
        vals = []
        for page in reader.pages:
            text = page.extract_text()
            vals.extend(extract_data(text, year))
        create_workbook_from_tr_converter_data(vals, year)        

    

def get_year(first_page_text:str) -> str:
    line = first_page_text.split("\n")[1]
    text_finder = "Trade Republic Bank GmbHDATA"
    start = line.find(text_finder) + len(text_finder) + 8
    end = start + 4
    return line[start:end]

def extract_data(text:str, year:str) -> list[list[str]]:
    def normalize_date(text:str) -> str:
        return text[:4] + DIVIDER + text[4:] 
    
    def normalize_balance(text:str) -> str:
        for i in range(len(text)):
            if text[i].isupper():
                break
        
        count_comma = 0
        for j in reversed(range(len(text))):
            if text[j] == ",":
                count_comma += 1
                if count_comma == 2:
                    break

        while text[j] != " ":
            j-=1

        for k in reversed(range(len(text))):
            if text[k] == " ":
                break
        
        return text[:i] + DIVIDER + text[i:j] + DIVIDER + text[j:k] + DIVIDER + text[k:]
    
    def filter_all(text:str) -> str:
        # tipo end position
        for pos_tipo_end in range(4, len(text)):
            if text[pos_tipo_end] == " ":
                break
        # saldo end position
        for pos_saldo_end in reversed(range(len(text))):
            if text[pos_saldo_end] == "€":
                break
        # saldo start position
        for pos_saldo_start in reversed(range(pos_saldo_end-1)):
            if not text[pos_saldo_start].isnumeric():
                break
        # in_out start position
        for pos_in_out_end in reversed(range(pos_saldo_start)):
            if text[pos_in_out_end] == "€":
                break
        # in_out end position
        for pos_in_out_start in reversed(range(pos_in_out_end-1)):
            if not text[pos_in_out_start].isnumeric():
                break
        
        return text[:4] + DIVIDER +\
                text[4:pos_tipo_end] + DIVIDER +\
                text[pos_tipo_end:pos_in_out_start] + DIVIDER +\
                text[pos_in_out_start:pos_in_out_end] + DIVIDER +\
                text[pos_saldo_start:pos_saldo_end]

    def filter_commercio(text:str) -> str:
        for i in range(6, len(text)):
            if text[i].isupper():
                break
        
        return text[:4] + DIVIDER +\
                text[4:i] + DIVIDER +\
                text[i:]

    def filter_commercio_numbers(text:str) -> str:
        # saldo end position
        for pos_saldo_end in reversed(range(len(text))):
            if text[pos_saldo_end] == "€":
                break
        # saldo start position
        for pos_saldo_start in reversed(range(pos_saldo_end-1)):
            if not text[pos_saldo_start].isnumeric():
                break
        # in_out start position
        for pos_in_out_end in reversed(range(pos_saldo_start)):
            if text[pos_in_out_end] == "€":
                break
        # Description end position
        pos_end_description = text.find("quantity:") + 9 + 1 + 8

        return text[:pos_end_description] + DIVIDER +\
                text[pos_end_description:pos_in_out_end] + DIVIDER +\
                text[pos_saldo_start:pos_saldo_end]

    data = []
    ltext = text.split("\n")
    for i in range(len(ltext)):
        if ltext[i].find(year) == 0:
            if len(ltext[i+1]) == 7 and ltext[i+1][-1] == ' ':
                    t_row = ltext[i-1].strip() + " " + filter_all(ltext[i])
            else:
                if ltext[i].find("Commercio") != -1:
                    t_row = ltext[i-1].strip() + " " + filter_commercio(ltext[i]).strip() + filter_commercio_numbers(ltext[i+1]) 
                else:
                    t_row = ltext[i-1].strip() + " " + normalize_date(ltext[i].strip()) + " " + normalize_balance(ltext[i+1].strip()) 
            data.append([sanitize_data(val) for val in t_row.split(DIVIDER)])
    return data

def sanitize_data(val:str)->str:
    val = val.strip()
    return val.replace("\xa0","")

if __name__ == '__main__':
    cwd = pathlib.Path.cwd()
    PATH_FROM = cwd / 'ToConvert' 
    PATH_TO = cwd / 'Converted'
    YEAR = str(datetime.now().year)

    if PATH_FROM.is_dir() and PATH_TO.is_dir():
        main()
    else:
        print("Folder \"ToConverted\" and \"Converted\" not found.")
