import sys
import mrutil

# NxN matrix
def serialLine(matrix):
	for line in matrix:
		list_new = [str(x) for x in line]
		kvstr = ",".join(list_new)
		mrutil.emit([kvstr])