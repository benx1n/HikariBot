from typing import List
import httpx
import traceback
import re
from pathlib import Path
from ..data_source import servers
from ..utils import match_keywords
from ..publicAPI import get_AccountIdByName,check_yuyuko_cache
from ..data_source import nations,shiptypes,levels
from nonebot.log import logger
from nonebot import get_driver
from httpx import ConnectTimeout
from asyncio.exceptions import TimeoutError

dir_path = Path(__file__).parent

headers = {
    'Authorization': get_driver().config.api_token
}
  
async def roll_ship(server_type,infolist,bot,ev):
    try:
        param_nation,infolist = await match_keywords(infolist,nations)
        if not param_nation:
            param_nation = ''
        
        param_shiptype,infolist = await match_keywords(infolist,shiptypes)
        if not param_shiptype:
            param_shiptype = ''
        
        param_level,infolist = await match_keywords(infolist,levels)
        if not param_level:
            param_level = ''
        params = {
            "accountId": ev.user_id,
            "server": server_type,
            "county":param_nation,
            "level":param_level,
            "shipName":'',
            "shipType":param_shiptype
        }
        url = 'https://api.wows.shinoaki.com/public/wows/roll/ship/roll'
        logger.success(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.post(url, json=params, timeout=None)
            logger.success(f"本次请求返回的状态码:{resp.status_code}")
            result = resp.json()
        if result['code'] == 200 and result['data']:
            msg = f"本次roll到了{result['data']['shipNameCn']}"
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