from typing import List
import httpx
import traceback
import jinja2
import re
from datetime import datetime
from pathlib import Path
from .data_source import servers,set_recentparams
from .utils import match_keywords
from nonebot_plugin_htmlrender import html_to_pic
from .publicAPI import get_AccountIdByName
from nonebot import get_driver
from nonebot.log import logger
from httpx import ConnectTimeout
from asyncio.exceptions import TimeoutError

dir_path = Path(__file__).parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)

headers = {
    'Authorization': get_driver().config.api_token
}


async def get_RecentInfo(qqid,info):
    try:
        params,day = None,0
        if datetime.now().hour < 7:
            day = 1
        if isinstance(info,List):
            for i in info:              #查找日期,没找到默认一天
                if str(i).isdigit() and len(i) <= 3:
                    day = str(i)
                    info.remove(i)
            for i in info:              #是否包含me或@，包含则调用平台接口
                if i == 'me':
                    url = 'https://api.wows.linxun.link//api/wows/recent/v2/recent/info'
                    params = {
                    "server": "QQ",
                    "accountId": qqid,
                    "day": day,
                    "status": 0
                    }
                match = re.search(r"CQ:at,qq=(\d+)",i)
                if match:
                    url = 'https://api.wows.linxun.link//api/wows/recent/v2/recent/info'
                    params = {
                    "server": "QQ",
                    "accountId": match.group(1),
                    "day": day,
                    "status": 0
                    }
                    break
            if not params and len(info) == 2:
                param_server,info = await match_keywords(info,servers)
                if param_server:
                    param_accountid = await get_AccountIdByName(param_server,str(info[0]))
                    if isinstance(param_accountid,int):
                        url = 'https://api.wows.linxun.link//api/wows/recent/v2/recent/info'
                        params = {
                        "server": param_server,
                        "accountId": param_accountid,
                        "day": day,
                        "status": 0
                        }
                    else:
                        return f"{param_accountid}"
                else:
                    return '服务器参数似乎输错了呢'
            elif params:
                pass
            else:
                return '您似乎准备用游戏昵称查询水表，请检查参数中是否包含服务器和游戏昵称，以空格区分'
        else:
            return '参数似乎出了问题呢'
        logger.info(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=20)
            result = resp.json()
            logger.info(f"本次请求返回的状态码:{result['code']}")
        if result['code'] == 200:
            if result['data']['shipData'][0]['shipData']:
                template = env.get_template("wws-info-recent.html")
                template_data = await set_recentparams(result['data'])
                content = await template.render_async(template_data)
                return await html_to_pic(content, wait=0, viewport={"width": 1200, "height": 100}) 
            else:
                return '该日期数据记录不存在'
        elif result['code'] == 403:
            return f"{result['message']}\n请先绑定账号"
        elif result['code'] == 404 or result['code'] == 405:
            return f"{result['message']}\n您可以发送wws help查看recent相关说明"
        elif result['code'] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return 'wuwuu好像出了点问题，过一会儿还是不行的话请联系麻麻~'
    except Exception:
        logger.warning(traceback.format_exc())
        return 'wuwuu好像出了点问题，过一会儿还是不行的话请联系麻麻~'