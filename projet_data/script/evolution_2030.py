import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


df = pd.read_csv('../data/nombre_vehicules_electriques2.csv', sep=';', encoding='utf-8')

df_temporal = df[['DATE_ARRETE', 'NB_VP_RECHARGEABLES_EL']].copy()
df_temporal['DATE_ARRETE'] = pd.to_datetime(df_temporal['DATE_ARRETE'])
df_temporal['Année'] = df_temporal['DATE_ARRETE'].dt.year


df_yearly = df_temporal.groupby('Année').sum().reset_index()


X = df_yearly[['Année']].values
y = df_yearly['NB_VP_RECHARGEABLES_EL'].values


poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)


années_futures = np.arange(X.min(), 2031).reshape(-1, 1)
années_futures_poly = poly.transform(années_futures)
predictions = model.predict(années_futures_poly)


plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', label='Données réelles')
plt.plot(années_futures, predictions, color='red', label='Prédictions (2030)')
plt.xlabel('Année')
plt.ylabel('Nombre de véhicules électriques')
plt.title('Évolution du nombre de véhicules électriques jusqu’en 2030')
plt.legend()
plt.tight_layout()
plt.show()
