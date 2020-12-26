import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Outputs/bioresources_market_information_STC_Pairings_MEGA.csv')
company = ['ANH', 'SVT', 'SWB', 'TMS', 'UUW', 'WSX']


for i in company:
    a = df[f'{i} site'].dropna().nunique(())
    print(f'{i} has ' + str(a) + ' STC sites in total')
    b = df[f'{i} site'][df.Near==True].dropna().nunique()
    print(f'{i} has ' + str(b) + ' STC sites near to another water company')
    c = b / a * 100
    print(f'{i} has ' + str(round(c)) + '% of its STC sites close to another water companies')

"""plt.hist(df[df["Company_combo"]=="ANH/SVT"]['Distance'])
plt.show()"""

print(df['SWB site'].dropna().unique())