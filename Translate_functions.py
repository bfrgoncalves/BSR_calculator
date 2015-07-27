
from Bio.Seq import Seq
import HTSeq


def reverseComplement(strDNA):

	basecomplement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
	strDNArevC = ''
	for l in strDNA:

		strDNArevC += basecomplement[l]

	return strDNArevC[::-1]

def translateSeq(DNASeq):
	
	seq=DNASeq
	try:
		myseq= Seq(seq)
		protseq=Seq.translate(myseq, table=11,cds=True)

	except:
		try:
			seq=reverseComplement(seq)
			myseq= Seq(seq)
			protseq=Seq.translate(myseq, table=11,cds=True)

		except:
			try:
				seq=seq[::-1]
				myseq= Seq(seq)
				protseq=Seq.translate(myseq, table=11,cds=True)
			except:
				try:
					seq=seq[::-1]                           
					seq=reverseComplement(seq)
					myseq= Seq(seq)
					protseq=Seq.translate(myseq, table=11,cds=True)
				except:
					raise
	return protseq


def Translate_FASTA(FASTAfile, outputPath):
	
	gene_fp = HTSeq.FastaReader(FASTAfile)
	alleleProt=''
	for allele in gene_fp:
		x = str(translateSeq(allele.seq))
		alleleProt+=">"+str(allele.name)+"\n"+x+"\n"
	with open(outputPath, "wb") as f:
		f.write(alleleProt)

	return outputPath

