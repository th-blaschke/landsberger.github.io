import pandas as pd
from os.path import join

"""Einlesen der Metadatentabelle in einen Dataframe"""
df_metadata = pd.read_csv("Metadaten_Briefe.csv")

"""Einlesen der einzelnen Zeilen des Dataframe
Vergabe von Variablennamen für die einzelnen Spaltenwerte pro Zeile, um diese leichter in das TEI-Template einfügen zu können"""
for index, row in df_metadata.iterrows():
    filename = row["Dateiname"]
    signature = row["LandsbergerArchives Signatur"]
    date_iso = row["Datum (ISO 8601)"]
    date_de = row["Datum (de)"]
    sender = row["Absender*in"]
    sender_wikidata = row["Absender*in Wikidata ID"]
    addressee = row["Empfänger*in"]  
    addressee_wikidata = row["Empfänger*in Wikidata ID"]
    place_sender = row["Aufenthaltsort Absender*in"]
    place_sender_geonames = row["Aufenthaltsort Absender*in GeoNames ID"]
    place_addressee = row["Aufenthaltsort Empfänger*in"]
    place_addressee_geonames = row["Aufenthaltsort Empfänger*in GeoNames ID"]
    language = row["Sprache"]
    language_id = row["Sprache ID"]
    font = row["Schriftart"]
    kept = row["verwahrt von"]
    pages = row["Anzahl Seiten"]
    words = row["Anzahl Wörter"]
    keywords_string = row["Häufigste Wörter (relative Häufigkeit)"]

    """Die häufigsten Wörter sind als str gespeichert. Um die Einzelwerte trennen und damit besser durchsuchbar zu machen, werden sie jeweils getrennt in ein term-Tag eingefügt"""
    keywords_list = keywords_string.split(",") 
    single_keyword_list = []
    for i in keywords_list:
        if i != "nan":
            single_keyword_list.append(f"<term>{i}</term>")
    keyword_final = "\n".join(single_keyword_list)
    
    """Einfügen der Variablennamen in das TEI-Template, für jede Tabellenzeile (= jeden Brief) wird ein eigener Header erstellt und unter dem in der Metadatentabelle hinterlegten Dateinamen gespeichert"""
    with open(join("xml", "header", f"{filename}_header.xml"), "w", encoding="utf-8") as outfile:
        xml_text =f"""<?xml version="1.0" encoding="UTF-8"?>
    <?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
    <?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>
    <TEI xmlns="http://www.tei-c.org/ns/1.0">
        <teiHeader>
            <fileDesc>
                <titleStmt>
                    <title>Brief von {sender} an {addressee} vom {date_de} encoded in TEI</title>
                    <respStmt>
                        <resp>Encoded by, </resp>
                        <persName>Theresa Blaschke</persName>
                    </respStmt>
                </titleStmt>
                <publicationStmt>
                    <p>Bereitgestellt auf GitHub-Pages als Teil der Masterarbeit "Digitale Briefedition in der Fachhistoriographie der Altorientalistik. Eine Fallstudie zu Benno Landsberger" im Fach Cultural Data Studies, Philipps-Universität Marburg von Theresa Blaschke</p>
                </publicationStmt>
                <sourceDesc>
                    <bibl>
                        <title ref="https://www.gkr.uni-leipzig.de/altorientalisches-institut/forschung/landsberger-archives">Landsberger Archives</title>
                        <publisher>Altorientalisches Institut Universität Leipzig und Hebrew University Jerusalem</publisher>
                        <idno>https://www.gkr.uni-leipzig.de/fileadmin/Fakult%C3%A4t_GKR/Altorientalisches_Institut/Landsberger/{signature}.pdf</idno>
                        <extent>
                            <measure unit="pages" quantity="{pages}">{pages} Seiten</measure>
                            <measure unit="words" quantity="{words}">{words} Wörter</measure>
                        </extent>
                    </bibl>
                    <msDesc>
                        <msIdentifier>
                            <repository>{kept}</repository>
                            <idno>{signature}</idno>
                        </msIdentifier>
                        <physDesc>
                            <objectDesc>
                                <p>Beschreibart: {font}</p>
                            </objectDesc>
                        </physDesc>
                    </msDesc>
                </sourceDesc>
            </fileDesc>
            <profileDesc>
                <correspDesc>
                    <correspAction type="sent">
                        <persName ref="{sender_wikidata}">{sender}</persName>
                        <settlement ref="{place_sender_geonames}">{place_sender}</settlement>
                        <date when="{date_iso}">{date_de}</date>
                    </correspAction>
                    <correspAction type="received">
                        <persName ref="{addressee_wikidata}">{addressee}</persName>
                        <settlement ref="{place_addressee_geonames}">{place_addressee}</settlement>
                    </correspAction>
                </correspDesc>
                <langUsage>
                    <language ident="{language_id}">{language}</language>
                </langUsage>
                <textClass>
                    <keywords>
                    {keyword_final}
                    </keywords>
                </textClass>
            </profileDesc>
        </teiHeader>
    </TEI>
    """
        outfile.write(xml_text)