import pandas as pd

folder_path = 'dermatology'
# Define the input Excel file path
excel_file = folder_path + '/Derm Resident Analysis 2024.xlsx'

# Read the Excel file
xls = pd.ExcelFile(excel_file)

# Iterate over each sheet in the Excel file
for sheet_name in xls.sheet_names:
    # Read the sheet into a DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Define the output CSV file path
    csv_file = f'{folder_path}/{sheet_name}.csv'
    
    # Save the DataFrame as a CSV file
    df.to_csv(csv_file, index=False)