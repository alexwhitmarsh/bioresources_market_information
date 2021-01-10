import pandas as pd
from itertools import combinations
import sqlite3
import Bioresources_market_info_functions as bio


# THE OBJECTIVE OF THIS CODE IS TO FIND THE DISTANCE BETWEEN ALL COMPANIES' STCs.

# Connect to the databse containing companies' STC data
conn = sqlite3.connect(r'Outputs\bioresources.db')

# Just collect the data required and give them sensible ean,es
df_STC = pd.read_sql("""SELECT 
                            Company, 
                            "Sludge Treatment Centre (STC) name" AS "STC name",
                            "STC location (grid ref latitude)" AS latitude, 
                            "STC location (grid ref longitude)" AS longitude
                        FROM STC""", conn)

df_STC.set_index('Company', inplace=True)

companies = ['ANH', 'NES', 'SRN', 'SVE', 'SWB', 'TMS', 'UUW', 'WSH', 'WSX', 'YKY']

for company in companies:
    df_STC['Coordinates'] = [[df_STC['latitude'][i], df_STC['longitude'][i]]
                              for i in range(len(df_STC.index))]


company_combo = list(combinations(companies, 2))
comp1 = [company_combo[i][0] for i in range(len(company_combo))] # This extracts the first company in the company combo
comp2 = [company_combo[i][1] for i in range(len(company_combo))] # This extracts the second company in the company combo


# This loop applies the 'distance pairings' function to the relevant dataframe to each company combo
df_all = pd.DataFrame()
for i, j in zip(comp1, comp2):
    print(i, j)
    df = bio.distance_pairings(df_STC, i, j, "STC name").sort_values(by=['Distance'])
    df_all = pd.concat([df_all, df])

df_all = df_all.applymap(str) # SQL was struggling with datatypes - converting all to text resolves this
df_all.to_sql('STC_distance_Pairings', con=conn, if_exists='replace', index=False)








