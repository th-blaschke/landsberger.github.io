import glob
from os.path import join
import pandas as pd
import re
import itertools
import numpy as np

def read_text(textfile):
    """Einlesen einer TXT-Datei"""
    with open (textfile, "r", encoding="utf-8") as infile:
        text = infile.read()
    
    return text

def count_textlength(text):
    """Aufsplitten des Textes in eine Wortliste; 
    Ermitteln der Länge der Liste (= Wortanzahl des Textes) mit der len-Funktion"""
    text_list = re.split("\W+", text)
    number_words = len(text_list)

    return number_words

def count_wordfrequency(text):
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
    five_word_dict = dict(itertools.islice(word_dict.items(), 5))

    return five_word_dict

def get_dict_keys(five_word_dict):
    """Liste von Schlüsselwörtern"""
    key_list = list(five_word_dict.keys())
    
    return key_list

def create_term_doc(word_dict, name_textfile):
    """Aus dem dict wird eine pd.Series erstellt"""
    term_doc_series = pd.Series(word_dict, name = name_textfile, index=None)
    
    return term_doc_series

def save_tdm(tdm):
    """Speichern der Term-Dokument-Matrix als CSV-Datei"""
    with open("tdm_rel_test.csv", "w", encoding="utf-8") as outfile:
        tdm.to_csv(outfile, sep=",", lineterminator='\n')

def get_tdm_per_keywords (tdm, search_list, folder_name):
    """Lalalala"""
    names = tdm.columns.values.tolist()
    names.remove("Summe")
    for i,y in zip(search_list, names):
        new_df = tdm.loc[i].T
        final_df = new_df.loc[~(new_df==0).all(axis=1)]
        with open(f"{folder_name}/{y}_häufigkeiten.csv", "w", encoding="utf-8") as outfile2:
            final_df.to_csv(outfile2, sep=",", lineterminator="\n")

def main(textfiles):
    dict_list = []
    searchword_list = []
    folder_save = "Häufigkeiten_per_Brief"
    for textfile in textfiles:
        text = read_text(textfile)
        textname = textfile.split('\\')[1].split('.')[0]
        len_text = count_textlength(text)
        dict_word_numbers = count_wordfrequency(text)
        five_words_dict = get_dict_5_most(dict_word_numbers, len_text)
        words_df = create_term_doc(five_words_dict, textname)
        dict_list.append(words_df)
        keys_d = get_dict_keys(five_words_dict)
        searchword_list.append(keys_d)

    results = pd.DataFrame(dict_list).T.fillna(0)
    results["Summe"] = np.around(results.sum(axis='columns'), 2)
    print(results.head())
    save_tdm(results)
    get_tdm_per_keywords(results, searchword_list, folder_save)

textfiles = glob.glob(join("Kerntext_stop_removed", "*.txt"))
main(textfiles)