import re
import time
import traceback
from asyncio.exceptions import TimeoutError
from typing import List

import jinja2
import orjson
from httpx import ConnectTimeout
from nonebot.adapters.onebot.v11 import ActionFailed, Bot, MessageSegment
from nonebot.log import logger
from nonebot_plugin_htmlrender import html_to_pic

from ..data_source import (
    servers,
    set_damageColor,
    set_infoparams,
    set_upinfo_color,
    set_winColor,
    template_path,
)
from ..HttpClient_pool import client_yuyuko
from ..utils import match_keywords
from .publicAPI import check_yuyuko_cache, get_AccountIdByName

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

async def get_AccountInfo(server_type, info, bot:Bot, ev):
    try:
        url, params = "", ""
        if isinstance(info, List):
            for i in info:
                if str(i).lower() == "me":
                    params = {"server": server_type, "accountId": int(ev.user_id)}
                    break
                match = re.search(r"CQ:at,qq=(\d+)", i)
                if match:
                    params = {"server": server_type, "accountId": int(match.group(1))}
                    break
            if not params and len(info) == 2:
                param_server, info = await match_keywords(info, servers)
                if param_server:
                    param_accountid = await get_AccountIdByName(
                        param_server, str(info[0])
                    )
                    if isinstance(param_accountid, int):
                        params = {"server": param_server, "accountId": param_accountid}
                    else:
                        return f"{param_accountid}"
                else:
                    return "服务器参数似乎输错了呢"
            elif params:
                logger.success(f"{params}")
            else:
                return "您似乎准备用游戏昵称查询，请检查参数中是否包含服务器和游戏昵称，以空格区分，如果您准备查询单船战绩，请带上ship参数"
        else:
            return "参数似乎出了问题呢"
        is_cache = await check_yuyuko_cache(params["server"], params["accountId"])
        if is_cache:
            logger.success("上报数据成功")
        else:
            logger.success("跳过上报数据，直接请求")
        url = "https://api.wows.shinoaki.com/public/wows/account/user/info"
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        logger.success(f"本次请求总耗时{resp.elapsed.total_seconds()*1000}，服务器计算耗时:{result['queryTime']}")
        if result["code"] == 200 and result["data"]:
            template = env.get_template("wws-info.html")
            template_data = await set_infoparams(result["data"])
            content = await template.render_async(template_data)
            return await html_to_pic(
                content, wait=0, viewport={"width": 920, "height": 1000}
            )
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
