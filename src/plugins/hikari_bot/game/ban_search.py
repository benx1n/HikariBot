import re
import time
import traceback
from asyncio.exceptions import TimeoutError
from pathlib import Path
from typing import List

import httpx
import jinja2
from httpx import ConnectTimeout
from nonebot import get_driver
from nonebot.log import logger
from nonebot_plugin_htmlrender import html_to_pic

from ..data_source import servers
from ..publicAPI import  get_AccountIdByName
from ..utils import match_keywords
from ..wws_bind import get_DefaultBindInfo

dir_path = Path(__file__).parent.parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)

headers = {"Authorization": get_driver().config.api_token}


async def get_BanInfo(server_type, info, bot, ev):
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
            if params:
                bindResult = await get_DefaultBindInfo(params['server'],params['accountId'])
                if bindResult:
                    if bindResult['serverType'] == 'cn':
                        param_accountid = int(bindResult['accountId'])
                    else:
                        return "目前仅支持国服查询"
                else:
                    return "未查询到该用户绑定信息，请使用wws 查询绑定 进行检查"
            elif not params and len(info) == 2:
                param_server, info = await match_keywords(info, servers)
                if param_server == 'cn':
                    param_accountid = await get_AccountIdByName(
                        param_server, str(info[0])
                    )
                    if not isinstance(param_accountid,int):
                        return f"{param_accountid}"
                else:
                    return "目前仅支持国服查询"
            else:
                return "您似乎准备用游戏昵称查询，请检查参数中是否包含服务器和游戏昵称，以空格区分"
        else:
            return "参数似乎出了问题呢"
        url = 'https://api.wows.shinoaki.com/public/wows/ban/cn/user'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.post(url, json={"accountId":param_accountid}, timeout=None)
            result = resp.json()
            logger.success(f"本次请求返回的状态码:{result['code']}")
            logger.success(f"本次请求服务器计算时间:{result['queryTime']}")
        if result["code"] == 200 and result["data"]:
            template = env.get_template("wws-ban.html")
            template_data = {"data": result["data"]}
            content = await template.render_async(template_data)
            return await html_to_pic(
                content, wait=0, viewport={"width": 900, "height": 100}
            )
        elif result["code"] == 404 and result["data"]:
            template = env.get_template("wws-unban.html")
            template_data = {"data": result["data"]}
            content = await template.render_async(template_data)
            return await html_to_pic(
                content, wait=0, viewport={"width": 900, "height": 100}
            )
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return "请求超时了，请过会儿再尝试哦~"
    except Exception:
        logger.error(traceback.format_exc())
        return "wuwuwu出了点问题，请联系麻麻解决"
