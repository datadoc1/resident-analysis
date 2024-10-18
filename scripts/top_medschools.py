import pandas as pd
from scipy.stats import pearsonr, ttest_ind
from statsmodels.formula.api import ols
import statsmodels.api as sm
import seaborn as sns
import scipy.stats as stats
import os
import plotly.express as px

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
merged_table = merged_table[['Medical School', 'count', 'Matriculants', 'Affiliated Program', 'State', 'Medical School Research Tier (US News)', 'Urology Department Funding (Blue Ridge Institute for Medical Research)', 'Total NIH Funding']]
merged_table = merged_table.rename(columns={'count': 'Residents', 'Medical School Research Tier (US News)': 'Tier', 'Urology Department Funding (Blue Ridge Institute for Medical Research)': 'Urology Funding', 'Total NIH Funding': 'NIH Funding'})

# Compute the percentage of each class that goes into X specialty
merged_table['Ratio'] = merged_table['Residents'] / merged_table['Matriculants']
merged_table = merged_table.sort_values('Ratio', ascending=False)
merged_table['Ratio'] = (merged_table['Ratio']) / 5

# Find the percentage of US MD matriculants that go into X specialty
total_count = merged_table['Residents'].sum()
total_matriculants = merged_table['Matriculants'].sum()
average_ratio = total_count / total_matriculants / 5
print("Average Ratio: {:.2%}".format(average_ratio))

merged_table = merged_table.dropna(subset=['Matriculants'])
print(merged_table.describe())

output_folder = 'reports/' + specialty + '/school production/'
os.makedirs(output_folder, exist_ok=True)
merged_table.to_csv(output_folder + 'top schools.csv', index=False)

# Create a box of Residents by Tier using Plotly
fig = px.box(merged_table, x='Tier', y='Residents', labels={'Tier': 'Medical School Research Tier (US News 2024)', 'Residents': 'Number of Students Entering Urology Residency'})

# Add median labels
for tier in merged_table['Tier'].unique()[1:4]:
    median_value = merged_table[merged_table['Tier'] == tier]['Residents'].median()
    fig.add_annotation(
        x=tier,
        y=median_value,
        text=f'Median: {median_value}',
        showarrow=False,
        yshift=10
    )
fig.write_image(output_folder + 'number_of_class_entering_by_tier.png')

# Create a boxplot of Ratio by Tier using Plotly
fig = px.box(merged_table, x='Tier', y='Ratio', labels={'Tier': 'Medical School Research Tier (US News 2024)', 'Ratio': 'Percentage of Medical School Class Entering Urology Residency'})
# Add median labels
for tier in merged_table['Tier'].unique()[1:4]:
    median_value = merged_table[merged_table['Tier'] == tier]['Ratio'].median()
    fig.add_annotation(
        x=tier,
        y=median_value,
        text=f'Median: {median_value*100:.2f}%',
        showarrow=False,
        yshift=10
    )
fig.update_layout(
    yaxis_tickformat='.1%'
)
fig.write_image(output_folder + 'percentage_of_class_entering_by_tier.png')

# Create a scatter plot of Residents by Ratio using Plotly
fig = px.scatter(merged_table, x='Residents', y='Ratio', labels={'Residents': 'Number of Students Entering Urology Residency', 'Ratio': 'Percentage of Medical School Class Entering Urology Residency'})
fig.update_layout(
    yaxis_tickformat='.1%'
)

fig.write_image(output_folder + 'number_of_class_entering_vs_percentage_of_class.png')

# Create a scatterplot of Ratio by Urology Department Funding using Plotly
fig = px.scatter(merged_table, x='Ratio', y='Urology Funding', labels={'Ratio': 'Percentage of Medical School Class Entering Urology Residency', 'Urology Funding': 'Urology Department Funding'})
fig.update_layout(
    xaxis_tickformat='.1%'
)
fig.write_image(output_folder + 'percentage_of_class_entering_vs_urology_funding.png')

# Create a scatterplot of Ratio by NIH Funding using Plotly
fig = px.scatter(merged_table, x='Ratio', y='NIH Funding', labels={'Ratio': 'Percentage of Medical School Class Entering Urology Residency', 'NIH Funding': 'Total NIH Funding'})
fig.update_layout(
    xaxis_tickformat='.1%'
)
fig.write_image(output_folder + 'percentage_of_class_entering_vs_nih_funding.png')

# Create a scatterplot of Residents by NIH Funding using Plotly
fig = px.scatter(merged_table, x='Residents', y='NIH Funding', labels={'Residents': 'Number of Students Entering Urology Residency', 'NIH Funding': 'Total NIH Funding'})
fig.write_image(output_folder + 'number_of_class_entering_vs_nih_funding.png')




