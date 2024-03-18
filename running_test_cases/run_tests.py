import subprocess

def run_test_cases(code, test_cases_file):
    with open(test_cases_file, 'r') as f:
        file_content = f.read()
    
    # Normalize line endings to Unix style
    file_content = file_content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Splitting the file content into test cases based on '###ENDINPUT###'
    raw_test_cases = file_content.split('###ENDINPUT###')
    test_cases = []

    for case in raw_test_cases:
        if case.strip():  # Ensure case is not just whitespace
            parts = case.split('###ENDOUTPUT###')
            if len(parts) == 2:  # Ensure we have both input and output
                input_data, expected_output = [part.strip() for part in parts]
                test_cases.append((input_data, expected_output))

    for input_data, expected_output in test_cases:
        proc = subprocess.run(
            ["clang++", "-o", "program", "-x", "c++", "-"],
            input=code,
            text=True,
            capture_output=True
        )
        if proc.returncode != 0:
            print("Compilation Error:", proc.stderr)
            return

        proc = subprocess.run(
            ["./program"],
            input=input_data.encode(),
            text=True,
            capture_output=True
        )
        if proc.returncode != 0:
            print("Runtime Error:", proc.stderr)
            return

        output = proc.stdout.strip()
        if output == expected_output:
            print(f"Test case passed: Input({input_data}) => Output({output})")
        else:
            print(f"Test case failed: Input({input_data}) => Output({output}), Expected({expected_output})")

# Read the C++ code from the file
with open('code.cpp', 'r') as file:
    code = file.read()

# Specify the file path for test cases
test_cases_file = 'test_cases.txt'

run_test_cases(code, test_cases_file)
