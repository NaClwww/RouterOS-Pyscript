import asyncio
import logging

SCRIPT_NAME = "example"


logger = logging.getLogger("example-script")

async def Run(api):
    try:
        logger.info(f"Run {SCRIPT_NAME}")
 
        if api:
            try:
                # 获取系统标识
                script = api.path('/system/identity')
                # identity = identity_resource.get()[0]['name']
                mssage =tuple(script('print'))
                logger.info(f"Identity: {mssage[0]["name"]}")
                # 获取系统资源使用情况
                # resource = api.get_resource('/system/resource')
                # resource_data = resource[0]
                # logger.info(f"CPU Load: {resource_data.get('cpu-load')}%, Memory Usage: {resource_data.get('free-memory')}/{resource_data.get('total-memory')}")
            except Exception as e:
                logger.error(f"ERROR: {str(e)}")
        else:
            logger.warning("no api instance")
        
        logger.info(f"finish run {SCRIPT_NAME}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

async def Loop(api):
    try:
        logger.info(f"Loop {SCRIPT_NAME}")
        
        while True:            
            # 使用传入的API实例操作RouterOS
            # 无需自己创建连接
            if api:
                try:
                    # 获取系统资源使用情况
                    script = api.path('/system/resource')
                    resource_data = tuple(script('print'))[0]
                    # print(resource_data)
                    logger.info(f"CPU Load: {resource_data["cpu-load"]}%, Memory Usage: {(1-resource_data["free-memory"]/resource_data["total-memory"])*100}%")
                except Exception as e:
                    logger.error(f"Error: {str(e)}")
            else:
                logger.warning("未收到有效的API实例")
            
            # 模拟异步操作
            await asyncio.sleep(10)

    except Exception as e:
        logger.error(f"示例脚本执行出错: {str(e)}")