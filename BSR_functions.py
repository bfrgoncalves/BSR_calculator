


def getOwnBlastScore(FASTAfile, dbName, blast_out_file):

	translatedFile_path = Translate_FASTA(FASTAfile, 'translatedSequences.fasta')

	Gene_Blast_DB_name = Create_Blastdb(translatedFile_path,1,True, name)
	# --- get BLAST score ratio --- #
	cline = NcbiblastpCommandline(query='proteome.fasta', db=name, out=blast_out_file, outfmt=5)

	blast_records = runBlastParser(cline,blast_out_file, "")
	allelescores={}
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
							break
			else:
				break
	
	return allelescores



def getBlastScoreRatios(pathQuery, pathDB, allelescores, blast_out_file):
    
	translatedFile_path = Translate_FASTA(FASTAfile, 'translatedSequences.fasta')

	cline = NcbiblastpCommandline(query='proteome.fasta', db=pathDB, out=blast_out_file, outfmt=5)
	#print cline

	allelescore=0
	blast_records = runBlastParser(cline,blast_out_file, "")

	bestmatch=""
	for blast_record in blast_records:
		found=False 
		for alignment in blast_record.alignments:
			for match in alignment.hsps:

				blastScoreRatio = float(match.score) / float(allelescores[str(alignment.hit_def)])

				cdsStrName=blast_record.query

				if(blastScoreRatio == 1 and bestmatches[str(alignment.hit_def)][2]=="No"):
					bestmatches[str(alignment.hit_def)]=[str(match.score),str(blastScoreRatio),"Yes"]

				elif(blastScoreRatio == 1 and match.score>float(bestmatches[str(alignment.hit_def)][0])):
					bestmatches[str(alignment.hit_def)]=[str(match.score),str(blastScoreRatio),"Yes"]

				elif(match.score>float(bestmatches[str(alignment.hit_def)][0]) and blastScoreRatio>0.1 and blastScoreRatio>float(bestmatches[str(alignment.hit_def)][1])):
					bestmatches[str(alignment.hit_def)]=[str(match.score),str(blastScoreRatio),"Yes"]

		bestmatch=bestmatches[str(alignment.hit_def)][1]

	return bestmatch