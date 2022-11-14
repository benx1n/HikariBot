from dataclasses import dataclass
from typing import Tuple,List
import time
import traceback
from pathlib import Path
import re

dir_path = Path(__file__).parent
template_path = dir_path / "template"

@dataclass
class matching:
    keywords: Tuple[str, ...]
    match_keywords : str
    
nations = [
    matching(("commonwealth","英联邦",),"commonwealth"),
    matching(("europe","欧洲",),"europe"),
    matching(("france","法国",),"france"),
    matching(("germany","德国",),"germany"),
    matching(("italy","意大利",),"italy"),
    matching(("japan","日本",),"japan"),
    matching(("pan_america","泛美",),"pan_america"),
    matching(("pan_asia","泛亚",),"pan_asia"),
    matching(("uk","英国","United_Kingdom"),"United_Kingdom"),
    matching(("usa","美国",),"usa"),
    matching(("ussr","苏联",),"Russia"),
    matching(("netherlands","荷兰",),"netherlands"),
    matching(("spain","西班牙",),"spain"),
]

shiptypes = [
    matching(("Cruiser","巡洋舰","巡洋","CA"),"Cruiser"),
    matching(("Battleship","战列舰","战列","BB"),"Battleship"),
    matching(("Destroyer","驱逐舰","驱逐","DD"),"Destroyer"),
    matching(("Submarine","潜艇","SS"),"Submarine"),
    matching(("Auxiliary","辅助舰艇","DD"),"Auxiliary"),
    matching(("AirCarrier","航空母舰","航母","CV"),"AirCarrier"),
]

levels = [
    matching(("1","1级","一级","一"),"1"),
    matching(("2","2级","二级","二"),"2"),
    matching(("3","3级","三级","三"),"3"),
    matching(("4","4级","四级","四"),"4"),
    matching(("4","4级","四级","四"),"4"),
    matching(("5","5级","五级","五"),"5"),
    matching(("6","6级","六级","六"),"6"),
    matching(("7","7级","七级","七"),"7"),
    matching(("8","8级","八级","八"),"8"),
    matching(("9","9级","九级","九"),"9"),
    matching(("10","10级","十级","十"),"10"),
    matching(("11","11级","十一级","十一"),"11"),
]

servers = [
    matching(("asia","亚服","asian"),"asia"),
    matching(("eu","欧服","europe"),"eu"),
    matching(("na","美服","NorthAmerican"),"na"),
    matching(("ru","俄服","Russia"),"ru"),
    matching(("cn","国服","china"),"cn"),
]

tiers = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ"]

number_url_homes={
    "asia":"https://asia.wows-numbers.com",
    "eu":"https://wows-numbers.com",
    "na":"https://na.wows-numbers.com",
    "ru":"https://ru.wows-numbers.com",
    "cn": ""
}

nb2_file = [
    {
        "name":"bot.py",
        "url":"https://raw.fastgit.org/benx1n/HikariBot/master/bot.py"
    },
    {
        "name":".env",
        "url":"https://raw.fastgit.org/benx1n/HikariBot/master/.env"
    },
    {
        "name":"pyproject.toml",
        "url":"https://raw.fastgit.org/benx1n/HikariBot/master/pyproject.toml"
    }
]

pr_select = [
    {
        "value": 0,
        "name": "还需努力",
        "englishName": "Bad",
        "color": "#f44336"
    },
    {
        "value": 750,
        "name": "低于平均",
        "englishName": "Below Average",
        "color": "#FF9800"
    },
    {
        "value": 1100,
        "name": "平均水平",
        "englishName": "Average",
        "color": "#FFC107"
    },
    {
        "value": 1350,
        "name": "好",
        "englishName": "Good",
        "color": "#8BC34A"
    },
    {
        "value": 1550,
        "name": "很好",
        "englishName": "Very Good",
        "color": "#4CAF50"
    },
    {
        "value": 1750,
        "name": "非常好",
        "englishName": "Great",
        "color": "#00BCD4"
    },
    {
        "value": 2100,
        "name": "大佬水平",
        "englishName": "Unicum",
        "color": "#9C27B0"
    },
    {
        "value": 2450,
        "name": "神佬水平",
        "englishName": "Super Unicum",
        "color": "#673AB7"
    }
]

color_data = {
    "Bad": "#F44336",
    "Below Average": "#FF9800",
    "Average": "#FFC107",
    "Good": "#8BC34A",
    "Very Good": "#4CAF50",
    "Great": "#00BCD4",
    "Unicum": "#9C27B0",
    "Super Unicum": "#673AB7"
}

async def set_infoparams(List):
    try:
        result = {
            "template_path":template_path,
            "data":List
        }
        return result
    except Exception:
        traceback.print_exc()

async def set_recentparams(List):
    try:   
        result = {
            "data":List
        }
        return result
    except Exception:
        traceback.print_exc()
        
async def set_shipparams(List):
    try:   
        result = {
            "data":List
        }
        return result
    except Exception:
        traceback.print_exc()

async def set_shipRecentparams(List):
    try:   
        result = {
            "data":List,
        }
        return result
    except Exception:
        traceback.print_exc()
           
async def select_prvalue_and_color(pr):
    describe,color = None,None
    if pr:
        for select in pr_select :
            if pr > select['value']:
                describe = select['name']
                color = select['color']
    return describe,color


async def set_ShipRank_Numbers(data,server,shipId):
    try:
        info_list = list()
        for each in data[0:10]:
            index = int(each.select('td')[0].string)
            clan_name = each.select('td[style="text-align: left;  "] a')
            if len(clan_name) > 1:
                tag = clan_name[0].string.replace("[",'').replace("]",'')
                userName = clan_name[1].string
                url = clan_name[1].attrs['href']
            else:
                tag = None
                userName = clan_name[0].string
                url = clan_name[0].attrs['href']
            accountId = await search_accountId(url)
            battles = int(each.select('td span')[0].string.replace(' ',''))
            pr = int(each.select('td span')[1].string.replace(' ',''))
            prColor = await search_color(each.select('td span')[1].attrs['style'])
            wins = float(each.select('td span')[2].string.replace('%',''))
            winsColor = await search_color(each.select('td span')[2].attrs['style'])
            frags = float(each.select('td span')[3].string)
            fragsColor = await search_color(each.select('td span')[3].attrs['style'])
            maxFrags = int(each.select('td span')[4].string)
            damage = int(each.select('td span')[5].string.replace(' ',''))
            damageColor = await search_color(each.select('td span')[5].attrs['style'])
            maxDamage = int(each.select('td span')[6].string.replace(' ',''))
            xp = int(each.select('td span')[7].string.replace(' ',''))
            maxXp = int(each.select('td span')[8].string.replace(' ',''))
            planesDestroyed = float(each.select('td span')[9].string)
            planesDestroyedColor = await search_color(each.select('td span')[9].attrs['style'])
            maxPlanesDestroyed = int(each.select('td span')[10].string)
            info ={
                "accountId":accountId,
                "battles":battles,
                "damage":damage,
                "damageColor":damageColor,
                "frags":frags,
                "fragsColor":fragsColor,
                "index":index,
                "maxDamage":maxDamage,
                "maxFrags":maxFrags,
                "maxPlanesDestroyed":maxPlanesDestroyed,
                "maxXp":maxXp,
                "planesDestroyed":planesDestroyed,
                "planesDestroyedColor":planesDestroyedColor,
                "pr":pr,
                "prColor":prColor,
                "server":server,
                "shipId":shipId,
                "wins":wins,
                "winsColor":winsColor,
                "xp":xp,
                "tag":tag,
                "userName":userName
            }
            info_list.append(info)
        return info_list
            
    except Exception:
        traceback.print_exc()
        return None
    
async def set_clanRecord_params():
    return

async def search_accountId(str):
    try:
        match = re.search(r"/player/(.*?),",str)
        if match:
            return int(match.group(1).strip())
        else:
            return None
    except Exception:
        traceback.print_exc()
        return None
       
async def search_color(str):
    try:
        match = re.search(r"color:(.*?);",str)
        if match:
            return match.group(1).strip()
        else:
            return None
    except Exception:
        traceback.print_exc()
        return None

async def set_damageColor(type,value):
    try:
        if type == 'Destroyer':
            if not value or value < 33000:
                return color_data["Bad"]
            elif value < 40000:
                return color_data["Good"]
            elif value < 55000:
                return color_data["Great"]
            elif value < 64000:
                return color_data["Unicum"]
            else:
                return color_data["Super Unicum"]
        elif type == 'Cruiser':
            if not value or value < 47000:
                return color_data["Bad"]
            elif value < 55000:
                return color_data["Good"]
            elif value < 83000:
                return color_data["Great"]
            elif value < 95000:
                return color_data["Unicum"]
            else:
                return color_data["Super Unicum"]
        elif type == 'AirCarrier':
            if not value or value < 60000:
                return color_data["Bad"]
            elif value < 71000:
                return color_data["Good"]
            elif value < 84000:
                return color_data["Great"]
            elif value < 113000:
                return color_data["Unicum"]
            else:
                return color_data["Super Unicum"]
        else:
            if not value or value < 64000:
                return color_data["Bad"]
            elif value < 72000:
                return color_data["Good"]
            elif value < 97000:
                return color_data["Great"]
            elif value < 108000:
                return color_data["Unicum"]
            else:
                return color_data["Super Unicum"]
    except Exception:
        traceback.print_exc()
        return None

async def set_winColor(value):
    try:
        if not value or value < 45:
            return color_data["Bad"]
        elif value < 50:
            return color_data["Below Average"]
        elif value < 55:
            return color_data["Average"]
        elif value < 60:
            return color_data["Good"]
        elif value < 65:
            return color_data["Great"]
        elif value < 70:
            return color_data["Unicum"]
        else:
            return color_data["Super Unicum"]
    except Exception:
        traceback.print_exc()
        return None

async def set_upinfo_color(value):
    try:
        if not value or value < 0 :
            return color_data["Bad"]
        elif value > 0 :
            return color_data["Good"]
        else:
            return None
    except Exception:
        traceback.print_exc()
        return None