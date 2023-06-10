import re
import time
import traceback
from pathlib import Path
from typing import List

import httpx
import jinja2
import orjson
from bs4 import BeautifulSoup
from nonebot import get_driver
from nonebot_plugin_htmlrender import html_to_pic

from ..data_source import servers, template_path
from ..HttpClient_pool import client_default, client_yuyuko
from ..utils import match_keywords
from .publicAPI import get_AccountIdByName

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)



async def get_record(server_type, info, bot, ev):
    try:
        params = None
        if isinstance(info, List):
            for i in info:
                if i == "me":
                    params = {"server": server_type, "accountId": int(ev.user_id)}
                    break
                match = re.search(r"CQ:at,qq=(\d+)", i)
                if match:
                    params = {"server": server_type, "accountId": int(match.group(1))}
                    break
            if not params and len(info) == 2:
                param_server, info = await match_keywords(info, servers)
                if param_server and param_server != "cn":
                    param_accountid = await get_AccountIdByName(
                        param_server, str(info[0])
                    )
                    if isinstance(param_accountid, int):
                        params = {"server": param_server, "accountId": param_accountid}
                    else:
                        return f"{param_accountid}"
                elif param_server == "cn":
                    return "暂不支持国服"
                else:
                    return "服务器参数似乎输错了呢"
            elif params:
                pass
            else:
                return (
                    "您似乎准备用游戏昵称查询公会进出记录，请检查参数中时候包含服务器和游戏昵称，以空格区分，如果您准备查询单船战绩，请带上ship参数"
                )
        else:
            return "参数似乎出了问题呢"
        print(params)
        if type == "personal":
            url = "https://api.wows.shinoaki.com/upload/numbers/data/upload/user/clan/record"
            resp = await client_yuyuko.get(url, params=params, timeout=None)
            result = orjson.loads(resp.content)
            if result["code"] == 200 and result["data"]:
                template = env.get_template("wws-personalRecord.html")
                template_data = {"data": result["data"]}
                content = await template.render_async(template_data)
                return await html_to_pic(
                    content, wait=0, viewport={"width": 920, "height": 100}
                )
            elif result["code"] == 403:
                return f"{result['message']}\n请检查昵称或绑定账号"
            elif result["code"] == 404:
                template = env.get_template("wws-personalRecord.html")
                template_data = await get_personalRecord_Numbers(
                    result["data"][0]["httpUrl"], params
                )
                print(template_data)
                if template_data:
                    template_data = {"data": template_data}
                else:
                    return "查询失败了呢，可能是没有进出记录"
                content = await template.render_async(template_data)
                return await html_to_pic(
                    content, wait=0, viewport={"width": 920, "height": 100}
                )
            elif result["code"] == 500:
                return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
            else:
                return f"{result['message']}"
        else:
            url = ""
            resp = await client_yuyuko.get(url, params=params, timeout=None)
            result = orjson.loads(resp.content)
            if result["code"] == 200 and result["data"]:
                template = env.get_template("wws-clanRecord.html")
                template_data = {"data": result["data"]}
                content = await template.render_async(template_data)
                return await html_to_pic(
                    content, wait=0, viewport={"width": 920, "height": 100}
                )
            elif result["code"] == 403:
                return f"{result['message']}\n请检查昵称或绑定账号"
            elif result["code"] == 404:
                template = env.get_template("wws-clanRecord.html")
                template_data = await get_ClanRecord_Numbers(
                    result["data"][0]["httpUrl"], params["server"], params["accountId"]
                )
                print(template_data)
                if template_data:
                    template_data = {"data": template_data}
                else:
                    return "查询失败了呢，可能是没有进出记录"
                content = await template.render_async(template_data)
                return await html_to_pic(
                    content, wait=0, viewport={"width": 920, "height": 100}
                )
            elif result["code"] == 500:
                return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
            else:
                return f"{result['message']}"

    except Exception:
        traceback.print_exc()
        return "wuwuwu出了点问题，请联系麻麻解决，目前不支持国服哦"


async def get_personalRecord_Numbers(url, server, accountId):
    try:
        data = None
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=None)
            soup = BeautifulSoup(resp.content, "html.parser")
            data = soup.select(f'table[id="moreTransfers"]')
            if data:
                data = data.select(f"tr")
            else:
                data = soup.select(
                    f'table[class="table table-styled table-bordered cells-middle"]'
                )
                data = data[len(data) - 1].select(f"tr")
            info, info_list, clan_list = {}, [], []
            for each in data:
                class_list = each.select("td span")[0].attrs["class"]
                if class_list[2] == "transfer-out":
                    status = 1
                else:
                    status = 0
                timeGroup = re.match(
                    r"(.*?)\.(.*?)\.(.*?)$", each.select("td")[1].string
                )
                dt = f"{timeGroup.group(3)}-{timeGroup.group(2)}-{timeGroup.group(1)} 12:00:00"
                timestamp = int(time.mktime(time.strptime(dt, r"%Y-%m-%d %H:%M:%S")))
                clanId = re.match(
                    r"\/clan\/(.*?),", each.select("td a")[0].attrs["href"]
                ).group(1)
                clanName = each.select("td a")[0].string
                info["server"] = server
                info["accountId"] = accountId
                info["clanId"] = int(clanId)
                info["status"] = status
                info["time"] = timestamp
                info["clanName"] = clanName
                if clanId not in clan_list:
                    clan_list.append(clanId)
                info_list.append(info.copy())
            print(clan_list)
            clan_url = re.match(r"(.*?)player", url).group(1)
            for each in clan_list:
                await get_ClanRecord_Numbers(
                    f"{clan_url}clan/transfers/{each},111/", each
                )
            # result = await post_personalRecord_yuyuko(info_list)
            # if result:
            #    return result
            # else:
            #    return None
    except Exception:
        traceback.print_exc()
        return None


async def get_ClanRecord_Numbers(url, clanId):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=None)
        soup = BeautifulSoup(resp.content, "html.parser")
        data = soup.select(f"tr")
        info, info_list = {}, []
        for each_data in data[2:]:
            class_list = each_data.select("td span")[0].attrs["class"]
            if class_list[2] == "transfer-out":
                status = 1
            else:
                status = 0
            timeGroup = re.match(
                r"(.*?)\.(.*?)\.(.*?)$", each_data.select("td")[1].string
            )
            dt = f"{timeGroup.group(3)}-{timeGroup.group(2)}-{timeGroup.group(1)} 12:00:00"
            timestamp = int(time.mktime(time.strptime(dt, r"%Y-%m-%d %H:%M:%S")))
            accountMacthGroup = re.match(
                r"\/player\/(.*?),(.*?)\/", each_data.select("td a")[0].attrs["href"]
            )
            if accountMacthGroup:
                accountId = accountMacthGroup.group(1)
                accountName = accountMacthGroup.group(2)
            info["clanId"] = clanId
            info["status"] = status
            info["time"] = timestamp
            info["accountId"] = accountId
            info["accountName"] = accountName
            info_list.append(info.copy())


async def post_personalRecord_yuyuko(post_data):
    try:
        url = "https://api.wows.shinoaki.com/upload/numbers/data/upload/user/clan/record"
        resp = await client_yuyuko.post(url, json=post_data, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["data"]:
            return result["data"]
        else:
            return None
    except Exception:
        traceback.print_exc()
        return None
