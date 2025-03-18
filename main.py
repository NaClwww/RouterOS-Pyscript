import os
import sys
import asyncio
import importlib.util
import logging
import librouteros

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("RouterOS-PyScript")

ROUTER_IP = os.getenv('ROUTER_IP')
USER = os.getenv('ROUTER_USER')
PASSWORD = os.getenv('ROUTER_PASS')
SCRIPT_DIR = "scripts"


async def run_script(script_path, api):
    scripts = []
    for script in os.listdir(script_path):
        if script.endswith('.py') and not script.startswith('__'):
            scripts.append(script)
    
    async def run_single_script(script_name):
        try:
            module_name = script_name.split('.')[0]
            script_module = importlib.import_module(f"scripts.{module_name}")
            script_module.logger = logging.getLogger(module_name)
            
            try:
                await script_module.Run(api)
            except Exception as e:
                script_module.logger.error(f"Run Error: {str(e)}")
            
            try:
                await script_module.Loop(api)
            except Exception as e:
                script_module.logger.error(f"Loop Error: {str(e)}")
        except Exception as e:
            logger.error(f"Script {script_name} 加载失败: {str(e)}")
    
    tasks = [run_single_script(script) for script in scripts]
    if tasks:
        await asyncio.gather(*tasks)
    else:
        logger.warning(f"没有找到可执行的脚本在 {script_path}")

def get_api(username, password, routerip):
    try:
        api = librouteros.connect(
            username=str(username),
            password=str(password),
            host=str(routerip),
        )
        return api
    except Exception as e:
        logger.error(f"connect fail: {str(e)}")
        return None

async def main_async():
    if not all([ROUTER_IP, USER, PASSWORD]):
        logger.error("Please set essential env: ROUTER_IP, ROUTER_USER, ROUTER_PASS")
        return
    
    api = None
    while not api:
        logger.info(f"Connecting: {ROUTER_IP}")
        api = get_api(USER, PASSWORD, ROUTER_IP)
        if api:        
            logger.info(f"Connected to {ROUTER_IP}")
            break
        logger.error(f"Connected failed to {ROUTER_IP}")
        await asyncio.sleep(5)  # 正确的异步等待
    
    logger.info(f"Scanning Scripts:")
    await run_script(SCRIPT_DIR, api)
    
    # 关闭API连接
    api.close()

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    logger.info("RouterOS-PyScript 启动")
    try:
        main()
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"主程序出错: {str(e)}")
        sys.exit(1)
    logger.info("RouterOS-PyScript 正常退出")
