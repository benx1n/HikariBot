import time
import traceback
from os import getcwd
from pathlib import Path

import jinja2
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger
from nonebot_plugin_htmlrender import html_to_pic
from playwright.async_api import async_playwright

from .data_source import (
    select_prvalue_and_color,
    set_damageColor,
    set_upinfo_color,
    set_winColor,
)
from .publicAPI import get_all_shipList
from .utils import get_bot

dir_path = Path(__file__).parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)
env.globals.update(
    set_damageColor=set_damageColor,
    set_winColor=set_winColor,
    set_upinfo_color=set_upinfo_color,
    time=time,
    int=int,
    abs=abs,
    enumerate=enumerate,
)

headers = {"Authorization": get_driver().config.api_token}

# all_shipList = asyncio.run(get_all_shipList())


async def send_realTime_message(data):
    try:
        global all_shipList
        if not all_shipList:
            all_shipList = await get_all_shipList()
        bot = get_bot()
        template = env.get_template("wws-realTime.html")
        template_data = await set_realTime_params(data)
        content = await template.render_async(template_data)
        print(content)
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(f"file://{getcwd()}")
            await page.set_content(content, wait_until="networkidle")
            img = await page.screenshot(full_page=True)
            await browser.close()
        await bot.send_group_msg(
            group_id=639178962,
            message=f"[测试功能]雨季刚刚进入了一场战斗\n{MessageSegment.image(img)}",
        )
    except Exception:
        logger.error(traceback.format_exc())
        return


async def set_realTime_params(data):
    try:
        player_count = len(data["infoList"])
        for each_player in data["infoList"]:
            each_player["shipImgSmall"] = None
            for each_ship in all_shipList:
                if each_ship["id"] == each_player["shipId"]:
                    if each_ship["shipNameCn"]:
                        each_player["shipName"] = each_ship["shipNameCn"]
                    else:
                        each_player["shipName"] = each_ship["name"]
                    each_player["shipImgSmall"] = each_ship["imgSmall"]
                    each_player["shipIdValue"] = f"{each_ship['shipIdValue']}"
                    break
            if each_player["pvp"]:
                (
                    each_player["pvp"]["pr_name"],
                    each_player["pvp"]["pr_color"],
                ) = await select_prvalue_and_color(each_player["pvp"]["pr"])
            if each_player["ship"]:
                (
                    each_player["ship"]["pr_name"],
                    each_player["ship"]["pr_color"],
                ) = await select_prvalue_and_color(each_player["ship"]["pr"])
        data["player_count"] = player_count
        data["template_path"] = template_path
        logger.success(data)
        return data
    except Exception:
        logger.error(traceback.format_exc())
        return None


async def send_message(content):
    bot = get_bot()
    img = await html_to_pic(content, wait=0, viewport={"width": 1800, "height": 1000})
    await bot.send_group_msg(group_id=574432871, message=MessageSegment.image(img))
