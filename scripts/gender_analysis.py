import pandas as pd
from scipy.stats import pearsonr, ttest_ind
from statsmodels.formula.api import ols
import statsmodels.api as sm
import seaborn as sns
import scipy.stats as stats

folder_path = 'urology'

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

# Remove rows with empty values for 'Gender' and move them to 'Missing Gender' DataFrame
missing_gender = residents[residents['Gender'].isnull()]
residents = residents.dropna(subset=['Gender'])
unique_programs = residents['Program'].unique()

# Continue with the rest of the code
gender_ratio = []

for program in unique_programs:
    program_residents = residents[residents['Program'] == program]
    male_count = program_residents[program_residents['Gender'] == 'M'].shape[0]
    female_count = program_residents[program_residents['Gender'] == 'F'].shape[0]
    total_count = male_count + female_count
    
    # Debugging print statements
    print(f"Program: {program}")
    print(f"Male count: {male_count}")
    print(f"Female count: {female_count}")
    print(f"Total count: {total_count}")
    
    if total_count == 0:
        print(f"Skipping program {program} due to zero total count")
        continue
    
    female_percentage = (female_count / total_count) * 100
    gender_ratio.append((program, female_percentage, male_count, female_count, total_count))
    
gender_ratio_df = pd.DataFrame(gender_ratio, columns=['Program', 'Female Percentage', 'Male Count', 'Female Count', 'Total Count'])
gender_ratio_df.sort_values(by='Female Percentage', ascending=False, inplace=True)
print(gender_ratio_df.describe())
gender_ratio_df.to_csv('reports/' + folder_path + '/gender_breakdown_by_school.csv', index=False)
gender_ratio_df.describe().to_csv('reports/' + folder_path + '/gender_breakdown_summary.csv', index=True)


residents_len = len(residents)
print(f"Number of residents: {residents_len}")

female_residents = residents[residents['Gender'] == 'F']
male_residents = residents[residents['Gender'] == 'M']

female_count = len(female_residents)
male_count = len(male_residents)

print(f"Number of female residents: {female_count}")
print(f"Number of male residents: {male_count}")

region_key = pd.read_csv('eras_regions.csv')
programs['Region'] = programs['State'].map(region_key.set_index('State')['Region'])
merged_df = pd.merge(gender_ratio_df, programs[['Program Name', 'PD Gender', 'Total Spots', 'Region']], left_on='Program', right_on='Program Name', how='left')
print(merged_df)

#####################################################
### STATISTICAL ANALYSIS ###
#####################################################

# Check for normality (value under 0.05 suggests non-normality)
shapiro_test = stats.shapiro(merged_df['Female Percentage'])
print(f"Shapiro-Wilk Test: Statistic={shapiro_test.statistic}, p-value={shapiro_test.pvalue}")

ks_test_program = stats.kstest(merged_df['Female Percentage'], 'norm', args=(merged_df['Female Percentage'].mean(), merged_df['Female Percentage'].std()))
print(f"Kolmogorov-Smirnov Test for Program Female Percentage: Statistic={ks_test_program.statistic}, p-value={ks_test_program.pvalue}")

merged_df.dropna(subset=['Total Spots', 'Female Percentage'], inplace=True)

#####################################################
### Run if data is not normally distributed ###
#####################################################
# Run Spearman correlation
correlation, p_value = stats.spearmanr(merged_df['Total Spots'], merged_df['Female Percentage'])
print(f"Spearman correlation: {correlation}")
print(f"P-value: {p_value}")

# Run Kruskal-Wallis test
kw_stat, p_value = stats.kruskal(merged_df[merged_df['PD Gender'] == 'F']['Female Percentage'], merged_df[merged_df['PD Gender'] == 'M']['Female Percentage'])
print(f"Kruskal-Wallis Test: Statistic={kw_stat}, p-value={p_value}")

# Run Mann-Whitney U test
mwu_stat, p_value = stats.mannwhitneyu(merged_df[merged_df['PD Gender'] == 'F']['Female Percentage'], merged_df[merged_df['PD Gender'] == 'M']['Female Percentage'])
print(f"Mann-Whitney U Test: Statistic={mwu_stat}, p-value={p_value}")

#####################################################
### Run if data is normally distributed ###
#####################################################
# Run Pearson correlation
correlation, p_value = pearsonr(merged_df['Total Spots'], merged_df['Female Percentage'])
print(f"Correlation: {correlation}")
print(f"P-value: {p_value}")

# Run independent t-test
t_stat, p_value = ttest_ind(merged_df[merged_df['PD Gender'] == 'F']['Female Percentage'], merged_df[merged_df['PD Gender'] == 'M']['Female Percentage'])
print(f"Independent t-test: t-statistic={t_stat}, p-value={p_value}")

# Run analysis of variance (ANOVA)
model = ols('Q("Female Percentage") ~ Q("PD Gender")', data=merged_df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
