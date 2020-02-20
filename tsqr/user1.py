import sys
import mrutil
import numpy as np

matrixCombine = []

# input is one 2NxN or two NxN, QR output is NxN
def simpleQR(matrix):
	global matrixCombine
	# first roundrobin input one 128 row matrix, mergeto input two 64 row matrix
	if len(matrix) == 128:
		kvlist = atomQR(matrix)
		mrutil.emit(kvlist)
	elif(len(matrix) == 64):
		matrixCombine += matrix
		if(len(matrixCombine) == 128):
			kvlist = atomQR(matrixCombine)
			mrutil.emit(kvlist)
			matrixCombine = []
	else:
		mrutil.writeLog("error happen matrix len=%d\n" %len(matrix))

def atomQR(matrix):
	arr = np.array(matrix)
	comArr = arr.astype(np.complex128)
	mt = np.matrix(comArr)
	q, r = np.linalg.qr(mt)
	comArr = np.asarray(r)
	arr = comArr.astype(np.string_)
	return arr.tolist()