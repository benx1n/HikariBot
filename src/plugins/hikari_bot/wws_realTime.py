from typing import List
import httpx
import traceback
import jinja2
import re
import time
from pathlib import Path
from .data_source import servers,set_infoparams,set_damageColor,set_winColor,set_upinfo_color
from .utils import match_keywords
from .publicAPI import get_AccountIdByName
from nonebot_plugin_htmlrender import html_to_pic
from nonebot import get_driver
from nonebot.log import logger
from httpx import ConnectTimeout
from asyncio.exceptions import TimeoutError
from .utils import match_keywords,get_bot

dir_path = Path(__file__).parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)
env.globals.update(set_damageColor=set_damageColor,set_winColor=set_winColor,set_upinfo_color=set_upinfo_color,time=time,int=int,abs=abs,enumerate=enumerate)

headers = {
    'Authorization': get_driver().config.api_token
}

async def send_realTime_message(data):
    bot = get_bot()
    await bot.send_group_msg(group_id=574432871,message=f"[测试功能]雨季刚刚进入了一场战斗\n")