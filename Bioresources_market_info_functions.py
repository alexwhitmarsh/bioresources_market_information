#from geopy import distance
import pandas as pd
import requests

def auto_download():
    dict = {
        'ANH': r'https://www.anglianwater.co.uk/siteassets/household/about-us/bioresources-market-information-2020-tables-1-5.xlsx',
        'HDD': r'https://www.hdcymru.co.uk/content/dam/hdcymru/regulatory-documents/2020-bioresources-market-information-HD-appendix1.xlsx',
        'NES': r'https://www.nwg.co.uk/globalassets/corporate-images/news-and-press/northumbrian-water-bioresources-market-information-2019-20.pdf',
        'SRN': r'https://www.southernwater.co.uk/media/3646/rc-20-rcfl-016-bioresources-market-information-completed.xlsm',
        'SVE': r'https://www.stwater.co.uk/content/dam/stw/regulatory-library/2020-bioresources-market-information-stw-appendix1.xlsx',
        'SWB': r'https://www.southwestwater.co.uk/siteassets/commercial/bioresources-market-information-2019-20.xlsx',
        'TMS': r'https://www.thameswater.co.uk/media-library/home/about-us/responsibility/managing-sewage-sludge/bioresources-locations-and-successful-contract-market-info-2019-20.xlsx',
        'UUW': r'https://www.unitedutilities.com/globalassets/z_corporate-site/about-us-pdfs/annual-performance-report-2020/bioresources-platform-2020.xlsx',
        'WSH': r'https://corporate.dwrcymru.com/-/media/Project/Files/Page-Documents/Corporate/Library/Annual-Performance-Reports/2019-2020/Dwr-Cymru-Bioresources-market-information-for-publication-2019-20.ashx',
         'WSX': r'https://www.wessexwater.co.uk/-/media/files/wessexwater/corporate/strategy-and-reports/bioresources-market-information-2020.xlsx',
        'YKY': r'https://www.yorkshirewater.com/media/2585/yky-bioresources-market-information-2020.xlsx'
    }

    for key in dict:
        r = requests.get(dict[key])
        with open(fr'C:\Users\Jacob\OneDrive\Python\Pycharm\Bioresources market information\inputs\auto_download\{key}.xlsx', 'wb') as f:
            f.write(r.content)

def data_mung(df, headers, company):
    """This function mungs a dataframe into the right format. """
    df.columns = headers.iloc[0, :].tolist()
    df.set_index(pd.MultiIndex.from_product([[company], df.index]), inplace=True)
    df.dropna(thresh=5, inplace=True)
    df['Company'] = company
    return df


def distance_pairings(df, company1, company2, site_name_key):
    """ This function coverts long and lat into coordinate pairs"""
    df2 = pd.DataFrame()
    df2['Locations'] = [df.loc[company1, site_name_key].iloc[i] + ' / ' + df.loc[company2, site_name_key].iloc[j]
                       for i in range(len(df.loc[company1, site_name_key]))
                       for j in range(len(df.loc[company2, site_name_key]))]

    df2[[company1 + ' site', company2 + ' site']] = df2.Locations.str.split(' / ', expand=True)

    df2['Coordinates'] = [df.loc[company1, 'Coordinates'].iloc[i] + df.loc[company2, 'Coordinates'].iloc[j]
                          for i in range(len(df.loc[company1, 'Coordinates']))
                          for j in range(len(df.loc[company2, 'Coordinates']))]

    # This finds the distance for coordinate pairs
    df2['Distance'] = [distance.distance(df.loc[company1, 'Coordinates'].iloc[i], df.loc[company2, 'Coordinates'].iloc[j]).miles
                       for i in range(len(df.loc[company1, 'Coordinates']))
                       for j in range(len(df.loc[company2, 'Coordinates']))]

    df2['Near'] = df2['Distance'] < 50

    df2['Company_combo'] = company1 + "/" + company2


    #df2.to_csv('Outputs/bioresources_market_information_STC_Pairings_{}_{}.csv'.format(company1, company2))

    return df2


def Concat():
    """This function concatenates all the three files from the main py file."""
    import pandas as pd
    df_small = pd.read_csv('Outputs/bioresources_market_information_small.csv')
    df_STC = pd.read_csv('Outputs/bioresources_market_information_STC.csv')
    df_WwTW = pd.read_csv('Outputs/bioresources_market_information_WwTW.csv')
    df_small.drop(columns=['WwTW classification', 'Coordinates'], inplace=True)
    df_small.rename(columns={'WwTW site name': 'Site Name',
                             'WwTW location (grid ref latitude)': 'Latitide',
                             'WwTW location (grid ref longitude)': 'Longitude',
                             'Volume of raw sludge produced per year': 'Sludge production',
                             'WwTW classification': 'Site classification'}, inplace=True)
    df_small['Type'] = 'Small WwTW'
    df_WwTW.drop(columns=["Estimated or Measured volume of sludge",
                          "Average Dry Solids of sludge produced by works %",
                          "Estimated or Measured %dry solids sludge",
                          "typical volatile solids content",
                          "WwTW classification",
                          "Inlet Screened <=6mm",
                          "De-gritting at inlet works",
                          "Sludge screened",
                          "Further information (unusual sludge constituents, planning constraints, freshness etc.) ",
                          "Is site co-located with a Sludge Treatment Centre (STC)?",
                          "Operating hours of the site",
                          "What is the maximum size (capacity) of tanker that can enter the works?",
                          "What is the minimum requirement for tanker sludge collection frequency?",
                          "Other",
                          "Coordinates"], inplace=True)
    df_WwTW.rename(columns={
        "WwTW site name": 'Site Name',
        "WwTW location grid ref latitude": 'Latitide',
        "WwTW location grid ref longitude": 'Longitude',
        "Volume of raw sludge produced per year": 'Sludge production'},
        inplace=True)
    df_WwTW['Type'] = 'WwTW'
    df_STC.drop(columns=["Estimated or Measured volume of treated sludge produced",
                         "Product Dry Solids %",
                         "Estimated or Measured product DS%",
                         "Sludge screened at STC",
                         "Usual operating hours of the site",
                         "Acceptance criteria for input material",
                         #"Type of site",
                         "Dry solids range accepted in to site %",
                         "Can site receive sludge not de-gritted?",
                         "Can site receive sludge from sites without screening?",
                         "Is the site producing untreated sludge?",
                         "Is the site producing conventionally treated sludge?",
                         "Is the site producing enhanced treated sludge?",
                         "Is the site compliant with and certified under the Biosolids Assurance Scheme?",
                         "Coordinates",
                         "Further information (planning constraints, operational defects that could impact on product quality etc.)",
                         "STC Only End product volume per year"], inplace=True)
    df_STC.rename(columns={
        "Sludge Treatment Centre (STC) name": 'Site Name',
        "STC location (grid ref latitude)": 'Latitide',
        "STC location (grid ref longitude)": 'Longitude',
        "End product volume per year": 'Sludge production'},
        inplace=True)
    df_STC['Type'] = 'STC'
    df = pd.concat([df_small, df_WwTW], join="inner")
    df = pd.concat([df, df_STC], join="outer")
    df['Company_Type'] = df.Company + ': ' + df.Type
    df.reset_index(inplace=True, drop=True)
    df['Type of site'].fillna(value='Wastewater Treatment Works', inplace=True)
    df.to_csv('Outputs/bioresources_market_information_Concat.csv')

def csv_to_sql_converter(csv_path, table_name):
    import sqlite3
    conn = sqlite3.connect(r'Outputs\bioresources.db')
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=conn, if_exists='replace', index=False)
