import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import librouteros
import asyncio
import logging
import importlib
import os

logger = logging.getLogger("scheduler")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

ROUTER_IP = os.getenv('ROUTER_IP','172.17.0.1')
USER = os.getenv('ROUTER_USER')
PASSWORD = os.getenv('ROUTER_PASS')
RELOAD_DETECT = os.getenv('RELOAD_DETECT','10')
SCRIPT_DIR = "scripts"

def get_api(username, password, routerip):
    try:
        api = librouteros.connect(
            username=username,
            password=password,
            host=routerip,
        )
        return api
    except Exception as e:
        logger.error(f"connect fail: {str(e)}")
        logger.error(f"{ROUTER_IP} {USER} {PASSWORD}")
        return None

async def get_script_list(script_path):
    scripts = []
    for script in os.listdir(script_path):
        if script.endswith('.py') and not script.startswith('__'):
            scripts.append(script[:-3])
    return scripts

async def run_script(script_name, api):
    try:
        script_module = importlib.import_module(f"{SCRIPT_DIR}.{script_name}")
        await script_module.Run(api)
    except Exception as e:
        logger.error(f"Run {script_name} fail: {str(e)}")
    
    try:
        if script_module.TRIGGER_TYPE == "interval":
            scheduler.add_job(script_module.Loop, 'interval', seconds=script_module.TRIGGER_SECONDS, args=[api])
        # elif script_module.TRIGGER_TYPE == "cron":
        #     scheduler.add_job(script_module.Loop, 'cron', second=script_module.TRIGGER_SECONDS, args=[api])
    except Exception as e:
        logger.error(f"Loop {script_name} fail: {str(e)}")

async def stop_script(script_name):
    global scheduler
    try:
        scheduler.remove_job(script_name)
    except Exception as e:
        logger.error(f"Stop {script_name} fail: {str(e)}")

async def main_async():
    # login
    while True:
        api = get_api(USER, PASSWORD, ROUTER_IP)
        if api:
            logger.info(f"connect success to {ROUTER_IP}")
            break
        else:
            logger.error(f"connect fail, retry in {10} seconds")
        await asyncio.sleep(int(10))
    
    # run scripts
    scripts_old = []
    global scheduler
    scheduler.start()
    while True:
        scripts_new = await get_script_list(SCRIPT_DIR)
        for script in scripts_new:  
            if script not in scripts_old:
                await run_script(script, api)  

        for script in scripts_old:  
            if script not in scripts_new:
                await stop_script(script) 
        scripts_old = scripts_new
        await asyncio.sleep(int(RELOAD_DETECT))

def check():
    if USER is None or PASSWORD is None:
        logger.error("Please set USER and PASSWORD in environment")
        exit(1)

if __name__ == "__main__":
    check()
    global scheduler
    scheduler = AsyncIOScheduler()
    asyncio.run(main_async())