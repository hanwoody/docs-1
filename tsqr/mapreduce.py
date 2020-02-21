import sys
import mrutil
import argparse
import threading	
from time import sleep
import grpc
import gleam_pb2
import gleam_pb2_grpc

parser = argparse.ArgumentParser(description="mapreduce args")
parser.add_argument('--pymodule', '-module', required=True, type=str, help='python mapreduce module file')
group = parser.add_mutually_exclusive_group()
group.add_argument('--pymapper', '-mapper', type=str, help='map function')
group.add_argument("--pyreducer", '-reducer', type=str, help='reduce function')
parser.add_argument('--keyFields', '-keyFields', type=str, help='reduce keyFields')

parser.add_argument('--executor', '-gleam.executor')
parser.add_argument('--hashcode', '-flow.hashcode')
parser.add_argument('--stepId', '-flow.stepId')
parser.add_argument('--taskId', '-flow.taskId')
args = parser.parse_args()


def reportStat(stoppingReport, finishedReport):
	lastRound = False
	while True:
		exeStat = gleam_pb2.ExecutionStat()
		exeStat.flowHashCode = int(args.hashcode)
		stat = exeStat.stats.add()
		stat.stepId = int(args.stepId)
		stat.taskId = int(args.taskId)
		stat.inputCounter = mrutil.InputCounter
		stat.outputCounter = mrutil.OutputCounter
		yield exeStat
		if(lastRound):
			break
		stoppingReport.wait(timeout=1.0)		
		if(stoppingReport.isSet()):
			lastRound = True

def reportMain(stoppingReport, finishedReport):
	with grpc.insecure_channel(args.executor) as channel:
		stub = gleam_pb2_grpc.GleamExecutorStub(channel)
		# get report stream iterator
		statIter = reportStat(stoppingReport, finishedReport)
		stub.CollectExecutionStatistics(statIter)
	finishedReport.set()

def getUserMapper():
	if(args.pymapper == None):
		return None
	else:
		module = __import__(args.pymodule)
		f = getattr(module, args.pymapper)
		return f

def getUserReducer():
	if(args.pyreducer == None):
		return None, None
	else:
		# get reducer
		module = __import__(args.pymodule)
		f = getattr(module, args.pyreducer)
		# get reduce keyindexes
		keyIndexes = []		
		keyFields = args.keyFields.split(',')
		for index in keyFields:
			keyIndexes.append(int(index))	
		# mrutil.writeLogObject(keyIndexes)
		return f, keyIndexes

def mainMapReduce():
	# start report thread
	stoppingReport = threading.Event()
	finishedReport = threading.Event()
	t = threading.Thread(target=reportMain, args=(stoppingReport, finishedReport))
	t.start()
	# start mapreduce in main
	if(args.pymapper != None):
		mapMain()
	elif(args.pyreducer != None):
		reduceMain()
	else:
		mrutil.writeError("python mapper or reducer do not specify\n")
	# stop report notify
	stoppingReport.set()
	# wait report stopped
	finishedReport.wait()

def useKeys(keyValues, keyIndexes):
	if(len(keyValues) < len(keyIndexes)):
		mrutil.writeError("python reduce keyindexes > keyvalues\n")
		return None, None
	keys = []
	values = []	
	used = []	
	for i in range(len(keyValues)):
		used.append(False)
	for pos in keyIndexes:
		# key pos start from 1
		keys.append(keyValues[pos-1])
		used[pos-1] = True
	for i, kv in enumerate(keyValues):
		if(not used[i]):
			values.append(kv)
	return keys, values

def getTsKeyValues(kvdict):
	ts = 0
	kvList = []
	if kvdict.get('K__slc'):
		for key in kvdict['K__slc']:
			kvList.append(key)
	if kvdict.get('V__slc'):
		for val in kvdict['V__slc']:
			kvList.append(val)
	if kvdict.get('T__i64'):
		ts = kvdict['T__i64']
	return ts, kvList

def getKeyValues(kvdict):
	kvList = []
	if kvdict.get('K__slc'):
		for key in kvdict['K__slc']:
			kvList.append(key)
	if kvdict.get('V__slc'):
		for val in kvdict['V__slc']:
			kvList.append(val)
	return kvList		

def reduce(f, x, y):
	if(len(x) == 1 and len(y) == 1):
		return [f(x[0], y[0])]
	else:
		kvList = f(x, y)	
		return kvList

def doProcessReducer(f):
	kvdict = mrutil.readRow()
	if kvdict == None:
		# mrutil.writeError("python reducer input row error\n")
		return
	mrutil.inputCounterInc()
	lastTs, lastKvList = getTsKeyValues(kvdict)
	while True:
		kvdict = mrutil.readRow()
		if kvdict == None:
			break
		mrutil.inputCounterInc()
		ts, kvList = getTsKeyValues(kvdict)
		lastVList = reduce(f, lastKvList, kvList)
		lastKList = kvList
		if(ts > lastTs):
			lastTs = ts
	mrutil.tsWriteRow(lastTs, lastKList, lastVList)

def doProcessReducerByKeys(f, keyIndexes):
	kvdict = mrutil.readRow()
	if kvdict == None:
		# mrutil.writeError("python reducerByKeys input row error\n")
		return
	mrutil.inputCounterInc()

	lastTs, lastKvList = getTsKeyValues(kvdict)
	lastKList, lastVList = useKeys(lastKvList, keyIndexes)
	while True:
		kvdict = mrutil.readRow()
		if kvdict == None:
			return
		mrutil.inputCounterInc()
		ts, kvList = getTsKeyValues(kvdict)
		kList, vList = useKeys(kvList, keyIndexes)
		if(mrutil.compare(lastKList, kList)):
			lastVList = reduce(f, lastVList, vList)
		else:
			mrutil.tsWriteRow(lastTs, lastKList, lastVList)
			lastKList, lastVList = kList, vList
			if(ts > lastTs):
				lastTs = ts

def reduceMain():
	f, keyIndexes = getUserReducer()
	if(f == None or keyIndexes == None):
		mrutil.writeError("python reducer not found\n")
		return
	else:
		# mrutil.writeLogObject(keyIndexes)
		if(len(keyIndexes) == 1 and keyIndexes[0] == 0):
			return doProcessReducer(f)
		else:
			return doProcessReducerByKeys(f, keyIndexes)

def mapMain():
	f = getUserMapper()
	if f == None:
		mrutil.writeError("python get mapper fail\n")
		return
	while True:
		kvdict = mrutil.readRow()
		if kvdict == None:
			return
		mrutil.inputCounterInc()
		kvList = getKeyValues(kvdict)
		if(kvList != None):
			f(kvList)
		else:
			mrutil.writeError("python map get bad row\n")
			return

mainMapReduce()



