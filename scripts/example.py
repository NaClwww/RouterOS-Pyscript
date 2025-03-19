import asyncio
import logging
import sys

# 脚本名称，方便log识别
SCRIPT_NAME = "example"

# 设置触发器类型和触发器设置
# TRIGGER_TYPE = "interval" 表示定时触发
# TRIGGER_SETTING = 5 表示每5秒触发一次，暂时只支持秒级触发
# TRIGGER_TYPE = "cron" Developing
# 详见 https://apscheduler.readthedocs.io/
TRIGGER_TYPE = "interval" 
TRIGGER_SETTING = 5

# 配置日志输出到控制台，选配
logger = logging.getLogger(SCRIPT_NAME) 
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

async def Run(api):
    try:
        logger.debug(f"Run {SCRIPT_NAME}")
 
        if api:
            try:        

                # /system/identity/print    
                # 详细使用参考 https://librouteros.readthedocs.io/
                script = api.path('/system/identity')
                res =tuple(script('print'))[0]

                logger.info(f"Identity: {res['name']}")
            except Exception as e:
                logger.error(f"ERROR: {str(e)}")
        else:
            logger.warning("no api instance")
        logger.debug(f"finish run {SCRIPT_NAME}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")


async def Loop(api):
    try:
        logger.debug(f"Loop {SCRIPT_NAME}")
        if api:
            try:

                # /system/resource/print
                script = api.path('/system/resource')
                resource_data = tuple(script('print'))[0]

                logger.info(f"CPU Load: {resource_data['cpu-load']}%, Memory Usage: {((1 - resource_data['free-memory'] / resource_data['total-memory']) * 100):.2f}%")
            except Exception as e:
                logger.error(f"Error: {str(e)}")
        else:
            logger.warning("api connect fail")
    except Exception as e:
        logger.error(f"error: {str(e)}")