import pandas as pd
from itertools import combinations
import Bioresources_market_info_functions as bio
import copy
import sys


# ----------- PING COMPANIES' WEBSITES TO EXTRACT THEIR DATA -------------------------------
# --------- This is saved in a separate folder. So doesn't automatically get picked up below  -----
try:
    bio.auto_download()
except:
    print('Auto-download hit a snag.')


# ------------  INITIATION --------------------------------------------------
companies_WwTW = ['ANH','HDD','NES','SRN','SVE', 'SWB', 'TMS', 'UUW','WSH', 'WSX', 'YKY']
poo = copy.copy(companies_WwTW)
poo.remove('HDD')
print(poo)
companies_STC =  ['ANH',      'NES','SRN','SVE', 'SWB', 'TMS', 'UUW','WSH', 'WSX', 'YKY'] # HDD has no STCs
companies_dict = {'ANH': 'Anglian Water', 'HDD': 'Hafren Dyfrdwy', 'NES': 'Northumbrian Water',
                     'SRN': 'Southern Water', 'SVE': 'Severn Trent Water', 'SWB': 'South West Water',
                     'TMS': 'Thames Water', 'UUW': 'United Utilities', 'WSH': 'Dŵr Cymru',
                     'WSX': 'Wessex Water', 'YKY': 'Yorkshire Water'}

df_small = pd.DataFrame()
df_WwTW = pd.DataFrame()
df_STC = pd.DataFrame()
df4 = pd.DataFrame()
df_mega = pd.DataFrame()


# -----------  GRAB THE RELEVANT HEADERS TO BE USED IN THE DATAFRAME -------------------
# Grab the column names from the Anglian sheet (TMS and possibly others had changed there's, causing problems)
headers_small = pd.read_excel(r'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\inputs\Ofwat_template.xlsx',
                             header=None, sheet_name='Small WwTW', skiprows=6, usecols=('D:F, H:I'),
                             nrows=1)

headers_WwTW = pd.read_excel(r'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\inputs\Ofwat_template.xlsx',
                             header=None, sheet_name='WwTW', skiprows=5, usecols=('D:F, H:M, O:R, T:X'),
                             nrows=1)

headers_STC = pd.read_excel(r'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\inputs\Ofwat_template.xlsx',
                            header=None, sheet_name='STC', skiprows=4, usecols=('D:F, H:O, Q:S, U:X'), nrows=1)


# Whack the data together into a big data from using a for loop
for company in companies_WwTW:
    path = fr'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\inputs\\{company}.xlsx'
    df_temp0 = pd.read_excel(path, header=None, sheet_name='Small WwTW', skiprows=10, usecols=('D:F, H:I') )
    df_temp0 = bio.data_mung(df_temp0, headers_small, company)
    df_small = pd.concat([df_small, df_temp0])

    # This creates a pair of lat/long coordinates to enable analysis later
    df_small['Coordinates'] = [[df_small['WwTW location (grid ref latitude)'][i],
                              df_small['WwTW location (grid ref longitude)'][i]]
                              for i in range(len(df_small.index))]

    df_small['Company Name'] = df_small['Company'].map(companies_dict)




for company in companies_WwTW:
    path = fr'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\inputs\\{company}.xlsx'
    df_temp = pd.read_excel(path, header=None, sheet_name='WwTW', skiprows=10, usecols=('D:F, H:M, O:R, T:X'), )
    df_temp = bio.data_mung(df_temp, headers_WwTW, company)
    df_WwTW = pd.concat([df_WwTW, df_temp])

    # This creates a pair of lat/long coordinates to enable analysis later
    df_WwTW['Coordinates'] = [[df_WwTW['WwTW location grid ref latitude'][i],
                              df_WwTW['WwTW location grid ref longitude'][i]]
                              for i in range(len(df_WwTW.index))]

    df_WwTW['Company Name'] = df_WwTW['Company'].map(companies_dict)

for company in companies_STC:
    path = fr'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\inputs\\{company}.xlsx'
    df_temp2 = pd.read_excel(path, header=None, sheet_name='STC', skiprows=10, usecols=('D:F, H:O, Q:S, U:X'))
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

df_small.reset_index(drop=True).to_csv('Outputs/bioresources_market_information_small.csv')
df_STC.reset_index(drop=True).to_csv('Outputs/bioresources_market_information_STC.csv')
df_WwTW.reset_index(drop=True).to_csv('Outputs/bioresources_market_information_WwTW.csv')

sys.exit()



# 2. This creates a set of possible company combinations
company_combo = list(combinations(companies_STC, 2))
comp1 = [company_combo[i][0] for i in range(len(company_combo))] # This extracts the first company in the company combo
comp2 = [company_combo[i][1] for i in range(len(company_combo))] # This extracts the second company in the company combo

# This loop applies the 'distance pairings' function to the relevant dataframe to each company combo
for i, j in zip(comp1, comp2):
    print(i, j)
    df = bio.distance_pairings(df_STC, i, j, "Sludge Treatment Centre (STC) name").sort_values(by=['Distance'])
    df_mega = pd.concat([df_mega, df])

df_mega.to_csv('Outputs/bioresources_market_information_STC_Pairings_MEGA.csv')




"""
for i in range(len(lst)):
    df3[lst[i][0]] = df.loc[lst[i][0], 'Coordinates']

for i in df_STC['WwTW site name']:
    if i in df_WwTW['WwTW site name'].values:
        print(i)

# Group by analysis
poo= df.groupby(['Company']).agg(['max', 'mean', 'min']).transpose()
poo2 = poo.swaplevel(0).sort_index(axis=0)
#print(poo2)


# Visualisaitons- pick and choose these

# Distribution of quantity of sludge produced per year
plt.hist(df.iloc[:,3].loc['ANH'], bins=50, alpha=0.5, density=True, label='ANH')
plt.hist(df.iloc[:,3].loc['SVE'], bins=50, alpha=0.5, density=True, label='SVT')
plt.hist(df.iloc[:,3].loc['TMS'], bins=50, alpha=0.5, density=True, label='TMS')
plt.legend()
plt.xlabel('quantity (TDS)')
plt.title('Distribution of quantity of sludge produced per year')
plt.show()


sns.catplot(data=df, x='Company', y= 'Quantity of raw sludge produced per year (only sites where sludge leaves assets under network plus price control) ',
            estimator=np.median, kind='bar', hue='Inlet Screened <=6mm', col='Sludge screened')
plt.ylabel('Median')
plt.show()


sns.barplot(data=df, x='Company', y='Quantity of raw sludge produced per year (only sites where sludge leaves assets under network plus price control) ',
            estimator=np.median)
plt.ylabel('Median')
plt.show()

sns.violinplot(data=df, x='Company', y='Quantity of raw sludge produced per year (only sites where sludge leaves assets under network plus price control) ')
plt.show()


sns.kdeplot(df.iloc[:,3].loc['ANH'])
sns.kdeplot(df.iloc[:,3].loc['SVT'])
sns.kdeplot(df.iloc[:,3].loc['TMS'])
plt.show()
"""