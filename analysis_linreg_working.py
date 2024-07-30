import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# models to try: linear regression, RF regression(sklearn.ensemble.RandomForestRegressor), 
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from combine_data import final_dataset


final_dataset = final_dataset.dropna(subset=['ndvi'])
print(final_dataset.head())


useful_predictors = ['srad', 'tmax', 'vp','prcp', 'ndvi']
for c in useful_predictors:
    final_dataset.plot(x=c, y='mean_ozone', style='o')

plt.show()
    #final_dataset.plot(x='date', y='mean_ozone', secondary_y=c)

corr_matrix = final_dataset[useful_predictors].corr()
print(corr_matrix)


X = final_dataset[['srad', 'tmax', 'vp', 'ndvi']]
y = final_dataset[['mean_ozone']]

X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.2, random_state=42)

sc = MinMaxScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

linreg = LinearRegression()

linreg.fit(X_train, y_train)

y_preds = linreg.predict(X_test)

print(y_preds[:10])
print(y_test[:10])
print("LINREG STATS ======================================================================================")
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_preds))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_preds))
print('RMSE Squared Error:', metrics.root_mean_squared_error(y_test, y_preds))
print('R^2 value:', metrics.r2_score(y_test, y_preds))

# Print the coefficients and intercept
print('Coefficients:', linreg.coef_)
print('Intercept:', linreg.intercept_)
