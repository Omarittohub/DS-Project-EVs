import pandas as pd

# Step 1: Load datasets
# Document 1: Population evolution (1999-2024)
pop_evolution = pd.read_csv("department_population.csv", sep=';')
pop_evolution.columns = pop_evolution.columns.str.split(';').str[0]
print("Population Evolution:")
print(pop_evolution.head(4))

# Document 2: Revenue data (normalized by department)
revenue = pd.read_csv("BASE_TD_FILO_DEC_IRIS_2018.csv")
coords = pd.read_csv("cities.csv")
print("Revenue Data:")
print(revenue.head(4))
print("Coordinates Data:")
print(coords.head(4))

# Normalize department codes and group by department
revenue['Code département'] = revenue['COM'].astype(str).str[:2]
revenue['LIBCOM'] = revenue['LIBCOM'].str.upper()
coords['label'] = coords['label'].str.upper()

# Calculate the average median income for each department
grouped_revenue = revenue.groupby('Code département', as_index=False)['DEC_MED18'].mean()
print("Grouped Revenue Data by Department:")
print(grouped_revenue.head(4))

# Merge revenue data with coordinates
merged_revenue_coords = pd.merge(grouped_revenue, coords, left_on='Code département', right_on='department_number', how='inner')
print("Merged Revenue and Coordinates Data:")
print(merged_revenue_coords.head(4))

# Normalize the median incomes for heatmap integration
max_revenue = merged_revenue_coords['DEC_MED18'].max()
min_revenue = merged_revenue_coords['DEC_MED18'].min()
merged_revenue_coords['normalized_revenue'] = (merged_revenue_coords['DEC_MED18'] - min_revenue) / (max_revenue - min_revenue)

# Group by department
revenue_grouped = revenue.groupby('Code département', as_index=False)['DEC_MED18'].mean()
print("Revenue Grouped by Department:")
print(revenue_grouped.head(4))

# Document 3: Charging stations per department
charging_stations = pd.read_csv("nombre-de-points-de-charge-accessibles-au-public-pour-100-000-habitants-par-dept.csv", sep=";")
charging_stations['Code département'] = charging_stations['Code département'].astype(str)

print("Charging Stations Data:")
print(charging_stations.head(4))

# Document 5: Electric cars data
electric_cars = pd.read_csv("voitures-par-commune-par-energie.csv", sep=';')
electric_cars['CODGEO'] = electric_cars['CODGEO'].astype(str)
electric_cars['LIBGEO'] = electric_cars['LIBGEO'].str.upper()
print("Electric Cars Data:")
print(electric_cars.head(4))

# Merge electric cars data with coordinates to get department codes
merged_cars_coords = pd.merge(electric_cars, coords, left_on='LIBGEO', right_on='label', how='inner')
print("Merged Electric Cars and Coordinates Data:")
print(merged_cars_coords.head(4))

# Sum up the number of rechargeable electric cars by department
electric_cars_by_dept = merged_cars_coords.groupby('department_number', as_index=False)['NB_VP_RECHARGEABLES_EL'].sum()
electric_cars_by_dept.rename(columns={'department_number': 'Code département', 'NB_VP_RECHARGEABLES_EL': 'Total_Electric_Cars'}, inplace=True)
print("Electric Cars by Department:")
print(electric_cars_by_dept.head(4))

# Step 2: Merge datasets
# Merge population evolution with charging stations
print(pop_evolution.columns)
merged = pd.merge(pop_evolution, charging_stations, on='Code département', how='inner')
print("Merged Population Evolution and Charging Stations Data:")
print(merged.head(4))

# Merge with revenue data
merged = pd.merge(merged, revenue_grouped, on='Code département', how='inner')
print("Merged with Revenue Data:")
print(merged.head(4))

# Merge with electric cars data
merged = pd.merge(merged, electric_cars_by_dept, on='Code département', how='inner')
print("Merged with Electric Cars Data:")
print(merged.head(4))

# Select and rename the required columns
final_result = merged[['PopulationTotale', 'DEC_MED18', 'Nombre de points de charge ouverts au public pour 100 000 habitants', 'Total_Electric_Cars']]
final_result.to_csv("final_result.csv", index=False)
print("Final result saved to 'final_result.csv'")
print("Final Result:")
print(final_result.head(4))
