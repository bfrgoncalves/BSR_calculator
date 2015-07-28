
from Translate_functions import Translate_FASTA
from BLAST_functions import runBlastParser
from BLAST_functions import Create_Blastdb
from BLAST_functions import run_BLAST
import os



def getOwnBlastScore(FASTAfile, dbName, blast_out_file):

	fileName = os.path.basename(FASTAfile)

	dirName = os.path.dirname(FASTAfile)

	print FASTAfile
	print fileName
	print dirName

	translatedFile_path = Translate_FASTA(FASTAfile, os.path.join(dirName, fileName + '_translatedSequences.fasta'))

	cline = run_BLAST(translatedFile_path, dbName, translatedFile_path, False, blast_out_file)

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



def getBlastScoreRatios(pathQuery, pathReference, pathDB, allelescores, bestmatches, blast_out_file):

	fileNamequery = os.path.basename(pathQuery)
    
	translatedqueryFile_path = Translate_FASTA(pathQuery, fileNamequery + '_translatedSequences.fasta')

	fileNameref = os.path.basename(pathReference)

	translatedreferenceFile_path = Translate_FASTA(pathReference, fileNameref + '_translatedSequences.fasta')

	cline = run_BLAST(translatedreferenceFile_path, pathDB, translatedqueryFile_path, False, blast_out_file)

	allelescore=0
	blast_records = runBlastParser( blast_out_file, "")

	bestmatch=""
	bestmatchArray = []
	
	for blast_record in blast_records:
		found=False 
		for alignment in blast_record.alignments:
			for match in alignment.hsps:

				blastScoreRatio = float(match.score) / float(allelescores[str(alignment.hit_def)])

				cdsStrName=blast_record.query

				if(blastScoreRatio == 1 and bestmatches[str(alignment.hit_def)][2]=="No"):
					bestmatches[str(alignment.hit_def)]=[str(match.score),str(blastScoreRatio),"Yes", blast_record.query]

				elif(blastScoreRatio == 1 and match.score>float(bestmatches[str(alignment.hit_def)][0])):
					bestmatches[str(alignment.hit_def)]=[str(match.score),str(blastScoreRatio),"Yes", blast_record.query]

				elif(match.score>float(bestmatches[str(alignment.hit_def)][0]) and blastScoreRatio>0.6 and blastScoreRatio>float(bestmatches[str(alignment.hit_def)][1])):
					bestmatches[str(alignment.hit_def)]=[str(match.score),str(blastScoreRatio),"Yes", blast_record.query]

		
	for i in bestmatches:
		if bestmatches[i][2] == 'Yes':
			bestmatchArray.append([i, bestmatches[i][1], bestmatches[i][3]])

	return bestmatchArray