import asyncio
import logging
import sys

SCRIPT_NAME = "example2"

TRIGGER_TYPE = "interval" 
TRIGGER_SECONDS = 5

# 配置日志输出到控制台
logger = logging.getLogger(SCRIPT_NAME)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

async def Run(api):
    try:
        logger.info(f"Run {SCRIPT_NAME}")
 
        if api:
            try:
                script = api.path('/system/identity')
                mssage =tuple(script('print'))
                logger.info(f"Identity: {mssage[0]['name']}")
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
        if api:
            try:
                script = api.path('/system/resource')
                resource_data = tuple(script('print'))[0]
                logger.info(f"CPU Load: {resource_data['cpu-load']}%, Memory Usage: {((1 - resource_data['free-memory'] / resource_data['total-memory']) * 100):.2f}%")
            except Exception as e:
                logger.error(f"Error: {str(e)}")
        else:
            logger.warning("api connect fail")
    except Exception as e:
        logger.error(f"error: {str(e)}")