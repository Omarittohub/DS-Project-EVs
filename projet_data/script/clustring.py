import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


df = pd.read_csv('../data/nombre_vehicules_electriques2.csv', sep=';', encoding='utf-8')


df['Département'] = df['CODGEO'].astype(str).str[:2]
df_aggregated = df.groupby('Département')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()
df_aggregated.columns = ['Département', 'Nombre_Voitures']


km_annuel = 12000
co2_thermique = 120
co2_electrique = 20
df_aggregated['Emissions_Evitees_kg'] = (
    df_aggregated['Nombre_Voitures'] * km_annuel * (co2_thermique - co2_electrique) / 1000
)


scaler = StandardScaler()
features = df_aggregated[['Nombre_Voitures', 'Emissions_Evitees_kg']]
features_scaled = scaler.fit_transform(features)


kmeans = KMeans(n_clusters=4, random_state=42)  # 4 clusters par exemple
df_aggregated['Cluster'] = kmeans.fit_predict(features_scaled)


plt.figure(figsize=(10, 6))
plt.scatter(
    df_aggregated['Nombre_Voitures'],
    df_aggregated['Emissions_Evitees_kg'],
    c=df_aggregated['Cluster'],
    cmap='viridis',
    s=100,
    alpha=0.7
)
plt.title('Clustering des départements : Véhicules et émissions évitées')
plt.xlabel('Nombre de véhicules électriques')
plt.ylabel('Émissions de CO₂ évitées (kg)')
plt.colorbar(label='Cluster')
plt.tight_layout()
plt.show()
