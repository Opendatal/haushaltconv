# Skript zur Konvertierung der Haushaltsdaten der Stadt Wuppertal in das Format von offenerhaushalt.de.
# Es wird das Python-Paket pandas verwendet, das z.B. in anaconda (www.continuum.io) enthalten ist


# -----------------------------------------------
# Laden benoetigter Bibliotheken
# -----------------------------------------------

import pandas as pd
import os
import numpy as np

# -----------------------------------------------
# Definition von Konstanten
# -----------------------------------------------

# Ordner, in dem die Aufstellungen fuer die einzelnen Produkte enthalten sind
strDataFolder = os.getcwd() + "/../Offener-Haushalt/2016-2017/04_Produkte/"

# 5. Spalte = Planung 2016
spalte = 4

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

# -----------------------------------------------
# Definition von spaeter benoetigten Funktionen
# -----------------------------------------------

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
# Hier geht das eigentliche Skript los
# -----------------------------------------------

# Array, in das die Ausgabedaten abgelegt werden
output = []

# Lade die einzelnen Produktdateien und extrahiere, Ausgaben und Ertraege
for file in os.listdir(strDataFolder):    
    if not file.endswith(".csv"):
        continue
    
    strFileName = strDataFolder + file
    
    produktid = int(file[8:15])    
    
    df_produkt = pd.read_csv(strFileName, sep=';', header=0)    
    
    ertraege = 0.0
    for zeile in zeilenErtraege:       
        wert = str(df_produkt.iloc[zeile,spalte])
        # Ueberspringe Zeile, falls Nan
        if (wert == 'nan'):
            continue        
        ertraege = ertraege + conv_betrag(wert)
    
    aufwendungen = 0.0
    for zeile in zeilenAufwendungen:       
        wert = str(df_produkt.iloc[zeile,spalte])
        # Ueberspringe Zeile, falls Nan
        if (wert == 'nan'):
            continue        
        aufwendungen = aufwendungen + conv_betrag(wert)
    
    if(ertraege != 0):
        output.append([produktid, 'Ertrag', 2016, -ertraege])
    if (aufwendungen != 0):
        output.append([produktid, 'Aufwendung', 2016, aufwendungen])

# Erstelle DataFrame aus dem Array mit den Kosten
output = np.array(output)    
df_output = pd.DataFrame(output, columns=['ProduktNR', 'Kontotyp', 'Year', 'Amount'])
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