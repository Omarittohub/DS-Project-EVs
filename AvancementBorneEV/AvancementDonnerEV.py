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

# Create a complete range of years from 1930 to 2025
all_years = pd.DataFrame({'year': range(1930, 2026)})

# Merge the complete range of years with the grouped data
merged_df = pd.merge(all_years, grouped_df, on='year', how='left').fillna(0)

# Ensure the count column is of integer type
merged_df['count'] = merged_df['count'].astype(int)

# Calculate the cumulative total per year
merged_df['cumulative_total'] = merged_df['count'].cumsum()

# Save merged data to a CSV file for R Studio
merged_df.to_csv('grouped_by_year_for_R_AllYears.csv', index=False)

# Print the merged data
print(merged_df)