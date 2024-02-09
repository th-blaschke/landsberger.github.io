import glob
import re
from os.path import join

"""Einlesen der Stoppwörter als Liste"""
with open("stopwords.txt", "r", encoding="utf-8") as infile1:
    lines = [line.rstrip() for line in infile1]

"""Einlesen des Kerntextes der Briefe und Umwandeln in eine Wortliste; Entfernen von Nicht-Wortzeichen; 
Abgleich der Stoppwörter-Liste und der Text-Liste und Entfernen aller Stoppwörter aus der Text-Liste;
Zusammenführen der von Stoppwörtern bereinigten Wortliste zurück in einen Fließtext;
Speichern der neu entstandenen Texte als TXT-Datei
"""
for file in glob.glob(join("Kerntext_txt", "*.txt")):
    with open(file, "r", encoding="utf-8") as infile2:
        text = infile2.read()
        text = re.sub("-\n", "", text) # führt Wörter zusammen, die am Ende einer Zeile durch Bindestrich getrennt sind
        text = re.sub("\n", " ", text) # entfernt Zeilenumbrüche
        text = re.sub ("\d", "", text) # entfernt alle Zahlen
        text = re.sub("\W", " ", text) # entfernt alle Nicht-Wortzeichen
        text = re.sub("  ", " ", text) # entfernt alle doppelten Leerzeichen
        text = ' '.join([word for word in text.split() if word.lower() not in lines])
        file = file.split('\\')[2].split('.')[0]

        with open(f"Kerntext_stop_removed/{file}.txt", "w", encoding="utf-8") as outfile:
            output_text=outfile.write(text)