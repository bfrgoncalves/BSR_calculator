
import subprocess
import argparse
import os
import shutil
from os import listdir
from os.path import isfile, join, isdir
import sys
from datetime import datetime




def main():

	parser = argparse.ArgumentParser(description="This program calculates the BLAST-score ratio (BSR) between a query sequence file and a reference sequence file.")
	parser.add_argument('-q', nargs='?', type=str, help="Input query fasta file", required=True)
	parser.add_argument('-r', nargs='?', type=int, help='reference sequences file', required=True)
	#parser.add_argument('-c', nargs='?', type=int, help='Number of BSR and nucleotide similarity calculations.', required=True)
	parser.add_argument('-o', nargs='?', type=float, help="results folder", required=False)

	args = parser.parse_args()

	currentDir = os.getcwd()

	if not os.path.isdir(os.path.join(args.o)):
		os.makedirs(os.path.join(args.o))

	with open(os.path.join(currentDir, args.r), "r") as referenceFile:
