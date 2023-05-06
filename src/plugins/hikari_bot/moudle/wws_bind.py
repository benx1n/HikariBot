import re
import traceback
from asyncio.exceptions import TimeoutError
from typing import List

import orjson
from httpx import ConnectTimeout
from nonebot.adapters.onebot.v11 import ActionFailed, Bot, MessageSegment
from nonebot.log import logger

from ..data_source import servers
from ..HttpClient_pool import client_yuyuko
from ..utils import match_keywords
from .publicAPI import get_AccountIdByName


async def get_BindInfo(server_type, info, bot:Bot, ev):
    try:
        url, params = "", ""
        if isinstance(info, List) and len(info) == 1:
            for i in info:  # 是否包含me或@
                if str(i).lower() == "me":
                    url = "https://api.wows.shinoaki.com/public/wows/bind/account/platform/bind/list"
                    params = {
                        "platformType": server_type,
                        "platformId": ev.user_id,
                    }
                match = re.search(r"CQ:at,qq=(\d+)", i)
                if match:
                    url = "https://api.wows.shinoaki.com/public/wows/bind/account/platform/bind/list"
                    params = {
                        "platformType": server_type,
                        "platformId": match.group(1),
                    }
                    break
            if not url or not params:
                return "参数似乎出了问题呢，请使用me或@群友"
        else:
            return "参数似乎出了问题呢，请使用me或@群友"
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["message"] == "success":
            if result["data"]:
                msg1 = f"当前绑定账号\n"
                msg2 = f"绑定账号列表\n"
                flag = 1
                for bindinfo in result["data"]:
                    msg2 += f"{flag}：{bindinfo['serverType']} {bindinfo['userName']}\n"
                    flag += 1
                    if bindinfo["defaultId"]:
                        msg1 += f"{bindinfo['serverType']} {bindinfo['userName']}\n"
                msg = msg1 + msg2 + "本人发送wws [切换/删除]绑定+序号 切换/删除对应账号"
                return msg
            else:
                return "该用户似乎还没绑定窝窝屎账号"
        elif result["code"] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return "请求超时了，请过会儿再尝试哦~"
    except Exception:
        logger.error(traceback.format_exc())
        return "wuwuwu出了点问题，请联系麻麻解决"


async def set_BindInfo(server_type, info, bot:Bot, ev):
    try:
        param_server = None
        if isinstance(info, List):
            if len(info) == 2:
                param_server, info = await match_keywords(info, servers)
                if param_server:
                    param_accountid = await get_AccountIdByName(
                        param_server, str(info[0])
                    )
                    if isinstance(param_accountid, int):
                        url = "https://api.wows.shinoaki.com/api/wows/bind/account/platform/bind/put"
                        params = {
                            "platformType": server_type,
                            "platformId": str(ev.user_id),
                            "accountId": param_accountid,
                        }
                    else:
                        return f"{param_accountid}"
                else:
                    return "服务器参数似乎输错了呢"
            else:
                return "参数似乎输错了呢，请确保后面跟随服务器+游戏昵称"
        else:
            return "参数似乎输错了呢，请确保后面跟随服务器+游戏昵称"
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["message"] == "success":
            return "绑定成功"
        elif result["code"] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return "请求超时了，请过会儿再尝试哦~"
    except Exception:
        logger.error(traceback.format_exc())
        return "wuwuwu出了点问题，请联系麻麻解决"


async def change_BindInfo(server_type, info, bot:Bot, ev):
    try:
        if isinstance(info, List) and len(info) == 1 and str(info[0]).isdigit():
            url = "https://api.wows.shinoaki.com/public/wows/bind/account/platform/bind/list"
            params = {
                "platformType": server_type,
                "platformId": ev.user_id,
            }
        else:
            return "参数似乎出了问题呢，请跟随要切换的序号"
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["message"] == "success":
            if result["data"] and len(result["data"]) >= int(info[0]):
                account_name = result["data"][int(info[0]) - 1]["userName"]
                param_server = result["data"][int(info[0]) - 1]["serverType"]
                param_accountid = result["data"][int(info[0]) - 1]["accountId"]
                url = "https://api.wows.shinoaki.com/api/wows/bind/account/platform/bind/put"
                params = {
                    "platformType": server_type,
                    "platformId": str(ev.user_id),
                    "accountId": param_accountid,
                }
            else:
                return "没有对应序号的绑定记录"
        elif result["code"] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["message"] == "success":
            return f"切换绑定成功,当前绑定账号{param_server}：{account_name}"
        elif result["code"] == 403:
            return f"{result['message']}\n请先绑定账号"
        elif result["code"] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return "请求超时了，请过会儿再尝试哦~"
    except Exception:
        logger.error(traceback.format_exc())
        return "wuwuwu出了点问题，请联系麻麻解决"


async def set_special_BindInfo(server_type, info, bot:Bot, ev):
    try:
        param_server = None
        if isinstance(info, List):
            if len(info) == 2:
                param_server, info = await match_keywords(info, servers)
                if param_server:
                    if str(info[0]).isdigit():
                        url = "https://api.wows.shinoaki.com/api/wows/bind/account/platform/bind/put"
                        params = {
                            "platformType": server_type,
                            "platformId": str(ev.user_id),
                            "accountId": int(info[0]),
                        }
                    else:
                        return "特殊绑定只能使用网页查询到的AccountID哦"
                else:
                    return "服务器参数似乎输错了呢"
            else:
                return "参数似乎输错了呢，请确保后面跟随服务器+网页查询到的AccountID"
        else:
            return "参数似乎输错了呢，请确保后面跟随服务器+游戏昵称"
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["message"] == "success":
            return "绑定成功"
        elif result["code"] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return "请求超时了，请过会儿再尝试哦~"
    except Exception:
        logger.error(traceback.format_exc())
        return "wuwuwu出了点问题，请联系麻麻解决"


async def delete_BindInfo(server_type, info, bot:Bot, ev):
    try:
        if isinstance(info, List) and len(info) == 1 and str(info[0]).isdigit():
            url = "https://api.wows.shinoaki.com/public/wows/bind/account/platform/bind/list"
            params = {
                "platformType": server_type,
                "platformId": ev.user_id,
            }
        else:
            return "参数似乎出了问题呢，请跟随要切换的序号"
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["message"] == "success":
            if result["data"] and len(result["data"]) >= int(info[0]):
                account_name = result["data"][int(info[0]) - 1]["userName"]
                param_server = result["data"][int(info[0]) - 1]["serverType"]
                param_accountid = result["data"][int(info[0]) - 1]["accountId"]
                url = "https://api.wows.shinoaki.com/api/wows/bind/account/platform/bind/remove"
                params = {
                    "platformType": server_type,
                    "platformId": str(ev.user_id),
                    "accountId": param_accountid,
                }
            else:
                return "没有对应序号的绑定记录"
        elif result["code"] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["message"] == "success":
            return f"删除绑定成功,删除的账号为{param_server}：{account_name}"
        elif result["code"] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return "请求超时了，请过会儿再尝试哦~"
    except Exception:
        logger.error(traceback.format_exc())
        return "wuwuwu出了点问题，请联系麻麻解决"


async def get_DefaultBindInfo(platformType,platformId):
    try:
        url = 'https://api.wows.shinoaki.com/public/wows/bind/account/platform/bind/list'
        params = {
            "platformType": platformType,
            "platformId": platformId,
        }
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result['code'] == 200 and result['message'] == "success":
            if result['data']:
                for each in result['data']:
                    if each['defaultId']:
                        return each
            else:
                return None
    except Exception:
        logger.error(traceback.format_exc())
        return None