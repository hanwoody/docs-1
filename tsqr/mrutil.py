from io import BytesIO
import msgpack
import sys
import struct
import pprint
import time

logfile = open("/tmp/log.txt", mode='a+')

PY3K = sys.version_info > (3, 0)

InputCounter = 0
OutputCounter = 0

def inputCounterInc():
	global InputCounter
	InputCounter += 1

def outputCounterInc():
	global OutputCounter
	OutputCounter += 1

def rawRead(length):
	if PY3K:
		return sys.stdin.buffer.read(length)
	else:
		return sys.stdin.read(length)

def rawWrite(encodedBytes):
	if PY3K:
		sys.stdout.buffer.write(encodedBytes)
	else:
		sys.stdout.write(encodedBytes)

def readEncodedBytes():
	bytesLen = rawRead(4)
	if(len(bytesLen) == 4):
		bodyLen = struct.unpack('<i', bytesLen)
		encodedBytes = rawRead(bodyLen[0])
		# logfile.write("read len=%d, body=%s\n" %(len(encodedBytes), encodedBytes))
		return encodedBytes
	else:
		return ""

def decodeRow(encodeBytes):
	kvdict = {}
	kvdict = msgpack.unpackb(encodeBytes, use_list = False, raw = False)
	# logfile.write("kvdict:\n")
	# pprint.pprint(kvdict, logfile)
	return kvdict

def readRow():
	encoded = readEncodedBytes()
	if(len(encoded) > 0):	
		return decodeRow(encoded)
	else:
		return None

def writeEncoded(encodedBytes):
	rawWrite(encodedBytes)

def tsWriteRow(ts, keys, values):
	# t = time.time()
	# tick = int(round(t * 1000))

	buf = BytesIO()
	kvs = {u'K__slc':keys, u'V__slc':values, u'T__i64':0}

	buf.write(msgpack.packb(kvs, use_bin_type = True))		
	msgBody = buf.getvalue()
	lenBytes = struct.pack('<i', len(msgBody))

	writeEncoded(lenBytes)
	writeEncoded(msgBody)
	outputCounterInc()	

def writeRow(keys, values):
	tsWriteRow(0, keys, values)

def emit(kvList):
	keys = [kvList[0]]
	values = kvList[1:]
	writeRow(keys, values)

def writeError(errString):
	sys.stderr.write(errString)

def writeLog(logString):
	logfile.write(logString)

def writeLogObject(object):
	pprint.pprint(object, logfile)

def compare(a, b):
	if(len(a) != len(b)):
		return False
	for i, val in enumerate(a):
		if(type(val) != type(b[i])):
			return False
		if(val != b[i]):
			return False
	return True