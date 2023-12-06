import asyncio
import os
import platform
import re
import sys
import traceback
from collections import defaultdict, namedtuple

import httpx
from hikari_core import callback_hikari, init_hikari, set_hikari_config
from hikari_core.data_source import __version__
from hikari_core.game.help import check_version
from hikari_core.model import Hikari_Model
from hikari_core.moudle.wws_real_game import get_diff_ship
from nonebot import get_driver, on_command, on_fullmatch, on_message, require
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot_plugin_guild_patch import GuildMessageEvent

from .data_source import dir_path, nb2_file, template_path
from .game.ocr import (
    downlod_OcrResult,
    get_Random_Ocr_Pic,
    pic2txt_byOCR,
    upload_OcrResult,
)
from .game.pupu import get_pupu_msg
from .utils import DailyNumberLimiter, FreqLimiter, download, get_bot

scheduler = require('nonebot_plugin_apscheduler').scheduler

_max = 100
EXCEED_NOTICE = f'您今天已经冲过{_max}次了，请明早5点后再来！'
is_first_run = True
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(3)
__bot_version__ = '1.0.6'

bot_get_random_pic = on_fullmatch('wws 随机表情包', block=True, priority=5)
bot_update = on_fullmatch('wws 更新Hikari', priority=5, block=True, permission=SUPERUSER)
bot = on_command('wws', block=False, aliases={'WWS'}, priority=54)
bot_pupu = on_fullmatch('噗噗', block=False, priority=5)
bot_listen = on_message(priority=5, block=False)
ocr_listen = on_message(priority=6, block=False)
driver = get_driver()

_proxy = None
if driver.config.proxy_on:
    _proxy = driver.config.proxy

set_hikari_config(
    use_broswer=driver.config.htmlrender_browser,
    http2=driver.config.http2,
    proxy=_proxy,
    token=driver.config.api_token,
    game_path=str(dir_path / 'game'),
)

SlectState = namedtuple('SlectState', ['state', 'SlectIndex', 'SelectList'])
SecletProcess = defaultdict(lambda: SlectState(False, None, None))


@bot.handle()
async def main(bot: Bot, ev: MessageEvent, matchmsg: Message = CommandArg()):  # noqa: B008, PLR0915
    try:
        server_type = None
        if isinstance(ev, PrivateMessageEvent) and (driver.config.private or str(ev.user_id) in driver.config.superusers):  # 私聊事件,superusers默认不受影响
            server_type = 'QQ'
        elif isinstance(ev, GroupMessageEvent) and driver.config.group and ev.group_id not in driver.config.ban_group_list:  # 群聊事件
            server_type = 'QQ'
        elif isinstance(ev, GuildMessageEvent) and driver.config.channel:  # 频道事件
            if driver.config.all_channel or ev.channel_id in driver.config.channel_list:
                server_type = 'QQ_CHANNEL'
            else:
                return False
        else:
            return False
        qqid = ev.user_id
        group_id = None
        if ev.message_type == 'group':
            group_id = ev.group_id
        if not _nlmt.check(qqid):
            await bot.send(ev, EXCEED_NOTICE, at_sender=True)
            return False
        if not _flmt.check(qqid):
            await bot.send(ev, '您冲得太快了，请稍候再冲', at_sender=True)
            return False
        _flmt.start_cd(qqid)
        _nlmt.increase(qqid)
        superuser_command_list = ['重置监控']
        adminuser_command_list = ['添加监控', '删除监控']
        for each in superuser_command_list:
            if (each in str(ev.message) or each in matchmsg) and str(qqid) not in driver.config.superusers:
                await bot.send(ev, '该命令仅限超级管理员使用')
                return
        if str(qqid) not in driver.config.superusers:
            for each in adminuser_command_list:
                if (each in str(ev.message) or each in matchmsg) and qqid not in driver.config.admin_list:
                    await bot.send(ev, '请联系机器人搭建者添加权限')
                    return
        hikari = await init_hikari(platform=server_type, PlatformId=str(qqid), command_text=str(matchmsg), GroupId=group_id)
        if hikari.Status == 'success':
            if isinstance(hikari.Output.Data, bytes):
                await bot.send(ev, MessageSegment.image(hikari.Output.Data))
            elif isinstance(hikari.Output.Data, str):
                await bot.send(ev, hikari.Output.Data)
        elif hikari.Status == 'wait':
            await bot.send(ev, MessageSegment.image(hikari.Output.Data))
            hikari = await wait_to_select(hikari)
            if hikari.Status == 'error':
                await bot.send(ev, str(hikari.Output.Data))
                return
            hikari = await callback_hikari(hikari)
            if isinstance(hikari.Output.Data, bytes):
                await bot.send(ev, MessageSegment.image(hikari.Output.Data))
            elif isinstance(hikari.Output.Data, str):
                await bot.send(ev, str(hikari.Output.Data))
        else:
            await bot.send(ev, str(hikari.Output.Data))
    except ActionFailed:
        logger.warning(traceback.format_exc())
        try:
            await bot.send(ev, '发不出图片，可能被风控了QAQ')
            return True
        except Exception:
            pass
        return False
    except Exception:
        logger.error(traceback.format_exc())
        await bot.send(ev, '呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')


@bot_listen.handle()
async def change_select_state(bot: Bot, ev: MessageEvent):
    try:
        # bot = get_bot()
        msg = str(ev.message)
        qqid = str(ev.user_id)
        if SecletProcess[qqid].state and str(msg).isdigit():
            if int(msg) <= len(SecletProcess[qqid].SelectList):
                SecletProcess[qqid] = SecletProcess[qqid]._replace(state=False)
                SecletProcess[qqid] = SecletProcess[qqid]._replace(SlectIndex=int(msg))
            else:
                await bot.send(ev, '请选择列表中的序号哦~')
        return
    except Exception:
        logger.error(traceback.format_exc())
        return


async def wait_to_select(hikari):
    SecletProcess[hikari.UserInfo.PlatformId] = SlectState(True, None, hikari.Input.Select_Data)
    a = 0
    while a < 40 and not SecletProcess[hikari.UserInfo.PlatformId].SlectIndex:
        a += 1
        await asyncio.sleep(0.5)
    if SecletProcess[hikari.UserInfo.PlatformId].SlectIndex:
        hikari.Input.Select_Index = SecletProcess[hikari.UserInfo.PlatformId].SlectIndex
        SecletProcess[hikari.UserInfo.PlatformId] = SlectState(False, None, None)
        return hikari
    else:
        SecletProcess[hikari.UserInfo.PlatformId] = SlectState(False, None, None)
        return hikari.error('已超时退出')


@ocr_listen.handle()
async def OCR_listen(bot: Bot, ev: MessageEvent):
    try:
        if not driver.config.ocr_on:
            return
        if not (str(ev.message).find('[CQ:image') + 1):  # 判断收到的信息是否为图片，不是就退出
            return
        tencent_url = ''
        for seg in ev.message:
            if seg.type == 'image':
                tencent_url = seg.data['url']
                filename = str(seg.data['file']).replace('.image', '')
        ocr_text = await pic2txt_byOCR(tencent_url, filename)
        if ocr_text:
            match = re.search(r'^(/?)wws(.*?)$', ocr_text)
            if match:
                searchtag = re.sub(r'^(/?)wws', '', ocr_text)  # 删除wws和/wws
                is_send = await main(bot, ev, searchtag)
                if is_send:
                    await upload_OcrResult(ocr_text, filename)
    except Exception:
        logger.error(traceback.format_exc())
        return


@bot_get_random_pic.handle()
async def send_random_ocr_image(bot: Bot, ev: MessageEvent):
    try:
        img = await get_Random_Ocr_Pic()
        if isinstance(img, bytes):
            await bot.send(ev, MessageSegment.image(img))
        elif isinstance(img, str):
            await bot.send(ev, str(img))
    except Exception:
        logger.error(traceback.format_exc())
        await bot.send(ev, '呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~')
        return


@bot_update.handle()
async def update_Hikari(ev: MessageEvent, bot: Bot):
    try:
        from nonebot_plugin_reboot import Reloader

        await bot.send(ev, '正在更新Hikari，完成后将自动重启，如果没有回复您已上线的消息，请登录服务器查看')
        if hasattr(driver.config, 'nb2_path'):
            # 并发fastgit会429，改为顺序请求
            for each in nb2_file:
                await download(each['url'], f"{driver.config.nb2_path}\\{each['name']}")
                await asyncio.sleep(0.5)

            # await asyncio.gather(
            #    *[download(each["url"], f"{driver.config.nb2_path}\{each['name']}") for each in nb2_file]
            # )
        logger.info(f'当前解释器路径{sys.executable}')
        os.system(f'{sys.executable} -m pip install hikari-bot -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade')
        os.system(f'{sys.executable} -m pip install hikari-core -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade')
        os.system(f'{sys.executable} -m pip install nonebot-plugin-gocqhttp -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade')
        Reloader.reload(delay=1)
    except RuntimeError:
        if str(platform.system()).lower() == 'linux':
            try:
                import multiprocessing

                for child in multiprocessing.active_children():
                    child.terminate()
                sys.stdout.flush()
                # not compatible with cmdline with '\n'
                os.execv(
                    os.readlink('/proc/self/exe'),
                    open('/proc/self/cmdline', 'rb').read().replace(b'\0', b'\n').decode().split('\n')[:-1],
                )
            except Exception:
                logger.error(traceback.format_exc())
                await bot.send(ev, '自动更新失败了QAQ，请登录服务器查看具体报错日志')
        else:
            logger.error(traceback.format_exc())
            await bot.send(ev, '不支持nb run启动的方式更新哦，请使用python bot.py 启动Hikari')
    except Exception:
        logger.error(traceback.format_exc())
        await bot.send(ev, '自动更新失败了QAQ，请登录服务器查看具体报错日志')


@driver.on_startup
async def startup():
    try:
        if driver.config.ocr_on:
            await downlod_OcrResult()
    except Exception:
        logger.error(traceback.format_exc())
        return


@driver.on_bot_connect
async def remind(bot: Bot):
    superid = driver.config.superusers
    await bot.get_login_info()
    for each in superid:
        await bot.send_private_msg(user_id=int(each), message=f'Hikari已上线，当前BOT版本{__bot_version__},内核版本{__version__}')


async def startup_download(url, name):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=20)
        with open(template_path / name, 'wb+') as file:
            file.write(resp.content)


async def job_chech_version():
    bot = get_bot()
    hikari = Hikari_Model()
    hikari = await check_version(hikari)
    superid = driver.config.superusers
    for each in superid:
        await bot.send_private_msg(user_id=int(each), message=hikari.Output.Data)


async def job_listen_battle():
    bot = get_bot()
    hikari = Hikari_Model()
    hikari = await get_diff_ship(hikari)
    if hikari.Status == 'success':
        for _each in hikari.Output.Data:
            await bot.send_group_msg(group_id=_each['group_id'], message=_each['msg'])


scheduler.add_job(job_chech_version, 'cron', hour=12)
scheduler.add_job(startup, 'cron', hour=4)
scheduler.add_job(downlod_OcrResult, 'interval', minutes=10)
scheduler.add_job(job_listen_battle, 'interval', minutes=driver.config.battle_listen_time)


@bot_pupu.handle()
async def send_pupu_msg(ev: MessageEvent, bot: Bot):
    try:
        if driver.config.pupu and isinstance(ev, GroupMessageEvent) and driver.config.group and ev.group_id not in driver.config.ban_group_list:
            msg = await get_pupu_msg()
            await bot.send(ev, msg)
    except ActionFailed:
        logger.warning(traceback.format_exc())
        try:
            await bot.send(ev, '噗噗寄了>_<可能被风控了QAQ')
        except Exception:
            pass
        return
