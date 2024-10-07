import pandas as pd
from scipy.stats import pearsonr, ttest_ind
from statsmodels.formula.api import ols
import statsmodels.api as sm
import seaborn as sns
import scipy.stats as stats

specialty = input("Enter the specialty folder name: ")
data_path = 'data/' + specialty + '/csv'


# Specify the file path
programs_file = data_path + '/Programs.csv'
residents_file = data_path + '/Residents.csv'
standardized_names_file = data_path + '/Standardized Medical Schools.csv'

# Read the CSV file into a DataFrame
programs = pd.read_csv(programs_file)
residents = pd.read_csv(residents_file)
standardized_medical_school_names = pd.read_csv(standardized_names_file)

# Remove rows where Name is NaN
residents = residents.dropna(subset=['Name'])

frequency_table = pd.DataFrame(residents['Medical School'].value_counts())
frequency_table = frequency_table.reset_index().rename(columns={'index': 'Medical School'})

merged_table = pd.merge(frequency_table, standardized_medical_school_names, left_on='Medical School', right_on='School')
merged_table = merged_table[['Medical School', 'count', 'Matriculants', 'Affiliated Program', 'State']]

# Compute the percentage of each class that goes into Dermatology
merged_table['Ratio'] = merged_table['count'] / merged_table['Matriculants']
merged_table = merged_table.sort_values('Ratio', ascending=False)
merged_table['Ratio'] = (merged_table['Ratio'] * 100) / 5

# Find the percentage of US MD matriculants that go into Dermatology
total_count = merged_table['count'].sum()
total_matriculants = merged_table['Matriculants'].sum()
average_ratio = total_count / total_matriculants / 5
print("Average Ratio: {:.2%}".format(average_ratio))

merged_table = merged_table.dropna(subset=['Matriculants'])

top_10 = merged_table.head(10)
bottom_10 = merged_table.tail(10)
print(top_10)
print(bottom_10)

output_table = 'reports/' + specialty + '/top schools.csv'
merged_table.to_csv(output_table, index=False)
