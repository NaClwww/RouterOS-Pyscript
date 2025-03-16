import os
import sys
import asyncio
import importlib.util
import logging
import librouteros
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("RouterOS-PyScript")

ROUTER_IP = os.getenv('ROUTER_IP')
ROUTER_PORT = os.getenv('ROUTER_PORT', '8728')
USER = os.getenv('ROUTER_USER')
PASSWORD = os.getenv('ROUTER_PASS')
SCRIPT_DIR = "/app/main/scripts"


async def run_script(script_path, api):
    # 扫描脚本目录
    scripts = []
    for script in os.listdir(script_path):
        if script.endswith('.py') and not script.startswith('__'):
            scripts.append(script)
    for script in scripts:
        script_name = script.split('.')[0]
        script_module = importlib.import_module(f"scripts.{script_name}")
        script_module.logger = logging.getLogger(script_name)
        try:
            await script_module.Run(api)
        except Exception as e:
            script_module.logger.error(f"Error: {str(e)}")
        try:
            await script_module.Loop(api)
        except Exception as e:
            script_module.logger.error(f"Error: {str(e)}")

def get_api(username, password, routerip, routerport='8728'):
    try:
        api = librouteros.connect(
            username=username,
            password=password,
            host=routerip,
            port=int(routerport)
        )
        return api
    except Exception as e:
        logger.error(f"connect fail: {str(e)}")
        return None

async def main():
    if not all([ROUTER_IP, USER, PASSWORD]):
        logger.error("Please set essential env: ROUTER_IP, ROUTER_USER, ROUTER_PASS")
        return
    
    # 连接到RouterOS
    logger.info(f"Connecting: {ROUTER_IP}:{ROUTER_PORT}")
    api = get_api(USER, PASSWORD, ROUTER_IP, ROUTER_PORT)
    if not api:
        logger.error("Connected failed to {ROUTER_IP}")
        return
    
    logger.info(f"Connected to {ROUTER_IP}")

    logger.info(f"Scaning Scripts:")
    
    await run_script(SCRIPT_DIR, api)
    
    # 关闭API连接
    api.close()

if __name__ == "__main__":
    logger.info("RouterOS-PyScript 启动")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"主程序出错: {str(e)}")
        sys.exit(1)
    logger.info("RouterOS-PyScript 正常退出")
