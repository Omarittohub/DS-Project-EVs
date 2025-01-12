import pandas as pd
import matplotlib.pyplot as plt


data_dir = "../data/"
population_file = data_dir + "population_par_departement2.csv"
vehicles_file = data_dir + "nombre_vehicules_electriques2.csv"


try:
    df_population = pd.read_csv(population_file, sep=';', encoding='utf-8')
    print("Colonnes détectées dans le fichier population :", df_population.columns)

    # Filtrer pour les totaux ('_T') et les âges 15 ans et plus ('Y_GE15')
    df_population = df_population[(df_population['SEX'] == '_T') & (df_population['AGE'] == 'Y_GE15')]


    df_population['Département'] = df_population['GEO'].astype(str).str[:2]


    df_population = df_population.groupby('Département')['OBS_VALUE'].sum().reset_index()
    df_population.columns = ['Département', 'Population']
except Exception as e:
    print("Erreur lors du traitement des données de population :", e)
    exit()


try:
    df_vehicles = pd.read_csv(vehicles_file, sep=';', encoding='utf-8')
    df_vehicles['Département'] = df_vehicles['CODGEO'].astype(str).str[:2]

    # Agréger les données par département
    df_aggregated = df_vehicles.groupby('Département')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()
    df_aggregated.columns = ['Département', 'Nombre_Voitures']
except Exception as e:
    print("Erreur lors du traitement des données de véhicules électriques :", e)
    exit()


try:
    df_final = pd.merge(df_aggregated, df_population, on='Département', how='left')
except Exception as e:
    print("Erreur lors de la fusion des données :", e)
    exit()


km_annuel = 12000
co2_thermique = 120
co2_electrique = 20

df_final['VE_par_habitant'] = df_final['Nombre_Voitures'] / df_final['Population']
df_final['CO2_evite_par_habitant'] = (
    df_final['Nombre_Voitures'] * km_annuel * (co2_thermique - co2_electrique) / 1000
) / df_final['Population']


plt.figure(figsize=(12, 6))
plt.bar(df_final['Département'], df_final['VE_par_habitant'], color='blue', alpha=0.7)
plt.xlabel("Département")
plt.ylabel("VE par habitant")
plt.title("Ratio : Véhicules électriques par habitant")
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()


output_dir = "../output/"
output_file_ve = output_dir + "graphe_ve_par_habitant.png"
plt.savefig(output_file_ve)
print(f"Graphique 'VE par habitant' enregistré dans {output_file_ve}")


plt.show()


plt.figure(figsize=(12, 6))
plt.bar(df_final['Département'], df_final['CO2_evite_par_habitant'], color='orange', alpha=0.7)
plt.xlabel("Département")
plt.ylabel("CO₂ évité par habitant (kg)")
plt.title("Ratio : CO₂ évité par habitant")
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()


output_file_co2 = output_dir + "graphe_co2_evite_par_habitant.png"
plt.savefig(output_file_co2)
print(f"Graphique 'CO₂ évité par habitant' enregistré dans {output_file_co2}")


plt.show()
