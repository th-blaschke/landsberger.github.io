import glob
import itertools
import numpy as np
import pandas as pd
import re
from os.path import join

def read_text(textfile):
    """Einlesen einer TXT-Datei"""
    with open (textfile, "r", encoding="utf-8") as infile:
        text = infile.read()
    
    return text

def get_textlength(text):
    """Aufsplitten des Textes in eine Wortliste; 
    Ermitteln der Länge der Liste (= Wortanzahl des Textes) mit der len-Funktion"""
    text_list = re.split("\W+", text)
    number_words = len(text_list)

    return number_words

def get_wordfrequency(text):
    """Aufsplitten des Textes in eine Wortliste; 
    Ermitteln der Häufigkeit jedes Wortes im Text; 
    Speichern von Dateiname und Worthäufigkeit in einem Dictionary"""
    text_list = re.split("\W+", text)
    word_dict = {}
    for item in text_list:
       if item in word_dict:
           word_dict[item] +=1
       else:
            word_dict[item] = 1
    
    return word_dict

def get_dict_5_most(word_dict, number_words):
    """Ermitteln von relativen Häufigkeiten für die einzelnen Wörter des Textes;
    Ermitteln der fünf häufigsten Wörter"""
    word_dict.update((k, round(v/number_words * 100, 2)) for k, v in word_dict.items())
    word_dict = {k: v for k, v in sorted(word_dict.items(), key=lambda x: x[1], reverse=True)}
    five_words_dict = dict(itertools.islice(word_dict.items(), 5))

    return five_words_dict

def get_dict_keys(five_words_dict):
    """Überführen der Keys des Dictionary (= die fünf häufigsten Wörter) in eine Liste"""
    keyword_list = list(five_words_dict.keys())
    
    return keyword_list

def create_term_doc(five_words_dict, name_textfile):
    """Erstellen einer pandas.Series aus dem Dictionary"""
    term_doc_series = pd.Series(five_words_dict, name = name_textfile, index=None)
    
    return term_doc_series

def save_tdm(tdm):
    """Speichern der Term-Dokument-Matrix als CSV-Datei"""
    with open("term_document_matrix.csv", "w", encoding="utf-8") as outfile:
        tdm.to_csv(outfile, sep=",", lineterminator="\n")

def compare_word_frequency (tdm, keyword_list):
    """Abgleich der fünf häufigsten Wörter eines jeden Textes mit der Term-Dokument-Matrix;
    Ausgabe aller weiteren Texte des Textkorpus, die einen oder alle dieser fünf häufigsten Wörter ebenfalls unter den fünf häufigsten Wörtern enthalten;
    Speichern der Ergebnisse als CSV-Dateien (eine CSV-Datei pro je 5 Stichwörter/Text)
    """
    text_names = tdm.columns.values.tolist()
    text_names.remove("Summe")
    for i,y in zip(keyword_list, text_names):
        keyword_df = tdm.loc[i].T
        df_compare_5_most = keyword_df.loc[~(keyword_df==0).all(axis=1)]
        with open(f"{y}_häufigkeiten.csv", "w", encoding="utf-8") as outfile:
            df_compare_5_most.to_csv(outfile, sep=",", lineterminator="\n")

def main(textfiles):
    dict_list = []
    keywords = []
    for textfile in textfiles:
        text = read_text(textfile)
        textname = textfile.split("\\")[1].split(".")[0]
        len_text = get_textlength(text)
        dict_word_frequ = get_wordfrequency(text)
        five_words_dict = get_dict_5_most(dict_word_frequ, len_text)
        words_df = create_term_doc(five_words_dict, textname)
        dict_list.append(words_df)
        keys_dict_list = get_dict_keys(five_words_dict)
        keywords.append(keys_dict_list)

    results = pd.DataFrame(dict_list).T.fillna(0)
    results["Summe"] = np.around(results.sum(axis="columns"), 2)
    save_tdm(results)
    compare_word_frequency(results, keywords)

textfiles = glob.glob(join("landsberger_letters", "*.txt")) # Angabe des Datei-Ordners, der die Texte enthält

main(textfiles)