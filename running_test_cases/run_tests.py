import subprocess

def run_test_cases(code, test_cases_file, output_file_path):
    with open(test_cases_file, 'r') as f:
        file_content = f.read()
    
    # Normalize line endings to Unix style
    file_content = file_content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Splitting the file content into parts based on '###ENDINPUT###' and '###ENDOUTPUT###'
    test_case_parts = file_content.split('###ENDOUTPUT###')
    test_cases = []

    for part in test_case_parts:
        if part.strip():  # Ensure part is not just whitespace
            input_data, expected_output = part.split('###ENDINPUT###')
            input_data = input_data.strip()
            expected_output = expected_output.strip()
            test_cases.append((input_data, expected_output))

    with open(output_file_path, 'w') as outfile:  # Open an output file to write the results
        for input_data, expected_output in test_cases:
            proc = subprocess.run(
                ["clang++", "-o", "program", "-x", "c++", "-"],
                input=code,
                text=True,
                capture_output=True
            )
            if proc.returncode != 0:
                outfile.write("Compilation Error: " + proc.stderr + "\n")
                return

            proc = subprocess.run(
                ["./program"],
                input=input_data,
                text=True,
                capture_output=True
            )
            if proc.returncode != 0:
                outfile.write("Runtime Error: " + proc.stderr + "\n")
                return

            output = proc.stdout.strip()
            if output == expected_output:
                outfile.write(f"Test case passed: Input({input_data}) => Output({output})\n")
            else:
                outfile.write(f"Test case failed: Input({input_data}) => Output({output}), Expected({expected_output})\n")

# Example usage:
# Read the C++ code from the file
with open('code.cpp', 'r') as file:
    code = file.read()

# Specify the file path for test cases
test_cases_file = 'test_cases.txt'

# Specify the output file path
output_file_path = 'test_output.txt'

run_test_cases(code, test_cases_file, output_file_path)
