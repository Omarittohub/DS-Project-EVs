import pandas as pd
import folium
from folium.plugins import HeatMap

# Charger le fichier Excel contenant les données de revenus
file_path = './BASE_TD_FILO_DEC_IRIS_2018.csv'  # Remplacez par le chemin de votre fichier
data = pd.read_csv(file_path)

# Vérifier que les colonnes nécessaires existent
if 'LIBCOM' in data.columns and 'DEC_MED18' in data.columns:
    # Mettre les noms des villes en majuscules dans le fichier des revenus
    data['LIBCOM'] = data['LIBCOM'].str.upper()

    # Calculer la moyenne des médianes pour chaque ville
    grouped_data = data.groupby('LIBCOM', as_index=False)['DEC_MED18'].mean()

    # Charger les coordonnées géographiques des villes
    coords_path = './cities.csv'  # Chemin du fichier avec les coordonnées
    coords_data = pd.read_csv(coords_path)

    # Vérifier que les colonnes nécessaires existent dans le fichier des coordonnées
    if 'label' in coords_data.columns and 'latitude' in coords_data.columns and 'longitude' in coords_data.columns:
        # Mettre les noms des villes en majuscules dans le fichier des coordonnées
        coords_data['label'] = coords_data['label'].str.upper()

        # Fusionner les données de revenus avec les coordonnées
        merged_data = pd.merge(grouped_data, coords_data, left_on='LIBCOM', right_on='label', how='inner')

        # Normaliser les médianes des revenus pour les intégrer à la carte thermique
        max_revenue = merged_data['DEC_MED18'].max()
        min_revenue = merged_data['DEC_MED18'].min()
        merged_data['normalized_revenue'] = (merged_data['DEC_MED18'] - min_revenue) / (max_revenue - min_revenue)

        # Créer la carte
        start_location = [46.603354, 1.888334]  # Coordonnées approximatives du centre de la France
        map_ = folium.Map(location=start_location, zoom_start=6)

        # Ajouter les points avec un dégradé à 5 couleurs
        heatmap_data = [
            (row['latitude'], row['longitude'], row['normalized_revenue'])
            for _, row in merged_data.iterrows()
        ]

        # Définir un dégradé à 5 couleurs
        gradient = {
            0.0: 'red',      # Bas revenu
            0.25: 'orange',  # Revenu moyen-bas
            0.5: 'yellow',   # Revenu moyen
            0.75: 'lightgreen',  # Revenu moyen-élevé
            1.0: 'green'     # Haut revenu
        }

        HeatMap(
            heatmap_data,
            gradient=gradient,
            radius=15,
            blur=10,
            max_zoom=1
        ).add_to(map_)

        # Ajouter une légende pour la carte
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
            <i style="background: red; width: 20px; height: 20px; display: inline-block;"></i> Bas revenu<br>
            <i style="background: orange; width: 20px; height: 20px; display: inline-block;"></i> Revenu moyen-bas<br>
            <i style="background: yellow; width: 20px; height: 20px; display: inline-block;"></i> Revenu moyen<br>
            <i style="background: lightgreen; width: 20px; height: 20px; display: inline-block;"></i> Revenu moyen-élevé<br>
            <i style="background: green; width: 20px; height: 20px; display: inline-block;"></i> Haut revenu<br>
        </div>
        """
        map_.get_root().html.add_child(folium.Element(legend_html))

        # Enregistrer la carte
        map_.save('carte_thermique_revenus.html')
        print("Carte des revenus médianes enregistrée dans 'carte_thermique_revenus.html'")
    else:
        print("Les colonnes nécessaires ('label', 'latitude', 'longitude') sont introuvables dans le fichier des coordonnées.")
else:
    print("Les colonnes nécessaires ('LIBCOM', 'DEC_MED18') sont introuvables dans le fichier des revenus.")
