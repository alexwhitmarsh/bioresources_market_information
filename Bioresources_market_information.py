import pandas as pd
import Bioresources_market_info_functions as bio
import copy
import sqlite3

# ----------- PING COMPANIES' WEBSITES TO EXTRACT THEIR DATA -------------------------------
# --------- This is saved in a separate folder. So doesn't automatically get picked up below  -----
#try:
#    bio.auto_download()
#except:
#    print('Auto-download hit a snag.')


# ------------  INITIATION --------------------------------------------------
print("Initiating and creating table headers")
companies_WwTW = ['ANH','HDD','NES','SRN','SVE', 'SWB', 'TMS', 'UUW','WSH', 'WSX', 'YKY']
companies_STC = copy.copy(companies_WwTW)
companies_STC.remove('HDD') # HDD Have no STCs
companies_dict = {'ANH': 'Anglian Water', 'HDD': 'Hafren Dyfrdwy', 'NES': 'Northumbrian Water',
                     'SRN': 'Southern Water', 'SVE': 'Severn Trent Water', 'SWB': 'South West Water',
                     'TMS': 'Thames Water', 'UUW': 'United Utilities', 'WSH': 'Dwr Cymru',
                     'WSX': 'Wessex Water', 'YKY': 'Yorkshire Water'}

df_small = pd.DataFrame()
df_WwTW = pd.DataFrame()
df_STC = pd.DataFrame()


# -----------  GRAB THE RELEVANT HEADERS TO BE USED IN THE DATAFRAME -------------------
# Grab the column names from the Anglian sheet (TMS and possibly others had changed there's, causing problems)
headers_small = pd.read_excel(r'inputs\Ofwat_template.xlsx',
                             header=None, sheet_name='Small WwTW', skiprows=6, usecols=('D:F, H:I'),
                             nrows=1)

headers_WwTW = pd.read_excel(r'inputs\Ofwat_template.xlsx',
                             header=None, sheet_name='WwTW', skiprows=5, usecols=('D:F, H:M, O:R, T:X'),
                             nrows=1)

headers_STC = pd.read_excel(r'inputs\Ofwat_template.xlsx',
                            header=None, sheet_name='STC', skiprows=4, usecols=('D:F, H:O, Q:S, U:X, Z'), nrows=1)


# Whack the data together into a big data from using a for loop
print("Creating dataframe of small WwTWs")
for company in companies_WwTW:
    path = fr'inputs\{company}.xlsx'
    df_temp0 = pd.read_excel(path, header=None, sheet_name='Small WwTW', skiprows=10, usecols=('D:F, H:I') )
    df_temp0 = bio.data_mung(df_temp0, headers_small, company)
    df_small = pd.concat([df_small, df_temp0])

# This creates a pair of lat/long coordinates to enable analysis later
    df_small['Coordinates'] = [[df_small['WwTW location (grid ref latitude)'][i],
                              df_small['WwTW location (grid ref longitude)'][i]]
                              for i in range(len(df_small.index))]

    df_small['Company Name'] = df_small['Company'].map(companies_dict)



print("Creating dataframe of WwTWs")
for company in companies_WwTW:
    path = fr'inputs\\{company}.xlsx'
    df_temp = pd.read_excel(path, header=None, sheet_name='WwTW', skiprows=10, usecols=('D:F, H:M, O:R, T:X'), )
    df_temp = bio.data_mung(df_temp, headers_WwTW, company)
    df_WwTW = pd.concat([df_WwTW, df_temp])

    # This creates a pair of lat/long coordinates to enable analysis later
    df_WwTW['Coordinates'] = [[df_WwTW['WwTW location grid ref latitude'][i],
                              df_WwTW['WwTW location grid ref longitude'][i]]
                              for i in range(len(df_WwTW.index))]

    df_WwTW['Company Name'] = df_WwTW['Company'].map(companies_dict)


print("Creating dataframe of STCs")
for company in companies_STC:
    path = fr'C:\Users\Alex\OneDrive\Python\Pycharm\Bioresources market information\inputs\\{company}.xlsx'
    df_temp2 = pd.read_excel(path, header=None, sheet_name='STC', skiprows=10, usecols=('D:F, H:O, Q:S, U:X, Z'))
    df_temp2 = bio.data_mung(df_temp2, headers_STC, company)
    df_STC = pd.concat([df_STC, df_temp2])

    # This creates a pair of lat/long coordinates to enable analysis later
    df_STC['Coordinates'] = [[df_STC['STC location (grid ref latitude)'][i],
                               df_STC['STC location (grid ref longitude)'][i]]
                              for i in range(len(df_STC.index))]

    df_STC['Company Name'] = df_STC['Company'].map(companies_dict)


# Format relevant columns
df_STC['Estimated or Measured volume of treated sludge produced'] = df_STC['Estimated or Measured volume of treated sludge produced'].str.title()

for i in [4, 6]:
    df_WwTW.iloc[:, i] = df_WwTW.iloc[:, i].str.title().str.split().str.get(0).replace({'Estimate': 'Estimated'})  # split out words and just grab first

for i in [9, 10, 11, 12, 13]:
    df_WwTW.iloc[:, i] = df_WwTW.iloc[:, i].str.title().replace({'Y': 'Yes', 'N': 'No'})

for i in [4, 6, 10]:
    df_STC.iloc[:, i] = df_STC.iloc[:, i].str.title().str.split().str.get(0) # split out words and just grab first

for i in [7, 9, 12, 13, 14, 15, 16, 17]:
    df_STC.iloc[:, i] = df_STC.iloc[:, i].str.title().replace({'Y': 'Yes', 'N': 'No'})
#                         ,'Input Material To Be Assessed For Freshness, Alkalinity, Septicity, Rag/Grit Content And Potentially Toxic Elements.':'Yes',
#                         'Y 4% - 8%, N 19%-27%': 'Yes',
#                         'Y (Via Inlet)': 'Yes'})

# Address the double counting issue by only calculating volume going throught treatment centres (e.g. not de-watering centres)
df_STC['STC Only End product volume per year'] = df_STC.apply(lambda row: row['End product volume per year']
                                  if row['Type of site'] == 'Treatment'
                                  else 0, axis=1)

# Export the dataframes to csv files, including the combined (cut down) file
df_concat = bio.Concat()

# Export the dataframes to sql database (exporting directly from dataframe, rather than csvs, created an error)
print("Exporting to SQL database")

conn = sqlite3.connect(r'Outputs\bioresources.db')

# SQL struggled with the list-type nature of these columns, so altered to text
df_small['Coordinates'] = df_small['Coordinates'].map(str)
df_WwTW['Coordinates'] = df_WwTW['Coordinates'].map(str)
df_STC['Coordinates'] = df_STC['Coordinates'].map(str)

df_small.reset_index(drop=True).to_sql('small', conn, if_exists='replace', index=False)
df_WwTW.reset_index(drop=True).to_sql('WwTW', conn, if_exists='replace', index=False)
df_STC.reset_index(drop=True).to_sql('STC', conn, if_exists='replace', index=False)
df_concat.to_sql('concat', conn, if_exists='replace', index=False)



