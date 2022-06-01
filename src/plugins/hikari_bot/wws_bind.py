from typing import List
import httpx
import traceback
import re
from .data_source import servers
from .publicAPI import get_AccountIdByName
from .utils import match_keywords
from nonebot import get_driver
from nonebot.log import logger

headers = {
    'Authorization': get_driver().config.api_token
}

async def get_BindInfo(user,info):
    try:
        url,params = '',''
        if isinstance(info,List) and len(info) == 1:
            for i in info:              #是否包含me或@
                if i == 'me':
                    url = 'https://api.wows.linxun.link/public/wows/bind/account/platform/bind/list'
                    params = {
                    "platformType": "QQ",
                    "platformId": user,
                    }
                match = re.search(r"CQ:at,qq=(\d+)",i)
                if match:
                    url = 'https://api.wows.linxun.link/public/wows/bind/account/platform/bind/list'
                    params = {
                    "platformType": "QQ",
                    "platformId": match.group(1),
                    }
                    break
            if not url or not params:
                return '参数似乎出了问题呢，请使用me或@群友'
        else:
            return '参数似乎出了问题呢，请使用me或@群友'
        logger.info(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=10)
            logger.info(f"下面是本次请求返回的状态码，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{resp.status_code}")
            result = resp.json()
        if result['code'] == 200 and result['message'] == "success":
            if result['data']:
                msg1 = f'当前绑定账号\n'
                msg2 = f'绑定账号列表\n'
                flag = 1
                for bindinfo in result['data']:
                    msg2 += f"{flag}：{bindinfo['serverType']} {bindinfo['userName']}\n"
                    flag += 1
                    if bindinfo['defaultId']:
                        msg1 += f"{bindinfo['serverType']} {bindinfo['userName']}\n"
                msg = msg1+msg2+"本人发送[wws 切换绑定+序号] 切换对应账号"
                return msg
            else:
                return '该用户似乎还没绑定窝窝屎账号'
        else:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
    except Exception:
        logger.error(traceback.format_exc())
        return 'wuwuwu出了点问题，请联系麻麻解决'
    
async def set_BindInfo(user,info):
    try:
        param_server = None
        if isinstance (info,List):
            if len(info) == 2:
                param_server,info = await match_keywords(info,servers)
                if param_server:
                    param_accountid = await get_AccountIdByName(param_server,str(info[0]))
                    if param_accountid and param_accountid != 404:
                        url = 'https://api.wows.linxun.link/api/wows/bind/account/platform/bind/put'
                        params = {
                        "platformType": "QQ",
                        "platformId": str(user),
                        "accountId": param_accountid
                        }
                    elif param_accountid == 404:
                        return '无法查询该游戏昵称Orz，请检查昵称是否存在'
                    else:
                        return '发生了错误，有可能是网络波动，请稍后再试'
                else:
                    return '服务器参数似乎输错了呢'
            else:
                return '参数似乎输错了呢，请确保后面跟随服务器+游戏昵称'
        else:
            return '参数似乎输错了呢，请确保后面跟随服务器+游戏昵称'
        logger.info(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=20)
            logger.info(f"下面是本次请求返回的状态码，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{resp.status_code}")
            result = resp.json()
        if result['code'] == 200 and result['message'] == "success":
            return '绑定成功'
        elif result['code'] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return 'wuwuwu出了点问题，请联系麻麻解决'
    except Exception:
        logger.error(traceback.format_exc())
        return 'wuwuwu出了点问题，请联系麻麻解决'

async def change_BindInfo(user,info):
    try:
        if isinstance(info,List) and len(info) == 1 and str(info[0]).isdigit:
            url = 'https://api.wows.linxun.link/public/wows/bind/account/platform/bind/list'
            params = {
            "platformType": "QQ",
            "platformId": user,
            }
        else:
            return '参数似乎出了问题呢，请跟随要切换的序号'
        logger.info(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=10)
            logger.info(f"下面是本次请求返回的状态码，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{resp.status_code}")
            result = resp.json()
        if result['code'] == 200 and result['message'] == "success":
            if result['data'] and len(result['data']) >= int(info[0]):
                account_name = result['data'][int(info[0])-1]['userName']
                param_server = result['data'][int(info[0])-1]['serverType']
                param_accountid = await get_AccountIdByName(param_server,account_name)
                if param_accountid and param_accountid != 404:
                    url = 'https://api.wows.linxun.link/api/wows/bind/account/platform/bind/put'
                    params = {
                    "platformType": "QQ",
                    "platformId": str(user),
                    "accountId": param_accountid
                    }
                elif param_accountid == 404:
                        return '无法查询该游戏昵称Orz，请检查昵称是否存在'
                else:
                    return '发生了错误，有可能是网络波动，请稍后再试'
            else:
                return '没有对应序号的绑定记录'
        else:
            return '参数似乎不正确，请确保只跟随了序号'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=10)
            result = resp.json()
        if result['code'] == 200 and result['message'] == "success":
            return f'切换绑定成功,当前绑定账号{account_name}'
        elif result['code'] == 403:
            return f"{result['message']}\n请先绑定账号"
        elif result['code'] == 404:
            return f"{result['message']}"
        elif result['code'] == 500:
            return f"{result['message']}\n这是服务器问题，请联系雨季麻麻"
        else:
            return 'wuwuwu出了点问题，请联系麻麻解决'
    except Exception:
        logger.error(traceback.format_exc())
        return 'wuwuwu出了点问题，请联系麻麻解决'