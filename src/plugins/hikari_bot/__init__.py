import traceback
from loguru import logger
from nonebot import get_bot, on_command, on_message, get_driver
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment,MessageEvent,Bot
from nonebot.log import logger
from .publicAPI import get_nation_list,get_ship_name,get_ship_byName
from .wws_info import get_AccountInfo
from .wws_recent import get_RecentInfo
from .wws_bind import set_BindInfo,get_BindInfo,change_BindInfo
from .wws_ship import get_ShipInfo,SecletProcess
from .wws_shiprank import get_ShipRank
from .data_source import command_list
from .utils import find_and_replace_keywords,DailyNumberLimiter,FreqLimiter
from nonebot_plugin_htmlrender import text_to_pic
from pathlib import Path
import httpx
import json
from nonebot import require
scheduler = require("nonebot_plugin_apscheduler").scheduler

_max = 100
EXCEED_NOTICE = f'您今天已经冲过{_max}次了，请明早5点后再来！'
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(3)
__version__ = '0.2.2'
dir_path = Path(__file__).parent
css_path = dir_path / "template"/"text.css"

bot = on_command("wws", block=True, aliases={"WWS"},priority=5)
bot_listen = on_message(priority=5)
bot_checkversion = on_command("wws 检查更新",priority=5)

@bot.handle()
async def selet_command(ev:MessageEvent, matchmsg: Message = CommandArg()):
    msg = ''
    qqid = ev.user_id
    select_command = None
    if not _nlmt.check(qqid):
        await bot.send(EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(qqid):
        await bot.send('您冲得太快了，请稍候再冲', at_sender=True)
        return
    _flmt.start_cd(qqid)
    _nlmt.increase(qqid) 
    searchtag = str(matchmsg).strip()
    if not searchtag or searchtag=="":
        await send_bot_help()
    search_list = str(matchmsg).split()
    
    select_command,search_list = await find_and_replace_keywords(search_list,command_list)
    if not select_command:
        try:
            msg = await get_AccountInfo(qqid,search_list)
        except Exception:
            logger.warning(traceback.format_exc())
            await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
    elif select_command == 'ship':
        select_command = None
        select_command,search_list = await find_and_replace_keywords(search_list,command_list)         #第二次匹配
        if not select_command:
            try:
                msg = await get_ShipInfo(qqid,search_list,bot)
            except Exception:
                logger.warning(traceback.format_exc())
                await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
        elif select_command == 'recent':
            msg = "待开发：查单船近期战绩"
        else:
            msg = '看不懂指令QAQ'
    elif select_command == 'recent':
        select_command = None
        select_command,search_list = await find_and_replace_keywords(search_list,command_list)             #第二次匹配
        if not select_command:
            try:
                msg = await get_RecentInfo(qqid,search_list)
            except Exception:
                logger.warning(traceback.format_exc())
                await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
        elif select_command == 'ship':
            msg = '待开发：查单船近期战绩'
        else:
            msg = '：看不懂指令QAQ'
    elif select_command == 'ship_rank':
        try:
            msg = await get_ShipRank(qqid,search_list,bot)
        except Exception:
            logger.warning(traceback.format_exc())
            await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')    
    elif select_command == 'bind':
        try:
            msg = await set_BindInfo(qqid,search_list)
        except Exception:
            logger.warning(traceback.format_exc())
            await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
    elif select_command == 'bindlist':
        try:
            msg = await get_BindInfo(qqid,search_list)
        except Exception:
            logger.warning(traceback.format_exc())
            await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
    elif select_command == 'changebind':
        try:
            msg = await change_BindInfo(qqid,search_list)
        except Exception:
            logger.warning(traceback.format_exc())
            await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
    elif select_command == 'searchship':
        try:
            msg = await get_ship_name(search_list)
        except Exception:
            logger.warning(traceback.format_exc())
            await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
    elif select_command == 'help':
        try:
            msg = await send_bot_help()
        except Exception:
            logger.warning(traceback.format_exc())
            await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
    else:
        msg = '看不懂指令QAQ'
    if msg:
        if isinstance(msg,str):
            await bot.finish(msg)
        else:
            await bot.finish(MessageSegment.image(msg))
    else:
        await bot.finish('呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
                
async def send_bot_help():
    url = 'https://benx1n.oss-cn-beijing.aliyuncs.com/version.json'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10)
        result = json.loads(resp.text)
    latest_version = result['latest_version']
    url = 'https://benx1n.oss-cn-beijing.aliyuncs.com/wws_help.txt'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10)
        result = resp.text
    result = f'''帮助列表                                                当前版本{__version__}  最新版本{latest_version}\n{result}'''
    img = await text_to_pic(text = result,css_path= str(css_path), width = 800)
    return img
    
@bot_listen.handle()
async def change_select_state(ev:MessageEvent):
    msg = str(ev.message)
    qqid = ev.user_id
    if SecletProcess[qqid].SelectList and str(msg).isdigit():
        SecletProcess[qqid] = SecletProcess[qqid]._replace(state = True)
        SecletProcess[qqid] = SecletProcess[qqid]._replace(SlectIndex = int(msg))

@bot_checkversion.handle()
async def check_version():
    try:
        bot = get_bot()
        url = 'https://benx1n.oss-cn-beijing.aliyuncs.com/version.json'
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            result = json.loads(resp.text)
        superid = get_driver().config.superusers
        match,msg = False,f'发现新版本'
        for each in result['data']:
            if each['version'] > __version__:
                match = True
                msg += f"\n{each['date']} v{each['version']}\n"
                for i in each['description']:
                    msg += f"{i}\n"
        if match:
            for each in superid:
                await bot.send_private_msg(user_id=int(each),message=msg)
            try:
                await bot_checkversion.send(msg)
            except Exception:
                return
        return
    except Exception:
        logger.warning(traceback.format_exc())
        return
        
scheduler.add_job(
    check_version,
    "cron",
    hour = 12,
)
