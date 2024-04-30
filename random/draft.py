#import tsv file
#with open(r'C:\Users\nancy\OneDrive\Desktop\SPoC\data\train\split\spoc-train-test.tsv') as file:
    #for line in file:
        #l=line.split('\t')

#need somewhere to store the organized data
#   --tuple array ({[full text string, full code string]})
#       -- string has indents, separates lines by \n
#   --modified dataframe



#delimit the line into each value
text = "" #index 0
code = "" #index 1
workerid = "" #index 2
probid = "" #index 3
subid = "" #index 4
line = "" #index 5 - cast as int 
indent = "" #index 6 - cast as int

full_text = ""
full_code = ""


#check if it is a new cell of data

# --- line number goes down
def is_new(line):
    if line == 0:
        # want to create new cell of data
        return True 
    else:
        #continue with this cell
        return False

# --- change in sub-id


#add indents - add_indent(indent,text) or add_indent(indent,code)
def add_indents(i, str):
    result = ""
    if indent != 0:
        spaces = " " * 2 * i
        result += spaces
    result += str
    return result

#testing
full_line = "create integer n	int n;	01	1005A	48515762	1	1"
split = full_line.split("\t")
for s in split:
    print(s)

text = split[0]
code = split[1]
indent = int(split[6])
line = int(split[5])
print(add_indents(indent, text))
print(add_indents(indent, code))


#read full line




