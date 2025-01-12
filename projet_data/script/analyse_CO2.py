import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('../data/nombre_vehicules_electriques2.csv', sep=';', encoding='utf-8')


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


plt.figure(figsize=(12, 8))
plt.bar(df_aggregated['Département'], df_aggregated['Emissions_Evitees_kg'], color='green')
plt.xlabel('Département')
plt.ylabel('Émissions de CO₂ évitées (kg)')
plt.title('Émissions de CO₂ évitées par Département grâce aux Véhicules Électriques')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

