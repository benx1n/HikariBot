import traceback
from loguru import logger
from nonebot import on_command, on_message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment,MessageEvent
from nonebot.log import logger
from .publicAPI import get_nation_list,get_ship_name,get_ship_byName
from .wws_info import get_AccountInfo
from .wws_recent import get_RecentInfo
from .wws_bind import set_BindInfo,get_BindInfo,change_BindInfo
from .wws_ship import get_ShipInfo,SecletProcess
from .data_source import command_list
from .utils import match_keywords,find_and_replace_keywords
import base64

__help__plugin_name__ = "wows"
__des__ = "Hikari"
__cmd__ = """
wws
""".strip()
__short_cmd__ = __cmd__
__example__ = """
wws me recent
""".strip()
__usage__ = f"{__des__}\nUsage:\n{__cmd__}\nExample:\n{__example__}"
WWS_help ="""
    帮助列表
    wws set/bind/绑定 服务器 游戏昵称：绑定QQ与游戏账号
    wws 查询绑定/查绑定/绑定列表[me][@]：查询指定用户的绑定账号
    wws 切换绑定[id]：使用查绑定中的序号快速切换绑定账号
    wws [服务器+游戏昵称][@群友][me]：查询账号总体战绩
    wws [服务器+游戏昵称][@群友][me] recent [日期]：查询账号近期战绩，默认1天
    wws [服务器+游戏昵称][@群友][me] ship 船名：查询单船总体战绩
    wws [搜/查船名] [国家][等级][类型]：查找符合条件的舰船中英文名称
    [待开发] wws ship recent
    [待开发] wws rank
    以上指令参数顺序均无强制要求，即你完全可以发送wws eu 7 recent Test以查询欧服Test七天内的战绩
    搭建bot请加官方群：967546463，如果您觉得bot还可以的话请点个star哦~
    仓库地址：https://github.com/benx1n/HikariBot
"""

bot = on_command("wws", block=True, priority=1)
bot_listen = on_message(priority=2)

@bot.handle()
async def selet_command(ev:MessageEvent, matchmsg: Message = CommandArg()):
        msg = ''
        qqid = ev.user_id
        select_command = None
        searchtag = str(matchmsg).strip()
        if not searchtag or searchtag=="":
            await bot.finish(WWS_help.strip())
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
                    msg = await get_ShipInfo(qqid,search_list,bot,ev)
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
        else:
            msg = '看不懂指令QAQ'
        if isinstance(msg,str):
            await bot.finish(msg)
        else:
            await bot.finish(MessageSegment.image(msg))
            
@bot_listen.handle()
async def change_select_state(ev:MessageEvent):
    msg = str(ev.message)
    qqid = ev.user_id
    if SecletProcess[qqid].SelectList and str(msg).isdigit():
        SecletProcess[qqid] = SecletProcess[qqid]._replace(state = True)
        SecletProcess[qqid] = SecletProcess[qqid]._replace(SlectIndex = int(msg))
    return