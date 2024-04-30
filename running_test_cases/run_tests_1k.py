import csv
import subprocess
import argparse
import tempfile
import os

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
            proc = subprocess.run(
                [compiled_executable],
                input=input_data,
                text=True,
                capture_output=True
            )
            if proc.returncode != 0:
                outfile.write("Runtime Error: " + proc.stderr + "\n\n")
                return

            output = proc.stdout.strip()
            if output == expected_output:
                outfile.write(f"Test case passed: Input({input_data}) => Output({output})\n\n")
            else:
                outfile.write(f"Test case failed: Input({input_data}) => Output({output}), Expected({expected_output})\n\n")

def process_csv(csv_file_path, testcases_base_path, output_dir):
    max_rows = 10
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        next(reader, None)
        # for _ in range(2):  # Replace 'n' with the number of lines to skip
        #     next(reader)
            
        row_count = 0
        for row in reader:
            if row_count >= max_rows:
                break
            # row = {k: v for k, v in row.items() if k and not k.startswith('Unnamed')}
            code = row['# Test Case']
            print("Code:")
            print(code)
            print("\n") 
            problem_id = row['Input']
            print("Problem Id: ")
            print(problem_id)
            print("\n")
            
            # Adjusted to the new directory structure
            testcase_folder_path = os.path.join(testcases_base_path, problem_id)
            test_cases_file = os.path.join(testcase_folder_path, f"{problem_id}_testcases.txt")

            # Check if the test cases file exists
            if not os.path.isfile(test_cases_file):
                print(f"Test cases file for Problem ID {problem_id} does not exist. Skipping.")
                continue

            # Create a temporary .cpp file for the code snippet
            with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode='w+') as temp_cpp_file:
                cpp_file_path = temp_cpp_file.name
                temp_cpp_file.write(code)

            # Construct the output file path
            output_file_path = os.path.join(output_dir, f"{problem_id}_output.txt")
            
            # Ensure the header is included in the CPP file
            if include_header_in_cpp_file(cpp_file_path):
                # Compile the modified cpp file
                compile_proc = subprocess.run(
                    ["clang++", "-o", "program", cpp_file_path],
                    capture_output=True
                )
                if compile_proc.returncode != 0:
                    print(f"Compilation Error for Problem ID {problem_id}:", compile_proc.stderr.decode())
                else:
                    # Run the test cases on the compiled executable
                    run_test_cases("./program", test_cases_file, output_file_path)
            
            # Cleanup: Remove the temporary .cpp file
            os.remove(cpp_file_path)
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
