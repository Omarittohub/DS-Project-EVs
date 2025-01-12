import pandas as pd

# Load the CSV file
file_path = 'BASE_TD_FILO_DEC_IRIS_2018.csv'  # Replace with the actual path to your CSV file
data = pd.read_csv(file_path)

# Add 0 behind each number if its length is less than 5
data['COM'] = data['COM'].astype(str).apply(lambda x: x.zfill(5) if len(x) < 5 else x)

# Save the updated CSV file
data.to_csv('updated_file.csv', index=False)
