import pandas as pd
import folium
from folium.plugins import HeatMap
import unicodedata

# Charger les données des villes avec les coordonnées
cities_path = './cities.csv'  # Chemin du fichier contenant les coordonnées des villes
cities_data = pd.read_csv(cities_path)

# Charger les données des voitures par commune
car_data_path = './voitures-par-commune-par-energie.csv'  # Fichier des données des véhicules rechargeables par commune
car_data = pd.read_csv(car_data_path, sep=';')

# Fonction pour normaliser les noms des communes (supprimer les caractères spéciaux et mettre en majuscule)
def normalize_text(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')  # Normalisation
    text = text.upper()  # Mettre en majuscule
    text = text.replace('-', ' ')  # Remplacer les tirets par des espaces
    return text

# Appliquer la normalisation aux deux fichiers
cities_data['label'] = cities_data['label'].apply(normalize_text)
car_data['LIBGEO'] = car_data['LIBGEO'].apply(normalize_text)

# Regrouper les données par département (ex: par CODGEO ou en fonction du nom de département dans LIBGEO)
car_totals_by_dept = car_data.groupby('LIBGEO', as_index=False)['NB_VP_RECHARGEABLES_EL'].sum()

# Fusionner avec les coordonnées des villes
merged_data = pd.merge(cities_data, car_totals_by_dept, left_on='label', right_on='LIBGEO', how='inner')

# Filtrer les lignes où il manque des valeurs de latitude ou longitude
merged_data = merged_data.dropna(subset=['latitude', 'longitude'])

# Normaliser les données avec un facteur log
import numpy as np

merged_data['log_cars'] = np.log(merged_data['NB_VP_RECHARGEABLES_EL'] + 1)  # Utilisation de la fonction log
max_cars_log = merged_data['log_cars'].max()
min_cars_log = merged_data['log_cars'].min()
merged_data['normalized_cars'] = (merged_data['log_cars'] - min_cars_log) / (max_cars_log - min_cars_log)

# Créer la carte
start_location = [46.603354, 1.888334]  # Centre de la France
map_ = folium.Map(location=start_location, zoom_start=6)

# Préparer les données pour la heatmap
heatmap_data = [
    (row['latitude'], row['longitude'], row['normalized_cars'])
    for _, row in merged_data.iterrows()
]

# Définir un dégradé à 5 niveaux de couleur avec un contraste plus marqué
gradient = {
    0.0: 'blue',        # Très faible (moins de véhicules)
    0.2: 'lightblue',   # Faible
    0.4: 'yellow',      # Moyen
    0.6: 'orange',      # Élevé
    1.0: 'red'          # Très élevé (plus de véhicules)
}

HeatMap(
    heatmap_data,
    gradient=gradient,
    radius=15,
    blur=10,
    max_zoom=1
).add_to(map_)

# Ajouter une légende
legend_html = """
<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 300px;
    height: 180px;
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    font-size: 14px;
    padding: 10px;
    ">
    <b>Légende de la Carte Thermique</b><br>
    <i style="background: blue; width: 20px; height: 20px; display: inline-block;"></i> Très faible<br>
    <i style="background: lightblue; width: 20px; height: 20px; display: inline-block;"></i> Faible<br>
    <i style="background: yellow; width: 20px; height: 20px; display: inline-block;"></i> Moyen<br>
    <i style="background: orange; width: 20px; height: 20px; display: inline-block;"></i> Élevé<br>
    <i style="background: red; width: 20px; height: 20px; display: inline-block;"></i> Très élevé<br>
</div>
"""
map_.get_root().html.add_child(folium.Element(legend_html))

# Enregistrer la carte
map_.save('carte_thermique_voitures_par_departement.html')
print("Carte thermique des véhicules électriques par département enregistrée dans 'carte_thermique_voitures_par_departement.html'")
