# pyIDL
IDL to Python converter.

Currently supports a command line interface.

Supported Functionality:

	Single File Run
		pyIDL.py -f <filename>
		pyIDL.py --singlefile <filename>

	Multiple File Run
		pyIDL.py -m <filename1> <filename2> ... <filenameX>
		pyIDL.py --multifile <filename1> <filename2> ... <filenameX>


To-do:
	Refine the bracketize methodology to not clobber len()->len[]
	Refine command-line interface for error-handling
	Refine command-line interface for multiple flags
