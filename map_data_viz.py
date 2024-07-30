import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt



ca_daymet = pd.read_csv('./all_ca_inputs/full_ca_daymet_inputs.csv')
# Assuming df is your DataFrame and it has columns 'latitude', 'longitude', and 'value'
# Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(ca_daymet, geometry=gpd.points_from_xy(ca_daymet['long'], ca_daymet['lat']))

# Load a map (this example uses a built-in map of the world)
#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

invars = ['tmax', 'srad', 'prcp', 'vp']

ca_ndvi = pd.read_csv('./all_ca_inputs/ca_ndvi_all_inputs.csv')

vcd = pd.read_csv('./all_ca_inputs/ca_vcd_ozone_all_inputs_sampled_km.csv')
gdf = gpd.GeoDataFrame(vcd, geometry=gpd.points_from_xy(vcd['long'], vcd['lat']))

# Plot the map
fig, ax = plt.subplots()
# world.plot(ax=ax, color='white', edgecolor='black')
gdf.plot(column='O3_column_number_density', ax=ax, legend=True,cmap='magma')

plt.title('Ozone VCD')

plt.show()

