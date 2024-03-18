import json

full_text = ""
full_code = ""
problem_id =""
data = []

# train-test dataset 
#path = r'C:\Users\nancy\OneDrive\Desktop\SPoC\script\train-test.txt' 

path = r'C:\Users\nancy\OneDrive\Desktop\SPoC\script\train.txt'
output_file = "train-dataset.json"


def add_indents(i, str):
    result = ""
    if i != 0:
        spaces = " " * 2 * i
        result += spaces
    result += str
    return result


with open(path) as file:
    for line in file:
        split = line.split('\t')
        for s in split:
            text = split[0]
            code = split[1]
            line_num = int(split[5])
            indent = int(split[6])
        if (line_num == 0):
            d = {"Psuedocode": full_text, "Code": full_code, "Test Case": problem_id}
            data.append(d)
            
            full_text = ""
            full_code = ""
    
        full_text += add_indents(indent,text) + "\n"
        full_code += add_indents(indent,code) + "\n"
        problem_id = split[3]

with open(output_file, "a") as outfile:
    json.dump(data, outfile, indent = 4)
    




