# coding: utf8

# Skript zur Konvertierung der Haushaltsdaten der Stadt Wuppertal in das Format von offenerhaushalt.de.
# Es wird das Python-Paket pandas verwendet, das z.B. in anaconda (www.continuum.io) enthalten ist

# -----------------------------------------------
# Laden benoetigter Bibliotheken
# -----------------------------------------------

import pandas as pd
import os
import numpy as np

# -----------------------------------------------
# Definition von spaeter benoetigten Funktionen und Klassen
# -----------------------------------------------

class h:
    def __init__(self, jahr, verzeichnis, spalte, art, pos):
        self.jahr = jahr
        self.verzeichnis = verzeichnis
        self.spalte = spalte # In welcher Spalte stehen die Daten?        
        self.art = art # Plan / Ergebnis
        self.pos = pos # Wo steht im Dateinamen die Produktnummer?

# Funktion zur Konvertierung des Strings, der den Betrag in EUR enthaelt, in eine Zahl
def conv_betrag(wert):    
    # Entferne Buchstaben
    wert = wert.replace(' EUR', '')  
    # Entferne .
    wert = wert.replace('.', '')        
    # Ersetze , durch .
    wert = wert.replace(',', '.')
    # Konvertiere in Zahl    
    return float(wert)  

# -----------------------------------------------
# Definition von Konstanten
# -----------------------------------------------

# Ordner, in dem die Aufstellungen fuer die einzelnen Produkte enthalten sind
strDataFolder = os.getcwd() + "/../Offener-Haushalt/"

# 10. Zeile = Ordentliche Ertraege
# 19. Zeile = Finanzertraege
# 23. Zeile = Ausserordentliche Ertraege
# 27. Zeile = Ertraege aus internen Leistungsbeziehungen
zeilenErtraege = [9,18,22,26]

# 17. Zeile = Ordentliche Aufwendungen
# 20. Zeile = Zinsen und sonstige Finanzaufwendungen
# 24. Zeile = Ausserordentliche Aufwendungen
# 28. Zeile = Aufwendungen aus internen Leistungsbeziehungen
zeilenAufwendungen = [16,19,23,27]

# Pfad zur Datei mit den Produktbezeichnungen (derzeit nur fuer 2014/2015 vorhanden)
strFileNameUebersicht = os.getcwd() + "/../Offener-Haushalt/2014-2015/Uebersicht_Haushalt_2014-2015.csv"

datensaetze = [h(2009, '2012-2013/Band3/', 1, 'Ergebnis', 14),
               h(2010, '2012-2013/Band3/', 2, 'Ergebnis', 14),
               #h(2011, '2014-2015/06-Teilergebnispläne der Produkte/', 1, 'Ergebnis', 8),
               h(2012, '2012-2013/Band3/', 4, 'Plan', 14),
               #h(2012, '2014-2015/06-Teilergebnispläne der Produkte/', 2, 'Ergebnis', 8),
               h(2013, '2012-2013/Band3/', 5, 'Plan', 14),                              
               h(2013, '2016-2017/04_Produkte/', 1, 'Ergebnis', 8),
               #h(2014, '2014-2015/06-Teilergebnispläne der Produkte/', 4, 'Plan', 8),
               h(2014, '2016-2017/04_Produkte/', 2, 'Ergebnis', 8),
               #h(2015, '2014-2015/06-Teilergebnispläne der Produkte/', 5, 'Plan', 8),
               h(2015, '2016-2017/04_Produkte/', 3, 'Ergebnis', 8),
               h(2016, '2016-2017/04_Produkte/', 4, 'Plan', 8),
               h(2017, '2016-2017/04_Produkte/', 5, 'Plan', 8),
               h(2018, '2016-2017/04_Produkte/', 6, 'Plan', 8),
               h(2019, '2016-2017/04_Produkte/', 7, 'Plan', 8),
               h(2020, '2016-2017/04_Produkte/', 8, 'Plan', 8)
               ]



# -----------------------------------------------
# Hier geht das eigentliche Skript los
# -----------------------------------------------

# Array, in das die Ausgabedaten abgelegt werden
output = []

# Lade die einzelnen Produktdateien und extrahiere, Ausgaben und Ertraege
for datensatz in datensaetze:
    for file in os.listdir(strDataFolder + datensatz.verzeichnis):    
        if not file.endswith(".csv"):
            continue
        
        strFileName = strDataFolder + datensatz.verzeichnis + file
        
        produktid = int(file[datensatz.pos:(datensatz.pos+7)])    
        
        df_produkt = pd.read_csv(strFileName, sep=';', header=0)    
        
        ertraege = 0.0
        for zeile in zeilenErtraege:       
            wert = str(df_produkt.iloc[zeile,datensatz.spalte])
            # Ueberspringe Zeile, falls Nan
            if (wert == 'nan'):
                continue        
            ertraege = ertraege + conv_betrag(wert)
        
        aufwendungen = 0.0
        for zeile in zeilenAufwendungen:       
            wert = str(df_produkt.iloc[zeile,datensatz.spalte])
            # Ueberspringe Zeile, falls Nan
            if (wert == 'nan'):
                continue        
            aufwendungen = aufwendungen + conv_betrag(wert)
        
        if(ertraege != 0):
            output.append([produktid, 'Ertrag', datensatz.art, datensatz.jahr, -ertraege])
        if (aufwendungen != 0):
            output.append([produktid, 'Aufwendung', datensatz.art, datensatz.jahr, aufwendungen])

# Erstelle DataFrame aus dem Array mit den Kosten
output = np.array(output)    
df_output = pd.DataFrame(output, columns=['ProduktNR', 'Kontotyp', 'Art', 'Year', 'Amount'])
df_output[['ProduktNR']] = df_output[['ProduktNR']].astype(int)

# Leite die Produktgruppe und den Produktbereich aus der ProduktNR ab
df_output[['ProduktbereichNR']] = df_output[['ProduktNR']].apply(lambda x: np.floor(x/100000))
df_output[['ProduktgruppeNR']] = df_output[['ProduktNR']].apply(lambda x: np.floor(x/1000))

# Lade die Tabelle mit den Produktbezeichnungen
df_uebersicht = pd.read_csv(strFileNameUebersicht, sep=';', header=0)

# Waehle die relevanten Spalten aus
df_uebersicht = df_uebersicht[['PB-Nr.', 'Produktbereich', 'PG-Nr.', 'Produktgruppe', 'P-Nr.', 'Produkt']]
# Aendere die Spaltenbezeichnungen in das Bonner Format
df_uebersicht.columns = ['ProduktbereichNR', 'Produktbereich', 'ProduktgruppeNR', 'Produktgruppe', 'ProduktNR', 'Produkt']
df_uebersicht[['ProduktNR']] = df_uebersicht[['ProduktNR']].astype(int)
df_uebersicht[['ProduktbereichNR']] = df_uebersicht[['ProduktbereichNR']].astype(int)
df_uebersicht[['ProduktgruppeNR']] = df_uebersicht[['ProduktgruppeNR']].astype(int)

df_uebersicht_produkte = df_uebersicht[['ProduktNR', 'Produkt']]
df_uebersicht_produkte = df_uebersicht_produkte.drop_duplicates()
df_uebersicht_produktgruppen = df_uebersicht[['ProduktgruppeNR', 'Produktgruppe']]
df_uebersicht_produktgruppen = df_uebersicht_produktgruppen.drop_duplicates()
df_uebersicht_produktbereiche = df_uebersicht[['ProduktbereichNR', 'Produktbereich']]
df_uebersicht_produktbereiche = df_uebersicht_produktbereiche.drop_duplicates()

# Fuehre den JOIN der Kostentabelle mit den Bezeichnungstabellen durch
df_output = pd.merge(df_output, df_uebersicht_produkte, on='ProduktNR',how='left')
df_output = pd.merge(df_output, df_uebersicht_produktbereiche, on='ProduktbereichNR',how='left')
df_output = pd.merge(df_output, df_uebersicht_produktgruppen, on='ProduktgruppeNR',how='left')

df_output[['ProduktbereichNR']] = df_output[['ProduktbereichNR']].astype(int)
df_output[['ProduktgruppeNR']] = df_output[['ProduktgruppeNR']].astype(int)

df_output.to_csv('wuppertal_haushalt2016.csv', index=False)