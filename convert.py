# coding: utf8

import pandas as pd

def EUR2float(input):
    return float(str(input).replace(' EUR','').replace('.','').replace(',','.'))

df_input = pd.read_csv('HHPL_Entwurf_2019.csv')

df_output = pd.DataFrame()

ProduktbereichNR = {} # 1. Ebene
ProduktgruppeNR = {} #2. Ebene
#ProduktNR #3. Ebene


output_index = 0

for index, row in df_input.iterrows():
    current_Projektstrukturplan = int(row['Projektstrukturplan'])
    current_Produkt = str(row[1])
    print("\n" + current_Produkt)
    current_ProduktbereichNR = str(current_Projektstrukturplan)[1:3]
    print("ProduktbereichNR " + current_ProduktbereichNR )
    current_ProduktgruppeNR = str(current_Projektstrukturplan)[4:6]
    print("ProduktgruppeNR " + current_ProduktgruppeNR )
    current_ProduktNR = str(current_Projektstrukturplan)[6:8]
    print("ProduktNR " + current_ProduktNR )
    if current_ProduktgruppeNR == "00":
        ProduktbereichNR[current_ProduktbereichNR] = str(current_Produkt)
    if current_ProduktNR == "00":
        ProduktgruppeNR[current_ProduktgruppeNR] = str(current_Produkt)
    if row['Stufe in Projekthier'] != 4:
        continue
    current_Aufwendungen = EUR2float(row['Ordentiche.Aufwendungen'])
    current_Ertraege = EUR2float(row['Ordentliche Erträge'])

    df_output.at[output_index,'Art'] = "Plan"
    df_output.at[output_index,'Betrag'] = str(current_Aufwendungen)
    df_output.at[output_index,'Typ'] = "Aufwendung"
    df_output.at[output_index,'Produktbereich'] = str(ProduktbereichNR[current_ProduktbereichNR])
    df_output.at[output_index,'ProduktbereichNR'] = str(current_ProduktbereichNR)
    df_output.at[output_index,'Produktgruppe'] = str(ProduktgruppeNR[current_ProduktgruppeNR])
    df_output.at[output_index,'ProduktgruppeNR'] = str(current_ProduktgruppeNR)
    df_output.at[output_index,'Produkt'] = current_Produkt
    df_output.at[output_index,'ProduktNR'] = str(current_ProduktNR)
    output_index += 1
    df_output.at[output_index,'Art'] = "Plan"
    df_output.at[output_index,'Betrag'] = str(current_Ertraege*-1)
    df_output.at[output_index,'Typ'] = "Ertrag"
    df_output.at[output_index,'Produktbereich'] = str(ProduktbereichNR[current_ProduktbereichNR])
    df_output.at[output_index,'ProduktbereichNR'] = str(current_ProduktbereichNR)
    df_output.at[output_index,'Produktgruppe'] = str(ProduktgruppeNR[current_ProduktgruppeNR])
    df_output.at[output_index,'ProduktgruppeNR'] = str(current_ProduktgruppeNR)
    df_output.at[output_index,'Produkt'] = current_Produkt
    df_output.at[output_index,'ProduktNR'] = str(current_ProduktNR)
    output_index += 1

df_output['Year'] = '2019'

df_output.to_csv('wuppertal_haushalt_2019.csv', index=False)
