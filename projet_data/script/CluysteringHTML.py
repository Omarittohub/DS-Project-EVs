import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import plotly.express as px

# Charger les données
df = pd.read_csv(r'C:\Users\omari\Documents\GitHub\DS-Project-EVs\projet_data\data\nombre_vehicules_electriques2.csv', sep=';', encoding='utf-8')

# Agréger les données par département
df['Département'] = df['CODGEO'].astype(str).str[:2]
df_aggregated = df.groupby('Département')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()
df_aggregated.columns = ['Département', 'Nombre_Voitures']

# Calculer les émissions évitées
km_annuel = 12000
co2_thermique = 120
co2_electrique = 20
df_aggregated['Emissions_Evitees_kg'] = (
    df_aggregated['Nombre_Voitures'] * km_annuel * (co2_thermique - co2_electrique) / 1000
)

# Standardiser les caractéristiques
scaler = StandardScaler()
features = df_aggregated[['Nombre_Voitures', 'Emissions_Evitees_kg']]
features_scaled = scaler.fit_transform(features)

# Appliquer KMeans
kmeans = KMeans(n_clusters=4, random_state=42)
df_aggregated['Cluster'] = kmeans.fit_predict(features_scaled)

# Créer le graphique avec Plotly
fig = px.scatter(
    df_aggregated,
    x='Nombre_Voitures',
    y='Emissions_Evitees_kg',
    color='Cluster',
    title='Clustering des départements : Véhicules et émissions évitées',
    labels={'Nombre_Voitures': 'Nombre de véhicules électriques', 'Emissions_Evitees_kg': 'Émissions de CO₂ évitées (kg)'},
    template='plotly'
)

# Sauvegarder le graphique en fichier HTML
fig.write_html('clustering_departements.html')