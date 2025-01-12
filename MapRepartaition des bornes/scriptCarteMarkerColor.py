import pandas as pd
import folium
from scipy.spatial import KDTree
import numpy as np

# Load the CSV file
file_path = './consolidation-etalab-schema-irve-statique-v-2.3.1-20241123.csv'
data = pd.read_csv(file_path)

if 'consolidated_longitude' in data.columns and 'consolidated_latitude' in data.columns:
    coords = data[['consolidated_latitude', 'consolidated_longitude']].values

    # Build KDTree for proximity searches
    tree = KDTree(coords)
    threshold = 0.2  # Range for grouping points (tune this as needed)

    grouped_points = []
    visited = set()

    for i, point in enumerate(coords):
        if i not in visited:
            # Find nearby points within the threshold
            indices = tree.query_ball_point(point, threshold)
            visited.update(indices)

            # Group points and calculate intensity
            group = coords[indices]
            avg_lat, avg_lon = group.mean(axis=0)
            intensity = len(indices)  # Number of points in this group
            grouped_points.append((avg_lat, avg_lon, intensity))

    # Define color mapping function
    def get_marker_color(intensity, max_intensity):
        if intensity == 1:
            return 'darkblue'  # Very few points
        elif intensity <= max_intensity / 6:
            return 'blue'  # Few points
        elif intensity <= max_intensity / 3:
            return 'white'  # Average
        elif intensity <= max_intensity / 2:
            return 'yellow'  # A bit more
        elif intensity <= (2 * max_intensity) / 3:
            return 'orange'  # More points
        else:
            return 'red'  # Very high density

    # Find the maximum intensity
    max_intensity = max(point[2] for point in grouped_points)

    # Create the map centered at the first point
    start_location = [grouped_points[0][0], grouped_points[0][1]]
    map_ = folium.Map(location=start_location, zoom_start=10)

    # Add markers with colors based on intensity
    for lat, lon, intensity in grouped_points:
        color = get_marker_color(intensity, max_intensity)
        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(map_)

    # Save the map
    map_.save('map_colored_markers.html')
    print("Carte avec des marqueurs colorés enregistrée dans 'map_colored_markers.html'")
else:
    print("Les colonnes 'consolidated_longitude' et 'consolidated_latitude' sont introuvables dans le fichier.")
