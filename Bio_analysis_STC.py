
# THIS PROVIDES SUMMARY DATA REGARDING COMPANIES' STCs
import pandas as pd
import sqlite3
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

# Connect to the databse containing companies' STC data
conn = sqlite3.connect(r'Outputs\bioresources.db')

# 1. CALCULATE THE PROPORTION OF SITES WHERE i) VOLUME TREATED and ii) PRODUCT DS% IS MEASURED (RATHER THAN ESTIMATED)
df = pd.read_sql("""SELECT Company, 
                           "Estimated or Measured volume of treated sludge produced",
                           "Estimated or Measured product DS%" 
                    FROM STC""", conn)

g = df.groupby(['Company'])  # Group by Company - this just creates a groupby object

a = g['Estimated or Measured volume of treated sludge produced'].value_counts(normalize=True)
a.index.rename(['Company', 'Measured or Estimated'], inplace=True)  # This renames the second element of the multi-index
a = a.reset_index()  # This makes the 'values' column renamed to the original column name

b = g['Estimated or Measured product DS%'].value_counts(normalize=True)  # This works out the proportions
b.index.rename(['Company', 'Measured or Estimated'], inplace=True)
b = b.reset_index()

df2 = pd.merge(a, b, on=['Company', 'Measured or Estimated'], how='outer')
df2 = df2[df2['Measured or Estimated'] == 'Measured']
df2.reset_index().to_sql('Share_STCs_measured', con=conn, if_exists='replace', index=False)

# 2. VALUE COUNTS OF THE TYPE OF SITE COLUMN
df = pd.read_sql("""SELECT Company, "Type of site" FROM STC""", conn)
g = df.groupby(['Company'])
df3 = g['Type of site'].value_counts(normalize=True)
df3.name = 'Share'  # name the series
df3 = df3.reset_index()  # get a conventional index, rather than multi-index
df3 = df3.pivot(index='Company', columns='Type of site', values='Share')  # optional: convert to wide format
df3['Total'] = df3.sum(axis=1)  # optional: sum columns to check it totals to 1
df3.reset_index().to_sql('Share_STC_site_types', con=conn, if_exists='replace', index=False)

# 3. VALUE COUNTS FOR YES QUESTIONS
df = pd.read_sql("""SELECT Company, 
                           "Sludge screened at STC",
                           "Acceptance criteria for input material", 
                           "Can site receive sludge not de-gritted?", 
                           "Can site receive sludge from sites without screening?",
                           "Is the site producing untreated sludge?", 
                           "Is the site producing conventionally treated sludge?",
                           "Is the site producing enhanced treated sludge?", 
                           "Is the site compliant with and certified under the Biosolids Assurance Scheme?"
                FROM STC""", conn)

g = df.groupby(['Company'])

lst = []
for i in list(df.columns)[1:]:  # Skip first column as the 'Company' became index in groupby process
    j = g[i].value_counts(normalize=True)
    j.index.rename(['Company', 'Yes or No'], inplace=True)
    lst.append(j)

df4 = pd.merge(lst[0], lst[1], on=['Company', 'Yes or No'], how='outer')
for i in lst[2:]:
    df4 = pd.merge(df4, i, on=['Company', 'Yes or No'], how='outer')

df4.sort_values('Company', inplace=True)
df4.reset_index().to_sql('Share_STC_criteria_Yes', con=conn, if_exists='replace', index=False)







