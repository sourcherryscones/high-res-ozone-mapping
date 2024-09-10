import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

tbplotted_df = pd.read_csv('output_data_with_predictions.csv')

tbplotted_df = tbplotted_df.apply(pd.to_numeric)

geometry = [Point(xy) for xy in zip(tbplotted_df['long'], tbplotted_df['lat'])]
gdf = gpd.GeoDataFrame(tbplotted_df, geometry=geometry)

# Plot the GeoDataFrame
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.plot(column='predicted_value', ax=ax, legend=True, cmap='viridis', markersize=2, legend_kwds={'orientation': 'horizontal', 'shrink': 0.7})

# Set plot title and labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Modify the legend to be horizontal

# Show the plot
plt.show()