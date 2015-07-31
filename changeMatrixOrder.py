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
	parser.add_argument('-x', nargs='?', type=str, help="query Matrix", required=True)
	parser.add_argument('-y', nargs='?', type=str, help='reference Matrix', required=True)
	#parser.add_argument('-c', nargs='?', type=int, help='Number of BSR and nucleotide similarity calculations.', required=True)
	parser.add_argument('-o', nargs='?', type=str, help="results folder", required=True)

	args = parser.parse_args()


	my_x = importMatrix(args.x, ',', 1.0)
	my_y = importMatrix(args.y, '\t', 1.0)

	writeMatrix('newX.tab', my_x)
	writeMatrix('newY.tab', my_y)


def importMatrix(fileName, delimiter, ifEmpty):
	matrix={}
	row_header=[]
	first_row=True

	for line in open(fileName,'rU').xreadlines():         
		t = string.split(line[:-1], delimiter) ### remove end-of-line character - file is tab-delimited
		#print t
		if first_row:
			headers = t[1:]
			first_row=False
		else:
			#print t[0]
			matrix[t[0]] = []
			toAppend = {}
			countCol = 0
			for i in headers:
				#print headers
				countCol += 1
				if t[countCol] == '':
					t[countCol] = ifEmpty
				if float(t[countCol]) > 1.0:
					t[countCol] = float(t[countCol]) * 0.01
				toAppend[i] = float(t[countCol])

			sorted_toAppend = sorted(toAppend.items(), key=operator.itemgetter(0))

			matrix[t[0]].append(sorted_toAppend)


	sortedMatrix = sorted(matrix.items(), key=operator.itemgetter(0))
	#print sortedMatrix

	return sortedMatrix

def writeMatrix(resultsFile, matrix):

	#print matrix
	with open(os.path.join(resultsFile), 'w') as tabFile:
		headers = []
		for i in matrix:
			headers.append(i[0])
		headers.sort()
		tabFile.write('\t' + ('\t'.join([str(x) for x in headers])) + '\n')
		
		for x in matrix:
			print x
			#sortedLine = sorted(x[1][0].items(), key=operator.itemgetter(0))
			Line = x[1][0]
			tabFile.write(x[0] + '\t' + ('\t'.join([str(z[1]) for z in Line])) + '\n')

	return True


if __name__ == "__main__":
	main()