import pandas as pd
import plotly.express as px
import os

def check_file_exists(filepath):
    if not os.path.isfile(filepath):
        print(f"Erreur : Le fichier {filepath} est introuvable.")
        exit()

def check_columns_exist(df, required_columns):
    for col in required_columns:
        if col not in df.columns:
            print(f"Erreur : La colonne {col} est introuvable dans le fichier.")
            exit()

# Check if files exist
population_file = r"C:\Users\omari\Documents\GitHub\DS-Project-EVs\projet_data\data\population_par_departement2.csv"
vehicles_file = r"C:\Users\omari\Documents\GitHub\DS-Project-EVs\projet_data\data\nombre_vehicules_electriques2.csv"
check_file_exists(population_file)
check_file_exists(vehicles_file)

try:
    df_population = pd.read_csv(population_file, sep=';', encoding='utf-8', dtype={'GEO': str, 'SEX': str, 'AGE': str, 'OBS_VALUE': float})
    print("Colonnes détectées dans le fichier population :", df_population.columns)
    check_columns_exist(df_population, ['GEO', 'SEX', 'AGE', 'OBS_VALUE'])

    # Filtrer pour les totaux ('_T') et les âges 15 ans et plus ('Y_GE15')
    df_population = df_population[(df_population['SEX'] == '_T') & (df_population['AGE'] == 'Y_GE15')]

    df_population['Département'] = df_population['GEO'].astype(str).str[:2]

    df_population = df_population.groupby('Département')['OBS_VALUE'].sum().reset_index()
    df_population.columns = ['Département', 'Population']
except Exception as e:
    print("Erreur lors du traitement des données de population :", e)
    exit()

try:
    df_vehicles = pd.read_csv(vehicles_file, sep=';', encoding='utf-8', dtype={'CODGEO': str, 'NB_VP_RECHARGEABLES_EL': float})
    check_columns_exist(df_vehicles, ['CODGEO', 'NB_VP_RECHARGEABLES_EL'])
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
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

fig_ve = px.bar(df_final, x='Département', y='VE_par_habitant', title='Ratio : Véhicules électriques par habitant',
                labels={'VE_par_habitant': 'VE par habitant', 'Département': 'Département'},
                color='Département', color_discrete_sequence=px.colors.qualitative.Pastel)
output_file_ve = os.path.join(output_dir, "graphe_ve_par_habitant.html")
fig_ve.write_html(output_file_ve)
print(f"Graphique 'VE par habitant' enregistré dans {output_file_ve}")

fig_co2 = px.bar(df_final, x='Département', y='CO2_evite_par_habitant', title='Ratio : CO₂ évité par habitant',
                 labels={'CO2_evite_par_habitant': 'CO₂ évité par habitant (kg)', 'Département': 'Département'},
                 color='Département', color_discrete_sequence=px.colors.qualitative.Vivid)
output_file_co2 = os.path.join(output_dir, "graphe_co2_evite_par_habitant.html")
fig_co2.write_html(output_file_co2)
print(f"Graphique 'CO₂ évité par habitant' enregistré dans {output_file_co2}")
