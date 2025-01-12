import pandas as pd

# Load the CSV file
file_path = 'consolidation-etalab-schema-irve-statique-v-2.3.1-20241226.csv'  # Replace with your file path

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Ensure column names and handle empty spaces
df['date_mise_en_service'] = df['date_mise_en_service'].str.strip()

# Extract the year directly from the date_mise_en_service column
df['year'] = pd.to_datetime(df['date_mise_en_service'], errors='coerce').dt.year

# Group by the year and count the number of charging stations
grouped = df.groupby('year').size()

# Convert the grouped data to a DataFrame
grouped_df = grouped.reset_index(name='count')

# Calculate the cumulative total per year
grouped_df['cumulative_total'] = grouped_df['count'].cumsum()

# Print the grouped data with cumulative total
print(grouped_df)

# Save grouped data to a CSV file
grouped_df.to_csv('grouped_by_year3.csv', index=False)