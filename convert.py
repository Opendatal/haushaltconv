# coding: utf8

import pandas as pd

csv = pd.read_csv('HHPL_Entwurf_2018.csv')

df_output = csv
df_output[['Projektstrukturplan']] = df_output[['Projektstrukturplan']].astype(int)

ProduktbereichNR = {} # 1. Ebene
ProduktgruppeNR = {} #2. Ebene
#ProduktNR #3. Ebene

df_output['Produktbereich'] = None
df_output['Produktgruppe'] = None
df_output['Produkt'] = None
df_output['ProduktNR'] = None

for index, row in df_output.iterrows():
    current_Produkt = str(row[1])
    print("\n" + current_Produkt)
    current_ProduktbereichNR = str(row['Projektstrukturplan'])[1:3]
    print("ProduktbereichNR " + current_ProduktbereichNR )
    current_ProduktgruppeNR = str(row['Projektstrukturplan'])[4:6]
    print("ProduktgruppeNR " + current_ProduktgruppeNR )
    current_ProduktNR = str(row['Projektstrukturplan'])[6:8]
    print("ProduktNR " + current_ProduktNR )
    if current_ProduktgruppeNR == "00":
        ProduktbereichNR[current_ProduktbereichNR] = str(current_Produkt)
    if current_ProduktNR == "00":
        ProduktgruppeNR[current_ProduktgruppeNR] = str(current_Produkt)

    df_output.set_value(index,'Produktbereich',str(ProduktbereichNR[current_ProduktbereichNR]))
    df_output.set_value(index,'Produktgruppe',str(ProduktgruppeNR[current_ProduktgruppeNR]))
    df_output.set_value(index,'Produkt',current_Produkt)


    df_output.set_value(index,'ProduktbereichNR',str(current_ProduktbereichNR))
    df_output.set_value(index,'ProduktgruppeNR',str(current_ProduktgruppeNR))
    df_output.set_value(index,'ProduktNR',str(current_Produkt))


df_output['Year'] = '2018'

df_output.to_csv('wuppertal_haushalt.csv', index=False)
