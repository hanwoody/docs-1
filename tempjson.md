# flowJson约束

## 应用基础信息字段

* name, version, description 是必选字段，中文描述：应用名称，版本号，应用描述

* dataset_manager_on　中文描述: 实时计算数据集管理功能, 默认关闭, 若点击打开需要提示“打开此功能会带来较大性能损失，确定要开启吗？” 

## 应用算法文件，（描述信息：在该算法文件列表中的算法程序，将被广播到本应用相关的每个节点，供每个执行器调用）

* executables　可选字段，中文描述:算法文件列表

## 数据源列表（描述信息：一个数据源为应用指定了数据的输入，它可以来自于文件(txt,csv,tsv等格式），也可来自网络（通过tcp,http等协议），还可来自于与FPGA/DSP关联的外部数据，如AD采样数据，您可以为一个应用指定一个数据源，也可指定多个数据源）

* name, 必选字段，中文描述:数据源名称

* type, 必选字段，枚举型, txt, csv, tsv, dsp, fpga ...，后续可以添加，中文描述:数据源类型

* path, 可选字段，字符串，中文描述：数据源位置

* args, 可选字段，字符串列表，中文描述：附加参数

* partition_count, 必选字段，自然数１,2...，默认值为１，中文描述：数据分区数　（当数据分区大于１时，数据源数据将被顺序分发到多个分区处理，提高计算并行度）

* tags, 可选字段，中文描述：数据源标签　（通过数据源标签，可以向RTFRAME调度器传递调度信息，将fpga/dsp数据源程序调度到具有特定特征的计算节点上）

## 数据操作流列表　（描述信息：　一个数据操作流描述了数据被加工处理的过程，它的输入可能是一个数据源，也有可能是一个数据操作流，一个应用可以包含一个或多个数据操作流）

* name, 必选字段，字符串，中文描述：数据操作流名称

* input, 必选字段，中文描述：数据操作流输入，type是dataSource, step两个类型的枚举, ref是指前面的dataSource或steps的name

* ops, 必选字段，中文描述：操作流，至少存在一个操作，其中，在每个操作中

* * op，中文名称：操作指令，枚举类型，RoundRobin，ReduceByKey，Printlnf，JoinByKey,Select，MergeSortedTo，MergeTo，DspOutput，FpgaOutput...，后续可添加

* * processor_type，　中文名称：计算类型，是枚举, cpu, dsp, fpga

* * args, 必选字段，字符串列表，中文名称：参数

* tags, 可选字段，中文描述：数据操作流标签　（通过数据操作流标签，可以向RTFRAME调度器传递调度信息，将fpga/dsp执行器调度到具有特定特征的计算节点上）

## DSP指令映射表　（描述信息：　DSP指令映射表描述了DSP镜像文件与运行指令的对应关系，一个DSP镜像文件可以包含数据操作流中的一个或多个操作）

* dsp_instruction_map, 当数据操作流中存在计算类型为dsp时，必须设置，否则，不能设置（前段能否根据计算类型，决定是否显示该字段？）

* * ops, 中文名称：指令列表。操作指令列表必须是数据操作流中出现的操作，且计算类型为dsp

* * img, 中文名称：算法镜像。从算法库中选取，前端能否根据arch提前做筛选？


## FPGA指令映射表　（描述信息：　FPGA指令映射表描述了FPGA镜像文件与运行指令的对应关系，一个FPGA镜像文件可以包含数据操作流中的一个或多个操作）

* fpga_instruction_map, 当数据操作流中存在计算类型为fpga时，必须设置，否则，不能设置（前段能否根据计算类型，决定是否显示该字段？）

* * ops, 中文名称：指令列表。操作指令列表必须是数据操作流中出现的操作，且计算类型为FPGA

* * img, 中文名称：算法镜像。从算法库中选取，前端能否根据arch提前做筛选？

# 范例文件

```
{
  "name": "common words count",
  "version": "1.2.2",
  "description": "this app description",
  "executables": ["alg1:1.1.1", "alg2:1.2.1"],
  "dataset_manager_on": false,
  "dataSource": [
    {
      "name": "etc_conf",
      "path": "/etc/*.conf",
      "type": "txt",
      "args": ["arg1", "arg2", "arg3"],
      "partition_count": 3,
      "tags": [
        {
          "key": "adc",
          "value": "1"
        },
        {
          "key": "dac",
          "value": "2"
        }
      ]
    },
    {
      "name": "etc_group",
      "path": "/etc/group
      "type": "txt",
      "args": ["arg1", "arg2", "arg3"],      
      "partition_count": 3,
      "tags": [
        {
          "key": "adc",
          "value": "1"
        }
      ]      
    }
  ],
  "steps": [
    {
      "name": "a",
      "input": {
        "type": "dataSource",
        "ref": ["etc_conf"]
      },
      "ops": [
        {"op": "Map", "processor_type": "dsp", "args": ["tokenize", "Tokenize"]},
        {"op": "Map", "processor_type": "dsp", "args": ["slow step", "Delay"]},
        {"op": "Map", "processor_type": "dsp", "args": ["addOne", "AppendOne"]},
        {"op": "ReduceByKey", "processor_type": "dsp", "args":["sum", "SumInt64"]}
      ],
      "tags": [
        {
          "key": "adc",
          "value": "1"
        },
        {
          "key": "dac",
          "value": "2"
        }
      ]
    },
    {
      "name": "b",
      "input": {
        "type": "dataSource",
        "ref": ["etc_group"]
      },
      "ops": [
        {"op": "Map", "processor_type": "cpu", "args": ["tokenize", "Tokenize"]},
        {"op": "Map", "processor_type": "cpu", "args": ["slow step", "Delay"]},
        {"op": "Map", "processor_type": "cpu", "args": ["addOne", "AppendOne"]},
        {"op": "ReduceByKey", "processor_type": "cpu", "args":["sum", "SumInt64"]}
      ],
      "tags": [
        {
          "key": "adc",
          "value": "1"
        }
      ]      
    },
    {
      "name": "c",
      "input": {
        "type": "step",
        "ref":["a", "b"]
      },
      "ops": [
        {"op": "JoinByKey", "processor_type": "dsp", "args": ["shared words", "a", "b"]},
        {"op": "Printlnf", "processor_type": "fpga", "args": ["%s\t%d\t%d"]}
      ],
      "tags": [
        {
          "key": "adc",
          "value": "1"
        }
      ]      
    }
  ],
  "dsp_instruction_map": [
    {
      "ops": ["map", "ReduceByKey"],
      "img": "alg1:1.1"
    },
    {
      "ops": ["JoinByKey"],
      "img": "alg2:1.1"
    }
  ],
  "fpga_instruction_map": [
    {
      "ops": ["Printlnf"],
      "img": "alg3:1.1"
    }
  ]  
}
```