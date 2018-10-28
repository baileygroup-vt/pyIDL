# pyIDL
## IDL to Python converter. Currently supports a command line interface.

### File Conversion:

	> Single File Run
	> 		pyIDL.py -f <filename>
	> 		pyIDL.py --singlefile <filename>

	> Multiple File Run
	> 		pyIDL.py -m <filename1> <filename2> ... <filenameX>
	> 		pyIDL.py --multifile <filename1> <filename2> ... <filenameX>

### Supported Functionality:
	> Math Conversion
	> - exp to numpy.exp
	> - alog10 to numpy.log10
	> - dblarr to numpy.zeroes
	> - n_elements to len
	> - findgen to numpy.arange
	> - fltarr to numpy.zeroes
	> - ^ to \*\* 

	> Logical Conversion
	> - and to &
	> - or to |

	> Equality Conversion
	> - gt to \>
	> - lt to <
	> - eq to ==
	> - le to <=
	> - ge to \>=
	> - me to !=

	> Scientific Notation Conversion
	> - Extracts base and exponent and reformats
	> - Example: 1d2 to (1.0e2.0)

	> Keyword Set Conversion
	> - Replaces keyword_set with Python's check of variable definition. 
	> - Accounts for double negatives
	> - keyword_set(var) to (var is not None)
	> - not keyword_set(var) to (var is None)

	> Where Conversion
	> - Replicates IDL's where() utility
	> - Supports second parameter vector length
	> - Example IDL: 
	>		k = where(px lt p_h2o, n)
	> - Example Python (shown with equality operators converted):
	>		k = (px < p_h2o).nonzero()
	>		k = k[0]
	>		n = len(k)

	> Comment Conversion
	> - Retains all comments and their locations on each line
	> - ;Comment to #Comment

	> Single to Multi Conversion
	> - Handles the IDL single line, multi-variable value declaration
	> - Example IDL:
	>		p1 = 0 & t1 = 0 & p2 = 0 & t2 = 0
	> - Example Python:
	>		p1 = 0
	>		t1 = 0
	>		p2 = 0
	>		t2 = 0

	> For Loop Conversion
	> - Only supports 2 parameter for loops
	> - Removes any presence of -1+1 in the ranging
	> - Example IDL: for i = 0,nk-1 
	> - Example Python: for i in range(0, nk)

	> Then Removal and conversion
	> - Removes then begin, do begin, and then. replaces with colon
	> - Removes then stop and replaces with exit()
	> - Removes endif and endfor

	> Vector Index Conversion
	> - IDL supports vector indexing with parenthesis
	> - Python supports vector indexing with brackets
	> - This is accomplished by converting all other parts of the file, then recording all the defined variables. The file is written, then read back in and all the variables are searched for and bracketized. 
	> - vector(2) to vector[2]
	> - vector1(vector2(3)) to vector1[vector2[3]]

	> Whitespace Handling
	> - Peak whitespace handling occurs when IDL code levels are separated by one space
	> - Deviation from this will cause errors as Python is whitespace dependent
	> - Example IDL Code:
	> 		code line 1
	>		 code line 2
	>		  code line 3
	> - Example Python Code:
	>		code line 1
	>			code line 2
	>				code line 3


### To-do:
	Refine command-line interface for error-handling
	Refine command-line interface for multiple flags
