# import subprocess

# def run_test_cases(code, test_cases_file, output_file_path):
#     with open(test_cases_file, 'r') as f:
#         file_content = f.read()
    
#     # Normalize line endings to Unix style
#     file_content = file_content.replace('\r\n', '\n').replace('\r', '\n')
    
#     # Splitting the file content into parts based on '###ENDINPUT###' and '###ENDOUTPUT###'
#     test_case_parts = file_content.split('###ENDOUTPUT###')
#     test_cases = []

#     for part in test_case_parts:
#         if part.strip():  # Ensure part is not just whitespace
#             input_data, expected_output = part.split('###ENDINPUT###')
#             input_data = input_data.strip()
#             expected_output = expected_output.strip()
#             test_cases.append((input_data, expected_output))

#     with open(output_file_path, 'w') as outfile:  # Open an output file to write the results
#         for input_data, expected_output in test_cases:
#             proc = subprocess.run(
#                 ["clang++", "-o", "program", "-x", "c++", "-"],
#                 input=code,
#                 text=True,
#                 capture_output=True
#             )
#             if proc.returncode != 0:
#                 outfile.write("Compilation Error: " + proc.stderr + "\n")
#                 return

#             proc = subprocess.run(
#                 ["./program"],
#                 input=input_data,
#                 text=True,
#                 capture_output=True
#             )
#             if proc.returncode != 0:
#                 outfile.write("Runtime Error: " + proc.stderr + "\n")
#                 return

#             output = proc.stdout.strip()
#             if output == expected_output:
#                 outfile.write(f"Test case passed: Input({input_data}) => Output({output})\n")
#             else:
#                 outfile.write(f"Test case failed: Input({input_data}) => Output({output}), Expected({expected_output})\n")

# # Example usage:
# # Read the C++ code from the file
# with open('code.cpp', 'r') as file:
#     code = file.read()

# # Specify the file path for test cases
# test_cases_file = 'test_cases.txt'

# # Specify the output file path
# output_file_path = 'test_output.txt'

# run_test_cases(code, test_cases_file, output_file_path)

#######################################
# import subprocess
# import argparse

# def run_test_cases(code_file, test_cases_file, output_file_path):
#     with open(code_file, 'r') as f:
#         code = f.read()

#     with open(test_cases_file, 'r') as f:
#         file_content = f.read()

#     # Normalize line endings to Unix style
#     file_content = file_content.replace('\r\n', '\n').replace('\r', '\n')
    
#     # Splitting the file content into parts based on '###ENDINPUT###' and '###ENDOUTPUT###'
#     test_case_parts = file_content.split('###ENDOUTPUT###')
#     test_cases = []

#     for part in test_case_parts:
#         if part.strip():  # Ensure part is not just whitespace
#             input_data, expected_output = part.split('###ENDINPUT###')
#             input_data = input_data.strip()
#             expected_output = expected_output.strip()
#             test_cases.append((input_data, expected_output))

#     with open(output_file_path, 'w') as outfile:  # Open an output file to write the results
#         for input_data, expected_output in test_cases:
#             proc = subprocess.run(
#                 ["clang++", "-o", "program", "-x", "c++", "-"],
#                 input=code,
#                 text=True,
#                 capture_output=True
#             )
#             if proc.returncode != 0:
#                 outfile.write("Compilation Error: " + proc.stderr + "\n\n")
#                 return

#             proc = subprocess.run(
#                 ["./program"],
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

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run test cases for a given program.")
#     parser.add_argument("code_file", help="The path to the C++ code file.")
#     parser.add_argument("test_cases_file", help="The path to the test cases file.")
#     parser.add_argument("output_file", help="The path where the output will be saved.")

#     args = parser.parse_args()

#     run_test_cases(args.code_file, args.test_cases_file, args.output_file)
##########################

# import subprocess
# import argparse
# import re

# # Function to detect and add missing includes and possibly "using namespace std;"
# def add_missing_includes(code):
#     STANDARD_LIBRARIES = {
#         'iostream': 'iostream',
#         'vector': 'vector',
#         'string': 'string',
#         'map': 'map',
#         'set': 'set',
#         'queue': 'queue',
#         'stack': 'stack',
#         'algorithm': 'algorithm',
#         'cmath': 'cmath',
#         'numeric': 'numeric',
#     }

#     includes = set()
#     for component, header in STANDARD_LIBRARIES.items():
#         if re.search(r'\bstd::' + component + r'\b', code) or re.search(r'\b' + component + r'\b', code):
#             includes.add('#include <' + header + '>')

#     existing_includes = set(re.findall(r'#include <(.+)>', code))
#     new_includes = list(includes - existing_includes)
    
#     if new_includes:
#         code = '\n'.join(sorted(new_includes)) + '\n\n' + code
    
#     if 'using namespace std;' not in code and any(ns in code for ns in ['std::', 'using namespace std;']):
#         code = 'using namespace std;\n\n' + code

#     return code

# def run_test_cases(code_file, test_cases_file, output_file_path):
#     with open(code_file, 'r') as f:
#         code = f.read()

#     # Preprocess the code to add missing includes and namespaces
#     code = add_missing_includes(code)

#     with open(test_cases_file, 'r') as f:
#         file_content = f.read()

#     # Normalize line endings to Unix style
#     file_content = file_content.replace('\r\n', '\n').replace('\r', '\n')
#     # Splitting the file content into parts
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
#                 ["clang++", "-o", "program", "-x", "c++", "-"],
#                 input=code,
#                 text=True,
#                 capture_output=True
#             )
#             if proc.returncode != 0:
#                 outfile.write("Compilation Error: " + proc.stderr + "\n\n")
#                 return

#             proc = subprocess.run(
#                 ["./program"],
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

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run test cases for a given program.")
#     parser.add_argument("code_file", help="The path to the C++ code file.")
#     parser.add_argument("test_cases_file", help="The path to the test cases file.")
#     parser.add_argument("output_file", help="The path where the output will be saved.")

#     args = parser.parse_args()

#     run_test_cases(args.code_file, args.test_cases_file, args.output_file)
