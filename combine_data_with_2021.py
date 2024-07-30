import pandas as pd
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler


site_names = ['simiValley', 'reseda', 'northHollywood', 'westLA', 'mainLA', 'Pasadena', 'picoRivera', 'compton']
met_vars = ['prcp', 'srad', 'tmax', 'vp']
data_dict = {}
data_dict21 = {}
for n in site_names:
    data_dict[n] = []
    for m in met_vars:
        tba = gpd.read_file('./CA22daymet/' + n + '/Daymet_' + m + '_2022_' + n + '.csv')[['date', 'lat', 'long', m]]
        tba['locationName'] = n
        data_dict[n].append(tba)
    data_dict[n].append(gpd.read_file('./ca_ozone_2022/' + n + '.csv')[['date', 'lat', 'long', 'mean_ozone']])
for val in data_dict:
    #print(val, 'is the location name')
    ndvi_df = gpd.read_file('./CA_NDVI22/NDVI_2022_' + val + '.csv')
    data_dict[val] = data_dict[val][0].merge(data_dict[val][1].merge(data_dict[val][2].merge(data_dict[val][3].merge(data_dict[val][4].merge(ndvi_df)))))
## DOWNLOAD EPA 2021 DATA BEFORE YOU RUN [x]
## ALSO DOWNLOAD NDVI DATA2 [x]
for n in site_names:
    data_dict21[n] = []
    for m in met_vars:
        tba = gpd.read_file('./CA21daymet/outfiles' + '/Daymet_' + m + '_2021_' + n + '.csv')[['date', 'lat', 'long', m]]
        tba['locationName'] = n
        data_dict21[n].append(tba)
    data_dict21[n].append(gpd.read_file('./ca_ozone_2021/' + n + '.csv')[['date', 'lat', 'long', 'mean_ozone']])
for val in data_dict21:
    #print(val, 'is the location name')
    ndvi_df = gpd.read_file('./CA_NDVI21/NDVI_2021_' + val + '.csv')
    data_dict21[val] = data_dict21[val][0].merge(data_dict21[val][1].merge(data_dict21[val][2].merge(data_dict21[val][3].merge(data_dict21[val][4].merge(ndvi_df)))))

dfs_arr = []
dfs_arr21 = []
for v in data_dict:
    #print(v, "is the location name")
    data_dict[v][['lat', 'long', 'prcp', 'srad', 'tmax', 'vp', 'mean_ozone', 'ndvi']] = data_dict[v][['lat', 'long', 'prcp', 'srad', 'tmax', 'vp', 'mean_ozone', 'ndvi']].apply(pd.to_numeric)
    data_dict[v][['date']] = data_dict[v][['date']].apply(pd.to_datetime)
    # print(data_dict[v].head())
    dfs_arr.append(data_dict[v])

# actual analysis

full_dataset = pd.concat(dfs_arr)

for v in data_dict21:
    #print(v, "is the location name")
    data_dict21[v][['lat', 'long', 'prcp', 'srad', 'tmax', 'vp', 'mean_ozone', 'ndvi']] = data_dict21[v][['lat', 'long', 'prcp', 'srad', 'tmax', 'vp', 'mean_ozone', 'ndvi']].apply(pd.to_numeric)
    data_dict21[v][['date']] = data_dict21[v][['date']].apply(pd.to_datetime)
    # print(data_dict[v].head())
    dfs_arr21.append(data_dict21[v])

full_dataset21 = pd.concat(dfs_arr21)

full_dataset = pd.concat([full_dataset, full_dataset21])

final_dataset = full_dataset.sample(frac=1)

print(final_dataset.head())
print(len(final_dataset))


final_dataset.to_csv('final_dataset.csv')
'''
data_dict = {
    'simiValley': [PRCP_DF, SRAD_DF, TMAX_DF, VP_DF, NDVI_DF],
    'reseda': [PRCP_DF, SRAD_DF, TMAX_DF, VP_DF, NDVI_DF]
    ...
    'compton': [PRCP_DF, SRAD_DF, TMAX_DF, VP_DF, NDVI_DF]
}
'''

