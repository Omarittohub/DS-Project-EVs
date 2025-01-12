import pandas as pd

import plotly.express as px

df = pd.read_csv(r'C:\Users\omari\Documents\GitHub\DS-Project-EVs\projet_data\data\nombre_vehicules_electriques2.csv', sep=';', encoding='utf-8')

df['Département'] = df['CODGEO'].astype(str).str[:2]

df_aggregated = df.groupby('Département')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()

df_aggregated.columns = ['Département', 'Nombre_Voitures']

km_annuel = 12000  # Kilométrage annuel moyen (km/an)
co2_thermique = 120  # Émissions d'un véhicule thermique (g CO₂/km)
co2_electrique = 20  # Émissions d'un véhicule électrique (g CO₂/km)

df_aggregated['Emissions_Evitees_kg'] = (
    df_aggregated['Nombre_Voitures'] * km_annuel * (co2_thermique - co2_electrique) / 1000
)

print(df_aggregated)

fig = px.bar(df_aggregated, x='Département', y='Emissions_Evitees_kg', 
             labels={'Emissions_Evitees_kg': 'Émissions de CO₂ évitées (kg)', 'Département': 'Département'},
             title='Émissions de CO₂ évitées par Département grâce aux Véhicules Électriques')

fig.update_layout(xaxis={'categoryorder':'total descending'})

fig.write_html('emissions_evitees.html')
fig.show()