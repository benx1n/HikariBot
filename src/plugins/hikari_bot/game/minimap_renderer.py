import base64
import hashlib
import os

import requests
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, NoticeEvent
from requests.auth import HTTPBasicAuth

driver = get_driver()
minimap_renderer_temp = "minimap_renderer_temp"


async def get_rep(wows_rep_file_base64: str, bot: Bot, ev: NoticeEvent):
    file_hex = hashlib.sha256(wows_rep_file_base64.encode('utf-8')).hexdigest()
    file_bytes = base64.b64decode(wows_rep_file_base64)

    file_path_temp = os.getcwd() + os.sep + minimap_renderer_temp + os.sep + file_hex
    wowsrepla_file = file_path_temp + ".wowsreplay"
    if not os.path.exists(wowsrepla_file):
        with open(wowsrepla_file, 'wb') as f:
            f.write(file_bytes)
    await bot.send(ev, MessageSegment.text("正在处理replays文件.预计耗时1分钟"))
    upload_url = driver.config.minimap_renderer_url + "/upload_replays_video_url"
    with open(wowsrepla_file, 'rb') as file:
        files = {'file': file}
        response = requests.post(upload_url, files=files, auth=HTTPBasicAuth(driver.config.minimap_renderer_user_name, driver.config.minimap_renderer_password), timeout=600)
        if response.status_code == 200:
            await send_video(bot, ev, response.text)
        else:
            await bot.send(ev, MessageSegment.text("生成视频文件异常！请检查 minimap_renderer 是否要更新."))


async def send_video(bot: Bot, ev: NoticeEvent, url: str):
    # 构造视频文件消息
    data = str(driver.config.minimap_renderer_url + "/video_url?file_name=" + url.replace("\"", ""))
    await  bot.send(ev, MessageSegment.video(data))
