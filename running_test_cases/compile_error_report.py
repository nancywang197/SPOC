################################################

# Path to the file containing sorted filenames
# filename_path = '/Users/dsanagaram/Documents/GitHub/SPOC/running_test_cases/run_unique_tests_1k_out/sorted_filenames.txt'

# # Read the sorted filenames from the file
# with open(filename_path, 'r') as file:
#     filenames = file.readlines()

# # Extract the problem numbers from the filenames
# problem_numbers = [int(name.split('_')[-1].split('.')[0]) for name in filenames]

# # Find the missing problem numbers
# max_problem_number = max(problem_numbers)
# all_problem_numbers = set(range(1, max_problem_number + 1))
# missing_problem_numbers = all_problem_numbers - set(problem_numbers)

# # Print missing problem numbers
# if missing_problem_numbers:
#     print("Missing problem numbers:", sorted(missing_problem_numbers))
# else:
#     print("No problem numbers are missing.")

################################################

# import subprocess
# import os

# # Define the directory to work with
# directory_path = '/Users/dsanagaram/Documents/GitHub/SPOC/running_test_cases/run_unique_tests_1k_out'

# # Command to generate sorted_filenames.txt, excluding the file itself from the listing
# sort_command = "ls | grep -v '^sorted_filenames.txt$' | awk -F '_' '{print $0 \" \" $3}' | sort -t ' ' -k2,2n | awk '{print $1}' > sorted_filenames.txt"

# # Run the sort command in the specific directory
# subprocess.run(sort_command, shell=True, cwd=directory_path, check=True)

# # Path to the sorted filenames file
# filename_path = os.path.join(directory_path, 'sorted_filenames.txt')

# # Read the sorted filenames from the file
# with open(filename_path, 'r') as file:
#     filenames = file.readlines()

# # Extract the problem numbers from the filenames
# problem_numbers = [int(name.split('_')[-1].split('.')[0].strip()) for name in filenames]

# # Find the missing problem numbers
# max_problem_number = max(problem_numbers)
# all_problem_numbers = set(range(1, max_problem_number + 1))
# missing_problem_numbers = all_problem_numbers - set(problem_numbers)

# # Print missing problem numbers
# if missing_problem_numbers:
#     print("Missing problem numbers:", sorted(missing_problem_numbers))
# else:
#     print("No problem numbers are missing.")

# # Find files containing 'fail'
# files_with_fail = []
# for root, dirs, files in os.walk(directory_path):
#     for file in files:
#         if file != 'sorted_filenames.txt':  # Exclude the sorted_filenames.txt
#             file_path = os.path.join(root, file)
#             with open(file_path, 'r', errors='ignore') as f:
#                 if 'fail' in f.read():
#                     files_with_fail.append(file_path)

# # Print the results
# if files_with_fail:
#     print("\nFiles containing 'fail':")
#     for file in files_with_fail:
#         print(file)
# else:
#     print("\nNo files containing 'fail' were found.")

################################################

import subprocess
import os
import re

# Define the directory to work with
directory_path = '/Users/dsanagaram/Documents/GitHub/SPOC/running_test_cases/run_unique_tests_1k_out'

# Command to generate sorted_filenames.txt, excluding the file itself from the listing
sort_command = "ls | grep -v '^sorted_filenames.txt$' | awk -F '_' '{print $0 \" \" $3}' | sort -t ' ' -k2,2n | awk '{print $1}' > sorted_filenames.txt"

# Run the sort command in the specific directory
subprocess.run(sort_command, shell=True, cwd=directory_path, check=True)

# Path to the sorted filenames file
filename_path = os.path.join(directory_path, 'sorted_filenames.txt')

# Read the sorted filenames from the file
with open(filename_path, 'r') as file:
    filenames = file.readlines()

# Extract the problem numbers from the filenames
problem_numbers = [int(name.split('_')[-1].split('.')[0].strip()) for name in filenames]

# Calculate and print the ratio of missing problem numbers
max_problem_number = max(problem_numbers)
total_problem_numbers = set(range(1, max_problem_number + 1))
missing_problem_numbers = total_problem_numbers - set(problem_numbers)
missing_ratio = len(missing_problem_numbers) / max_problem_number
print(f"Missing problem numbers: {sorted(missing_problem_numbers)}")
print(f"Ratio of missing problem numbers to total problem numbers: {missing_ratio:.2f}")

# Initialize lists for files containing 'fail' and 'timed out'
files_with_fail = []
files_with_timed_out = []

# Reset total_files to 0
total_files = 0

# Ensure we only increment total_files for relevant test files
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file != 'sorted_filenames.txt':  # Exclude the sorted_filenames.txt
            total_files += 1  # Count each relevant file
            file_path = os.path.join(root, file)
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
                if 'fail' in content:
                    files_with_fail.append(file_path)
                if 'timed out' in content:
                    files_with_timed_out.append(file_path)

# Calculate and print ratios
fail_ratio = len(files_with_fail) / total_files
timed_out_ratio = len(files_with_timed_out) / total_files
print(f"\nFiles containing 'fail': {files_with_fail}")
print(f"Ratio of files containing 'fail' to total test runs: {fail_ratio:.2f}")
print(f"\nFiles containing 'timed out': {files_with_timed_out}")
print(f"Ratio of files containing 'timed out' to total test runs: {timed_out_ratio:.2f}")
