import sys
import mrutil

lineNum = 0
matrix = []

def dataSplit(row):
	global lineNum
	global matrix
	lineNum += 1
	matrix.append(row[:64])
	if(lineNum >= 128):
		lineNum = 0
		mrutil.emit(matrix)
		matrix = []

