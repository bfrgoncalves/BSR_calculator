
from Translate_functions import Translate_FASTA
from BLAST_functions import runBlastParser
from BLAST_functions import Create_Blastdb


def getOwnBlastScore(FASTAfile, dbName, blast_out_file):

	translatedFile_path = Translate_FASTA(FASTAfile, 'translatedSequences.fasta')

	run_BLAST(translatedFile_path, dbName, True, blast_out_file)

	blast_records = runBlastParser( blast_out_file, "")
	allelescores = {}
	bestmatches = {}
	for blast_record in blast_records:
		found=False 
		for alignment in blast_record.alignments:
			if found is False:
				for match in alignment.hsps:
					try:
						if allelescores[str(alignment.hit_def)] < match.score:
							allelescores[str(alignment.hit_def)] = int(match.score)
							break
						except KeyError:
							allelescores[str(alignment.hit_def)] = int(match.score)
							bestmatches[str(alignment.hit_def)] = [ str(-1), str(0), 'No', '']
							break
			else:
				break
	
	return allelescores, bestmatches



def getBlastScoreRatios(pathQuery, pathDB, allelescores, bestmatches, blast_out_file):
    
	translatedFile_path = Translate_FASTA(FASTAfile, 'translatedSequences.fasta')

	run_BLAST(translatedFile_path, pathDB, True, blast_out_file)

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
			bestmatchArray.append([i, bestmatches[i][1], bestmatches[i][3])

	return bestmatchArray