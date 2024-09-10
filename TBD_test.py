import pandas as pd


epa_full_data = pd.read_csv('epa_ozone_2024.csv')

ozone_data = epa_full_data.loc[epa_full_data['Parameter Name'] == "Ozone"][['Date (Local)', 'Latitude', 'Longitude', 'Parameter Name', 'Arithmetic Mean']]

print(ozone_data.head())

print(ozone_data.columns)

ozone_data.to_csv('ozone_data.csv')