# import subprocess

# def include_header_in_cpp_file(cpp_file_path, header_file="CommonLibs.h"):
#     with open(cpp_file_path, 'r+') as file:
#         content = file.readlines()
        
#         # Check if the header is already included
#         header_include = f'#include "{header_file}"\n'
#         if header_include in content:
#             print(f"The file {header_file} is already included.")
#             return False  # Indicate that no inclusion was needed
#         else:
#             content.insert(0, header_include)
            
#         # Go to the start of the file to write the updated content
#         file.seek(0)
#         file.writelines(content)
#         print(f"Added {header_file} to {cpp_file_path}.")
#         return True  # Indicate that the file was modified

# def run_test_cases(compiled_executable, test_cases_file, output_file_path):
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

# if __name__ == "__main__":
#     cpp_file_path = '/Users/dsanagaram/Documents/GitHub/SPOC/running_test_cases/code2_no_fix.cpp'
#     test_cases_file = 'path/to/test_cases_file.txt'  # Update this path
#     output_file_path = 'path/to/output_file.txt'  # Update this path

#     # Include the header in the cpp file if not already included
#     if include_header_in_cpp_file(cpp_file_path):
#         # Compile the modified cpp file
#         compile_proc = subprocess.run(
#             ["clang++", "-o", "program", cpp_file_path],
#             capture_output=True
#         )
#         if compile_proc.returncode != 0:
#             print("Compilation Error:", compile_proc.stderr.decode())
#         else:
#             # Run the test cases on the compiled executable
#             run_test_cases("./program", test_cases_file, output_file_path)



import subprocess
import argparse

def include_header_in_cpp_file(cpp_file_path, header_file="CommonLibs.h"):
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run test cases for a given C++ program.")
    parser.add_argument("cpp_file_path", help="The path to the C++ code file.")
    parser.add_argument("test_cases_file", help="The path to the test cases file.")
    parser.add_argument("output_file_path", help="The path where the output will be saved.")

    args = parser.parse_args()

    # Include the header in the cpp file if not already included
    if include_header_in_cpp_file(args.cpp_file_path):
        # Compile the modified cpp file
        compile_proc = subprocess.run(
            ["clang++", "-o", "program", args.cpp_file_path],
            capture_output=True
        )
        if compile_proc.returncode != 0:
            print("Compilation Error:", compile_proc.stderr.decode())
        else:
            # Run the test cases on the compiled executable
            run_test_cases("./program", args.test_cases_file, args.output_file_path)
