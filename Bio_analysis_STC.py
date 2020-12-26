import pandas as pd

df = pd.read_csv('Outputs/bioresources_market_information_STC.csv')

print(df.columns)
print(df.transpose())

g = df.groupby(['Company'])



# VALUE COUNTS AND MERGING OF THE MEASURED VS. ESTIMATED COLUMNS
a = g['Estimated or Measured volume of treated sludge produced'].value_counts(normalize=True)
a.index.rename(['Company', 'Measured or Estimated'], inplace=True)
a = a.reset_index()

b = g['Estimated or Measured product DS%'].value_counts(normalize=True)
b.index.rename(['Company', 'Measured or Estimated'], inplace=True)
b = b.reset_index()

df2 = pd.merge(a,b, on=['Company','Measured or Estimated'], how='outer')
df2 = df2[df2['Measured or Estimated'] == 'Measured']
df2.reset_index().to_csv('Outputs/bioresources_market_information_STC_measured_count.csv')

# VALUE COUNTS OF THE TYPE OF SITE COLUMN
df3 = g['Type of site'].value_counts(normalize=True)
df3.name = 'Share'
df3.reset_index().to_csv('Outputs/bioresources_market_information_STC_site_types.csv')


# VALUE COUNTS FOR YES QUESTIONS
lst = ['Sludge screened at STC',
       'Acceptance criteria for input material',
       'Can site receive sludge not de-gritted?',
       'Can site receive sludge not de-gritted?',
       'Can site receive sludge from sites without screening?',
       'Is the site producing untreated sludge?',
       'Is the site producing conventionally treated sludge?',
       'Is the site producing enhanced treated sludge?',
       'Is the site compliant with and certified under the Biosolids Assurance Scheme?']

lst2 = []
for i in lst:
    j = g[i].value_counts(normalize=True)
    j.index.rename(['Company', 'Yes or No'], inplace=True)
    lst2.append(j)

df4 = pd.merge(lst2[0], lst2[1], on=['Company', 'Yes or No'], how='outer')
for i in lst2[2:]:
    df4 = pd.merge(df4, i, on=['Company','Yes or No'], how='outer')


df4.reset_index(inplace=True)
df4 = df4[df4['Yes or No'] == 'Yes']
df4.reset_index().to_csv('Outputs/bioresources_market_information_STC_Yes_count.csv')







