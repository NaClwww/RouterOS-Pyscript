# RouterOS-Pyscript

一个轻量级的RouterOS Python脚本框架，使您能够通过Python脚本轻松扩展和自动化RouterOS设备功能。

Make RouterOS Great Again！！！（雾

它允许您编写Python脚本来自动化RouterOS配置任务、监控网络状态、实现动态DNS更新等各种功能，而无需编写RouterOS的脚本，同时，python提供更多功能（目前只带了标准库+librouteros+apscheduler），能够更加方便的编写脚本。

## 项目简介

采用api与RouterOS通信，api采用librouteros,详见https://librouteros.readthedocs.io/

将需要的脚本按照一定格式编写即可自动运行

## 食用说明

### 0.创建容器

从本地导入或者从github拉container

### 1.创建环境变量

| 变量名        | 描述               | 必填                 |
| ------------- | ------------------ | -------------------- |
| ROUTER_IP     | RouterOS设备IP地址 | 选填，默认172.17.0.1 |
| ROUTER_USER   | RouterOS用户名     | 是                   |
| ROUTER_PASS   | RouterOS密码       | 是                   |
| RELOAD_DETECT | 扫描脚本间隔       | 选填，默认10秒       |

### 2.创建脚本文件夹

在file中创建文件夹，并将文件夹挂载到`/app/scripts`中

如果遇到无法创建文件夹的问题，请参考https://github.com/phistrom/routeros-mkdir

在container中创建Mounts，Src填写本地地址，Dst填写`/app/scripts`

### 3.启动container

在container中添加

- Envlist
- Mounts

## 编写脚本说明

在scripts目录中创建Python文件，脚本需要实现两个异步函数：

```python
async def Run(api):
	#初始化时执行的代码 
    
async def Loop(api):
    #需要定时或循环执行的代码

```

具体参考项目中的`scripts/example.py`样例

## To Do List

 - [x] 支持从本地文件导入scripts
 - [x] 合理的多任务调度
 - [x] 支持热重载
 - [ ] 更好的环境隔离，防止一摸知所有
 - [ ] 更多的trigger类型支持
 - [ ] 动态加载更多的库

## 项目参考

Tiny Python Docker image： https://github.com/CrafterKolyan/tiny-python-docker-image

librouteros：https://github.com/luqasz/librouteros
