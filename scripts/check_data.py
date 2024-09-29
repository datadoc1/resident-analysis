import pandas as pd
import os

def check_data(user_input):
    # Programs.csv
    programs_df = pd.read_csv(os.path.join('data',user_input, 'csv', 'Programs.csv'))
    print(f"There are {programs_df.shape[0]} unique programs.")
    
    # Check column names
    required_columns = ['State', 'City', 'Program Name', 'PD Gender', 'Total Spots']
    if not all(col in programs_df.columns for col in required_columns):
        print("Error: Missing columns in Programs.csv. Please ensure all required columns exist.")
    
    # Check column values
    for col in required_columns:
        if col == 'Total Spots':
            if not programs_df[col].apply(lambda x: isinstance(x, int)).all():
                print(f"Error: Invalid values in 'Total Spots' column. All values should be integers.")
        elif col == 'PD Gender':
            if not programs_df[col].isin(['M', 'F']).all():
                print(f"Error: Invalid values in 'PD Gender' column. All values should be 'M' or 'F'.")
        else:
            if programs_df[col].isnull().any():
                print(f"Error: Missing values in '{col}' column. Please ensure all values are filled.")
    
    # Residents.csv
    residents_df = pd.read_csv(os.path.join(user_input, 'csv', 'Residents.csv'))
    print(f"There are {residents_df.shape[0]} rows in Residents.csv.")
    
    # Check column names
    required_columns = ['Program', 'Name', 'Gender', 'Medical School', 'Year']
    if not all(col in residents_df.columns for col in required_columns):
        print("Error: Missing columns in Residents.csv. Please ensure all required columns exist.")
    
    # Check for complete rows
    complete_rows = residents_df.dropna()
    print(f"There are {complete_rows.shape[0]} rows with values for all columns.")
    
    # Check Gender values
    invalid_genders = residents_df['Gender'].unique()
    invalid_genders = [gender for gender in invalid_genders if gender not in ['M', 'F']]
    if invalid_genders:
        print(f"Error: Invalid Gender values found: {invalid_genders}. Please ensure all Gender values are 'M' or 'F'.")
    
    # Check Medical School values
    standardized_schools_df = pd.read_csv(os.path.join(user_input, 'csv', 'Standardized Medical Schools.csv'))
    invalid_schools = residents_df['Medical School'].unique()
    invalid_schools = [school for school in invalid_schools if school not in standardized_schools_df['Medical School'].unique()]
    print(f"The following Medical Schools are not found in the Standardized Medical Schools.csv: {invalid_schools}. These should only be International Schools.")
    
    # Update Medical School values
    for school in invalid_schools:
        if school in residents_df['Medical School'].values:
            residents_df.loc[residents_df['Medical School'] == school, 'Medical School'] = standardized_schools_df.loc[standardized_schools_df['Medical School'] == school, 'Medical School'].values[0]
    
    # Standardized Medical Schools.csv
    print(f"There are {standardized_schools_df['Affiliated Program'].nunique()} unique Affiliated Programs in Standardized Medical Schools.csv.")
    
    if invalid_genders or invalid_schools:
        print("Errors found in formatting.")
    else:
        print("No errors found in formatting.")

check_data(input("Enter the folder name: "))