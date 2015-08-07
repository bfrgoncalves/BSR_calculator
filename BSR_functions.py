
from Translate_functions import Translate_FASTA
from BLAST_functions import runBlastParser
from BLAST_functions import Create_Blastdb
from BLAST_functions import run_BLAST
import os



def getOwnBlastScore(FASTAfile, dbName, blast_out_file):

	fileName = os.path.basename(FASTAfile)

	dirName = os.path.dirname(FASTAfile)


	translatedFile_path = Translate_FASTA(FASTAfile, os.path.join(dirName, fileName + '_translatedSequences.fasta'))

	cline = run_BLAST(translatedFile_path, dbName, translatedFile_path, True, blast_out_file)

	os.remove(translatedFile_path)

	blast_records = runBlastParser(blast_out_file, "")
	
	allelescores = {}
	totalBestMatches = {}
	for blast_record in blast_records:
		found=False 
		queryName = blast_record.query
		bestmatches = {}

		for alignment in blast_record.alignments:
			if found is False:
				for match in alignment.hsps:
					try:
						if allelescores[str(alignment.hit_def)] < match.score:
							allelescores[str(alignment.hit_def)] = int(match.score)
							break
					except KeyError:
						allelescores[str(alignment.hit_def)] = int(match.score)
						break
			else:
				break
	
	return allelescores



def getBlastScoreRatios(pathQuery, pathReference, pathDB, allelescores, blast_out_file, countQueries):

	fileNamequery = os.path.basename(pathQuery)

	dirNamequery = os.path.dirname(pathQuery)
    
	translatedqueryFile_path = Translate_FASTA(pathQuery, os.path.join(dirNamequery, fileNamequery + '_translatedSequences.fasta'))

	dirNameref = os.path.dirname(pathReference)

	fileNameref = os.path.basename(pathReference)

	translatedreferenceFile_path = Translate_FASTA(pathReference, os.path.join(dirNameref, fileNameref + str(countQueries) + '_translatedSequences.fasta'))


	cline = run_BLAST(translatedreferenceFile_path, pathDB, translatedqueryFile_path, True, blast_out_file)


	allelescore = 0
	blast_records = runBlastParser( blast_out_file, "")

	bestmatch = ""
	bestmatchArray = {}
	
	for blast_record in blast_records:
		bestmatchArray[str(blast_record.query)] = []
		
		for alignment in blast_record.alignments:
			for match in alignment.hsps:

				blastScoreRatio = float(match.score) / float(allelescores[str(alignment.hit_def)])

				cdsStrName=blast_record.query

				if blastScoreRatio > 0:
					bestmatchArray[str(blast_record.query)].append([str(alignment.hit_def), str(match.score), str(blastScoreRatio)])
					break

	return bestmatchArray