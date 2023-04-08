import asyncio
import html
import json
import os
import platform
import random
import re
import sys
import traceback
from pathlib import Path

import httpx
from loguru import logger
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
from nonebot_plugin_htmlrender import text_to_pic

from .command_select import select_command
from .data_source import nb2_file
from .game.ocr import downlod_OcrResult, pic2txt_byOCR, upload_OcrResult
from .game.pupu import get_pupu_msg
from .mqtt import mqtt_run
from .utils import DailyNumberLimiter, FreqLimiter, download, get_bot
from .wws_clan import ClanSecletProcess
from .wws_ship import ShipSecletProcess

scheduler = require("nonebot_plugin_apscheduler").scheduler

_max = 100
EXCEED_NOTICE = f"您今天已经冲过{_max}次了，请明早5点后再来！"
is_first_run = True
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(3)
__version__ = "0.3.8"
dir_path = Path(__file__).parent
template_path = dir_path / "template"

bot = on_command("wws", block=False, aliases={"WWS"}, priority=54)
bot_pupu = on_fullmatch("噗噗", block=False, priority=5)
bot_checkversion = on_command("wws 检查更新", priority=5, block=False)
bot_update = on_command("wws 更新Hikari", priority=5, block=False, permission=SUPERUSER)
bot_listen = on_message(priority=5, block=False)
ocr_listen = on_message(priority=6, block=False)
driver = get_driver()


@bot.handle()
async def main(bot: Bot, ev: MessageEvent, matchmsg: Message = CommandArg()):
    try:
        server_type = None
        if isinstance(ev, PrivateMessageEvent) and (
            driver.config.private or str(ev.user_id) in driver.config.superusers
        ):  # 私聊事件,superusers默认不受影响
            server_type = "QQ"
        elif (
            isinstance(ev, GroupMessageEvent)
            and driver.config.group
            and ev.group_id not in driver.config.ban_group_list
        ):  # 群聊事件
            server_type = "QQ"
        elif isinstance(ev, GuildMessageEvent) and driver.config.channel:  # 频道事件
            if driver.config.all_channel or ev.channel_id in driver.config.channel_list:
                server_type = "QQ_CHANNEL"
            else:
                return False
        else:
            return False
        msg = ""
        qqid = ev.user_id
        replace_name = None
        if not _nlmt.check(qqid):
            await bot.send(ev, EXCEED_NOTICE, at_sender=True)
            return False
        if not _flmt.check(qqid):
            await bot.send(ev, "您冲得太快了，请稍候再冲", at_sender=True)
            return False
        _flmt.start_cd(qqid)
        _nlmt.increase(qqid)
        if random.randint(1,1000) == 1:
            await bot.send(ev, "一天到晚惦记你那b水表，就nm离谱")
            return False
        searchtag = html.unescape(str(matchmsg)).strip()
        if not searchtag:
            await bot.send(ev, "请发送wws help查看相关帮助")
            return False
        if searchtag == "help":
            msg = await send_bot_help()
            await bot.send(ev, MessageSegment.image(msg))
            return True
        match = re.search(r"(\(|（)(.*?)(\)|）)", searchtag)
        if match:
            replace_name = match.group(2)
            search_list = searchtag.replace(match.group(0), "").split()
        else:
            search_list = searchtag.split()
        command, search_list = await select_command(search_list)
        if replace_name:
            search_list.append(replace_name)
        msg = await command(server_type, search_list, bot, ev)
        if msg:
            if isinstance(msg, str):
                await bot.send(ev, msg)
                return True
            else:
                await bot.send(ev, MessageSegment.image(msg))
                return True
        else:
            await bot.send(ev, "没有获取到数据，可能是内部问题")
            return False
    except ActionFailed:
        logger.warning(traceback.format_exc())
        try:
            await bot.send(ev, "发不出图片，可能被风控了QAQ")
            return True
        except Exception:
            pass
        return False
    except Exception:
        logger.error(traceback.format_exc())
        await bot.send(ev, "呜呜呜发生了错误，可能是网络问题，如果过段时间不能恢复请联系麻麻哦~")


async def send_bot_help():
    try:
        url = "https://benx1n.oss-cn-beijing.aliyuncs.com/version.json"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            result = json.loads(resp.text)
        latest_version = result["latest_version"]
        url = "https://benx1n.oss-cn-beijing.aliyuncs.com/wws_help.txt"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            result = resp.text
        result = f"""帮助列表                                                当前版本{__version__}  最新版本{latest_version}\n{result}"""
        img = await text_to_pic(
            text=result, css_path=str(template_path / "text-help.css"), width=800
        )
        return img
    except Exception:
        logger.warning(traceback.format_exc())
        return "wuwuwu出了点问题，请联系麻麻解决"


@bot_listen.handle()
async def change_select_state(ev: MessageEvent):
    try:
        bot = get_bot()
        msg = str(ev.message)
        qqid = ev.user_id
        if ShipSecletProcess[qqid].SelectList and str(msg).isdigit():
            if int(msg) <= len(ShipSecletProcess[qqid].SelectList):
                ShipSecletProcess[qqid] = ShipSecletProcess[qqid]._replace(state=True)
                ShipSecletProcess[qqid] = ShipSecletProcess[qqid]._replace(
                    SlectIndex=int(msg)
                )
            else:
                await bot.send(ev, "请选择列表中的序号哦~")
        if ClanSecletProcess[qqid].SelectList and str(msg).isdigit():
            if int(msg) <= len(ClanSecletProcess[qqid].SelectList):
                ClanSecletProcess[qqid] = ClanSecletProcess[qqid]._replace(state=True)
                ClanSecletProcess[qqid] = ClanSecletProcess[qqid]._replace(
                    SlectIndex=int(msg)
                )
            else:
                await bot.send(ev, "请选择列表中的序号哦~")
    except Exception:
        logger.warning(traceback.format_exc())
        return


@ocr_listen.handle()
async def OCR_listen(bot: Bot, ev: MessageEvent):
    try:
        import time

        if not driver.config.ocr_on:
            return
        if not (str(ev.message).find("[CQ:image") + 1):  # 判断收到的信息是否为图片，不是就退出
            return
        tencent_url = ""
        for seg in ev.message:
            if seg.type == "image":
                tencent_url = seg.data["url"]
                filename = str(seg.data["file"]).replace(".image", "")
        ocr_text = await pic2txt_byOCR(tencent_url, filename)
        if ocr_text:
            match = re.search(r"^(/?)wws(.*?)$", ocr_text)
            if match:
                searchtag = re.sub(r"^(/?)wws", "", ocr_text)  # 删除wws和/wws
                is_send = await main(bot, ev, searchtag)
                if is_send:
                    await upload_OcrResult(ocr_text, filename)
    except Exception:
        logger.error(traceback.format_exc())
        return


@bot_update.handle()
async def update_Hikari(ev: MessageEvent, bot: Bot):
    try:
        from nonebot_plugin_reboot import Reloader

        await bot.send(ev, "正在更新Hikari，完成后将自动重启，如果没有回复您已上线的消息，请登录服务器查看")
        if hasattr(driver.config, "nb2_path"):
            await asyncio.gather(
                *[
                    download(each["url"], f"{driver.config.nb2_path}\{each['name']}")
                    for each in nb2_file
                ]
            )
        logger.info(f"当前解释器路径{sys.executable}")
        os.system(f"{sys.executable} -m pip install --upgrade hikari-bot")
        os.system(f"{sys.executable} -m pip install --upgrade nonebot-plugin-gocqhttp")
        Reloader.reload(delay=1)
    except RuntimeError:
        if str(platform.system()).lower() == "linux":
            try:
                import multiprocessing

                for child in multiprocessing.active_children():
                    child.terminate()
                sys.stdout.flush()
                # not compatible with cmdline with '\n'
                os.execv(
                    os.readlink("/proc/self/exe"),
                    open("/proc/self/cmdline", "rb")
                    .read()
                    .replace(b"\0", b"\n")
                    .decode()
                    .split("\n")[:-1],
                )
            except Exception:
                logger.error(traceback.format_exc())
                await bot.send(ev, "自动更新失败了QAQ，请登录服务器查看具体报错日志")
        else:
            logger.error(traceback.format_exc())
            await bot.send(ev, "不支持nb run启动的方式更新哦，请使用python bot.py 启动Hikari")
    except Exception:
        logger.error(traceback.format_exc())
        await bot.send(ev, "自动更新失败了QAQ，请登录服务器查看具体报错日志")


@bot_checkversion.handle()
async def check_version():
    try:
        bot = get_bot()
        url = "https://benx1n.oss-cn-beijing.aliyuncs.com/version.json"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            result = json.loads(resp.text)
        superid = driver.config.superusers
        match, msg = False, f"发现新版本"
        for each in result["data"]:
            if each["version"] > __version__:
                match = True
                msg += f"\n{each['date']} v{each['version']}\n"
                for i in each["description"]:
                    msg += f"{i}\n"
        msg += "实验性更新指令：wws 更新Hikari，请在能登录上服务器的情况下执行该命令"
        if match:
            for each in superid:
                await bot.send_private_msg(user_id=int(each), message=msg)
            try:
                await bot_checkversion.send(msg)
            except Exception:
                return
        else:
            for each in superid:
                await bot.send_private_msg(
                    user_id=int(each), message="Hikari:当前已经是最新版本了"
                )
            try:
                await bot_checkversion.send("Hikari:当前已经是最新版本了")
            except Exception:
                return
        return
    except Exception:
        logger.warning(traceback.format_exc())
        return


@driver.on_startup
async def startup():
    try:
        tasks = []
        loop = asyncio.get_running_loop()
        url = "https://benx1n.oss-cn-beijing.aliyuncs.com/template_Hikari_Latest/template.json"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=20)
            result = resp.json()
            for each in result:
                for name, url in each.items():
                    tasks.append(asyncio.ensure_future(startup_download(url, name)))
        await asyncio.gather(*tasks)
        if driver.config.ocr_on:
            await downlod_OcrResult()
    except Exception:
        logger.error(traceback.format_exc())
        return


@driver.on_bot_connect
async def remind(bot: Bot):
    superid = driver.config.superusers
    bot_info = await bot.get_login_info()
    for each in superid:
        await bot.send_private_msg(
            user_id=int(each), message=f"Hikari已上线，当前版本{__version__}"
        )
    # global is_first_run
    # if is_first_run:
    #    mqtt_run(bot_info['user_id'])
    #    is_first_run = False


async def startup_download(url, name):
    async with httpx.AsyncClient() as client:
        resp = resp = await client.get(url, timeout=20)
        with open(template_path / name, "wb+") as file:
            file.write(resp.content)


scheduler.add_job(
    check_version,
    "cron",
    hour=12,
)
scheduler.add_job(startup, "cron", hour=4)
scheduler.add_job(downlod_OcrResult, "interval", minutes=10)


@bot_pupu.handle()
async def send_pupu_msg(ev: MessageEvent, bot: Bot):
    try:
        if (
            driver.config.pupu
            and isinstance(ev, GroupMessageEvent)
            and driver.config.group
            and ev.group_id not in driver.config.ban_group_list
        ):
            msg = await get_pupu_msg()
            await bot.send(ev, msg)
    except ActionFailed:
        logger.warning(traceback.format_exc())
        try:
            await bot.send(ev, "噗噗寄了>_<可能被风控了QAQ")
        except Exception:
            pass
        return
