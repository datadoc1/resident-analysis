import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from scipy.stats import pearsonr

# Specify Folder Path
folder_path = input("Enter the specialty name: ")

# Specify the file path
programs_file = 'data/' + folder_path + '/csv/Programs.csv'
residents_file = 'data/' + folder_path + '/csv/Residents.csv'
standardized_names_file = 'data/' + folder_path + '/csv/Standardized Medical Schools.csv'

# Read the CSV file into a DataFrame
programs = pd.read_csv(programs_file)
residents = pd.read_csv(residents_file)
standardized_names = pd.read_csv(standardized_names_file)

# Remove rows where Name is NaN
residents = residents.dropna(subset=['Name'])

print(programs.head())
print(residents.head())
print(standardized_names.head())

print(f"Length of residents: {len(residents)}")
print(f"Unique values of 'Medical School': {len(residents['Medical School'].unique())}")

# Find unique values of 'Medical School' in residents that don't appear in 'School' column of standardized_names
missing_med_schools = residents[~residents['Medical School'].isin(standardized_names['School'])]['Medical School'].unique()
print("Unique values of 'Medical School' that don't appear in standardized_names:")
print(missing_med_schools)

# Remove columns that are not Program, Year, Name, Gender, Medical School
residents = residents[['Program', 'Year', 'Name', 'Gender', 'Medical School']]

# Merge residents DataFrame with standardized_names DataFrame on 'Medical School'
residents = residents.merge(standardized_names[['School', 'Affiliated Program']], left_on='Medical School', right_on='School', how='left')

# Create 'excluded' DataFrame with the rest of the rows
excluded = residents[~residents['Program'].isin(standardized_names['Affiliated Program'])]
print(len(excluded))
print(len(excluded['Program'].unique()))

# Delete rows with Program values that don't show up in standardized_names['School']
residents = residents[residents['Program'].isin(standardized_names['Affiliated Program'])]
print(len(residents))
print(len(residents['Program'].unique()))

# Create 'Home Program' column and set default value as 'N'
residents['Home Program'] = 'N'

# Update 'Home Program' column to 'Y' where 'Affiliated Program' matches 'Program'
residents.loc[residents['Affiliated Program'] == residents['Program'], 'Home Program'] = 'Y'

# Calculate the percentage of 'Home Program' that is 'Y'
percentage_home_program = (residents['Home Program'] == 'Y').mean() * 100
print(f"Percentage of 'Home Program' that is 'Y': {percentage_home_program}%")

# Group by Program and compute Percentage of Home Program that is "Y"
program_group = residents.groupby('Program')['Home Program'].apply(lambda x: (x == 'Y').mean() * 100).sort_values(ascending=False)
print("Percentage of 'Home Program' that is 'Y' by Program (sorted high to low):")
print(program_group)

# Print out the Median, 25th, 75th, 10th, and 90th percentile for Home Program by Program
program_percentiles = program_group.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])
print("Median, 25th, 75th, 10th, and 90th percentile for 'Home Program' by Program:")
print(program_percentiles[['10%', '25%', '50%', '75%', '90%']])

# Group by Gender and compute Percentage of Home Program that is "Y"
gender_group = residents.groupby('Gender')['Home Program'].apply(lambda x: (x == 'Y').mean() * 100).sort_values(ascending=False)
print("Percentage of 'Home Program' that is 'Y' by Gender:")
print(gender_group)

########################################################################################
# Trim programs DataFrame by rows where 'Program Name' is in the set of standardized_names['Affiliated Program']
programs = programs[programs['Program Name'].isin(standardized_names['Affiliated Program'])]
no_resident_data = programs[~programs['Program Name'].isin(residents['Program'])]
programs = programs[programs['Program Name'].isin(residents['Program'])]

# Count the unique values of 'PD Gender'
gender_count = programs['PD Gender'].value_counts()
print("Count of each unique value of 'PD Gender':")
print(gender_count)

# Count the unique values of 'Region'
region_key = pd.read_csv('eras_regions.csv')
programs['Region'] = programs['State'].map(region_key.set_index('State')['Region'])
programs.to_csv('reports/' + folder_path + '/programs.csv', index=False)
region_count = programs['Region'].value_counts()
region_count.to_csv('reports/' + folder_path + '/program_count_by_region.csv', header=True, index=True)


# Merge programs DataFrame onto residents DataFrame
residents = residents.merge(programs[['Program Name', 'State', 'PD Gender', 'Region', 'Total Spots']], left_on='Program', right_on='Program Name', how='left')
# Drop the redundant 'Program Name' column
residents.drop(['Program Name', 'School', 'Affiliated Program'], axis=1, inplace=True)

# Print the updated residents DataFrame
print(residents.columns)

# Group by PD Gender and compute Percentage of Home Program that is "Y"
pd_gender_group = residents.groupby('PD Gender')['Home Program'].apply(lambda x: (x == 'Y').mean() * 100).sort_values(ascending=False)
print("Percentage of 'Home Program' that is 'Y' by PD Gender:")
print(pd_gender_group)

# Group by Total Spots and compute Percentage of Home Program that is "Y"
total_spots_group = residents.groupby('Total Spots')['Home Program'].apply(lambda x: (x == 'Y').mean() * 100).sort_values(ascending=False)
print("Percentage of 'Home Program' that is 'Y' by Total Spots:")
print(total_spots_group)

# Group by Region and compute Percentage of Home Program that is "Y"
region_group = residents.groupby('Region')['Home Program'].apply(lambda x: (x == 'Y').mean() * 100).sort_values(ascending=False)
print("Percentage of 'Home Program' that is 'Y' by Region:")
print(region_group)

state_group = residents.groupby('Region')['State'].apply(lambda x: (x == 'Y').mean() * 100).sort_values(ascending=False)
print("Percentage of 'Home Program' that is 'Y' by Region:")
print(state_group)

# Save region_group to CSV file
region_group.to_csv('region_group.csv', header=True, index=True)

# Calculate the percentage of 'Home Program' that is 'Y' by Program
program_percentage_home_program = residents.groupby('Program')['Home Program'].apply(lambda x: (x == 'Y').mean() * 100)
print("Percentage of 'Home Program' that is 'Y' by Program:")

program_percentage_home_program = pd.DataFrame(program_percentage_home_program)
program_percentage_home_program = program_percentage_home_program.merge(standardized_names[['Affiliated Program', 'Matriculants']], left_on='Program', right_on='Affiliated Program', how='left')
print(program_percentage_home_program)

# Perform Pearson correlation test between 'Matriculants' and 'Home Program'
correlation, p_value = pearsonr(program_percentage_home_program['Matriculants'], program_percentage_home_program['Home Program'])
print(f"Pearson correlation coefficient: {correlation}")
print(f"P-value: {p_value}")

# Sort by 'Home Program'
program_percentage_home_program = program_percentage_home_program.sort_values('Home Program', ascending=False)
print(program_percentage_home_program.head(20))
print(program_percentage_home_program.tail(20))







