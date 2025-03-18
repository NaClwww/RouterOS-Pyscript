import asyncio
import logging

SCRIPT_NAME = "example"


logger = logging.getLogger("example-script")

async def Run(api):
    try:
        logger.info(f"Run {SCRIPT_NAME}")
 
        if api:
            try:
                script = api.path('/system/identity')
                mssage =tuple(script('print'))
                logger.info(f"Identity: {mssage[0]["name"]}")
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
            if api:
                try:
                    script = api.path('/system/resource')
                    resource_data = tuple(script('print'))[0]
                    logger.info(f"CPU Load: {resource_data["cpu-load"]}%, Memory Usage: {(1-resource_data["free-memory"]/resource_data["total-memory"])*100}%")
                except Exception as e:
                    logger.error(f"Error: {str(e)}")
            else:
                logger.warning("未收到有效的API实例")
            await asyncio.sleep(10)

    except Exception as e:
        logger.error(f"示例脚本执行出错: {str(e)}")