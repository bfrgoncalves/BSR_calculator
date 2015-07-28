#!/usr/bin/python
import sys
import pickle
import os
from BSR_functions import getOwnBlastScore


def main():

	try:
		input_file = sys.argv[1]
		temppath = sys.argv[2]
	except IndexError:
		print "usage: list_pickle_obj"

	argumentList=[]
	
	print type(input_file)
	print input_file
	with open(input_file,'rb') as f:
		argumentList = pickle.load(f)


	def ownScoreCalc(args):
	    ownScoreResults = getOwnBlastScore(args[0], args[1], args[2])

	    final =	(args[0], ownScoreResults)

	    filepath=os.path.join(temppath , str(args[3]) +"_OwnScore_result.txt")

	    with open(filepath, 'wb') as f:
			pickle.dump(final, f)

	    return True


	ownScoreCalc(argumentList)

if __name__ == "__main__":
    main()
