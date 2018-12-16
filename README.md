# pyIDL
## IDL to Python converter. Currently supports a command line interface.
## Author: Gaeron Friedrichs

### Usage Overview:
		This program should be used as a tool to jump-start the translation process for projects and 
	files that are written in IDL. It handles a lot of mundane conversions such as replacing comment 
	types, for loop styles, primitive whitespace conversion, and math and logical operators.   

### File Conversion:
	Single File Run
	 		pyIDL.py -f <filename>
	 		pyIDL.py --singlefile <filename>

	Multiple File Run
	 		pyIDL.py -m <filename1> <filename2> ... <filenameX>
	 		pyIDL.py --multifile <filename1> <filename2> ... <filenameX>

### Supported Functionality:
	Math Conversion
	 - exp to numpy.exp
	 - alog10 to numpy.log10
	 - dblarr to numpy.zeroes
	 - n_elements to len
	 - findgen to numpy.arange
	 - fltarr to numpy.zeroes
	 - ^ to ** 

	Logical Conversion
	 - and to &
	 - or to |

	Equality Conversion
	 - gt to >
	 - lt to <
	 - eq to ==
	 - le to <=
	 - ge to >=
	 - me to !=

	Scientific Notation Conversion
	 - Extracts base and exponent and reformats
	 - Example: 1d2 to (1.0e2.0)

	Keyword Set Conversion
	 - Replaces keyword_set with Python's check of variable definition. 
	 - Accounts for double negatives
	 - keyword_set(var) to (var is not None)
	 - not keyword_set(var) to (var is None)

	Where Conversion
	 - Replicates IDL's where() utility
	 - Supports second parameter vector length
	 - Example IDL: 
			k = where(px lt p_h2o, n)
	 - Example Python (shown with equality operators converted):
			k = (px < p_h2o).nonzero()
			k = k[0]
			n = len(k)

	Comment Conversion
	 - Retains all comments and their locations on each line
	 - ;Comment to #Comment

	Single to Multi Conversion
	 - Handles the IDL single line, multi-variable value declaration
	 - Example IDL:
			p1 = 0 & t1 = 0 & p2 = 0 & t2 = 0
	 - Example Python:
			p1 = 0
			t1 = 0
			p2 = 0
			t2 = 0

	For Loop Conversion
	 - Only supports 2 parameter for loops
	 - Removes any presence of -1+1 in the ranging
	 - Example IDL: for i = 0,nk-1 
	 - Example Python: for i in range(0, nk)

	Then Removal and conversion
	 - Removes then begin, do begin, and then. replaces with colon
	 - Removes then stop and replaces with exit()
	 - Removes endif and endfor

	Vector Index Conversion
	 - IDL supports vector indexing with parenthesis
	 - Python supports vector indexing with brackets
	 - This is accomplished by converting all other parts of the file, then recording all the defined variables. 
	 - The file is written, then read back in and all the variables are searched for and bracketized. 
	 - vector(2) to vector[2]
	 - vector1(vector2(3)) to vector1[vector2[3]]

	Whitespace Handling
	 - Peak whitespace handling occurs when IDL code levels are separated by one space
	 - Deviation from this will cause errors as Python is whitespace dependent
	 - Example IDL Code:
	 		code line 1
			 code line 2
			  code line 3
	 - Example Python Code:
			code line 1
				code line 2
					code line 3

	Imports
	 - The only current import is for numpy. 
	 - Any further desired imports should be placed in the imports list				

	 Common Blocks
	 - Supports conversion of common blocks
	 - Creates a file filled with global variables and assigns them to none
	 - The file must be imported and initialized. 
	 - The variable names in the common blocks cannot be python special names

	 Accessing Common Blocks
	 - Accessing a common block assumes the Common Block conversion format
	 - Converts the @ to an import, and appends the initialization
	 - Needs each variable to prefixed with "module."
	 - Example:
	 	- @sample_common.prg 
	 	- import sample_common.py
	 	  sample_common.initialize()
	 	  sample_common.var = 1


### Not Supported:
	 - Method/function headers with inputs/outputs
	 - Return statements

### Quirks:
	 - Clean, organized IDL code and line spacing will yield the best conversion results
	 - The code comments out the function header and thus does not process the variables 
	 that are in that header. In order to bracketize those (potential) vectors, one must
	 write a line like "variable = input" as a place holder somewhere in the code, so 
	 the variables are properly bracketized.

### Adding Functionality:
	This program was created using a minimum-code based approach. A file should be run through
	the conversion process. Methods and functions should be added to support the conversion of 
	the desired IDL functionality until it works generally, and for the specific case being 
	tested against. Performed iteratively, most functionality can be converted.

### To-do:
	 - Refine command-line interface for error-handling
	 - Command line update for directory running
	 - Multiple parameter for loop support
	 - Define variables from #pro header
	 - Handle min/max functions (< and >)
	 - Handle where() with matrix[i,*] conditions
