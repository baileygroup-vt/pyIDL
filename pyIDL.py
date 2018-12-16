# pyIDL.py
# This is an experimental program, use with discretion.
# Author: Gaeron Friedrichs gaeron@vt.edu
# Advisor: Dr. Scott Bailey
# Updated: 12.16.18
#----------------------------------------------------------#
import sys


# Determines whether a line contains a given statement
def has(line, statement): return line.find(statement) != -1

# Determines whether a line is a for loop
def isFor(line): return line.lstrip().find("for") == 0

# Determines whether the given statement is an IDL comment
def isIDLComment(line): return line.lstrip().find(";") == 0

# Determines whether the given statement is a python comment
def isPythonComment(line): return line.lstrip().find("#") == 0

# Determines whether the given statement has a python comment
def hasPythonComment(line): return line.find("#") != -1

# Determines whether the given statement has an IDL comment
def hasIDLComment(line): return line.find(";") != -1

# Determines if statement 1 is before statement 2 if statement 1 is in the line
def isBefore(line, statement1, statement2): return (line.find(statement1) < line.find(statement2)) and (line.find(statement1) != -1)

# Strips away the python comment from a line
def getPyCommentless(line): return line.split("#")[0]

# Strips away everything but the python comment from a line
def getPyComment(line): return line.split("#")[len(line.split("#")) - 1] if hasPythonComment(line) else ""

# Converts comment from IDL to python
def convertComments(line): return line.replace(";", "#")

# Add leading whitespace
def addLeadingWhitespace(line, whitespace): return (4*whitespace)*" " + line

# Removes variable from a line containing an equals sign
def getVariable(line): return line.split("=")[0].strip()

# Determines if an expression given is a variable
def isVar(expression): return (len(expression.split(" ")) == 1 and len(expression.split("[")) == 1)

# Converts the IDL style equality operators to Python
def convertEqualityOperators(line):
    if isBefore(line, " gt ", ";") or not hasIDLComment(line): line = line.replace(" gt ", " > ")
    if isBefore(line, " lt ", ";") or not hasIDLComment(line): line = line.replace(" lt ", " < ")
    if isBefore(line, " eq ", ";") or not hasIDLComment(line): line = line.replace(" eq ", " == ")
    if isBefore(line, " le ", ";") or not hasIDLComment(line): line = line.replace(" le ", " <= ")
    if isBefore(line, " ge ", ";") or not hasIDLComment(line): line = line.replace(" ge ", " >= ")
    if isBefore(line, " ne ", ";") or not hasIDLComment(line): line = line.replace(" ne ", " != ")
    return line

# Removes IDL end statements
def removeEndStatements(line):
    line = line.replace("endif", "")
    line = line.replace("endfor", "")
    return line

# Replaces IDL then statements to colons
def convertThenStatements(line, whitespace):
    # Then begin case:
    if isBefore(line, "then begin", ";") or not hasIDLComment(line):     
        line = line.replace(" then begin ", ":")
        line = line.replace("then begin", ":")
    # Then stop case:
    if (isBefore(line, "then stop", ";") or not hasIDLComment(line)) and has(line, "then stop"):
        line = line.replace("\n", "")
        line = line.replace("," , " ", 1)
        extension = ""
        if has(line, " then stop "):
            extension = "\")\n" + ((4*whitespace + 4))*" " + "exit()\n"     
        line = line.replace(" then stop ", ":\n" + ((4*whitespace + 4))*" "+ "print(\"") + extension
        if has(line, "then stop"):
            extension = "\")\n" + ((4*whitespace + 4))*" " + "exit()\n" 
        else:
            extension = ""
        line = line.replace("then stop", ":\n" + ((4*whitespace + 4))*" "+ "print(\"") + extension
    # Then case:
    if isBefore(line, "then", ";") or not hasIDLComment(line):
        line = line.replace(" then ", ": ")
        line = line.replace("then", ": ")
    # Do begin case:
    if isBefore(line, "do begin", ";") or not hasIDLComment(line):
        line = line.replace(" do begin ", ":")
        line = line.replace("do begin", ":" )
    return line

# Convert an IDL for loop to Python for Loop
def convertFor(line):
    line = line.replace("for", "") # strip away the for and colon
    line = line.replace(":", "")
    components = line.split(",") # break the line down into its components
    # 2 Parameter For Loop Case:
    if len(components) == 2:
        # Extract the components individually
        variable = components[0].split("=")
        variable_name = variable[0].strip()
        variable_start = variable[1].strip()
        variable_end = components[1].strip()
        #Rewrite in python format
        line = "for " + variable_name + " in range(" + variable_start + ", " + variable_end + "+1):\n"
        line = line.replace("-1+1", "") #accomodate any index magic
        return line, variable_name
    # Non 2 parameter for loop case:
    else:
        return line + "# ADD FUNCTIONALITY", None

# Convert IDL math functions to numpy and python syntax
def convertMath(line):
    line = line.replace("exp(", "numpy.exp(")
    line = line.replace("alog10(", "numpy.log10(")
    line = line.replace("alog(", "numpy.log(")
    line = line.replace("dblarr(", "numpy.zeroes(")
    line = line.replace("n_elements(", "len(")
    line = line.replace("findgen(", "numpy.arange(")
    line = line.replace("fltarr(", "numpy.zeroes(")
    line = line.replace("^", "**")
    return line

# Covert parenthesis to brackets for first layer of index conversion    
def convertIndicies(line, variables):
    for variable in variables:
        line = line.replace("(" + variable.strip() + ")", "[" + variable.strip() + "]")
    return line

# Convert and/or gate functions     
def convertGate(line):
    line = line.replace(" and ", " & ")
    line = line.replace(" or ", " | ")
    return line

# Expands single line variable declaration to multi line
def singleToMulti(line, whitespace):
    without_Comment = getPyCommentless(line) #removes the comment
    # Checks if it is multii line variable declaration format
    if (len(without_Comment.split("=")) == len(without_Comment.split("&")) + 1) and len(without_Comment.split("&")) != 1:
        chunks = without_Comment.split("&") # Extracts all variable declarations
        comment = getPyComment(line) # Extracts original comment
        line = chunks.pop(0) + "\n"  # Add the first declaration
        # Add all the remaining declarations
        for declaration in chunks:
            line = line + (4*whitespace)*" " + declaration.strip() + "\n"
        line = line + (4*whitespace)*" " + "#" + comment # Add back in the comment
    return line

# Extracts scientific notation from IDL statements
def extractSci(line, loc):
    root_bool = False
    exp_bool = False
    root = None
    exp = None
    root_loc = loc-1
    exp_loc = loc+1
    
    # Extract the base/root
    while root_loc > 0:
        try:
            root = float(line[root_loc:loc])
            root_bool = True
            root_loc = root_loc - 1
        except:
            break

    # Extract the exponential 
    while exp_loc < len(line):
        try:
            exp = float(line[loc+1:exp_loc])
            exp_bool = True
            exp_loc = exp_loc + 1
        except:
            if (exp_loc - loc) <= 2:
                exp_loc = exp_loc +1
            else:
                break  

    return (root_bool and exp_bool), str(root), str(exp), root_loc, exp_loc

# Converts scientific notation
def convertScientificNotation(line):
    index = 0
    # Loop through the entire line
    while index < len(line):
        # Find the next location of "d"
        loc = line.find("d", index)
        # If it isn't valid, bail
        if loc == -1 or loc == len(line):
            break
        # If it is valid
        if loc is not 0:
            # Extract its propterties
            is_scientific, root, exp, root_loc, exp_loc = extractSci(line, loc)
            if is_scientific:
                line = line.replace(line[root_loc+1:exp_loc-1], " (" + root+"e"+exp + ") ")
        index = loc + 1
    return line    

# Replace IDL's keyword set functionality
def replaceKeywordSet(line):
    keyword_loc = line.find("keyword_set")
    close_loc = line.find(")", keyword_loc)
    not_loc = line.find("not", keyword_loc - 4)
    if (not_loc == keyword_loc - 4) and (not_loc != -1): line = line[:not_loc] + line[not_loc+4:close_loc] + " is not None" + line[close_loc:]
    else: line = line[:close_loc] + " is None" + line[close_loc:] 
    return line.replace("keyword_set", "")

# Determines the end parenthesis given a line (for where conversion)
def findZeroCrossing(line):
    starting_index = line.find("where")
    index = starting_index + len("where")
    count = 0
    #print(line.rstrip()[:-1])
    while index < (len(line.rstrip())-1):
        if line[index] == "(": count = count + 1
        if line[index] == ")": count = count - 1        

        if count == 0: return index

        index = index + 1

    return -1

# Converts IDL's where functionality 
def convertWhere(line, whitespace):
    flag = False
    extension = None
    if line.find(",") != -1 and line.find(")", line.find(",") != -1):
        extension = line[line.find(",")+1:line.find(")")]
        flag = True

    if findZeroCrossing(getPyCommentless(line)) == -1:
        variable = getVariable(line)
        statement = getPyCommentless(line)
        comment = getPyComment(line).replace("\n", "")

        line = statement.rstrip() + ".nonzero()\t#" + comment + "\n"
        line = line + (4*whitespace)*" " + variable + " = " + variable + "[0]\n"
    else:
        to_split = getPyCommentless(line)[findZeroCrossing(getPyCommentless(line)) + 1:]
        original = getPyCommentless(line)[0:findZeroCrossing(getPyCommentless(line))+1]
        
        variable = getVariable(original)
        statement = getPyCommentless(original)
        comment = getPyComment(original).replace("\n", "")

        line = statement.rstrip() + ".nonzero()\t#" + comment + "\n"
        line = line + (4*whitespace)*" " + variable + " = " + variable + "[0]"
        line = line + to_split.lstrip().replace("& ", "\n" + (4*whitespace)*" ") + "\n"

    if flag: line = line.replace(","+extension, "") + (4*whitespace)*" " + extension.strip() + " = len(" + variable + ")\n"
  
    return line.replace("where", "")


def commonHandle(line):
    total_line = ""
    chunks = None
    if(line.lstrip().find("common") == 0): 
        seg = line.lstrip()[0:line.lstrip().find(",")]
        line = line.replace(seg, "def initialize():\n")
        line = line.replace("$", "")
        chunks = line.split(",")
        total_line = chunks.pop(0)
    if not chunks: chunks = line.replace("$","").split(",")
    for chunk in chunks:
        if not chunk.isspace(): 
            total_line = total_line + "\tglobal " + chunk.lstrip().rstrip() + "\n\t" + chunk.lstrip().rstrip() + " = None \n\n"
    return total_line

def commonBlock(line):
    if line[0] == "@":
        block_name = line[1:line.find(".prg")]
        line = line.replace("@", "import ")
        line = line.replace(".prg", ".py\n")
        line = line + block_name + ".initialize()"
    return line

def convertLine_prg(line, flag, offset, last_white, original, variables):
    temp_line = line    # This is just to save a copy of our original line
    more_var = None     # Default to no additional variables
    whitespace = len(line) - len(line.lstrip()) # Track whitespace
    
    if flag: whitespace = whitespace - offset   # Flag dictates when we start removing whitespace offset
    return_original = whitespace                # Track original whitespace

    # If there are some inconsistencies, adjust
    if original != whitespace:
        while (whitespace-last_white) >= 2 and last_white >= 0:
            whitespace = whitespace-1
    else: whitespace = last_white
    
                        
    line = line.lstrip()                    # Remove leading whitespace
    line = convertComments(line)            # Convert comments from ; to # MUST BE AFTER EQ OP AND thenCONV 
    line = addLeadingWhitespace(line, whitespace)   # Add back in the proper whitespace
    
    if not (isPythonComment(line)): line = commonHandle(line)

    return line, whitespace, return_original, variables   


# Main driver for line conversion
def convertLine(line, flag, offset, last_white, original, variables):
    temp_line = line    # This is just to save a copy of our original line
    more_var = None     # Default to no additional variables
    whitespace = len(line) - len(line.lstrip()) # Track whitespace
    
    if flag: whitespace = whitespace - offset   # Flag dictates when we start removing whitespace offset
    return_original = whitespace                # Track original whitespace

    # If there are some inconsistencies, adjust
    if original != whitespace:
        while (whitespace-last_white) >= 2 and last_white >= 0:
            whitespace = whitespace-1
    else: whitespace = last_white
    
                        
    line = line.lstrip()                    # Remove leading whitespace
    line = commonBlock(line)
    line = convertEqualityOperators(line)   # Convert the equality operators (ge, le, etc.)
    line = removeEndStatements(line)        # Remove the end statements 
    line = convertThenStatements(line, whitespace)  # Remove the then statements and replace with colons 
    line = convertMath(line)                # Replace the math to numpy functionality
    line = convertGate(line)                # Replace and/or
    line = convertComments(line)            # Convert comments from ; to # MUST BE AFTER EQ OP AND thenCONV 

    if isBefore(line, "d", "#"): line = convertScientificNotation(line)     # Convert the double precision scientific notation
    if isBefore(line, "where", "#") or (not hasPythonComment(line) and has(line, "where")): line = convertWhere(line, whitespace)
        # Write for multiparameter where
        # Write for multi-statement lines including where
    if isFor(line): line, more_var = convertFor(line)
    if has(line, "keyword_set"): line = replaceKeywordSet(line)
    if more_var not in variables and more_var is not None: variables.append(more_var)     # Track and append new variables
    
    line = singleToMulti(line, whitespace)
    line = convertIndicies(line, variables)         # Convert indicies from parenthesis to bracketts
    line = addLeadingWhitespace(line, whitespace)   # Add back in the proper whitespace
    
    return line, whitespace, return_original, variables

# Determine if its only a variable rather than method
def isOnlyVar(var, line):
    if getPyCommentless(line).find(var) == -1: return False
    location = -1
    locations = []
    while True:
        location = getPyCommentless(line).find(var, location + 1)
        if location == -1: break
        locations.append(location)

    for loc in locations:
        if loc == 0: return True
        character_value = ord(line[loc-1])
        if not ((character_value <= 122 and character_value >= 97) 
            or (character_value <= 90 and character_value >= 65) 
            or (character_value <= 57 and character_value >= 48) 
            or (character_value == 44)
            or (character_value == 46)
            or (character_value == 95)):
            return True

    return False

# Changes parenthesis to brackets thouroughly
def bracketize(line, var):
    loc = -1
    locations = []
    while True:
        loc = getPyCommentless(line).find(var+"(", loc+1)
        if loc == -1: break
        if(loc != 0):
            character_value = ord(line[loc-1])
            if not ((character_value <= 122 and character_value >= 97) 
                or (character_value <= 90 and character_value >= 65) 
                or (character_value <= 57 and character_value >= 48) 
                or (character_value == 44)
                or (character_value == 46)
                or (character_value == 95)):
                locations.append(loc)
        else: locations.append(loc)

    for loc in locations:
        line = line.replace(var+"(", var+"[", 1)
        index = loc + 1
        count = 1
        while count != 0:
            if  line[index] == "(" : count = count + 1
            if line[index] == ")" : count = count - 1
            index = index + 1
        line = line[:index-1] + "]" + line[index:]
    return line 

# Driver for index conversion
def variableIndexConversion(line, variables):
    count = 0
    new_var = []
    for var in variables: 
        if isOnlyVar(var, line): line = bracketize(line, var)
    return line

# Extracts variables from a given line
def extractVar(line):
    variable = None
    if has(getPyCommentless(line), "if ") and not (len(getPyCommentless(line).strip())-1) == getPyCommentless(line).strip().find(":"):
        variable = line[line.find(":")+1:line.find("=", line.find(":"))].strip()
    elif has(getPyCommentless(line), " = "): variable = getPyCommentless(line).split(" = ")[0].strip()
    return variable

# Runs the conversion for a given file    
def run_pro(input_file):
    imports = ["import numpy\n"]
    input_gather = []   #List to hold the translated lines
    variables = []      #List of variables
    flag = False        #Flag that looks for the first non-commented line
    last_white = 0      #Last Whitespace
    offset = 0          #Code whitespace offset
    original = 0        #Original Whitespace

    # Open Input File
    with open(input_file, "r") as idl_code:
        for line in idl_code:
            if line.strip():     
                if (not flag) and (line.lstrip()[:1] != ";") and (line.lstrip()[:1] != "#"):
                    flag = True
                    offset = len(line) - len(line.lstrip())                   
                line, last_white, original, variables = convertLine(line, flag, offset, last_white, original, variables)
            input_gather.append(line)
               
    # Convert I/O file extension
    if(input_file.find(".pro") != -1):
        try: output_file = input_file.replace(".pro", ".py")
        except: print("Something went wrong with the file name.")
    elif(input_file.find(".prg") != -1):
        try: output_file = input_file.replace(".prg", ".py")
        except: print("Something went wrong with the file name.")
    else: print("No valid file extension.")

    # Write to File
    with open(output_file, "w") as python_code:
        for import_statement in imports: python_code.write(import_statement)
        for line in input_gather: python_code.write(line)

    input_gather = []
    with open(output_file, "r") as py_code: 
        for line in py_code: 
            var = extractVar(line)
            if var not in variables and var is not None and isVar(var): variables.append(extractVar(line))
            input_gather.append(line)

    output_gather = []

    #Convert all the indicies
    for line in input_gather: 
        to_add = line
        if getPyCommentless(line).strip() and line.strip():
            to_add = variableIndexConversion(line, variables) 
        output_gather.append(to_add)

    # Re write the file
    with open(output_file, "w") as python_code:
        for line in output_gather: python_code.write(line)


def run_prg(input_file):
    input_gather = []   #List to hold the translated lines
    variables = []      #List of variables
    flag = False        #Flag that looks for the first non-commented line
    last_white = 0      #Last Whitespace
    offset = 0          #Code whitespace offset
    original = 0        #Original Whitespace    # Open Input File
    
    with open(input_file, "r") as idl_code:
        for line in idl_code:
            if line.strip():     
                if (not flag) and (line.lstrip()[:1] != ";") and (line.lstrip()[:1] != "#"):
                    flag = True
                    offset = len(line) - len(line.lstrip())                   
                line, last_white, original, variables = convertLine_prg(line, flag, offset, last_white, original, variables)
            input_gather.append(line)
               
    # Convert I/O file extension
    if(input_file.find(".prg") != -1):
        try: output_file = input_file.replace(".prg", ".py")
        except: print("Something went wrong with the file name.")
    else: print("No valid file extension.")

    # Write to File
    with open(output_file, "w") as python_code:
        for line in input_gather: python_code.write(line)


# Runs a list of files        
def multiRun(input_list): 
    for file in input_list: 
        if(file.find(".pro")!= -1): run_pro(file)
        else: run_prg(file)


if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) < 3:
        print("Error: Invalid Number of Command Line Arguments")
    elif len(arguments) >= 3:
        if arguments[1] == "-f" or arguments[1] == "--singlefile":
            print(arguments[2] + " translation: Started")
            if(arguments[2].find(".pro")!= -1): run_pro(arguments[2])
            else: run_prg(arguments[2])
            print(arguments[2] + " translation: Complete")
        elif arguments[1] == "-m" or arguments[1] == "--multifile":
            files = arguments[2:]
            for file in files:
                print("---------------------------------------------")
                print(file + " translation: Started")
                if(file.find(".pro")!= -1): run_pro(file)
                else: run_prg(file)
                print(file + " translation: Complete")
        else:
            print("Error: Invalid Conversion Operator")


# TO DO
# Add command line parsing functionality
    # Support folder run

#Add robustness to multi line 

# Common blocks just need to be global variables.
# assume they are assigned somewhere else

# Add functionality to support importing common blocks