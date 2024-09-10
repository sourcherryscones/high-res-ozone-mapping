import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# models to try: linear regression, RF regression(sklearn.ensemble.RandomForestRegressor), 
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from add_vcd_with_2021 import fd as final_dataset


final_dataset = final_dataset.dropna(subset=['ndvi'])


useful_predictors = ['srad', 'tmax', 'vp','prcp', 'ndvi', 'vcd', 'mean_ozone']
#final_dataset.plot(x='vcd', y='mean_ozone', style='o')
    #final_dataset.plot(x='date', y='mean_ozone', secondary_y=c)
#plt.show()
corr_matrix = final_dataset[useful_predictors].corr()
print(corr_matrix)

sbd = final_dataset.sort_values('date')
print(sbd.sort_values('date'))
sbd.plot(x='date', y='mean_ozone')
plt.ylim(0,0.2)
sbd.plot(x='date', y='vcd')
plt.ylim(0,0.2)
plt.show()

X = final_dataset[['srad', 'tmax', 'vp', 'ndvi', 'vcd', 'prcp']]
y = final_dataset[['mean_ozone']]

X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.2, random_state=42)

print("X TRAIN HEAD")
print(X_train.head())

sc = MinMaxScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

linreg = LinearRegression()

linreg.fit(X_train, y_train)

y_preds = linreg.predict(X_test)

print("LINREG STATS ======================================================================================")
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_preds))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_preds))
print('RMSE Squared Error:', metrics.root_mean_squared_error(y_test, y_preds))
print('R^2 value:', metrics.r2_score(y_test, y_preds))

# Print the coefficients and intercept
print('Coefficients:', linreg.coef_)
print('Intercept:', linreg.intercept_)

## NOW WE DO PROCESSING FOR THE NEW MAP :D

ca_daymet23 = pd.read_csv('./all_ca_inputs/full_ca_daymet_inputs.csv')
ca_daymet23[['lat', 'long', 'prcp', 'srad', 'tmax', 'vp']] = ca_daymet23[['lat', 'long', 'prcp', 'srad', 'tmax', 'vp']].apply(pd.to_numeric)
ca_tropomi23 = pd.read_csv('./all_ca_inputs/ca_vcd_ozone_all_inputs_sampled_km.csv')
ca_tropomi23 = ca_tropomi23.rename(columns={'O3_column_number_density': 'vcd'})
ca_tropomi23[['vcd', 'lat', 'long']] = ca_tropomi23[['vcd', 'lat', 'long']].apply(pd.to_numeric)
ca_ndvi23 = pd.read_csv('./all_ca_inputs/ca_ndvi_all_inputs.csv')
ca_ndvi23 = ca_ndvi23.rename(columns={'NDVI': 'ndvi'})
print("CA NDVI23 HEAD")
print(ca_ndvi23.columns)
print(ca_ndvi23.head())
#ca_ndvi23[['ndvi', 'lat', 'long']] = ca_tropomi23[['ndvi', 'lat', 'long']].apply(pd.to_numeric)
print("CA DAYMET")
print(ca_daymet23.sort_values('lat').head())

print("CA TROPOMI")
print(ca_tropomi23.sort_values('lat').head())

print("CA NDVI")
print(ca_ndvi23.sort_values('lat').head())

final_ca_input = ca_daymet23.merge(ca_tropomi23.merge(ca_ndvi23, on='.geo'), on='.geo')

print("FINAL INPUT ================================================================================")
print(final_ca_input.head())
print('='*20)

final_ca_input['estimated_o3'] = linreg.predict(final_ca_input[['srad', 'tmax', 'vp', 'ndvi', 'vcd', 'prcp']])

print(final_ca_input.head())

print(len(final_ca_input))

# Assuming df is your DataFrame and it has columns 'latitude', 'longitude', and 'value'
# Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(final_ca_input, geometry=gpd.points_from_xy(final_ca_input['long'], final_ca_input['lat']))

# Load a map (this example uses a built-in map of the world)
#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot the map
fig, ax = plt.subplots()
# world.plot(ax=ax, color='white', edgecolor='black')
gdf.plot(column='estimated_o3', ax=ax, legend=True)

plt.show()
