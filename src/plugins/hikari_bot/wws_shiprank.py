from typing import List
import httpx
import traceback
import json
import jinja2
import re
import asyncio
from pathlib import Path
from .data_source import servers,set_shipparams,tiers,number_url_homes
from .utils import html_to_pic,match_keywords
from .wws_info import get_AccountIdByName
from .wws_ship import SecletProcess,ShipSlectState
from.publicAPI import get_ship_byName
from bs4 import BeautifulSoup
from nonebot import get_driver

dir_path = Path(__file__).parent
template_path = dir_path / "template"

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)

headers = {
    'Authorization': get_driver().config.api_token,
    'accept':'application/json',
    'Content-Type':'application/json',
}

async def get_ShipRank(qqid,info,bot):
    try:
        if len(info) == 2:
            param_server,info = await match_keywords(info,servers)
            if param_server and not param_server == 'cn':
                number_url = number_url_homes[param_server] + "/ship/"
            else:
                return '请检查服务器是否正确，暂不支持国服'
        else:
            return '参数似乎出了问题呢'
        shipList = await get_ship_byName(str(info[0]))
        print(shipList)
        if shipList:
            if len(shipList) < 2:
                select_shipId = shipList[0]
                number_url += f"{select_shipId},{shipList[2]}"
            else:
                msg = f'存在多条名字相似的船，请在二十秒内选择对应的序号\n'
                flag = 0
                for each in shipList:
                    flag += 1
                    msg += f"{flag}：{tiers[each[3]-1]} {each[1]}：{each[2]}\n"
                SecletProcess[qqid] = ShipSlectState(False, None, shipList)
                await bot.send(msg)
                a = 0
                while a < 200 and not SecletProcess[qqid].state:
                    a += 1
                    await asyncio.sleep(0.1)
                    #print(SecletProcess[qqid].SelectList)
                if SecletProcess[qqid].state and SecletProcess[qqid].SlectIndex <= len(shipList):
                    select_shipId = int(shipList[SecletProcess[qqid].SlectIndex-1][0])
                    number_url += f"{select_shipId},{shipList[SecletProcess[qqid].SlectIndex-1][2]}"
                    print(number_url)
                else:
                    return '已超时退出'
        else:
            return '找不到船'
        content = await search_ShipRank_Yuyuko(select_shipId)
        if content:                                         #存在缓存，直接出图
            return await html_to_pic(content, wait=0, viewport={"width": 1800, "height": 100})
        else:                                               #无缓存，去Number爬
            content,numbers_data = await search_ShipRank_Numbers(number_url)
            if content:
                await post_ShipRank(select_shipId,numbers_data)     #上报Yuyuko
                return await html_to_pic(content, wait=0, viewport={"width": 1800, "height": 100})
            else:
                return 'wuwuu好像出了点问题，可能是网络问题，过一会儿还是不行的话请联系麻麻~'   
    except Exception:
        traceback.print_exc()
        return    
   
async def search_ShipRank_Yuyuko(shipId):
    try:
        content = None
        async with httpx.AsyncClient(headers=headers) as client:        #查询是否有缓存
            url = 'https://api.wows.linxun.link/upload/numbers/data/upload/ship/rank'
            params = {
                "shipId":int(shipId)
            }
            resp = await client.get(url, params=params,timeout=20)
            result = resp.json()
            if result['code'] == 200 and result['data']:
                template = env.get_template("wws-ship.html")
                template_data = await set_shipparams(result['data'])
                content = await template.render_async(template_data)
                return content
            else:
                return None
    except Exception:
        traceback.print_exc()
        return None 
        
async def search_ShipRank_Numbers(url):
    try:
        content = None
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=20)
        soup = BeautifulSoup(resp.content, 'html.parser')
        data = soup.select_one('div[style="clear:both;"]')
        if data:
            template = env.get_template("ship-rank.html")
            result_data = {"data":data}
            content = await template.render_async(result_data)
            return content,data
        else:
            return None,None
    except Exception:
        traceback.print_exc()
        return None,None
            
async def post_ShipRank(shipId,data):
    try:
        async with httpx.AsyncClient(headers=headers) as client:
            url = 'https://api.wows.linxun.link/upload/numbers/data/upload/ship/rank'
            post_data = {
                "bodyHtml": str(data),
                "shipId": int(shipId)
            }
            resp = await client.post(url, data = post_data, timeout=20)
            result = resp.json()
            print(result)
    except Exception:
        traceback.print_exc()