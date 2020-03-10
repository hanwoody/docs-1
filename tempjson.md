# flowJson约束

* dataSource中的type是枚举, txt, csv, tsv, dsp, fpga ...，后续可以添加

* steps中input字段的type是dataSource, step两个类型的枚举, ref是指前面的dataSource或steps的name

* steps中的ops, op字段是枚举，RoundRobin，ReduceByKey，Printlnf，JoinByKey,Select，MergeSortedTo，MergeTo，DspOutput，FpgaOutput...，后续可添加

* steps中的ops, processor_type是枚举, cpu, dsp, fpga

* steps中的ops，args的第一个其实是op的名字, 前端可以设置第一个args为name，让用户输入，在让用户输入后面的变长参数

* executables、dsp_instruction_map、fpga_instruction_map中的算法,需要从库中选取

* 当指定dsp_instruction_map中的操作时，op必须是step中已经使用，并且processor_type=dsp

* 当指定fpga_instruction_map中的操作时，op必须是step中已经使用，并且processor_type=fpga



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
      "path": "/etc/group",
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