import pandas as pd
import unicodedata
import plotly.express as px

# Charger les données des voitures par commune
car_data_path = 'C:\\Users\\omari\\Desktop\\Work\\DATASC\\MapVoitureElecparVille\\voitures-par-commune-par-energie.csv'  # Fichier des données des véhicules rechargeables par commune
car_data = pd.read_csv(car_data_path, sep=';')

# Fonction pour normaliser les noms des communes (supprimer les caractères spéciaux et mettre en majuscule)
def normalize_text(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')  # Normalisation
    text = text.upper()  # Mettre en majuscule
    text = text.replace('-', ' ')  # Remplacer les tirets par des espaces
    return text

# Appliquer la normalisation aux deux fichiers
car_data['LIBGEO'] = car_data['LIBGEO'].apply(normalize_text)

# Extraire l'année de la colonne DATE_ARRETE
car_data['ANNEE'] = pd.to_datetime(car_data['DATE_ARRETE']).dt.year

# Filtrer les données pour les années 2020 à 2024
car_data_filtered = car_data[car_data['ANNEE'].isin([2020, 2021, 2022, 2023, 2024])]

# Extraire les deux premiers chiffres de CODEGEO pour obtenir le département
car_data_filtered['DEPARTEMENT'] = car_data_filtered['CODGEO'].astype(str).str[:2]

# Grouper les données par département et année
car_data_grouped = car_data_filtered.groupby(['DEPARTEMENT', 'ANNEE']).size().reset_index(name='count')

# Créer l'histogramme avec Plotly
fig = px.histogram(
    car_data_grouped,
    x='DEPARTEMENT',
    y='count',
    color='ANNEE',
    barmode='stack',  # Change barmode to 'stack'
    title='Nombre de véhicules électriques par département et par année',
    labels={'DEPARTEMENT': 'Département', 'count': 'Nombre de véhicules'}
)

# Sauvegarder l'histogramme en tant que fichier HTML
fig.write_html('histogram.html')

# Afficher l'histogramme
fig.show()