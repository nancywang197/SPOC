# import csv

# # Replace with your actual CSV file path
# csv_file_path = '/Users/dsanagaram/Documents/GitHub/SPOC/running_test_cases/train-dataset-recovered.csv'

# with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     headers = next(reader)  # This reads the first line which is supposed to be headers
#     print(headers)


###############################
# import csv

# Replace with your actual CSV file path
# csv_file_path = '/Users/dsanagaram/Documents/GitHub/SPOC/running_test_cases/train-dataset-recovered.csv'

# # Open the CSV file and skip lines if necessary
# with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#     # Read the file into a csv.reader object
#     reader = csv.reader(csvfile)
    
#     # Skip lines if the headers are not on the first line
#     for _ in range(1):  # Replace 'n' with the number of lines to skip
#         next(reader)
    
#     # Read the headers
#     headers = next(reader)
#     print(headers)  # Print the headers to verify
###############################

import csv

# Replace with your actual CSV file path
csv_file_path = '/Users/dsanagaram/Documents/GitHub/SPOC/running_test_cases/train-dataset-recovered.csv'

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        print(row)  # Print each row's dictionary
        code = row.get('Code', None)  # Returns None if 'Code' is not a key in the row
        if code is None:
            print("'Code' not present")# Handle the case where 'Code' is not present
        if i == 1:  # Stop after printing the first two rows
            break

