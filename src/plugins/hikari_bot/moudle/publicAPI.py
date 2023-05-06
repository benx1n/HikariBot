import asyncio
import gzip
import traceback
from asyncio.exceptions import TimeoutError
from base64 import b64encode
from typing import List

import orjson
from httpx import ConnectTimeout
from nonebot import get_driver
from nonebot.log import logger

from ..data_source import levels, nations, shiptypes
from ..HttpClient_pool import client_wg, client_yuyuko
from ..utils import match_keywords


async def get_nation_list():
    try:
        msg = ""
        url = "https://api.wows.shinoaki.com/public/wows/encyclopedia/nation/list"
        resp = await client_yuyuko.get(url, timeout=None)
        result = orjson.loads(resp.content)
        for nation in result["data"]:
            msg: str = msg + f"{nation['cn']}：{nation['nation']}\n"
        return msg
    except Exception:
        logger.error(traceback.format_exc())


async def get_ship_name(server_type, infolist: List, bot, ev):
    msg = ""
    try:
        param_nation, infolist = await match_keywords(infolist, nations)
        if not param_nation:
            return "请检查国家名是否正确"

        param_shiptype, infolist = await match_keywords(infolist, shiptypes)
        if not param_shiptype:
            return "请检查船只类别是否正确"

        param_level, infolist = await match_keywords(infolist, levels)
        if not param_level:
            return "请检查船只等级是否正确"
        params = {
            "county": param_nation,
            "level": param_level,
            "shipName": "",
            "shipType": param_shiptype,
        }
        url = "https://api.wows.shinoaki.com/public/wows/encyclopedia/ship/search"
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["data"]:
            for ship in result["data"]:
                msg += f"{ship['shipNameCn']}：{ship['shipNameNumbers']}\n"
        else:
            msg = "没有符合的船只"
        return msg
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
    except Exception:
        logger.error(traceback.format_exc())
        return "wuwuwu出了点问题，请联系麻麻解决"


async def get_ship_byName(shipname: str):
    try:
        url = "https://api.wows.shinoaki.com/public/wows/encyclopedia/ship/search"
        params = {"county": "", "level": "", "shipName": shipname, "shipType": ""}
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        List = []
        if result["code"] == 200 and result["data"]:
            for each in result["data"]:
                List.append(
                    [
                        each["id"],
                        each["shipNameCn"],
                        each["shipNameNumbers"],
                        each["tier"],
                        each['shipType']
                    ]
                )
            return List
        else:
            return None
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
    except Exception:
        logger.error(traceback.format_exc())
        return None


async def get_all_shipList():
    try:
        url = "https://api.wows.shinoaki.com/public/wows/encyclopedia/ship/search"
        params = {"county": "", "level": "", "shipName": "", "shipType": ""}
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["data"]:
            return result["data"]
        else:
            return None
    except Exception:
        return None


async def get_AccountIdByName(server: str, name: str):
    try:
        url = "https://api.wows.shinoaki.com/public/wows/account/search/user"
        params = {"server": server, "userName": name}
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["data"]:
            return result["data"]["accountId"]
        else:
            return result["message"]
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return "请求超时了，请过一会儿重试哦~"
    except Exception:
        logger.error(traceback.format_exc())
        return "好像出了点问题呢，可能是网络问题，如果重试几次还不行的话，请联系麻麻解决"


async def get_ClanIdByName(server: str, tag: str):
    try:
        url = "https://api.wows.shinoaki.com/public/wows/clan/search"
        params = {"server": server, "tag": tag, "type": 1}
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        List = []
        if result["code"] == 200 and result["data"]:
            # for each in result['data']:
            #    List.append([each['clanId'],each['name'],each['serverName'],each['tag']])
            return result["data"]
        else:
            return None
    except Exception:
        logger.error(traceback.format_exc())
        return None


async def check_yuyuko_cache(server, id):
    try:
        if get_driver().config.check_cache:
            yuyuko_cache_url = "https://api.wows.shinoaki.com/api/wows/cache/check"
            params = {"accountId": id, "server": server}
            resp = await client_yuyuko.post(yuyuko_cache_url, json=params, timeout=5)
            result = orjson.loads(resp.content)
            cache_data = {}
            if result["code"] == 201:
                if "DEV" in result["data"]:
                    await get_wg_info(cache_data, "DEV", result["data"]["DEV"])
                elif "pvp" in result["data"]:
                    tasks = []
                    loop = asyncio.get_running_loop()
                    for key in result["data"]:
                        tasks.append(
                            asyncio.ensure_future(
                                get_wg_info(cache_data, key, result["data"][key])
                            )
                        )
                    await asyncio.gather(*tasks)
                if not cache_data:
                    return False
                data_base64 = b64encode(
                    gzip.compress(orjson.dumps(cache_data))
                ).decode()
                params["data"] = data_base64
                resp = await client_yuyuko.post(yuyuko_cache_url, json=params, timeout=5)
                result = orjson.loads(resp.content)
                logger.success(result)
                if result["code"] == 200:
                    return True
                else:
                    return False
            return False
        return False
    except Exception:
        logger.error(traceback.format_exc())
        return False


async def get_wg_info(params, key, url):
    try:
        resp = await client_wg.get(url, timeout=5, follow_redirects=True)
        wg_result = orjson.loads(resp.content)
        if resp.status_code == 200 and wg_result["status"] == "ok":
            params[key] = resp.text
    except Exception:
        logger.error(traceback.format_exc())
        logger.error(f"上报url：{url}")
        return
