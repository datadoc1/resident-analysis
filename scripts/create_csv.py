import pandas as pd
import os

folder_path = "data/" + input("Enter the folder name: ")
# Define the input Excel file path
excel_file = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')][0]
excel_file = folder_path + '/' + excel_file

# Read the Excel file
xls = pd.ExcelFile(excel_file)

# Iterate over each sheet in the Excel file
os.makedirs(f'{folder_path}/csv', exist_ok=True)
for sheet_name in xls.sheet_names:
    # Read the sheet into a DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Define the output CSV file path
    csv_file = f'{folder_path}/csv/{sheet_name}.csv'
    
    # Save the DataFrame as a CSV file
    df.to_csv(csv_file, index=False)