
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
from Translate_functions import translateSeq

from cluster_utils import create_pickle, create_Jobs
import pickle




def main():

	parser = argparse.ArgumentParser(description="This program calculates the BLAST-score ratio (BSR) between a query sequence file and a reference sequence file.")
	parser.add_argument('-q', nargs='?', type=str, help="Input query fasta file", required=True)
	parser.add_argument('-r', nargs='?', type=str, help='reference sequences file', required=True)
	#parser.add_argument('-c', nargs='?', type=int, help='Number of BSR and nucleotide similarity calculations.', required=True)
	parser.add_argument('-o', nargs='?', type=str, help="results folder", required=True)

	args = parser.parse_args()

	currentDir = os.getcwd()

	databaseDir = os.path.join(os.getcwd(), 'Databases')

	dbName = os.path.join(databaseDir, 'refDatabase')

	blast_out_file = dbName + '_BLAST_out.xml'

	uniqueAllelesFolder = os.path.join(os.getcwd(), 'Alleles')

	if not os.path.isdir(args.o):
		os.makedirs(args.o)

	if not os.path.isdir(databaseDir):
		os.makedirs(databaseDir)

	if not os.path.isdir(uniqueAllelesFolder):
		os.makedirs(uniqueAllelesFolder)

	
	fastaFile = HTSeq.FastaReader(args.q)
	for allele in fastaFile:
		x = str(translateSeq(allele.seq))
		alleleProt=">"+str(allele.name)+"\n"+x+"\n"
		with open(os.path.join(uniqueAllelesFolder,allele.name + '.fasta'), "w") as f:
			f.write(alleleProt)

	onlyfiles = [ f for f in listdir(uniqueAllelesFolder) if isfile(join(uniqueAllelesFolder,f)) ]

	countAlleles = 0

	job_args = []
	allQueryBasePaths = []

	for allelefile in onlyfiles:
		countAlleles += 1
		dbName = os.path.join(databaseDir, 'refDatabase' + str(countAlleles))
		blast_out_file = dbName + '_BLAST_out_' + str(countAlleles) + '.xml'
		listOfArgs = (allelefile, dbName, blast_out_file, countAlleles)

		action = 'OwnScore'
		job_args, allQueryBasePaths = create_pickle(listOfArgs, uniqueAllelesFolder, job_args, action, 'OwnScore', allQueryBasePaths, countAlleles)

	create_Jobs(job_args, 'getOwnBLASTScore.py', allQueryBasePaths)

	for i in allQueryBasePaths:
		countResults += 1
		filepath=os.path.join(i, str(countResults)+"_"+ action + "_result.txt")

		with open(filepath,'rb') as f:
			x = pickle.load(f)

		print x


if __name__ == "__main__":
	main()