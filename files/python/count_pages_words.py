import pandas as pd
import glob
import os
from PyPDF2 import PdfReader
import re

# Einlesen der Metadatentabelle, zu der die Angabe der Seitenzahl und Wortzahl eines jeden Briefes hinzugefügt werden soll
df_metadata = pd.read_csv("Metadaten-Briefe.csv")

# Einlesen der Bilddigitalsate im PDF-Format, Zählen der Seitenanzahl mit der len-Funktion 
# Speichern von Dateiname und Seitenzahl in einem Dictionary
file_page_dict = {}
for file in glob.glob(os.path.join("pdf", "*.pdf")):
    with open(file, "r") as infile:
        pdf_file = PdfReader(file)
        filename_pdf = file.split("\\")[1].split(".")[0]
        num_pages = len(pdf_file.pages)
        file_page_dict[filename_pdf] = num_pages

# Einlesen der TXT-Dateien, die den Brieftext erhalten
# Entfernen von Zahlen und Nicht-Wortzeichen
# Aufsplitten des Brieftextes in eine Wortliste
# Zählen der Länge der Liste (= Wortanzahl des Briefes) mit der len-Funktion
# Speichern von Dateiname und Wortanzahl in einem Dictionary 
file_words_dict = {}
for file in glob.glob(os.path.join("txt", "*.txt")):
    with open(file, "r", encoding="utf-8") as infile:
        text = infile.read()
        filename_txt = file.split("\\")[1].split(".")[0]
        text = re.sub ("\d", "", text)
        text = re.sub ("\W", " ", text)
        words = text.split()
        number_words = len(words)
        file_words_dict[filename_txt] = number_words

# Die beiden erstellten Dictionarys werden mit dem eingelesenen Dataframe zu den Metadaten zusammengeführt
# Das Mapping erfolgt über den Dateinamen, der sowohl im Dataframe als auch in den Dictionarys vorliegt
df_metadata['Anzahl Seiten'] = df_metadata['Dateiname'].map(file_page_dict)
df_metadata['Anzahl Wörter'] = df_metadata['Dateiname'].map(file_words_dict)

# Speichern der um die Spalten 'Anzahl Seiten' und 'Anzahl Wörter' ergänzten Metadaten als CSV-Datei
df_metadata.to_csv("Metadaten_Briefe.csv")
