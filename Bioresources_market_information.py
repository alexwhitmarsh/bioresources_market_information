import pandas as pd
from itertools import combinations
import Bioresources_market_info_functions as bio

# ------------  INITIATION --------------------------------------------------
path = r''

company = ['ANH', 'SVT', 'SWB', 'TMS', 'UUW', 'WSX']
df_WwTW = pd.DataFrame()
df_STC = pd.DataFrame()
df4 = pd.DataFrame()
df_mega = pd.DataFrame()

# -----------  GRAB THE RELEVANT HEADERS TO BE USED IN THE DATAFRAME -------------------
# Grab the column names from the Anglian sheet (TMS and possibly others had changed there's, causing problems)
headers_WwTW = pd.read_excel(r'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\ANH.xlsx',
                             header=None, sheet_name='WwTW', skiprows=5, usecols=('D:F, H:M, O:R, T:X'),
                             nrows=1)

headers_STC = pd.read_excel(r'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\ANH.xlsx',
                            header=None, sheet_name='STC', skiprows=5, usecols=('D:F, H:O, Q:S, U:X'))

# Whack the data together into a big data from using a for loop
for i in range(len(company)):
    path = fr'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\inputs\\{company[i]}.xlsx'

    df_temp = pd.read_excel(path, header=None, sheet_name='WwTW', skiprows=10, usecols=('D:F, H:M, O:R, T:X'), )
    df_temp = bio.data_mung(df_temp, headers_WwTW, company[i])
    df_WwTW = pd.concat([df_WwTW, df_temp])

    #This creates a pair of lat/long coordinates to enable analysis later
    df_WwTW['Coordinates'] = [[df_WwTW['WwTW location grid ref latitude'][i],
                              df_WwTW['WwTW location grid ref longitude'][i]]
                              for i in range(len(df_WwTW.index))]

    df_temp2 = pd.read_excel(path, header=None, sheet_name='STC', skiprows=10, usecols=('D:F, H:O, Q:S, U:X'))
    df_temp2 = bio.data_mung(df_temp2, headers_STC, company[i])
    df_STC = pd.concat([df_temp2, df_STC])

    # This creates a pair of lat/long coordinates to enable analysis later
    df_STC['Coordinates'] = [[df_STC['STC location (grid ref latitude)'][i],
                               df_STC['STC location (grid ref longitude)'][i]]
                              for i in range(len(df_STC.index))]

    #df_merge = pd.merge(df_WwTW, df_STC, left_on='WwTW site name', right_on='WwTW site name', how='outer')
    #df['Company'] = df.apply(lambda row: row.Company_x if pd.isna(row.Company_x) == False else row.Company_y, axis=1)

# Export the concatenated dataframes to CSV
df_STC.to_csv('Outputs/bioresources_market_information_STC.csv')
df_WwTW.to_csv('Outputs/bioresources_market_information_WwTW.csv')




# 2. This creates a set of possible company combinations
company_combo = list(combinations(company, 2))
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
plt.hist(df.iloc[:,3].loc['SVT'], bins=50, alpha=0.5, density=True, label='SVT')
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