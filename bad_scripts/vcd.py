import pandas as pd
site_names = ['simiValley', 'reseda', 'northHollywood', 'westLA', 'mainLA', 'Pasadena', 'picoRivera', 'compton']

vcd_dict = {}

for site in site_names:
    trop_jan = pd.read_csv('./tropomi_data_biennial/TROPOMI_2022_jan_jun_' + site + '.csv')
    trop_jan = trop_jan.dropna()
    trop_jul = pd.read_csv('./tropomi_data_biennial/TROPOMI_2022_jul_dec_' + site + '.csv')
    trop_jul = trop_jul.dropna()
    year_df = pd.concat([trop_jan, trop_jul])
    # # print(year_df.head())
    # # print(year_df.tail())
    # # print(len(year_df))
    year_df[['lat', 'long', 'vcd']] = year_df[['lat', 'long', 'vcd']].apply(pd.to_numeric)
    year_df[['date']] = year_df[['date']].apply(pd.to_datetime)
    meaned_df = year_df[['date', 'vcd']].groupby('date').mean() # 
    meaned_df.reset_index('date')
    # print("HEAD OF ONLY 2 COLUMN MEANED DF")
    # print(meaned_df.dtypes)
    # print(meaned_df.head(15))
    '''
    # # print("FIRST OF YEAR DF COMPTON")
    # # print(year_df.iloc[0]['lat'])
    meaned_df['lat'] = year_df.iloc[0]['lat']
    meaned_df['long'] = year_df.iloc[0]['long']
    # print(meaned_df.head(15))
    # print(meaned_df.dtypes)
    vcd_dict[site] = meaned_df

vcd_dict = {
    'simiValley': pd.Dataframe(date, lat, lon, vcd),
    'reseda': ...

}
'''
# # print(vcd_dict)
# for jan 2: 0.126717
# for jan 7: 0.1255655
# for jan 13: 0.1142585
