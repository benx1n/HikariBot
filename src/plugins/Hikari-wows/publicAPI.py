from typing import List
import httpx
import traceback
from .data_source import nations,shiptypes,levels
from .utils import match_keywords
from nonebot import get_driver

headers = {
    'Authorization': get_driver().config.api_token
}

async def get_nation_list():
    try:
        msg = ''
        url = 'https://api.wows.linxun.link/public/wows/encyclopedia/nation/list'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, timeout=10)
            result = resp.json()
        for nation in result['data']:
            msg: str = msg + f"{nation['cn']}：{nation['nation']}\n"
        return msg
    except Exception:
        traceback.print_exc()
        
async def get_ship_name(infolist:List):
    msg = ''
    try:
        param_nation,infolist = await match_keywords(infolist,nations)
        if not param_nation:
            return '请检查国家名是否正确'
        
        param_shiptype,infolist = await match_keywords(infolist,shiptypes)
        if not param_shiptype:
            return '请检查船只类别是否正确'
        
        param_level,infolist = await match_keywords(infolist,levels)
        if not param_level:
            return '请检查船只等级是否正确'
        params = {
            "county":param_nation,
            "level":param_level,
            "shipName":'',
            "shipType":param_shiptype
        }
        url = 'https://api.wows.linxun.link/public/wows/encyclopedia/ship/search'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=10)
            result = resp.json()
        if result['data']:
            for ship in result['data']:
                msg += f"{ship['shipNameCn']}：{ship['shipNameNumbers']}\n"
        else:
            msg = '没有符合的船只'
        return msg
    except Exception:
        traceback.print_exc()
        return msg
    
async def get_ship_byName(shipname:str):
    try:
        url = 'https://api.wows.linxun.link/public/wows/encyclopedia/ship/search'
        params = {
        "county":'',
        "level":'',
        "shipName":shipname,
        "shipType":''
    }
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=10)
            result = resp.json()
        List = []
        if result['code'] == 200 and result['data']:
            for each in result['data']:
                List.append([each['id'],each['shipNameCn'],each['shipNameNumbers']])
            return List
        else:
            return None
    except Exception:
        traceback.print_exc()
        return None