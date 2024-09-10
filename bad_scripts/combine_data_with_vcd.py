import pandas as pd
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from bad_scripts.vcd import vcd_dict
from add_vcd import aggregated_data


site_names = ['simiValley', 'reseda', 'northHollywood', 'westLA', 'mainLA', 'Pasadena', 'picoRivera', 'compton']
met_vars = ['prcp', 'srad', 'tmax', 'vp']
data_dict = {}
for n in site_names:
    # for each of the 8 points:
    data_dict[n] = []
    for m in met_vars:
        # read meterological variables
        tba = gpd.read_file('./CA22daymet/' + n + '/Daymet_' + m + '_2022_' + n + '.csv')[['date', 'lat', 'long', m]]
        # add location column
        tba['locationName'] = n
        # cast data types
        tba[['lat', 'long', m]] = tba[['lat', 'long', m]].apply(pd.to_numeric)
        tba[['date']] = tba[['date']].apply(pd.to_datetime)
        data_dict[n].append(tba)
    data_dict[n].append(gpd.read_file('./ca_ozone_2022/' + n + '.csv')[['date', 'lat', 'long', 'mean_ozone']])
for val in data_dict:
    ## print(val, 'is the location name')
    ndvi_df = gpd.read_file('./CA_NDVI22/NDVI_2022_' + val + '.csv')
    ndvi_df[['lat', 'long', 'ndvi']] = ndvi_df[['lat', 'long', 'ndvi']].apply(pd.to_numeric)
    ndvi_df = ndvi_df.reset_index()
    ndvi_df[['date']] = ndvi_df[['date']].apply(pd.to_datetime)
    print("NDVI DTYPES ARE:")
    
    data_dict[val] = data_dict[val][0].merge(data_dict[val][1].merge(data_dict[val][2].merge(data_dict[val][3].merge(data_dict[val][4].merge(ndvi_df)))))
dfs_arr = []
for v in data_dict:
    ## print(v, "is the location name")
    data_dict[v][['lat', 'long', 'prcp', 'srad', 'tmax', 'vp', 'mean_ozone', 'ndvi']] = data_dict[v][['lat', 'long', 'prcp', 'srad', 'tmax', 'vp', 'mean_ozone', 'ndvi']].apply(pd.to_numeric)
    data_dict[v][['date']] = data_dict[v][['date']].apply(pd.to_datetime)
    # # print(data_dict[v].head())
    dfs_arr.append(data_dict[v])

# actual analysis

full_dataset = pd.concat(dfs_arr)

final_dataset = full_dataset.sample(frac=1)
print("AGGREGATED DATA:")
print(aggregated_data.dtypes)
final_dataset = pd.merge(final_dataset, aggregated_data)

# print(final_dataset.head())

'''
data_dict = {
    'simiValley': [PRCP_DF, SRAD_DF, TMAX_DF, VP_DF, NDVI_DF, O3_DF],
    'reseda': [PRCP_DF, SRAD_DF, TMAX_DF, VP_DF, NDVI_DF, O3_DF]
    ...
    'compton': [PRCP_DF, SRAD_DF, TMAX_DF, VP_DF, NDVI_DF]
}
'''

