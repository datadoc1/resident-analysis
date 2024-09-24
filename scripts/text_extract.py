import os
import csv
import sys

def get_line_after(text, contents, num_lines=1):
    # Find the index of the line that contains the given text
    index = -1
    for i in range(len(contents)):
        if text in contents[i]:
            index = i
            break

    # Check if the text was found
    if index != -1:
        # Calculate the index of the line after the text
        line_index = index + num_lines

        # Check if the line index is within the contents range
        if line_index < len(contents):
            # Return the line after the text
            return contents[line_index].strip()
        else:
            # Return None if the line index is out of range
            return None
    else:
        # Return None if the text was not found
        return None
    
# Define the path to the folder containing the text files
folder_path = sys.argv[1] + '/text'

# Define the path to the output CSV file
output_file = sys.argv[1] + '/output.csv'
with open(output_file, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header row if the file is empty
    if csvfile.tell() == 0:
        writer.writerow(['Region', 'Name', 'ACGME Program Code', 'Program Director', 'Program Coordinator', 'PGY1', 'PGY2', 'PGY3', 'Institutional Setting', 'Participates in ERAS', 'Program has Osteopathic Recognition', '# of Residents Who Were Graduates of a Joint MD-PhD program', 'Categorical Positions', 'Categorical Positions Filled','Advanced Positions Offered', 'Advanced Positions Filled', '# of Applicants:','Interviewed:',  'Alpha Omega Alpha (AOA)', 'Alpha Omega Alpha (AOA)', 'Gold Humanism Honor Society (GHHS)', 'Gold Humanism Honor Society (GHHS)', 'Sigma Sigma Phi (SSP)', 'Sigma Sigma Phi (SSP)'])

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a text file
        if filename.endswith('.txt'):
            # Open the file
            with open(os.path.join(folder_path, filename), 'r') as file:
                # Read the contents of the file
                contents = file.readlines()

                # Get the line after 'Region'
                region = get_line_after('Region', contents, 1)
                print(f"Region: {region}")

                # Get the line after 'Name'
                name = get_line_after(sys.argv[2], contents, 1)
                print(sys.argv[2])
                print(f"Name: {name}")

                # Get the line after 'ACGME Program Code'
                acgme_code = get_line_after('ACGME Program Code', contents, 1)
                print(f"ACGME Program Code: {acgme_code}")

                # Get the line after 'Program Director'
                program_director = get_line_after('Program Director', contents, 1)
                program_coordinator = get_line_after('Program Coordinator', contents, 1)
                pgy1 = get_line_after('PGY1', contents, 1)
                pgy2 = get_line_after('PGY2', contents, 1)
                pgy3 = get_line_after('PGY3', contents, 1)
                institutional_setting = get_line_after('Institutional Setting', contents, 1)
                participates_in_eras = get_line_after('Participates in ERAS', contents, 1)
                osteopathic = get_line_after('Program has Osteopathic Recognition', contents, 1)
                mdphd = get_line_after('# of Residents Who Were Graduates of a Joint MD-PhD program', contents, 1)
                categorical = get_line_after('Categorical', contents, 2)
                categorical_2 = get_line_after('Categorical', contents, 4)
                positions_offered = get_line_after('Advanced', contents, 2)
                positions_filled = get_line_after('Advanced', contents, 4)
                applicants = get_line_after('# of Applicants:', contents, 1)
                interview = get_line_after('Interviewed:', contents, 1)
                aoa = get_line_after('Alpha Omega Alpha (AOA)', contents, 1)
                aoa_2 = get_line_after('Alpha Omega Alpha (AOA)', contents, 2)
                ghhs = get_line_after('Gold Humanism Honor Society (GHHS)', contents, 1)
                ghhs_2 = get_line_after('Gold Humanism Honor Society (GHHS)', contents, 2)
                ssp = get_line_after('Sigma Sigma Phi (SSP)', contents, 1)
                ssp_2 = get_line_after('Sigma Sigma Phi (SSP)', contents, 2)

                # Check if any of the extracted data is None
                if any(data is None for data in [region, name, acgme_code, program_director, program_coordinator, pgy1, pgy2, pgy3, institutional_setting, participates_in_eras, osteopathic, mdphd, categorical, categorical_2, positions_offered, positions_filled, applicants, interview, aoa, aoa_2, ghhs, ghhs_2, ssp, ssp_2]):
                    print(f"Skipping file {filename} due to missing data")
                    # Skip the file if any data is missing
                    continue

                # Write the extracted data to the CSV file
                writer.writerow([region, name, acgme_code, program_director, program_coordinator, pgy1, pgy2, pgy3, institutional_setting, participates_in_eras, osteopathic, mdphd, categorical, categorical_2, positions_offered, positions_filled, applicants, interview, aoa, aoa_2, ghhs, ghhs_2, ssp, ssp_2])
                print(f"Written data for file {filename}")

