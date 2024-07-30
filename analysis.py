import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
# models to try: linear regression, RF regression(sklearn.ensemble.RandomForestRegressor), 
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from add_vcd_with_vocs import fd as final_dataset


final_dataset = final_dataset.dropna(subset=['ndvi'])


useful_predictors = ['srad', 'tmax', 'vp','prcp', 'ndvi', 'vcd', 'mean_ozone', 'no2vcd', 'covcd', 'hchovcd']
#final_dataset.plot(x='vcd', y='mean_ozone', style='o')
    #final_dataset.plot(x='date', y='mean_ozone', secondary_y=c)
#plt.show()
corr_matrix = final_dataset[useful_predictors].corr()
print("CORRELATION MATRIX:")
print(corr_matrix)

sbd = final_dataset.sort_values('date')
print(sbd.sort_values('date'))
sbd.plot(x='date', y='mean_ozone')
plt.ylim(0,0.2)
sbd.plot(x='date', y='vcd')
plt.ylim(0,0.2)
plt.show()

X = final_dataset[['srad', 'tmax', 'vp', 'ndvi', 'vcd', 'prcp','no2vcd', 'covcd', 'hchovcd']]
y = final_dataset[['mean_ozone']]

print("DATASET LENGTH IS", len(X))

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

rfregr = RandomForestRegressor(max_depth=7, random_state=0)
rfregr.fit(X_train, y_train)
rf_y_preds = rfregr.predict(X_test)
print("RFREG STATS ======================================================================================")
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, rf_y_preds))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, rf_y_preds))
print('RMSE Squared Error:', metrics.root_mean_squared_error(y_test, rf_y_preds))