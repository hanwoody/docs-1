# FPGA相关说明

## 函数接口，包含启、停、状态获取三个

### 启动函数，负责模型文件，权重文件加载

* slave_name: fpga0,fpga1,fpga2,fpga3

* file_name: 打包的tar包文件,　解包后，包含了两个文件，一个是模型文件，module.bin；另一个是权重文件，param.bin 

* 执行成功返回值为０，其它为错误代码
```
s32 startFpgaExecutor(const char *slave_name, const char *file_name)
```

### 停止函数，停止指定通道fpga, 停止后进入复位状态，准备下次加载

* slave_name: fpga0,fpga1,fpga2,fpga3

* 执行成功返回值为０，其它为错误代码

```
s32 stopFpgaExecutor(const char *slave_name)
```

### 统计信息获取函数，负责获取执行过程中收发的数据量信息

* slave_name: fpga0,fpga1,fpga2,fpga3

* pStat: 输出信息结构体指针，相关结构定义如下
```
typedef enum
{
    _ResetStatus = 0,
    _RunningSatus = 1,
    其它状态枚举值...
    NUM_ERR_STATUS
} CoreStatus;

typedef struct _executionStat {
    CoreStatus coreStatus;
    u64 inputCounter;
    u64 outputCounter;
}FpgaExecutionStat;
```

* 执行成功返回值为０，其它为错误代码

```
s32 getFpgaExecutionStat(const char *slave_name, FpgaExecutionStat *pStat)
```

## 算法验证方式，包含从linux系统PCIE注入和从RapidIO接口注入两种方式

### PCIE方式

目前考虑的方式是:（供参考）

首先提供从pcie注入图片数据的接口，然后，通过将图片文件放在FT2000的linux文件系统上, 调用该接口，返回推理结果

### RapidIO方式

该方式在RapidIO接口调试验证完毕，交付模块后，配合验证

