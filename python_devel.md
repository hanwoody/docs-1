# python与RTFRAME的方案选择

在实现上有两种方式

>第一种是通过框架本身的执行器，将数据反序列化后，通过三方库go-python调用python的算法，本质上是通过cgo调用cpython。
>第二种是框架启动一个python的解释器进程，由python直接运行python算法。

* 第一种方式虽然对框架本身改动很小，但cgo调用开销，数据转换等麻烦的问题很多，真正实现起来阻力不小，并且结构上就存在效率问题，实际的情况也是这样，这个实现方式中途停止了。

* 第二种方式需要开发支持python算法的基本python模块，主要实现参数的解析，业务数据的收发序列化，状态的上报等执行器基本功能，虽然有一些工作量，但结构清晰，效率得到了最大化保证，也是最终采用的方式

# python环境要求

python2与python3有很大不同，考虑到python2将很快不受官方支持，因此后期就主要基于python3进行，不过适配python2改动不大。

框架采用了protobuf/grpc作为控制信息传递的序列化方式，而为了打包效率，业务数据的序列化采用了msgpack。因此，python需要两者的支持

## protobuf/grpc支持

开发机上需要安装proto编译器，并将协议文件*.proto生成python执行器的grpc框架代码,*.pb2.py *.pb2_grpc.py。
运行设备上需要安装grpcio，增加对grpc的支持。

## msgpack支持

通过pip3 install msgpack安装msgpack模块。
我们在框架中定义了msg格式为

```
type Row struct {
	K []interface{} `msg:"K"`
	V []interface{} `msg:"V"`
	T int64         `msg:"T"`
}
```
注意T为int64类型的，而python中的msgpack会将一个数字优先转化为uint，因此在框架解析该字段时会报错，目前没有很好的办法，只有先将T字段设置为0

# python执行器框架代码

包含了mapreduce.py、mrutil.py两个文件，一个主运行模块，一个辅助功能模块。

# python算法编写

框架提供了PyMap与PyReduce两个数据操作

> PyMap(name, pyModule string, pyMapper string)

> PyReduceByKey(name string, pyModule string, pyReducer string)

实际上PyReduceByKey是调用的更通用的

> PyReduceBy(name string, pyModule string, pyReducer string, keyFields *SortOption)

以后若需要更复杂的reduce操作，可以采用PyReduceBy

*一个例子*

对一个2048*64长矩阵的分解，定义flow.json如下

```
{
  "name": "2048x64 tsqr test",
  "executables":["python3.7", "mapreduce.py", "mrutil.py", "user.py", "user1.py", "user2.py", "gleam_pb2.py", "gleam_pb2_grpc.py"],
  "dataSource": {
    "tsqrData": {
      "path": "2048x64.csv",
      "type": "csv"
    }
  },
  "steps": [
    {
      "name": "a",
      "input": {
        "type": "dataSource",
        "ref": ["tsqrData"]
      },
      "ops": [
        {"op": "PyMap", "processor_type": "cpu", "args": ["dataSplit", "user", "dataSplit"]},
        {"op": "RoundRobin", "processor_type": "cpu", "args": ["toMultiWorker", "16"]},
        {"op": "PyMap", "processor_type": "cpu", "args": ["simpleQR", "user1", "simpleQR"]},
        {"op": "MergeTo", "processor_type": "cpu", "args": ["combineQR", "8"]},
        {"op": "PyMap", "processor_type": "cpu", "args": ["simpleQR", "user1", "simpleQR"]},
        {"op": "MergeTo", "processor_type": "cpu", "args": ["combineQR", "4"]},
        {"op": "PyMap", "processor_type": "cpu", "args": ["simpleQR", "user1", "simpleQR"]},        
        {"op": "MergeTo", "processor_type": "cpu", "args": ["combineQR", "2"]},
        {"op": "PyMap", "processor_type": "cpu", "args": ["simpleQR", "user1", "simpleQR"]},
        {"op": "MergeTo", "processor_type": "cpu", "args": ["combineQR", "1"]},
        {"op": "PyMap", "processor_type": "cpu", "args": ["simpleQR", "user1", "simpleQR"]},
        {"op": "PyMap", "processor_type": "cpu", "args": ["serialLine", "user2", "serialLine"]},
        {"op": "Printlnf", "processor_type": "cpu", "args": ["%s"]}
      ]
    }
  ]
}
```
*通常为了方便管理，避免算法互相影响，可以将不同的算法放到不同的文件中*

我们可以看看第一个dataSplit函数的实现，它在user.py这个文件中。
```
import sys
import mrutil

lineNum = 0
matrix = []

def dataSplit(row):
	global lineNum
	global matrix
	lineNum += 1
	matrix.append(row)
	if(lineNum >= 128):
		lineNum = 0
		mrutil.emit(matrix)
		matrix = []
```
实现很简单，将从文件读取的矩阵数据，文件2048x64.csv一共有2048行，每行是以逗号隔开的复数，dataSplit就是将128行数据合并为一行数据发送出去。




