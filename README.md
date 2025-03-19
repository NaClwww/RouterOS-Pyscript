# RouterOS-Pyscript

一个轻量级的RouterOS Python脚本框架，使您能够通过Python脚本轻松扩展和自动化RouterOS设备功能。

Make RouterOS Great Again！！！（雾

它允许您编写Python脚本来自动化RouterOS配置任务、监控网络状态、实现动态DNS更新等各种功能，而无需编写RouterOS的脚本，同时，python提供更多功能（目前只带了标准库），能够更加方便的编写脚本。

目前正在施工中

## 项目简介

采用api与RouterOS通信，api采用librouteros,详见https://librouteros.readthedocs.io/en/3.4.1/

将需要的脚本按照一定格式编写即可自动运行

## 食用说明

### 1.创建环境变量

| 变量名      | 描述               | 必填 |
| ----------- | ------------------ | ---- |
| ROUTER_IP   | RouterOS设备IP地址 | 是   |
| ROUTER_USER | RouterOS用户名     | 是   |
| ROUTER_PASS | RouterOS密码       | 是   |

### 2.挂载脚本文件夹

在file中创建文件夹，并将文件夹挂载到`/app/scripts`中

如果遇到无法创建文件夹的问题，请参考https://github.com/phistrom/routeros-mkdir

### 3.启动container

在shell中输入

````

````



## 编写脚本说明

在scripts目录中创建Python文件，脚本需要实现两个异步函数：

```python
import asyncio
import logging

# 脚本名称
SCRIPT_NAME = "example"
logger = None  # 会被主程序设置

async def Run(api):
    """初始化函数，程序启动时执行一次"""
    logger.info(f"脚本 {SCRIPT_NAME} 启动")
    return True

async def Loop(api):
    """循环函数，重复执行"""
    logger.info(f"执行 {SCRIPT_NAME} 循环操作")
    # 执行业务逻辑
    await asyncio.sleep(60)  # 等待60秒后再次执行
  
```

## To Do List
 -[x] 支持从本地文件导入scripts

 -[ ] 合理的多任务调度
 
 -[ ] 支持热重载

## 项目参考

Tiny Python Docker image： https://github.com/CrafterKolyan/tiny-python-docker-image

librouteros：https://github.com/luqasz/librouteros
