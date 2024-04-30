import pandas as pd

test_case = "1A"
path = r"C:\Users\nancy\OneDrive\Desktop\SPoC\data\testcases\\" + test_case + "\\" + test_case + ".txt"

inputs =[]
outputs = []
with open(path) as file:
    lines = file.readlines()
    input = []
    output = []
    is_input = True

    for line in lines:
        if line.strip() == "###ENDINPUT###":
            is_input = False
            if (input != []):
                inputs.append(input)
                input = []

        elif line.strip() == "###ENDOUTPUT###":
            is_input = True
            if (output != []):
                outputs.append(output)
                output = []
        elif is_input:
            inputs.append(line.strip())
        else:
            outputs.append(line.strip())

df = pd.DataFrame({"Input": inputs, "Output": outputs})
excel_path = "test_case" + test_case + ".xlsx"
df.to_excel(excel_path, index=False)