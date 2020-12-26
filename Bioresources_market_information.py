import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import permutations

company = ['ANH', 'SVT', 'SWB', 'TMS', 'UUW', 'WSX']

df=pd.DataFrame()

# Grab the column names from the Anglian sheet (TMS and possibly others had changed there's, causing problems)
headers_WwTW = pd.read_excel(r'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\ANH.xlsx',
                             header=None, sheet_name='WwTW', skiprows=5, usecols=('D:F, H:M, O:R, T:X'),
                             nrows=1)

headers_STC = pd.read_excel(r'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\ANH.xlsx',
                            header=None, sheet_name='STC', skiprows=5, usecols=('D:F, H:O, Q:S, U:X'))

def f(df, headers):
    df.columns = headers.iloc[0, :].tolist()
    df.set_index(pd.MultiIndex.from_product([[company[i]], df.index]), inplace=True)
    df.dropna(thresh=5, inplace=True)
    df['Company'] = company[i]
    return df

# Whack the data together into a big data from using a for loop
for i in range(len(company)):
    path = r'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\\'
    path += company[i] + ".xlsx"

    df_WwTW = pd.read_excel(path, header=None, sheet_name='WwTW', skiprows=10, usecols=('D:F, H:M, O:R, T:X'), )
    df_WwTW = f(df_WwTW, headers_WwTW)

    #df_STC = pd.read_excel(path, header=None, sheet_name='STC', skiprows=10, usecols=('D:F, H:O, Q:S, U:X'))
    #df_STC = f(df_STC, headers_WwTW)

    #df_merge = pd.merge(df_WwTW, df_STC, left_on='WwTW site name', right_on='WwTW site name', how='outer')

    df = pd.concat([df, df_WwTW])
    #df['Company'] = df.apply(lambda row: row.Company_x if pd.isna(row.Company_x) == False else row.Company_y, axis=1)


#0. This coverts long and lat into coordinate pairs
df['Coordinates'] = [[df['WwTW location grid ref latitude'][i], df['WwTW location grid ref longitude'][i]] for i in range(len(df.index))]


# 1. This is the list of companies
companies = df.Company.unique()

# 2. This creates a set of possible company combinations
lst2 = [ [companies[i], companies[j]] for i in range(len(companies)) for j in range(len(companies)) if i!=j]
print(lst2)
# 3.
df3 = pd.DataFrame()

for i in range(len(companies)):
    df3[lst2[i][0]] = df.loc[lst2[i][0], 'Coordinates']
    print(df3[lst2[i][0]])


#print(df.loc['ANH', 'Coordinates'])

df.to_csv('bioresources_market_information.csv')


"""for i in df_STC['WwTW site name']:
    if i in df_WwTW['WwTW site name'].values:
        print(i)
"""



# Group by analysis
poo= df.groupby(['Company']).agg(['max', 'mean', 'min']).transpose()
poo2 = poo.swaplevel(0).sort_index(axis=0)
#print(poo2)


# Visualisaitons- pick and choose these
"""
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