import pandas as pd

fdataset = pd.read_csv('final_dataset.csv')
fdataset[['date']] = fdataset[['date']].apply(pd.to_datetime)
# # print(fdataset.dtypes)

site_names = ['simiValley', 'reseda', 'northHollywood', 'westLA', 'mainLA', 'Pasadena', 'picoRivera', 'compton']
compound_names = ['TROPOMI', 'no2', 'hcho']
vcd_arr = []
no2_arr = []
hcho_arr = []
co_arr = []

tbconcatted = {
    'TROPOMI': vcd_arr,
    'no2': no2_arr,
    'hcho': hcho_arr,
    'co': co_arr
}

for site in site_names:
    trop_jan = pd.read_csv('./tropomi_data_biennial/TROPOMI_2022_jan_jun_' + site + '.csv')
    trop_jan = trop_jan.dropna()
    trop_jan['locationName'] = site
    trop_jan['timeframe'] = 'janjun'
    trop_jul = pd.read_csv('./tropomi_data_biennial/TROPOMI_2022_jul_dec_' + site + '.csv')
    trop_jul = trop_jul.dropna()
    trop_jul['locationName'] = site
    trop_jul['timeframe'] = 'juldec'

    # 2021 time!

    jan21 = pd.read_csv('./tropomi_data_biennial/TROPOMI_2021_jan_jun_' + site + '.csv')
    jan21 = jan21.dropna()
    jan21['locationName'] = site
    jan21['timeframe'] = 'janjun'
    jul21 = pd.read_csv('./tropomi_data_biennial/TROPOMI_2021_jul_dec_' + site + '.csv')
    jul21 = jul21.dropna()
    jul21['locationName'] = site
    jul21['timeframe'] = 'juldec'
    print("SIZE OF JAN/JUL21 ARE", len(jan21), len(jul21))

    year_df = pd.concat([trop_jan, trop_jul, jan21, jul21])
    year_df[['lat', 'long', 'vcd']] = year_df[['lat', 'long', 'vcd']].apply(pd.to_numeric)
    year_df[['date']] = year_df[['date']].apply(pd.to_datetime)
    vcd_arr.append(year_df)

    # sort by column
    # add column for sourec location

final_vcd_df = pd.concat(vcd_arr)


sorteddf = final_vcd_df.sort_values(by='date')
# # print(sorteddf.head(15))
# # print("SORTED DF")
# # print(sorteddf.dtypes)

aggregated_data = sorteddf[['date', 'vcd']].groupby('date', as_index=False).mean()
# # print(aggregated_data.head(40))

fd = pd.merge(fdataset, aggregated_data)

fd = fd.dropna()

print(fd.sort_values('date').head(20))

# print(len(fd))

# print(fd[fd.isna().any(axis=1)])