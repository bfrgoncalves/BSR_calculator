
import os
import shutil
from os import listdir
from os.path import isfile, join, isdir
import sys
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast.Applications import NcbiblastnCommandline



def Create_Blastdb(questionDB, overwrite, dbtypeProt, dbName ):
	
	isProt=dbtypeProt

	if not os.path.isfile(dbName + ".nin") and not os.path.isfile(dbName + ".nhr") and not os.path.isfile(dbName + ".nsq"):

		if not isProt:
			os.system( "makeblastdb -in " + questionDB + " -out " + dbName + " -dbtype nucl -logfile " + dbName + "_blast.log" )
		else:
			print isProt
			print questionDB
			print dbName
			os.system( "makeblastdb -in " + questionDB + " -out " + dbName + " -dbtype prot -logfile " + dbName + "_blast.log" )

	elif overwrite:
		if not isProt:
			os.system( "makeblastdb -in " + questionDB + " -out " + dbName + " -dbtype nucl -logfile " + dbName + "_blast.log" )
		else:
			os.system( "makeblastdb -in " + questionDB + " -out " + dbName + " -dbtype prot -logfile " + dbName + "_blast.log" )

	else:
		print "BLAST DB files found. Using existing DBs.."  

	return( dbName )


def run_BLAST(databaseFilePath, dbPath, queryFilePath, isProtDB, blast_out_file):

	databaseName = os.path.basename(dbPath)

	if not os.path.isdir(dbPath):
		os.makedirs(dbPath)

	realdbPath = os.path.join(dbPath, databaseName)

	
	Create_Blastdb(databaseFilePath, 0, isProtDB, realdbPath)
	queryPath = os.path.join(os.getcwd(), queryFilePath)


	if isProtDB:
		cline = NcbiblastpCommandline(query=queryPath, db=realdbPath, out=blast_out_file, outfmt=5, num_descriptions = 100000)
	else:
		cline = NcbiblastnCommandline(query=queryPath, db=realdbPath, out=blast_out_file, outfmt=5, num_descriptions = 100000)

	os.system(str(cline))


def runBlastParser(bOutFile, locus_sbjct):
	rec = open(bOutFile)
	blast_records = NCBIXML.parse(rec)

	#os.remove(bOutFile)

	return blast_records
