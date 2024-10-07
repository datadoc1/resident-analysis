import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from io import BytesIO

def load_and_prepare_data(folder_path):
    # Load data
    programs = pd.read_csv(f'data/{folder_path}/csv/Programs.csv')
    residents = pd.read_csv(f'data/{folder_path}/csv/Residents.csv')
    standardized_names = pd.read_csv(f'data/{folder_path}/csv/Standardized Medical Schools.csv')
    
    # Data cleaning and preparation (similar to your original script)
    residents = residents.dropna(subset=['Name'])
    residents = residents[['Program', 'Year', 'Name', 'Gender', 'Medical School']]
    residents = residents.merge(
        standardized_names[['School', 'Affiliated Program']], 
        left_on='Medical School', 
        right_on='School', 
        how='left'
    )
    residents = residents[residents['Program'].isin(standardized_names['Affiliated Program'])]
    
    # Create Home Program column
    residents['Home Program'] = 'N'
    residents.loc[residents['Affiliated Program'] == residents['Program'], 'Home Program'] = 'Y'
    
    # Merge with programs data
    programs = programs[programs['Program Name'].isin(standardized_names['Affiliated Program'])]
    residents = residents.merge(
        programs[['Program Name', 'State', 'PD Gender', 'Region', 'Total Spots']], 
        left_on='Program', 
        right_on='Program Name', 
        how='left'
    )
    
    return residents, programs

def create_visualizations(residents):
    visuals = {}
    
    # Overall box plot
    plt.figure(figsize=(10, 6))
    program_percentages = residents.groupby('Program')['Home Program'].apply(
        lambda x: (x == 'Y').mean() * 100
    )
    sns.boxplot(y=program_percentages)
    plt.title('Distribution of Home Program Percentages')
    plt.ylabel('Percentage of Home Program Residents')
    
    img_bio = BytesIO()
    plt.savefig(img_bio)
    visuals['overall_boxplot'] = img_bio
    
    # Region bar chart
    plt.figure(figsize=(12, 6))
    region_percentages = residents.groupby('Region')['Home Program'].apply(
        lambda x: (x == 'Y').mean() * 100
    ).sort_values(ascending=False)
    
    sns.barplot(x=region_percentages.index, y=region_percentages.values)
    plt.title('Home Program Percentages by Region')
    plt.xticks(rotation=45)
    plt.ylabel('Percentage of Home Program Residents')
    
    img_bio = BytesIO()
    plt.savefig(img_bio)
    visuals['region_barchart'] = img_bio
    
    return visuals

def perform_statistical_tests(residents):
    tests = {}
    
    # Gender comparison
    gender_groups = [
        residents[residents['Gender'] == 'M']['Home Program'] == 'Y',
        residents[residents['Gender'] == 'F']['Home Program'] == 'Y'
    ]
    tests['gender'] = stats.chi2_contingency([
        [sum(g), len(g) - sum(g)] for g in gender_groups
    ])
    
    # PD Gender comparison
    pd_gender_groups = [
        residents[residents['PD Gender'] == 'M']['Home Program'] == 'Y',
        residents[residents['PD Gender'] == 'F']['Home Program'] == 'Y'
    ]
    tests['pd_gender'] = stats.chi2_contingency([
        [sum(g), len(g) - sum(g)] for g in pd_gender_groups
    ])
    
    # Region comparison
    region_data = residents.groupby('Region')['Home Program'].apply(
        lambda x: pd.Series([sum(x == 'Y'), sum(x == 'N')])
    ).values
    tests['region'] = stats.chi2_contingency(region_data)
    
    return tests

def create_pdf_report(residents, programs, visuals, tests, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph("Residency Program Analysis Report", title_style))
    
    # Methodology section
    story.append(Paragraph("Methodology", styles['Heading1']))
    methodology_text = """
    This analysis examines patterns in residency program selection, focusing on the tendency 
    of residents to match at programs affiliated with their medical school ('home programs'). 
    Data was collected on residents, their medical schools, and program characteristics. 
    The primary outcome measure was the binary classification of whether a resident matched 
    at their home program. Statistical analyses include chi-square tests for independence 
    to examine relationships between variables and the likelihood of matching at a home program.
    """
    story.append(Paragraph(methodology_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Results section
    story.append(Paragraph("Results", styles['Heading1']))
    
    # Overall statistics
    overall_percentage = (residents['Home Program'] == 'Y').mean() * 100
    story.append(Paragraph(f"Overall Home Program Percentage: {overall_percentage:.1f}%", styles['Heading2']))
    story.append(Paragraph("Distribution of home program percentages across all programs:", styles['Normal']))
    story.append(Image(visuals['overall_boxplot']))
    story.append(Spacer(1, 12))
    
    # Gender analysis
    story.append(Paragraph("Gender Analysis", styles['Heading2']))
    gender_percentages = residents.groupby('Gender')['Home Program'].apply(
        lambda x: (x == 'Y').mean() * 100
    )
    gender_text = f"""
    Male residents: {gender_percentages['M']:.1f}% home program
    Female residents: {gender_percentages['F']:.1f}% home program
    Chi-square test: p = {tests['gender'][1]:.4f}
    """
    story.append(Paragraph(gender_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Program Director Gender analysis
    story.append(Paragraph("Program Director Gender Analysis", styles['Heading2']))
    pd_gender_percentages = residents.groupby('PD Gender')['Home Program'].apply(
        lambda x: (x == 'Y').mean() * 100
    )
    pd_gender_text = f"""
    Male PD programs: {pd_gender_percentages['M']:.1f}% home program
    Female PD programs: {pd_gender_percentages['F']:.1f}% home program
    Chi-square test: p = {tests['pd_gender'][1]:.4f}
    """
    story.append(Paragraph(pd_gender_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Regional analysis
    story.append(Paragraph("Regional Analysis", styles['Heading2']))
    story.append(Paragraph("Home program percentages vary by region:", styles['Normal']))
    story.append(Image(visuals['region_barchart']))
    story.append(Paragraph(f"Chi-square test for regional differences: p = {tests['region'][1]:.4f}", styles['Normal']))
    
    # Build and save the PDF
    doc.build(story)

def main():
    folder_path = input("Enter the specialty name: ")
    residents, programs = load_and_prepare_data(folder_path)
    
    visuals = create_visualizations(residents)
    tests = perform_statistical_tests(residents)
    
    output_file = f'data/{folder_path}/analysis_report.pdf'
    create_pdf_report(residents, programs, visuals, tests, output_file)
    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    main()