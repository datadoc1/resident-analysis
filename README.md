# Resident Analysis

Take a look at the methods section of these three papers:

- [Factors Influencing the Gender Breakdown of Academic Radiology Residency Programs, JACR (2017)](https://pubmed.ncbi.nlm.nih.gov/28427906/)
- [Trends in Geographic and Home Program Preferences in the Dermatology Residency Match: A Retrospective Cohort Analysis, JAAD (2022)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8627793/)
- [Which medical schools produce the most neurosurgery residents? An analysis of the 2014-2020 cohort, JNS (2021)](https://pubmed.ncbi.nlm.nih.gov/34826816/)

These three different papers, each with 20+ citations, are in tier-1 journals for their specialties. What do they have in common? They all built a database of residents that doesn’t otherwise exist and performed data analysis on it.

## Project Overview
The goal is to create a centralized database of residents for a specific medical specialty, including their medical school affiliations, program characteristics, and other relevant factors. This data will be used to identify and analyze potential correlations between variables, producing publishable manuscripts. The template is designed to be easily adapted for any medical specialty.  Potential analyses include:

1. **Gender Breakdown:** What factors predict a program's acceptance of a disproportionate number of residents of a particular gender?
2. **Home Program Preference:** What factors predict a program's preference for residents from their home medical school?
3. **Medical School Production:** Which medical schools produce the most residents in this specialty?  What characteristics of these medical schools contribute to this high production?

This project offers a structured approach to create new data and insights that are often unavailable in existing databases, leading to more nuanced understanding of residency program dynamics.


## Data Collection

The project relies on compiling data from residency program websites, social media platforms (e.g., Instagram, LinkedIn, Doximity), and other publicly available sources. Standardized data entry forms are crucial to ensure accuracy and consistency across the dataset. Data will be organized into linked tables:

* **Programs:** Information about each residency program in the chosen specialty (name, program director gender, total spots, region, state, etc.). A list of State, City, and Program Name can be found [here](https://systems.aamc.org/eras/erasstats/par/index.cfm)
* **Residents:** Detailed information about each resident (program name, medical school, gender, relevant demographics).
* **Home Programs:** A mapping of medical schools to their affiliated programs for the chosen specialty.

## Data Analysis Plan

Data analysis will leverage Python libraries (e.g., pandas, SciPy, statsmodels, seaborn) for data manipulation, statistical tests, and visualizations. The analysis plan will include:

* **Data Cleaning:**  The pipeline includes steps to address missing data, inconsistencies, and outliers.
* **Descriptive Statistics:** Analysis will include examining distributions of residents and programs for each specialty.
* **Statistical Tests:** Correlation tests (e.g., Pearson, Spearman) and hypothesis tests (e.g., t-tests, ANOVA) will be applied to assess statistical significance between variables.  The choice of test depends on the data's distribution.
* **Data Visualization:** Relevant charts (histograms, bar charts, scatterplots) will be generated to visualize findings and understand patterns in the data.

## **Specialty-Specific Project Pages and Relevant Links**
* [Zotero Literature Base](https://www.zotero.org/groups/5607003/residency_match/library)
* [Data Entry Template](https://docs.google.com/spreadsheets/d/1rTTYPH0BOQYeZOcWbq8ysIkA9uvxbjLBB_Vk2gx215g/edit?gid=378789652#gid=378789652)**
* Paper Templates: [Gender Breakdown](https://docs.google.com/document/d/1c5HX65ORgStKNxXgjQs22QcWSf8gqdlenWCH2_X5Z7k/edit) | [Home Program Breakdown](https://docs.google.com/document/d/1gG4yruZJh2EVHqm3zXoa_Kpfm3oolSiosWPti9BZb8o/edit) | [Medical School Production](https://docs.google.com/document/d/1sV4WE1388i0wIzTobha0JGNTz8owlpDzoQK6FE-ogoo/edit)

**Dermatology (COMPLETE, Contact: Kyra Rozanitis, MS2)**
* [Data Entry](https://docs.google.com/spreadsheets/d/1CwiDUIbzlmIg_v6D5bjIGFCSrjr-3UFv12nZUvOenM4/edit?gid=777314366#gid=777314366) | Gender Breakdown | Home Program Breakdown | [Medical School Production](https://docs.google.com/document/d/1JTCio9HBBvA3N5NRQB5165iuboCa2aeSg7Q-H2wFgyQ/edit?usp=sharing)

**Urology (IN PROGRESS, Project Lead: Vinay Sagar, MS2)**
* [Data Entry](https://docs.google.com/spreadsheets/d/15QdufSZ20yhjXrSb4R2eZpruuSO6A9wlLHS8Cn2C7bw/edit?gid=777314366#gid=777314366) | [Gender Breakdown](https://docs.google.com/document/d/1e7mOLKBXcQUARnwq05NackrBRXd4IdiVqvmodz895BE/edit) | [Home Program Breakdown](https://docs.google.com/document/d/1NySVLA2a8o54nwRK6CBsmNx33eUlzpth5cCuYGWwIGE/edit#heading=h.dl0citqm87px) | [Medical School Production](https://docs.google.com/document/d/1bdUjG4pcex4dVJhuiJXXAJNsJmcT54aZ7RVLa4QplFY/edit)

**Orthopedics (IN PROGRESS)**
* [Data Entry](https://docs.google.com/spreadsheets/d/18yL7ZbQ-KVHxb8jjqgMZ9CCRcOl0j-pYctQgBbEJe1g/edit?gid=0#gid=0) | Gender Breakdown | Home Program Breakdown | Medical School Production

**Potential Future Targets**
* [AAMC Number of Active Residents By Specialty](https://www.aamc.org/data-reports/students-residents/data/table-b3-number-active-residents-type-medical-school-gme-specialty-and-sex) (Generally, specialties with 1000-3000 residents are a sweetspot. More residents and data entry may be tiresome, less residents and you run the risk of not finding anything interesting).

## Other Projects Going On
* Signal Analysis [project outline coming soon...]
* Thoughts and reflections on research [series of blog posts coming soon...]

Contact Keola Ching, MS2 at chingk@uthscsa.edu for questions
