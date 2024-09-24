import sys
import csv

with open(csv_file_path, 'r') as file:
    folder_path = sys.argv[1]
    csv_file_path = folder_path + "/output.csv"

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['Total Spots']
        rows = []
        for row in reader:
            categorical_positions = row['Categorical Positions']
            advanced_positions = row['Advanced Positions Offered']
            try:
                categorical_positions = int(categorical_positions)
            except ValueError:
                categorical_positions = 0
            try:
                advanced_positions = int(advanced_positions)
            except ValueError:
                advanced_positions = 0
            total_spots = categorical_positions + advanced_positions
            row['Total Spots'] = total_spots
            rows.append(row)

        with open(csv_file_path, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    pass