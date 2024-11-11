"""this module creates an excel from the csv data of Converted folder"""
import openpyxl as xl
import pathlib
from utils import COLUMNS
import csv 

cwd = pathlib.Path.cwd()
TO_FOLDER = cwd / 'Converted'

def process_csvs():
    wb = xl.Workbook()
    date = ""
    for file_path in TO_FOLDER.iterdir():
        if file_path.name.endswith(".csv"):
            if not date: date = file_path.name[:7]
            ws = wb.create_sheet(file_path.name.removesuffix(".csv"))
            with file_path.open("r") as fr:
                for row in csv.reader(fr, delimiter=";"):
                    ws.append(row)
    wb.save(f"{date}_Tracker.xlsx")

if __name__ == '__main__':
    process_csvs()