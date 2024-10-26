# pyTRConverter
Questo insieme di script sono stati creati per uniformare i dati degli estratti conto delle varie banche in un unico tipo csv. Con i file unificati si andrà a creare un foglio excel con i dati raggruppati e conforntati in modo da poter tener traccia delle varie spese.

## Modules
**ExtractFromTRRPdf**
This module contains the logic to extract data from TRR Pdf files from folder ToConvert.
IMPORTANT: The converted file will have the same name as the origin file.
1. Looks for pdf files into **ToConvert** folder   
2. Extracts relevant data from the pdf to cs


### Requirements
pip install -r requirements.txt 