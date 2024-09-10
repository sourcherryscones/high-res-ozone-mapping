import pandas as pd
import geopandas as gpd

# takes all local GEE-downloaded and EPA daily data and combines it into a single Pandas dataframe

site_names = ['simiValley', 'reseda', 'northHollywood', 'westLA', 'mainLA', 'Pasadena', 'picoRivera', 'compton']
met_vars = ['prcp', 'srad', 'tmax', 'vp']
data_dict = {}
for n in site_names:
    data_dict[n] = []
    for m in met_vars:
        tba = gpd.read_file('./CA22daymet/' + n + '/Daymet_' + m + '_2022_' + n + '.csv')[['date', 'lat', 'long', m]]
        tba['locationName'] = n
        data_dict[n].append(tba)
    data_dict[n].append(gpd.read_file('./ca_ozone_2022/' + n + '.csv')[['date', 'lat', 'long', 'mean_ozone']])
for val in data_dict:
    ndvi_df = gpd.read_file('./CA_NDVI22/NDVI_2022_' + val + '.csv')
    data_dict[val] = data_dict[val][0].merge(data_dict[val][1].merge(data_dict[val][2].merge(data_dict[val][3].merge(data_dict[val][4].merge(ndvi_df)))))

dfs_arr = []
for v in data_dict:
    data_dict[v][['lat', 'long', 'prcp', 'srad', 'tmax', 'vp', 'mean_ozone', 'ndvi']] = data_dict[v][['lat', 'long', 'prcp', 'srad', 'tmax', 'vp', 'mean_ozone', 'ndvi']].apply(pd.to_numeric)
    data_dict[v][['date']] = data_dict[v][['date']].apply(pd.to_datetime)
    dfs_arr.append(data_dict[v])

full_dataset = pd.concat(dfs_arr)

final_dataset = full_dataset.sample(frac=1)

print(final_dataset.head())

# save to local file 'final_dataset.csv'

final_dataset.to_csv('final_dataset.csv')

