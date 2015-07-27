
import os
import shutil
from os import listdir
from os.path import isfile, join, isdir
import sys
from Bio.Blast import NCBIXML


def Create_Blastdb(questionDB, overwrite, dbtypeProt,dbName ):
	
	isProt=dbtypeProt

	if not os.path.isfile(dbName + ".nin") and not os.path.isfile(dbName + ".nhr") and not os.path.isfile(dbName + ".nsq"):

		if not isProt:
			os.system( "makeblastdb -in " + questionDB + " -out " + dbName + " -dbtype nucl -logfile " + dbName + "_blast.log" )
		else:
			os.system( "makeblastdb -in " + questionDB + " -out " + dbName + " -dbtype prot -logfile " + dbName + "_blast.log" )

	elif overwrite:
		if not isProt:
			os.system( "makeblastdb -in " + questionDB + " -out " + dbName + " -dbtype nucl -logfile " + dbName + "_blast.log" )
		else:
			os.system( "makeblastdb -in " + questionDB + " -out " + dbName + " -dbtype prot -logfile " + dbName + "_blast.log" )

	else:
		print "BLAST DB files found. Using existing DBs.."  

	return( dbName )


def run_BLAST(queryFilePath, dbPath, isNucleotideDB, blast_out_file):
	
	Create_Blastdb( dbPath, 1, isNucleotideDB, name)
	cline = NcbiblastpCommandline(query=queryFilePath, db=name, out=blast_out_file, outfmt=5)

	return blast_out_file


def runBlastParser(bOutFile, locus_sbjct):
	os.system(str(cline))
	rec = open(bOutFile)
	blast_records = NCBIXML.parse(rec)

	os.remove(bOutFile)

	return blast_records
