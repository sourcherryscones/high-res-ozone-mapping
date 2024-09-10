import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
# models to try: linear regression, RF regression(sklearn.ensemble.RandomForestRegressor), 
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from shapely.geometry import Point
from add_vcd_with_vocs import fd as final_dataset
import xgboost


final_dataset = final_dataset.dropna(subset=['ndvi'])


useful_predictors = ['srad', 'tmax', 'vp','prcp', 'ndvi', 'vcd', 'mean_ozone', 'no2vcd', 'covcd', 'hchovcd']
#final_dataset.plot(x='vcd', y='mean_ozone', style='o')
    #final_dataset.plot(x='date', y='mean_ozone', secondary_y=c)
#plt.show()
corr_matrix = final_dataset[useful_predictors].corr()
# print("CORRELATION MATRIX:")
# print(corr_matrix)

sbd = final_dataset.sort_values('date')
# print(sbd.sort_values('date'))
sbd.plot(x='date', y='mean_ozone')
plt.ylim(0,0.2)
sbd.plot(x='date', y='vcd')
plt.ylim(0,0.2)
# plt.show()

X = final_dataset[['srad', 'tmax', 'vp', 'ndvi', 'vcd', 'prcp','no2vcd', 'covcd', 'hchovcd']]
y = final_dataset[['mean_ozone']]

print("DATASET LENGTH IS", len(X))

X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.2, random_state=42)

# print("X TRAIN HEAD")
# print(X_train.head())

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

rfregr = RandomForestRegressor(max_depth=7, random_state=0)
rfregr.fit(X_train, y_train)
rf_y_preds = rfregr.predict(X_test)
print("RFREG STATS ======================================================================================")
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, rf_y_preds))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, rf_y_preds))
print('RMSE Squared Error:', metrics.root_mean_squared_error(y_test, rf_y_preds))



mlpreg = MLPRegressor(solver='lbfgs', max_iter=2000, hidden_layer_sizes=(10,20,15))
mlpreg.fit(X_train, y_train)
mlp_y_preds = mlpreg.predict(X_test)
print("MLPREG STATS ======================================================================================")
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, mlp_y_preds))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, mlp_y_preds))
print('RMSE Squared Error:', metrics.root_mean_squared_error(y_test, mlp_y_preds))


xgbreg = xgboost.XGBRegressor(n_estimators=1000, max_depth=7, eta=0.1,subsample=1.0)
xgbreg.fit(X_train, y_train)
xgbreg_preds = xgbreg.predict(X_test)
print("MLPREG STATS ======================================================================================")
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, xgbreg_preds))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, xgbreg_preds))
print('RMSE Squared Error:', metrics.root_mean_squared_error(y_test, xgbreg_preds))
print('R^2 value:', metrics.r2_score(y_test, xgbreg_preds))

'''
(3,4,4,3) yielded ~0.008
(3,4,5,3) was same
(10,10,10) yielded 0.007
(10,15,10) yielded 0.0068
(10,15,15) yielded 0.006197ish
(10,20,15) yielded 0.00626046
'''

# WARNING: DEFINE tmodel AS ONE OF THE TRAINED MODELS ABOVE BEFORE YOU RUN!!

final_socal_dataset = pd.read_csv('../ozone_test/final_socal_dataset.csv')

final_socal_dataset = final_socal_dataset.apply(pd.to_numeric)

final_socal_dataset['rf_predval'] = rfregr.predict(final_socal_dataset[['srad', 'tmax', 'vp', 'NDVI', 'O3_column_number_density', 'prcp',\
                                                                             'tropospheric_NO2_column_number_density', 'CO_column_number_density',\
                                                                                'tropospheric_HCHO_column_number_density']])

# Make predictions for each row in the dataframe
final_socal_dataset['predicted_value'] = xgbreg.predict(final_socal_dataset[['srad', 'tmax', 'vp', 'NDVI', 'O3_column_number_density', 'prcp',\
                                                                             'tropospheric_NO2_column_number_density', 'CO_column_number_density',\
                                                                                'tropospheric_HCHO_column_number_density']])

# Save the updated dataframe to a new CSV file
final_socal_dataset.to_csv('output_data_with_predictions.csv', index=False)

# Print the updated dataframe
print(final_socal_dataset.head())