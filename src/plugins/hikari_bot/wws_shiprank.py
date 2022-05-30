from typing import List
import httpx
import traceback
import jinja2
import asyncio
from pathlib import Path
from nonebot.adapters.onebot.v11 import MessageSegment
from .data_source import servers,set_shipparams,tiers,number_url_homes
from .utils import match_keywords
from nonebot_plugin_htmlrender import html_to_pic,text_to_pic
from .wws_info import get_AccountIdByName
from .wws_ship import SecletProcess,ShipSlectState
from.publicAPI import get_ship_byName
from bs4 import BeautifulSoup
from nonebot import get_driver
from nonebot.log import logger

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
                select_shipId = shipList[0][0]
                number_url += f"{select_shipId},{shipList[0][2]}"
            else:
                msg = f'存在多条名字相似的船\n请在20秒内选择对应的序号\n=================\n'
                flag = 0
                for each in shipList:
                    flag += 1
                    msg += f"{flag}：{tiers[each[3]-1]} {each[1]}\n"
                SecletProcess[qqid] = ShipSlectState(False, None, shipList)
                img = await text_to_pic(text=msg,width=230)
                await bot.send(MessageSegment.image(img))
                a = 0
                while a < 200 and not SecletProcess[qqid].state:
                    a += 1
                    await asyncio.sleep(0.1)
                    #print(SecletProcess[qqid].SelectList)
                if SecletProcess[qqid].state and SecletProcess[qqid].SlectIndex <= len(shipList):
                    select_shipId = int(shipList[SecletProcess[qqid].SlectIndex-1][0])
                    number_url += f"{select_shipId},{shipList[SecletProcess[qqid].SlectIndex-1][2]}"
                else:
                    return '已超时退出'
        else:
            return '找不到船'
        content = await search_ShipRank_Yuyuko(select_shipId,param_server)
        if content:                                         #存在缓存，直接出图
            print('存在缓存')
            return await html_to_pic(content, wait=0, viewport={"width": 1800, "height": 100})
        else:                                               #无缓存，去Number爬
            content,numbers_data = await search_ShipRank_Numbers(number_url)
            if content:
                await post_ShipRank(select_shipId,param_server,numbers_data)     #上报Yuyuko
                return await html_to_pic(content, wait=0, viewport={"width": 1800, "height": 100})
            else:
                return 'wuwuu好像出了点问题，可能是网络问题，过一会儿还是不行的话请联系麻麻~'   
    except Exception:
        logger.error(traceback.format_exc())
        return 'wuwuu好像出了点问题，过一会儿还是不行的话请联系麻麻~' 
   
async def search_ShipRank_Yuyuko(shipId,server):
    try:
        content = None
        async with httpx.AsyncClient(headers=headers) as client:        #查询是否有缓存
            url = 'https://api.wows.linxun.link/upload/numbers/data/upload/ship/rank'
            params = {
                "shipId":int(shipId),
                "server":server
            }
            logger.info(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}\n{params}")
            resp = await client.get(url, params=params,timeout=20)
            logger.info(f"下面是本次请求返回的状态码，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{resp.status_code}")
            result = resp.json()
            if result['code'] == 200 and result['data']:
                template = env.get_template("ship-rank.html")
                result_data = {"data":result['data']}
                content = await template.render_async(result_data)
                return content
            else:
                return None
    except Exception:
        logger.error(traceback.format_exc())
        return None 
        
async def search_ShipRank_Numbers(url):
    try:
        content = None
        logger.info(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{url}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=20)
            logger.info(f"下面是本次请求返回的状态码，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{resp.status_code}")
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
        logger.error(traceback.format_exc())
        return None,None
            
async def post_ShipRank(shipId,server,data):
    try:
        async with httpx.AsyncClient(headers=headers) as client:
            url = 'https://api.wows.linxun.link/upload/numbers/data/upload/ship/rank'
            result = f'''{data}'''
            post_data = {
                "bodyHtml": result,
                "server": server,
                "shipId": int(shipId)
            }
            resp = await client.post(url, json = post_data, timeout=20)
            result = resp.json()
            print(result)
    except Exception:
        logger.error(traceback.format_exc())