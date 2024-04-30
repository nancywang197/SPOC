import csv
import subprocess
import argparse
import tempfile
import os
from subprocess import TimeoutExpired


def include_header_in_cpp_file(cpp_file_path, header_file="/Users/dsanagaram/Documents/GitHub/SPOC/running_test_cases/CommonLibs.h"):
    with open(cpp_file_path, 'r+') as file:
        content = file.readlines()
        
        # Check if the header is already included
        header_include = f'#include "{header_file}"\n'
        if header_include in content:
            print(f"The file {header_file} is already included.")
            return False  # Indicate that no inclusion was needed
        else:
            content.insert(0, header_include)
            
        # Go to the start of the file to write the updated content
        file.seek(0)
        file.writelines(content)
        print(f"Added {header_file} to {cpp_file_path}.")
        return True  # Indicate that the file was modified

# def run_test_cases(compiled_executable, test_cases_file, output_file_path):
#     with open(test_cases_file, 'r') as f:
#         file_content = f.read()

#     file_content = file_content.replace('\r\n', '\n').replace('\r', '\n')
#     test_case_parts = file_content.split('###ENDOUTPUT###')
#     test_cases = []

#     for part in test_case_parts:
#         if part.strip():
#             input_data, expected_output = part.split('###ENDINPUT###')
#             input_data = input_data.strip()
#             expected_output = expected_output.strip()
#             test_cases.append((input_data, expected_output))

#     with open(output_file_path, 'w') as outfile:
#         for input_data, expected_output in test_cases:
#             proc = subprocess.run(
#                 [compiled_executable],
#                 input=input_data,
#                 text=True,
#                 capture_output=True
#             )
#             if proc.returncode != 0:
#                 outfile.write("Runtime Error: " + proc.stderr + "\n\n")
#                 return

#             output = proc.stdout.strip()
#             if output == expected_output:
#                 outfile.write(f"Test case passed: Input({input_data}) => Output({output})\n\n")
#             else:
#                 outfile.write(f"Test case failed: Input({input_data}) => Output({output}), Expected({expected_output})\n\n")

#This run_test_cases has a mechanism to timeout if a test run is taking too long(10 s)
def run_test_cases(compiled_executable, test_cases_file, output_file_path):
    with open(test_cases_file, 'r') as f:
        file_content = f.read()

    file_content = file_content.replace('\r\n', '\n').replace('\r', '\n')
    test_case_parts = file_content.split('###ENDOUTPUT###')
    test_cases = []

    for part in test_case_parts:
        if part.strip():
            input_data, expected_output = part.split('###ENDINPUT###')
            input_data = input_data.strip()
            expected_output = expected_output.strip()
            test_cases.append((input_data, expected_output))

    with open(output_file_path, 'w') as outfile:
        for input_data, expected_output in test_cases:
            try:
                proc = subprocess.run(
                    [compiled_executable],
                    input=input_data,
                    text=True,
                    capture_output=True,
                    timeout=10  # Timeout of 10 seconds
                )
            except TimeoutExpired:
                outfile.write(f"Test case timed out: Input({input_data})\n\n")
                continue  # Skip to the next test case

            if proc.returncode != 0:
                outfile.write("Runtime Error: " + proc.stderr + "\n\n")
                return

            output = proc.stdout.strip()
            if output == expected_output:
                outfile.write(f"Test case passed: Input({input_data}) => Output({output})\n\n")
            else:
                outfile.write(f"Test case failed: Input({input_data}) => Output({output}), Expected({expected_output})\n\n")

# def process_csv(csv_file_path, testcases_base_path, output_dir, max_rows=1000):
#     with open(csv_file_path, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         next(reader, None)  # Skip the header or any unwanted rows if necessary
        
#         row_count = 0
#         for row in reader:
#             if row_count >= max_rows:
#                 break
            
#             code = row['# Test Case']
#             problem_id = row['Input']
#             unique_test_id = f"{problem_id}_{row_count}"  # Creating a unique test identifier
            
#             # Adjusted to the new directory structure
#             testcase_folder_path = os.path.join(testcases_base_path, problem_id)
#             test_cases_file = os.path.join(testcase_folder_path, f"{problem_id}_testcases.txt")

#             if not os.path.isfile(test_cases_file):
#                 print(f"Test cases file for Problem ID {problem_id} does not exist. Skipping.")
#                 continue

#             with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode='w+') as temp_cpp_file:
#                 cpp_file_path = temp_cpp_file.name
#                 temp_cpp_file.write(code)

#             output_file_path = os.path.join(output_dir, f"output_{unique_test_id}.txt")
            
#             if include_header_in_cpp_file(cpp_file_path):
#                 executable_name = f"program_{unique_test_id}"  # Store the executable name in a variable for later use
#                 compile_proc = subprocess.run(
#                     ["clang++", "-o", executable_name, cpp_file_path],  # Unique executable name
#                     capture_output=True
#                 )
#                 if compile_proc.returncode != 0:
#                     print(f"Compilation Error for Test ID {unique_test_id}: {compile_proc.stderr.decode()}")
#                 else:
#                     run_test_cases(f"./program_{unique_test_id}", test_cases_file, output_file_path)
#                     os.remove(executable_name)  # Cleanup the executable after running the test cases

#             os.remove(cpp_file_path)  # Cleanup
#             row_count += 1

#This process_csv has a mechanism to skip a test run that was already generated
def process_csv(csv_file_path, testcases_base_path, output_dir, max_rows=15000):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader, None)  # Skip the header or any unwanted rows if necessary
        
        row_count = 0
        for row in reader:
            if row_count >= max_rows:
                break
            
            code = row['# Test Case']
            problem_id = row['Input']
            unique_test_id = f"{problem_id}_{row_count}"  # Creating a unique test identifier

            output_file_path = os.path.join(output_dir, f"output_{unique_test_id}.txt")
            
            # Check if output file already exists; if so, skip to next row
            if os.path.exists(output_file_path):
                print(f"Output file {output_file_path} already exists. Skipping.")
                row_count += 1
                continue

            # Adjusted to the new directory structure
            testcase_folder_path = os.path.join(testcases_base_path, problem_id)
            test_cases_file = os.path.join(testcase_folder_path, f"{problem_id}_testcases.txt")

            if not os.path.isfile(test_cases_file):
                print(f"Test cases file for Problem ID {problem_id} does not exist. Skipping.")
                continue

            with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode='w+') as temp_cpp_file:
                cpp_file_path = temp_cpp_file.name
                temp_cpp_file.write(code)
            
            if include_header_in_cpp_file(cpp_file_path):
                executable_name = f"program_{unique_test_id}"  # Store the executable name in a variable for later use
                compile_proc = subprocess.run(
                    ["clang++", "-o", executable_name, cpp_file_path],  # Unique executable name
                    capture_output=True
                )
                if compile_proc.returncode != 0:
                    print(f"Compilation Error for Test ID {unique_test_id}: {compile_proc.stderr.decode()}")
                else:
                    run_test_cases(f"./{executable_name}", test_cases_file, output_file_path)
                    os.remove(executable_name)  # Cleanup the executable after running the test cases

            os.remove(cpp_file_path)  # Cleanup
            row_count += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run test cases for C++ programs defined in a CSV.")
    parser.add_argument("csv_file_path", help="The path to the CSV file.")
    parser.add_argument("testcases_base_path", help="The base path to the test cases folders.")
    parser.add_argument("output_dir", help="The directory where output files will be saved.")

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    process_csv(args.csv_file_path, args.testcases_base_path, args.output_dir)

