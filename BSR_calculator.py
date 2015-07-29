
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

	resultsFolder = os.path.join(os.getcwd(), args.o)

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
		alleleSeq=">"+str(allele.name)+"\n"+str(allele.seq)+"\n"
		with open(os.path.join(uniqueAllelesFolder, allele.name + '.fasta'), "w") as f:
			f.write(alleleSeq)

	onlyfiles = [ f for f in listdir(uniqueAllelesFolder) if isfile(join(uniqueAllelesFolder,f)) ]

	countAlleles = 0

	job_args = []
	allQueryBasePaths = []

	alleleScores = {}

	for allelefile in onlyfiles:

		alleleFilePath = os.path.join(os.getcwd(), 'Alleles', allelefile)
		countAlleles += 1
		dbName = os.path.join(databaseDir, 'refDatabase' + str(countAlleles))
		blast_out_file = dbName + '_BLAST_out_' + str(countAlleles) + '.xml'
		listOfArgs = (alleleFilePath, dbName, blast_out_file, countAlleles)

		action = 'OwnScore'
		job_args, allQueryBasePaths = create_pickle(listOfArgs, uniqueAllelesFolder, job_args, action, 'OwnScore', allQueryBasePaths, countAlleles)

	create_Jobs(job_args, 'getOwnBLASTScore.py', allQueryBasePaths)

	countResults = 0

	for i in allQueryBasePaths:
		countResults += 1
		filepath=os.path.join(i, str(countResults)+"_"+ action + "_result.txt")

		with open(filepath,'rb') as f:
			x = pickle.load(f)

		for i in x[1]:
			alleleScores[i] = x[1][i]

	print alleleScores
	
	countAlleles = 0

	referencePath = os.path.join(os.getcwd(), args.q)

	job_args = []
	allQueryBasePaths = []

	BSRresults = {}


	for allelefile in onlyfiles:
		countAlleles += 1
		alleleFilePath = os.path.join(os.getcwd(), 'Alleles', allelefile)
		dbName = os.path.join(databaseDir, 'refDatabase_' + str(countAlleles))
		blast_out_file = dbName + '_BLAST_out_' + str(countAlleles) + '.xml'
		listOfArgs = (alleleFilePath, referencePath, dbName, alleleScores, blast_out_file, countAlleles)
		action = 'BSR'
		job_args, allQueryBasePaths = create_pickle(listOfArgs, uniqueAllelesFolder, job_args, action, 'BSR', allQueryBasePaths, countAlleles)

	create_Jobs(job_args, 'getBLASTScoreRatios.py', allQueryBasePaths)

	countResults = 0

	for i in allQueryBasePaths:
		countResults += 1
		filepath=os.path.join(i, str(countResults)+"_"+ action + "_result.txt")

		with open(filepath,'rb') as f:
			x = pickle.load(f)

		for i in x[1]:
			BSRresults[i] = x[1][i]

	#print BSRresults
	alleleNames = {}
	newResults = {}
	for i in BSRresults:
		newResults[i] = []
		toAppend = {}
		for j in BSRresults[i]:
			toAppend[j[0]] = j[2]
		newResults[i].append(toAppend)

	#print newResults

	for i in newResults:
		for j in BSRresults:
			try:
				if newResults[i][0][j] > -1:
					print 'Exists'
			except KeyError:
				newResults[i][0][j] = 0
	
	print newResults

	with open(os.path.join(resultsFolder,'BSRresults.tab'), 'w') as tabFile:
		headers = []
		for i in newResults:
			headers.push(i)
		tabFile.write(('\t'.join([str(x) for x in headers])) + '\n')
		
		for x in headers:
			tabFile.write(x + '\t' + ('\t'.join([str(newResults[x]) for x in newResults])) + '\n')


if __name__ == "__main__":
	main()