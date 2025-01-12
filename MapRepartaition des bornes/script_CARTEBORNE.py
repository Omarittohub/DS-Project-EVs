import pandas as pd
import folium
from scipy.spatial import KDTree
from folium.plugins import HeatMap

# Charger le fichier CSV
file_path = './consolidation-etalab-schema-irve-statique-v-2.3.1-20241123.csv'
data = pd.read_csv(file_path)

if 'consolidated_longitude' in data.columns and 'consolidated_latitude' in data.columns:
    coords = data[['consolidated_latitude', 'consolidated_longitude']].values

    # Construire un KDTree pour les recherches de proximité
    tree = KDTree(coords)
    threshold = 0.15  # Définir la portée pour regrouper les points

    heatmap_points = []
    visited = set()

    for i, point in enumerate(coords):
        if i not in visited:
            # Trouver les points proches dans le seuil
            indices = tree.query_ball_point(point, threshold)
            visited.update(indices)

            # Regrouper les points et calculer l'intensité
            group = coords[indices]
            avg_lat, avg_lon = group.mean(axis=0)
            intensity = len(indices)  # Nombre de points dans ce groupe
            heatmap_points.append([avg_lat, avg_lon, intensity])

    # Normaliser les intensités globalement
    max_intensity = 100  # Limiter l'intensité maximale pour une meilleure visibilité
    heatmap_data = [
        (*point[:2], min(point[2], max_intensity) / max_intensity) for point in heatmap_points
    ]

    # Définir un dégradé à 6 couleurs
    gradient = {
        0.0: 'blue',     # Très faible densité
        0.2: 'cyan',     # Faible densité
        0.4: 'green',    # Densité moyenne
        0.6: 'yellow',   # Densité élevée
        0.8: 'orange',   # Très élevée
        1.0: 'red',      # Densité maximale
    }

    # Créer la carte centrée sur le premier point
    start_location = [heatmap_points[0][0], heatmap_points[0][1]]
    map_ = folium.Map(location=start_location, zoom_start=10)

    # Ajouter la couche de carte thermique
    HeatMap(
        heatmap_data,
        gradient=gradient,
        radius=15,  # Ajusté pour réduire le chevauchement
        blur=10,    # Réduit pour limiter le mélange
        max_zoom=1
    ).add_to(map_)

    # Ajouter une légende avec du HTML personnalisé
    legend_html = """
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 250px;
        height: 200px;
        background-color: white;
        border: 2px solid grey;
        z-index: 9999;
        font-size: 14px;
        padding: 10px;
        ">
        <b>Densite des bornes de recharges</b><br>
        <i style="background: blue; width: 20px; height: 20px; display: inline-block;"></i> Très faible<br>
        <i style="background: cyan; width: 20px; height: 20px; display: inline-block;"></i> Faible<br>
        <i style="background: green; width: 20px; height: 20px; display: inline-block;"></i> Moyenne<br>
        <i style="background: yellow; width: 20px; height: 20px; display: inline-block;"></i> Élevée<br>
        <i style="background: orange; width: 20px; height: 20px; display: inline-block;"></i> Très élevée<br>
        <i style="background: red; width: 20px; height: 20px; display: inline-block;"></i> Maximale<br>
    </div>
    """
    map_.get_root().html.add_child(folium.Element(legend_html))

    # Enregistrer la carte
    map_.save('carte_thermique_legende_6_couleurs.html')
    print("Carte avec légende enregistrée dans 'carte_thermique_legende_6_couleurs.html'")
else:
    print("Les colonnes 'consolidated_longitude' et 'consolidated_latitude' sont introuvables dans le fichier.")
