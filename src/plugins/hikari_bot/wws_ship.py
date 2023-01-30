import asyncio
import re
import time
import traceback
from asyncio.exceptions import TimeoutError
from collections import defaultdict, namedtuple
from datetime import datetime
from pathlib import Path
from typing import List

import httpx
import jinja2
from bs4 import BeautifulSoup
from httpx import ConnectTimeout
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import ActionFailed, MessageSegment
from nonebot.log import logger
from nonebot_plugin_htmlrender import html_to_pic, text_to_pic

from .data_source import (
    number_url_homes,
    servers,
    set_damageColor,
    set_shipparams,
    set_shipRecentparams,
    set_upinfo_color,
    set_winColor,
    tiers,
)
from .publicAPI import check_yuyuko_cache, get_AccountIdByName, get_ship_byName
from .utils import get_bot, match_keywords

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

ShipSlectState = namedtuple("ShipSlectState", ["state", "SlectIndex", "SelectList"])
ShipSecletProcess = defaultdict(lambda: ShipSlectState(False, None, None))


async def get_ShipInfo(server_type, info, bot, ev):
    try:
        bot = get_bot()
        url, params = "", ""
        if isinstance(info, List):
            for flag, i in enumerate(info):  # 是否包含me或@，包含则调用平台接口
                if str(i).lower() == "me":
                    params = {
                        "server": server_type,
                        "accountId": int(ev.user_id),
                    }
                    info.remove(str(i))
                match = re.search(r"CQ:at,qq=(\d+)", i)
                if match:
                    params = {
                        "server": server_type,
                        "accountId": int(match.group(1)),
                    }
                    info[flag] = str(i).replace(f"[{match.group(0)}]", "")
                    if not info[flag]:
                        info.remove("")
                    break
            if not params and len(info) == 3:
                param_server, info = await match_keywords(info, servers)
                if param_server:
                    param_accountid = await get_AccountIdByName(
                        param_server, str(info[0])
                    )  # 剩余列表第一个是否为游戏名
                    if isinstance(param_accountid, int):
                        info.remove(info[0])
                        params = {
                            "server": param_server,
                            "accountId": param_accountid,
                        }
                    else:
                        return f"{param_accountid}"
                else:
                    return "服务器参数似乎输错了呢"
            elif params and len(info) == 1:
                logger.success(f"{params}")
            elif params:
                return "您似乎准备用查询自己的单船战绩，请检查参数中是否带有船名，以空格区分"
            else:
                return "您似乎准备用游戏昵称查询单船战绩，请检查参数中是否包含服务器、游戏昵称和船名，以空格区分"
            shipList = await get_ship_byName(str(info[0]))
            logger.success(f"{shipList}")
            if shipList:
                if len(shipList) < 2:
                    params["shipId"] = shipList[0][0]
                else:
                    msg = f"存在多条名字相似的船\n请在20秒内选择对应的序号\n================\n"
                    flag = 0
                    for each in shipList:
                        flag += 1
                        msg += f"{flag}：{tiers[each[3]-1]} {each[1]}\n"
                    ShipSecletProcess[ev.user_id] = ShipSlectState(
                        False, None, shipList
                    )
                    img = await text_to_pic(
                        text=msg,
                        css_path=str(template_path / "text-ship.css"),
                        width=250,
                    )
                    await bot.send(ev, MessageSegment.image(img))
                    a = 0
                    while a < 40 and not ShipSecletProcess[ev.user_id].state:
                        a += 1
                        await asyncio.sleep(0.5)
                    if ShipSecletProcess[ev.user_id].state and ShipSecletProcess[
                        ev.user_id
                    ].SlectIndex <= len(shipList):
                        params["shipId"] = shipList[
                            ShipSecletProcess[ev.user_id].SlectIndex - 1
                        ][0]
                        ShipSecletProcess[ev.user_id] = ShipSlectState(
                            False, None, None
                        )
                    else:
                        ShipSecletProcess[ev.user_id] = ShipSlectState(
                            False, None, None
                        )
                        return "已超时退出"
            else:
                return "找不到船，请确认船名是否正确，可以使用【wws 查船名】查询船只中英文"
        else:
            return "参数似乎出了问题呢"
        is_cache = await check_yuyuko_cache(params["server"], params["accountId"])
        if is_cache:
            logger.success("上报数据成功")
        else:
            logger.success("跳过上报数据，直接请求")
        url = "https://api.wows.shinoaki.com/public/wows/account/ship/info"
        logger.success(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
        ranking = await get_MyShipRank_yuyuko(params)
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=None)
            result = resp.json()
            logger.success(f"本次请求返回的状态码:{result['code']}")
            logger.success(f"本次请求服务器计算时间:{result['queryTime']}")
        if result["code"] == 200 and result["data"]:
            if (
                not result["data"]["shipInfo"]["battles"]
                and not result["data"]["rankSolo"]["battles"]
            ):
                return "查询不到战绩数据"
            template = env.get_template("wws-ship.html")
            template_data = await set_shipparams(result["data"])
            template_data["shipRank"] = ranking
            content = await template.render_async(template_data)
            return await html_to_pic(
                content, wait=0, viewport={"width": 800, "height": 100}
            )
        elif result["code"] == 403:
            return f"{result['message']}\n请先绑定账号"
        elif result["code"] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        ShipSecletProcess[ev.user_id] = ShipSlectState(False, None, None)
        return "请求超时了，请过会儿再尝试哦~"
    except ActionFailed:
        logger.warning(traceback.format_exc())
        ShipSecletProcess[ev.user_id] = ShipSlectState(False, None, None)
        return "由于风控或禁言，无法发送消息"
    except Exception:
        logger.error(traceback.format_exc())
        ShipSecletProcess[ev.user_id] = ShipSlectState(False, None, None)
        return "wuwuu好像出了点问题，过一会儿还是不行的话请联系麻麻~"


async def get_MyShipRank_yuyuko(params):
    try:
        url = "https://api.wows.shinoaki.com/upload/numbers/data/upload/user/ship/rank"
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=None)
            result = resp.json()
            if result["code"] == 200 and result["data"]:
                if result["data"]["ranking"]:
                    return result["data"]["ranking"]
                elif (
                    not result["data"]["ranking"]
                    and not result["data"]["serverId"] == "cn"
                ):
                    ranking = await get_MyShipRank_Numbers(
                        result["data"]["httpUrl"], result["data"]["serverId"]
                    )
                    if ranking:
                        await post_MyShipRank_yuyuko(
                            result["data"]["accountId"],
                            ranking,
                            result["data"]["serverId"],
                            result["data"]["shipId"],
                        )
                    return ranking
                else:
                    return None
            else:
                return None
    except Exception:
        logger.error(traceback.format_exc())
        return None


async def get_MyShipRank_Numbers(url, server):
    try:
        data = None
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            if resp.content:
                result = resp.json()
                page_url = str(result["url"]).replace("\\", "")
                nickname = str(result["nickname"])
                my_rank_url = f"{number_url_homes[server]}{page_url}"
                async with httpx.AsyncClient() as client:
                    resp = await client.get(my_rank_url, timeout=10)
                    soup = BeautifulSoup(resp.content, "html.parser")
                    data = (
                        soup.select_one(f'tr[data-nickname="{nickname}"]')
                        .select_one("td")
                        .string
                    )
        if data and data.isdigit():
            return data
        else:
            return None
    except Exception:
        logger.error(traceback.format_exc())
        return None


async def post_MyShipRank_yuyuko(accountId, ranking, serverId, shipId):
    try:
        async with httpx.AsyncClient(headers=headers) as client:
            url = "https://api.wows.shinoaki.com/upload/numbers/data/upload/user/ship/rank"
            post_data = {
                "accountId": int(accountId),
                "ranking": int(ranking),
                "serverId": serverId,
                "shipId": int(shipId),
            }
            resp = await client.post(url, json=post_data, timeout=None)
            result = resp.json()
            return
    except Exception:
        logger.error(traceback.format_exc())
        return


async def get_ShipInfoRecent(server_type, info, bot, ev):
    try:
        bot = get_bot()
        params, day = None, 0
        if datetime.now().hour < 7:
            day = 1
        if isinstance(info, List):
            for i in info:  # 查找日期,没找到默认一天
                if str(i).isdigit():
                    if int(i) <= 30:
                        day = int(i)
                    else:
                        day = 30
                    info.remove(i)
            for flag, i in enumerate(info):  # 是否包含me或@，包含则调用平台接口
                if i == "me":
                    params = {
                        "server": server_type,
                        "accountId": int(ev.user_id),
                        "day": day,
                    }
                    info.remove("me")
                match = re.search(r"CQ:at,qq=(\d+)", i)
                if match:
                    params = {
                        "server": server_type,
                        "accountId": int(match.group(1)),
                        "day": day,
                    }
                    info[flag] = str(i).replace(f"[{match.group(0)}]", "")
                    if not info[flag]:
                        info.remove("")
                    break
            if not params and len(info) == 3:
                param_server, info = await match_keywords(info, servers)
                if param_server:
                    param_accountid = await get_AccountIdByName(
                        param_server, str(info[0])
                    )  # 剩余列表第一个是否为游戏名
                    if isinstance(param_accountid, int):
                        info.remove(info[0])
                        params = {
                            "server": param_server,
                            "accountId": param_accountid,
                            "day": day,
                        }
                    else:
                        return f"{param_accountid}"
                else:
                    return "服务器参数似乎输错了呢"
            elif params and len(info) == 1:
                logger.success(f"{params}")
            elif params:
                return "您似乎准备用查询自己的单船近期战绩，请检查参数中是否带有船名，以空格区分"
            else:
                return "您似乎准备用游戏昵称查询单船近期战绩，请检查参数中是否包含服务器、游戏昵称和船名，以空格区分"
            shipList = await get_ship_byName(str(info[0]))
            logger.success(f"{shipList}")
            if shipList:
                if len(shipList) < 2:
                    params["shipId"] = shipList[0][0]
                else:
                    msg = f"存在多条名字相似的船\n请在20秒内选择对应的序号\n================\n"
                    flag = 0
                    for each in shipList:
                        flag += 1
                        msg += f"{flag}：{tiers[each[3]-1]} {each[1]}\n"
                    ShipSecletProcess[ev.user_id] = ShipSlectState(
                        False, None, shipList
                    )
                    img = await text_to_pic(
                        text=msg, css_path=template_path / "text-ship.css", width=250
                    )
                    await bot.send(ev, MessageSegment.image(img))
                    a = 0
                    while a < 40 and not ShipSecletProcess[ev.user_id].state:
                        a += 1
                        await asyncio.sleep(0.5)
                    if ShipSecletProcess[ev.user_id].state and ShipSecletProcess[
                        ev.user_id
                    ].SlectIndex <= len(shipList):
                        params["shipId"] = shipList[
                            ShipSecletProcess[ev.user_id].SlectIndex - 1
                        ][0]
                        ShipSecletProcess[ev.user_id] = ShipSlectState(
                            False, None, None
                        )
                    else:
                        ShipSecletProcess[ev.user_id] = ShipSlectState(
                            False, None, None
                        )
                        return "已超时退出"
            else:
                return "找不到船，请确认船名是否正确，可以使用【wws 查船名】查询船只中英文"
        else:
            return "参数似乎出了问题呢"
        is_cache = await check_yuyuko_cache(params["server"], params["accountId"])
        if is_cache:
            logger.success("上报数据成功")
        else:
            logger.success("跳过上报数据，直接请求")
        url = "https://api.wows.shinoaki.com/api/wows/recent/v2/recent/info/ship"
        logger.success(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=None)
            result = resp.json()
        if result["code"] == 200 and result["data"]:
            template = env.get_template("wws-ship-recent.html")
            template_data = await set_shipRecentparams(result["data"])
            content = await template.render_async(template_data)
            return await html_to_pic(
                content, wait=0, viewport={"width": 800, "height": 100}
            )
        elif result["code"] == 403:
            return f"{result['message']}\n请先绑定账号"
        elif result["code"] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        ShipSecletProcess[ev.user_id] = ShipSlectState(False, None, None)
        return "请求超时了，请过会儿再尝试哦~"
    except ActionFailed:
        logger.warning(traceback.format_exc())
        ShipSecletProcess[ev.user_id] = ShipSlectState(False, None, None)
        return "由于风控或禁言，无法发送消息"
    except Exception:
        logger.error(traceback.format_exc())
        ShipSecletProcess[ev.user_id] = ShipSlectState(False, None, None)
        return "wuwuu好像出了点问题，过一会儿还是不行的话请联系麻麻~"
