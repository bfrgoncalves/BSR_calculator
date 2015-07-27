
import subprocess
import argparse
import os
import shutil
from os import listdir
from os.path import isfile, join, isdir
import sys
from datetime import datetime
import HTSeq
from BSR_functions import getOwnBlastScore
from BSR_functions import getBlastScoreRatios




def main():

	parser = argparse.ArgumentParser(description="This program calculates the BLAST-score ratio (BSR) between a query sequence file and a reference sequence file.")
	parser.add_argument('-q', nargs='?', type=str, help="Input query fasta file", required=True)
	parser.add_argument('-r', nargs='?', type=int, help='reference sequences file', required=True)
	#parser.add_argument('-c', nargs='?', type=int, help='Number of BSR and nucleotide similarity calculations.', required=True)
	parser.add_argument('-o', nargs='?', type=float, help="results folder", required=False)

	args = parser.parse_args()

	currentDir = os.getcwd()

	databaseDir = os.path.join(os.getcwd(), 'Databases')

	if not os.path.isdir(args.o):
		os.makedirs(args.o)

	if not os.path.isdir(databaseDir):
		os.makedirs(databaseDir)

	getOwnBlastScore(FASTAfile, dbName, blast_out_file)

	getBlastScoreRatios(pathQuery, pathDB, allelescores, bestmatches, blast_out_file):
    
