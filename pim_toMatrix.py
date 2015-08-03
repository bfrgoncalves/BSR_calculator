import subprocess
import argparse
import os
import shutil
from os import listdir
from os.path import isfile, join, isdir
import sys
from datetime import datetime
import numpy
import string
import operator
import collections


def main():

	parser = argparse.ArgumentParser(description="This program calculates the BLAST-score ratio (BSR) between a query sequence file and a reference sequence file.")
	parser.add_argument('-x', nargs='?', type=str, help="query .pim file", required=True)
	parser.add_argument('-o', nargs='?', type=str, help="results file name", required=True)

	args = parser.parse_args()

	pim_matrix = pim_to_Matrix(args.x, ':', 1.0, args.o)



def pim_to_Matrix(fileName, delimiter, ifEmpty, resultsFile):
	matrix={}
	row_header=[]
	first_row=True
	headers = []

	for line in open(fileName,'rU').xreadlines(): 
		try:
			t = string.split(line[:-1], delimiter) ### remove end-of-line character - file is tab-delimited
			newHeader = t[1].split(' ')[1]
			headers.append(newHeader)
		except IndexError:
			continue
	print len(headers)

	with open(os.path.join(resultsFile), 'w') as tabFile:
		tabFile.write('\t' + ('\t'.join([str(x) for x in headers])) + '\n')

		for line in open(fileName,'rU').xreadlines(): 
			try:       
				t = string.split(line[:-1], delimiter) ### remove end-of-line character - file is tab-delimited
				newLine = t[1].split(' ')
				resultLine = [x for x in newLine if x]
				tabFile.write(('\t'.join([str(x) for x in resultLine])) + '\n')
			except IndexError:
				continue


	return True


if __name__ == "__main__":
	main()