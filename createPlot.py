
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
from pylab import *

def main():

	parser = argparse.ArgumentParser(description="This program calculates the BLAST-score ratio (BSR) between a query sequence file and a reference sequence file.")
	parser.add_argument('-x', nargs='?', type=str, help="X axis data", required=True)
	parser.add_argument('-y', nargs='?', type=str, help='Y axis data', required=True)
	parser.add_argument('-xl', nargs='?', type=str, help="X label", required=True)
	parser.add_argument('-yl', nargs='?', type=str, help='Y label', required=True)
	#parser.add_argument('-c', nargs='?', type=int, help='Number of BSR and nucleotide similarity calculations.', required=True)
	parser.add_argument('-o', nargs='?', type=str, help="results folder", required=True)

	args = parser.parse_args()


	my_x = importData(args.x)
	my_y = importData(args.y)

	y_values = []
	x_values = []

	for i in my_y[0]:
		y_values = y_values + i

	for i in my_x[0]:
		x_values = x_values + i

	for i in range(0, len(y_values)):
		if y_values[i] > 0.98 and x_values[i] < 0.56:
			print 'AQUI', i
			print y_values[i]
			print x_values[i]

	print len(y_values)
	print len(x_values)

	plot(x_values, y_values, marker='o', color='r', ls='')
	xlabel(args.xl)
	ylabel(args.yl)

	show()





def importData(filename):
    #start_time = time.time()
    matrix=[]
    row_header=[]
    first_row=True

    if '/' in filename:
        dataset_name = string.split(filename,'/')[-1][:-4]
    else:
        dataset_name = string.split(filename,'\\')[-1][:-4]

        
    for line in open(filename,'rU').xreadlines():         
        t = string.split(line[:-1],'\t') ### remove end-of-line character - file is tab-delimited
        if first_row:
            column_header = t[1:]
            first_row=False
        else:
            if ' ' not in t and '' not in t: ### Occurs for rows with missing data
                s = map(float,t[1:])
                if (abs(max(s)-min(s)))>0:
                    matrix.append(s)
                    row_header.append(t[0])
            
    #time_diff = str(round(time.time()-start_time,1))
    try:
        print '\n%d rows and %d columns imported for %s in %s seconds...' % (len(matrix),len(column_header),dataset_name)
    except Exception:
        print 'No data in input file.'
    return matrix, column_header, row_header




if __name__ == "__main__":
	main()