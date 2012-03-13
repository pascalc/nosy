from nltk.tokenize import WhitespaceTokenizer

TOKENIZER = WhitespaceTokenizer()

def read(file_name):
	try:
		f_in = '%s.txt' % file_name
		file_in = open(f_in, 'r')
		f_out = '%s.csv' % file_name
		file_out = open(f_out, 'wb')
	except Exception, e:
		raise e

	data = ', '.join( [TOKENIZER.tokenize(line)[1] for line in file_in] )

	try:
		file_out.write(data)
	except Exception, e:
		raise e

#read()

if __name__ == "__main__":
    # Command line arguments
    import argparse
    parser = argparse.ArgumentParser(
        description='Converts a space two column space separted file into csv containing second column'
    )
    parser.add_argument('file', help='The file to convert')
    args = parser.parse_args()

    read(args.file)
