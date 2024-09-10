import pandas as pd

fdataset = pd.read_csv('final_dataset.csv')
fdataset[['date']] = fdataset[['date']].apply(pd.to_datetime)
# # print(fdataset.dtypes)

site_names = ['simiValley', 'reseda', 'northHollywood', 'westLA', 'mainLA', 'Pasadena', 'picoRivera', 'compton']
compound_names = ['TROPOMI', 'no2', 'hcho', 'co']
# ./no2_data_biennial/ should contain ALL NO2 DATA, BOTH 2021 AND 2022 TOGETHER SAME LEVEL
# same with hcho and co!
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

compcolumns = {
    'TROPOMI':'vcd',
    'no2': 'no2vcd',
    'hcho': 'hchovcd',
    'co': 'covcd'
}

for site in site_names:
    for c in compound_names:
        # MAKE SURE TO STORE HCHO/NO2 IN FORMAT '[compound_name]_data_biennial'
        trop_jan = pd.read_csv('./'+ c + '_data_biennial/' + c + '_2022_jan_jun_' + site + '.csv')
        trop_jan = trop_jan.dropna()
        trop_jan['locationName'] = site
        trop_jan['timeframe'] = 'janjun'
        trop_jul = pd.read_csv('./'+c+'_data_biennial/' + c + '_2022_jul_dec_' + site + '.csv')
        trop_jul = trop_jul.dropna()
        trop_jul['locationName'] = site
        trop_jul['timeframe'] = 'juldec'

        # 2021 time!

        jan21 = pd.read_csv('./'+ c +'_data_biennial/'+ c +'_2021_jan_jun_' + site + '.csv')
        jan21 = jan21.dropna()
        jan21['locationName'] = site
        jan21['timeframe'] = 'janjun'
        jul21 = pd.read_csv('./' + c + '_data_biennial/' + c + '_2021_jul_dec_' + site + '.csv')
        jul21 = jul21.dropna()
        jul21['locationName'] = site
        jul21['timeframe'] = 'juldec'

        year_df = pd.concat([trop_jan, trop_jul, jan21, jul21])
        year_df[['lat', 'long', str(compcolumns[c])]] = year_df[['lat', 'long', str(compcolumns[c])]].apply(pd.to_numeric)
        year_df[['date']] = year_df[['date']].apply(pd.to_datetime)
        #
        tbconcatted[c].append(year_df)

    # sort by column
    # add column for sourec location

for comp in compound_names:
    tbconcatted[comp] = pd.concat(tbconcatted[comp])

# for compound in compound_names:
    #print(tbconcatted[compound].head())

all_compound_dfs = []
for com in compound_names:
    all_compound_dfs.append(tbconcatted[com])

final_vocs_df = pd.concat(all_compound_dfs)

final_vocs_df = final_vocs_df.sample(frac=1)

# print(final_vocs_df.head())
# so rn we have some overlapping values, but we've got all the data for 2021 AND 2022 in one huge yes-duplicates dataframe


sorteddf = final_vocs_df.sort_values(by='date')
# # print(sorteddf.head(15))
# # print("SORTED DF")
# # print(sorteddf.dtypes)

aggregated_data = sorteddf[['date', 'vcd', 'no2vcd', 'hchovcd', 'covcd']].groupby('date', as_index=False).mean()
# ^^ gets rid of duplicates!

# # print(aggregated_data.head(40))

fd = pd.merge(fdataset, aggregated_data)

fd = fd.dropna()

fd = fd.sample(frac=1)

fd.to_csv('final_dataset_with_vocs.py')

# print(fd.sort_values('date').head(20))

# print(len(fd))

# print(fd[fd.isna().any(axis=1)])
