from typing import List
import httpx
import traceback
import jinja2
import re
import time
from pathlib import Path
from ..data_source import servers,set_infoparams,set_damageColor,set_winColor,set_upinfo_color
from ..utils import match_keywords
from ..publicAPI import get_AccountIdByName,check_yuyuko_cache
from nonebot_plugin_htmlrender import html_to_pic
from nonebot import get_driver
from nonebot.log import logger
from httpx import ConnectTimeout
from asyncio.exceptions import TimeoutError

dir_path = Path(__file__).parent.parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)
env.globals.update(set_damageColor=set_damageColor,set_winColor=set_winColor,set_upinfo_color=set_upinfo_color,time=time,int=int,abs=abs,enumerate=enumerate)

headers = {
    'Authorization': get_driver().config.api_token
}
  
async def check_christmas_box(server_type,info,bot,ev):
    try:
        url,params = '',''
        if isinstance(info,List):
            if len(info) == 0:
                params = {
                    "server": "QQ",
                    "accountId": int(ev.user_id)
                    }
            for i in info:
                if str(i).lower() == 'me':
                    params = {
                    "server": server_type,
                    "accountId": int(ev.user_id)
                    }
                    break
                match = re.search(r"CQ:at,qq=(\d+)",i)
                if match:
                    params = {
                    "server": server_type,
                    "accountId": int(match.group(1))
                    }
                    break
            if not params and len(info) == 2:
                param_server,info = await match_keywords(info,servers)
                if param_server:
                    param_accountid = await get_AccountIdByName(param_server,str(info[0]))
                    if isinstance(param_accountid,int):
                        params = {
                        "server": param_server,
                        "accountId": param_accountid
                        }
                    else:
                        return f"{param_accountid}"
                else:
                    return '服务器参数似乎输错了呢'
            elif params:
                logger.success(f"{params}")
            else:
                return '您似乎准备用游戏昵称查询，请检查参数中是否包含服务器和游戏昵称，以空格区分，如果您准备查询单船战绩，请带上ship参数'
        else:
            return '参数似乎出了问题呢'
        url = 'https://api.wows.shinoaki.com/public/wows/christmas/ship/box'
        logger.success(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=None)
            result = resp.json()
            logger.success(f"本次请求返回的状态码:{result['code']}")
            logger.success(f"本次请求服务器计算时间:{result['queryTime']}")
        if result['code'] == 200 and result['data']:
            template = env.get_template("wws-box-christmas.html")
            template_data = await set_infoparams(result['data'])
            content = await template.render_async(template_data)
            return await html_to_pic(content, wait=0, viewport={"width": 920, "height": 1000})
        elif result['code'] == 403:
            return f"{result['message']}\n请先绑定账号"
        elif result['code'] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return f"{result['message']}"
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return '请求超时了，请过会儿再尝试哦~'
    except Exception:
        logger.error(traceback.format_exc())
        return 'wuwuwu出了点问题，请联系麻麻解决'