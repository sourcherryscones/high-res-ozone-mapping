import pandas as pd

site_ids = ['06-111-2002', '06-037-1201', '06-037-4010', '06-037-0113', '06-037-1103','06-037-2005', '06-037-1602', '06-037-1302']
site_names = ['simiValley', 'reseda', 'northHollywood', 'westLA', 'mainLA', 'Pasadena', 'picoRivera', 'compton']

for i in range(0,len(site_ids)):
    epa_point_ts = pd.read_csv('https://www3.epa.gov/cgi-bin/broker?_service=data&_program=dataprog.Daily.sas&check=void&polname=Ozone&debug=0&year=2021&site=' + site_ids[i])
    ozone_data = epa_point_ts.loc[epa_point_ts['Parameter Name'] == "Ozone"][['Date (Local)', 'Latitude', 'Longitude', 'Parameter Name', 'Arithmetic Mean']]
    ozone_data = ozone_data.rename(columns={'Arithmetic Mean':'mean_ozone', 'Latitude': 'lat', 'Longitude': 'long', 'Date (Local)': 'date'})
    ozone_data = ozone_data.drop_duplicates(subset=['date'])
    ozone_data.to_csv('./ca_ozone_2021/'+site_names[i]+'.csv')
    
# change '&year=' parameter to 2022 to get 2022's data!