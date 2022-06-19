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
    
command_list = [        #同指令中越长的匹配词越靠前
    matching(("切换绑定","更换绑定","更改绑定"),"changebind"),
    matching(("查询绑定","绑定查询","绑定列表","查绑定"),"bindlist"),
    matching(("删除绑定",),"delete_bind"),
    matching(("特殊绑定",),"special_bind"),
    matching(("ship.rank","SHIP.RANK","rank","RANK"),"ship_rank"),
    matching(("bind","BIND","绑定","set","SET"),"bind"),
    matching(("recent","RECENT","近期",),"recent"),
    matching(("ship","SHIP","单船",),"ship"),
    matching(("搜船名","查船名","船名"),"searchship"),
    matching(("clan","军团","公会","工会"),"clan"),
    matching(("help","HELP","帮助"),"help"),
]

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
    matching(("ussr","苏联",),"ussr"),
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
    "cn": None
}

pr_select = [
    {
        "value": 0,
        "name": "还需努力",
        "englishName": "Bad",
        "color": "#FE0E00"
    },
    {
        "value": 750,
        "name": "低于平均",
        "englishName": "Below Average",
        "color": "#FE7903"
    },
    {
        "value": 1100,
        "name": "平均水平",
        "englishName": "Average",
        "color": "#FFC71F"
    },
    {
        "value": 1350,
        "name": "好",
        "englishName": "Good",
        "color": "#44B300"
    },
    {
        "value": 1550,
        "name": "很好",
        "englishName": "Very Good",
        "color": "#318000"
    },
    {
        "value": 1750,
        "name": "非常好",
        "englishName": "Great",
        "color": "#02C9B3"
    },
    {
        "value": 2100,
        "name": "大佬水平",
        "englishName": "Unicum",
        "color": "#D042F3"
    },
    {
        "value": 2450,
        "name": "神佬水平",
        "englishName": "Super Unicum",
        "color": "#A00DC5"
    }
]

color_data = {
    "Bad": "#FE0E00",
    "Below Average": "#FE7903",
    "Average": "#FFC71F",
    "Good": "#44B300",
    "Very Good": "#318000",
    "Great": "#02C9B3",
    "Unicum": "#D042F3",
    "Super Unicum": "#A00DC5"
}

async def set_infoparams(List):
    try:
        winsColor = await set_winColor(List['pvp']['wins'])
        damageColor = await set_damageColor(None,List['pvp']['damage'])
        bb_winsColor = await set_winColor(List['type']['Battleship']['wins'])
        ca_winsColor = await set_winColor(List['type']['Cruiser']['wins'])
        dd_winsColor = await set_winColor(List['type']['Destroyer']['wins'])
        cv_winsColor = await set_winColor(List['type']['AirCarrier']['wins'])
        bb_damageColor = await set_damageColor(None,List['type']['Battleship']['damage'])
        ca_damageColor = await set_damageColor('Cruiser',List['type']['Cruiser']['damage'])
        dd_damageColor = await set_damageColor('Destroyer',List['type']['Destroyer']['damage'])
        cv_damageColor = await set_damageColor('AirCarrier',List['type']['AirCarrier']['damage'])
        solo_winsColor = await set_winColor(List['pvpSolo']['wins'])
        solo_damageColor = await set_damageColor(None,List['pvpSolo']['damage'])
        div2_winsColor = await set_winColor(List['pvpTwo']['wins'])
        div2_damageColor = await set_damageColor(None,List['pvpTwo']['damage'])
        div3_winsColor = await set_winColor(List['pvpThree']['wins'])
        div3_damageColor = await set_damageColor(None,List['pvpThree']['damage'])
        rank_winsColor = await set_winColor(List['rankSolo']['wins'])
        rank_damageColor = await set_damageColor(None,List['rankSolo']['damage'])
        newDamageColor = await set_upinfo_color(List['dwpDataVO']['damage'])
        newWinsColor = await set_upinfo_color(List['dwpDataVO']['wins'])
        newPrColor = await set_upinfo_color(List['dwpDataVO']['pr'])
        result = {
            "template_path":template_path,
            "guild":List['clanInfo']['tag'],
            "userName":List['userName'],
            "karma":List['karma'],
            "serverName":List['serverName'],
            "newDamage":f"{List['dwpDataVO']['damage']:+} ",
            "newWins":f"{List['dwpDataVO']['wins']:+.2f}",
            "newPr":f"{List['dwpDataVO']['pr']:+}",
            "prValue":f"{List['pr']['value']} {List['pr']['name']}",
            "time":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(abs(List['lastDateTime']))),
            "battles":List['pvp']['battles'],
            "wins":List['pvp']['wins'],
            "damage":List['pvp']['damage'],
            "xp":List['pvp']['xp'],
            "kd":List['pvp']['kd'],
            "frags":f"{List['pvp']['frags']:.2f}",
            "hit":List['pvp']['hit'],
            "bb_battles":List['type']['Battleship']['battles'],
            "bb_pr":List['type']['Battleship']['pr']['value'],
            "bb_wins":List['type']['Battleship']['wins'],
            "bb_damage":List['type']['Battleship']['damage'],
            "bb_hit":List['type']['Battleship']['hit'],
            "ca_battles":List['type']['Cruiser']['battles'],
            "ca_pr":List['type']['Cruiser']['pr']['value'],
            "ca_wins":List['type']['Cruiser']['wins'],
            "ca_damage":List['type']['Cruiser']['damage'],
            "ca_hit":List['type']['Cruiser']['hit'],
            "dd_battles":List['type']['Destroyer']['battles'],
            "dd_pr":List['type']['Destroyer']['pr']['value'],
            "dd_wins":List['type']['Destroyer']['wins'],
            "dd_damage":List['type']['Destroyer']['damage'],
            "dd_hit":List['type']['Destroyer']['hit'], 
            "cv_battles":List['type']['AirCarrier']['battles'],
            "cv_pr":List['type']['AirCarrier']['pr']['value'],
            "cv_wins":List['type']['AirCarrier']['wins'],
            "cv_damage":List['type']['AirCarrier']['damage'],
            "cv_hit":List['type']['AirCarrier']['hit'],      
            "solo_battles":List['pvpSolo']['battles'],
            "solo_wins":List['pvpSolo']['wins'],
            "solo_pr":List['pvpSolo']['pr']['value'],
            "solo_xp":List['pvpSolo']['xp'],
            "solo_damage":List['pvpSolo']['damage'],
            "solo_kd":List['pvpSolo']['kd'],
            "solo_hit":List['pvpSolo']['hit'],
            "solo_frags":f"{List['pvpSolo']['frags']:.2f}",
            "div2_battles":List['pvpTwo']['battles'],
            "div2_wins":List['pvpTwo']['wins'],
            "div2_pr":List['pvpTwo']['pr']['value'],
            "div2_xp":List['pvpTwo']['xp'],
            "div2_damage":List['pvpTwo']['damage'],
            "div2_kd":List['pvpTwo']['kd'],
            "div2_hit":List['pvpTwo']['hit'],
            "div2_frags":f"{List['pvpTwo']['frags']:.2f}",
            "div3_battles":List['pvpThree']['battles'],
            "div3_wins":List['pvpThree']['wins'],
            "div3_pr":List['pvpThree']['pr']['value'],
            "div3_xp":List['pvpThree']['xp'],
            "div3_damage":List['pvpThree']['damage'],
            "div3_kd":List['pvpThree']['kd'],
            "div3_hit":List['pvpThree']['hit'],
            "div3_frags":f"{List['pvpThree']['frags']:.2f}",
            "rank_battles":List['rankSolo']['battles'],
            "rank_wins":List['rankSolo']['wins'],
            "rank_pr":List['rankSolo']['pr']['value'],
            "rank_xp":List['rankSolo']['xp'],
            "rank_damage":List['rankSolo']['damage'],
            "rank_kd":List['rankSolo']['kd'],
            "rank_hit":List['rankSolo']['hit'],
            "rank_frags":f"{List['rankSolo']['frags']:.2f}",
            "lv1":List['battleCountAll']['1'],
            "lv2":List['battleCountAll']['2'],
            "lv3":List['battleCountAll']['3'],
            "lv4":List['battleCountAll']['4'],
            "lv5":List['battleCountAll']['5'],
            "lv6":List['battleCountAll']['6'],
            "lv7":List['battleCountAll']['7'],
            "lv8":List['battleCountAll']['8'],
            "lv9":List['battleCountAll']['9'],
            "lv10":List['battleCountAll']['10'],
            "lv11":List['battleCountAll']['11'],
            "newDamageColor":newDamageColor,
            "newWinsColor":newWinsColor,
            "newPrColor":newPrColor,
            "prValueColor":List['pr']['color'],
            "winsColor":winsColor,
            "damageColor":damageColor,
            "bb_prColor":List['type']['Battleship']['pr']['color'],
            "ca_prColor":List['type']['Cruiser']['pr']['color'],
            "dd_prColor":List['type']['Destroyer']['pr']['color'],
            "cv_prColor":List['type']['AirCarrier']['pr']['color'],
            "solo_prColor":List['pvpSolo']['pr']['color'],
            "div2_prColor":List['pvpTwo']['pr']['color'],
            "div3_prColor":List['pvpThree']['pr']['color'],
            "rank_prColor":List['rankSolo']['pr']['color'],
            "clanColor":List['clanInfo']['colorRgb'],
            "bb_winsColor":bb_winsColor,
            "ca_winsColor":ca_winsColor,
            "dd_winsColor":dd_winsColor,
            "cv_winsColor":cv_winsColor,
            "bb_damageColor":bb_damageColor,
            "ca_damageColor":ca_damageColor,
            "dd_damageColor":dd_damageColor,
            "cv_damageColor":cv_damageColor,
            "solo_winsColor":solo_winsColor,
            "solo_damageColor":solo_damageColor,
            "div2_winsColor":div2_winsColor,
            "div2_damageColor":div2_damageColor,
            "div3_winsColor":div3_winsColor,
            "div3_damageColor":div3_damageColor,
            "rank_winsColor":rank_winsColor,
            "rank_damageColor":rank_damageColor
        }
        return result
    except Exception:
        traceback.print_exc()

async def set_recentparams(List):
    try:   
        InfoRecent_RandomData = await set_InfoRecent_RandomData(List['shipData'][0])
        InfoRecent_RankData = await set_InfoRecent_RankData(List['shipData'][0])
        winsColor = await set_winColor(List['shipData'][0]['pvpInfo']['wins'])
        damageColor = await set_damageColor(None,List['shipData'][0]['pvpInfo']['damage'])
        solo_winsColor = await set_winColor(List['shipData'][0]['pvpSoloInfo']['wins'])
        solo_damageColor = await set_damageColor(None,List['shipData'][0]['pvpSoloInfo']['damage'])
        div2_winsColor = await set_winColor(List['shipData'][0]['pvpTwoInfo']['wins'])
        div2_damageColor = await set_damageColor(None,List['shipData'][0]['pvpTwoInfo']['damage'])
        div3_winsColor = await set_winColor(List['shipData'][0]['pvpThreeInfo']['wins'])
        div3_damageColor = await set_damageColor(None,List['shipData'][0]['pvpThreeInfo']['damage'])
        rank_winsColor = await set_winColor(List['shipData'][0]['rankInfo']['wins'])
        rank_damageColor = await set_damageColor(None,List['shipData'][0]['rankInfo']['damage'])
        result = {
            "guild":List['clanInfo']['tag'],
            "userName":List['userName'],
            "serverName":List['serverName'],
            "prValue":f"{List['shipData'][0]['pvpInfo']['pr']['value']} {List['shipData'][0]['pvpInfo']['pr']['name']}",
            "reTime":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(abs(List['shipData'][0]['recordDateTime']/1000)))),
            "battles":List['shipData'][0]['pvpInfo']['battles'],
            "wins":List['shipData'][0]['pvpInfo']['wins'],
            "damage":List['shipData'][0]['pvpInfo']['damage'],
            "xp":List['shipData'][0]['pvpInfo']['xp'],
            "kd":List['shipData'][0]['pvpInfo']['kd'],
            "hit":f"{List['shipData'][0]['pvpInfo']['hit']:.2f}",
            "frags":f"{List['shipData'][0]['pvpInfo']['frags']:.2f}",
            "solo_battles":List['shipData'][0]['pvpSoloInfo']['battles'],
            "solo_wins":List['shipData'][0]['pvpSoloInfo']['wins'],
            "solo_pr":f"{List['shipData'][0]['pvpSoloInfo']['pr']['value']} {List['shipData'][0]['pvpSoloInfo']['pr']['name']}",
            "solo_xp":List['shipData'][0]['pvpSoloInfo']['xp'],
            "solo_damage":List['shipData'][0]['pvpSoloInfo']['damage'],
            "solo_kd":List['shipData'][0]['pvpSoloInfo']['kd'],
            "solo_hit":f"{List['shipData'][0]['pvpSoloInfo']['hit']:.2f}",
            "solo_frags":f"{List['shipData'][0]['pvpSoloInfo']['frags']:.2f}",
            "div2_battles":List['shipData'][0]['pvpTwoInfo']['battles'],
            "div2_wins":List['shipData'][0]['pvpTwoInfo']['wins'],
            "div2_pr":f"{List['shipData'][0]['pvpTwoInfo']['pr']['value']} {List['shipData'][0]['pvpTwoInfo']['pr']['name']}",
            "div2_xp":List['shipData'][0]['pvpTwoInfo']['xp'],
            "div2_damage":List['shipData'][0]['pvpTwoInfo']['damage'],
            "div2_kd":List['shipData'][0]['pvpTwoInfo']['kd'],
            "div2_hit":f"{List['shipData'][0]['pvpTwoInfo']['hit']:.2f}",
            "div2_frags":f"{List['shipData'][0]['pvpTwoInfo']['frags']:.2f}",
            "div3_battles":List['shipData'][0]['pvpThreeInfo']['battles'],
            "div3_wins":List['shipData'][0]['pvpThreeInfo']['wins'],
            "div3_pr":f"{List['shipData'][0]['pvpThreeInfo']['pr']['value']} {List['shipData'][0]['pvpThreeInfo']['pr']['name']}",
            "div3_xp":List['shipData'][0]['pvpThreeInfo']['xp'],
            "div3_damage":List['shipData'][0]['pvpThreeInfo']['damage'],
            "div3_kd":List['shipData'][0]['pvpThreeInfo']['kd'],
            "div3_hit":f"{List['shipData'][0]['pvpThreeInfo']['hit']:.2f}",
            "div3_frags":f"{List['shipData'][0]['pvpThreeInfo']['frags']:.2f}",
            "rank_battles":List['shipData'][0]['rankInfo']['battles'],
            "rank_wins":List['shipData'][0]['rankInfo']['wins'],
            "rank_pr":f"{List['shipData'][0]['rankInfo']['pr']['value']} {List['shipData'][0]['rankInfo']['pr']['name']}",
            "rank_xp":List['shipData'][0]['rankInfo']['xp'],
            "rank_damage":List['shipData'][0]['rankInfo']['damage'],
            "rank_kd":List['shipData'][0]['rankInfo']['kd'],
            "rank_hit":f"{List['shipData'][0]['rankInfo']['hit']:.2f}",
            "rank_frags":f"{List['shipData'][0]['rankInfo']['frags']:.2f}",
            "InfoRecent_RandomData":InfoRecent_RandomData,
            "InfoRecent_RankData":InfoRecent_RankData,
            "prValueColor":List['shipData'][0]['pvpInfo']['pr']['color'],
            "solo_prColor":List['shipData'][0]['pvpSoloInfo']['pr']['color'],
            "div2_prColor":List['shipData'][0]['pvpTwoInfo']['pr']['color'],
            "div3_prColor":List['shipData'][0]['pvpThreeInfo']['pr']['color'],
            "rank_prColor":List['shipData'][0]['rankInfo']['pr']['color'],
            "clanColor":List['clanInfo']['colorRgb'],
            "winsColor":winsColor,
            "damageColor":damageColor,
            "solo_winsColor":solo_winsColor,
            "solo_damageColor":solo_damageColor,
            "div2_winsColor":div2_winsColor,
            "div2_damageColor":div2_damageColor,
            "div3_winsColor":div3_winsColor,
            "div3_damageColor":div3_damageColor,
            "rank_winsColor":rank_winsColor,
            "rank_damageColor":rank_damageColor
        }
        return result
    except Exception:
        traceback.print_exc()
        
async def set_shipparams(List):
    try:   
        damageTopColor = await set_upinfo_color(List['dwpDataVO']['damage'])
        winsTopColor = await set_upinfo_color(List['dwpDataVO']['wins'])
        prTopColor = await set_upinfo_color(List['dwpDataVO']['pr'])
        winsColor = await set_winColor(List['shipInfo']['wins'])
        damageColor = await set_damageColor(List['shipInfo']['shipInfo']['shipType'],List['shipInfo']['damage'])
        solo_winsColor = await set_winColor(List['shipSolo']['wins'])
        solo_damageColor = await set_damageColor(List['shipInfo']['shipInfo']['shipType'],List['shipSolo']['damage'])
        div2_winsColor = await set_winColor(List['shipTwo']['wins'])
        div2_damageColor = await set_damageColor(List['shipInfo']['shipInfo']['shipType'],List['shipTwo']['damage'])
        div3_winsColor = await set_winColor(List['shipThree']['wins'])
        div3_damageColor = await set_damageColor(List['shipInfo']['shipInfo']['shipType'],List['shipThree']['damage'])
        rank_winsColor = await set_winColor(List['rankSolo']['wins'])
        rank_damageColor = await set_damageColor(List['shipInfo']['shipInfo']['shipType'],List['rankSolo']['damage'])
        if List['shipInfo']['shipInfo']['nameEnglish']:
            shipNameEn = List['shipInfo']['shipInfo']['nameEnglish']
            shipNameCn = List['shipInfo']['shipInfo']['nameCn']
        else:
            shipNameEn = List['rankSolo']['shipInfo']['nameEnglish']
            shipNameCn = List['rankSolo']['shipInfo']['nameEnglish']
        result = {
            "guild":List['clanInfo']['tag'],
            "userName":List['userName'],
            "serverName":List['serverName'],
            "shipNameEn":shipNameEn,
            "shipNameCn":shipNameCn,
            "damageTop":f"{List['dwpDataVO']['damage']:+}",
            "winsTop":f"{List['dwpDataVO']['wins']:+.2f}",
            "prTop":f"{List['dwpDataVO']['pr']:+}",
            "prValue":f"{List['shipInfo']['pr']['value']} {List['shipInfo']['pr']['name']}",
            "lastTime":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(abs(List['shipInfo']['lastBattlesTime']))),
            "battles":List['shipInfo']['battles'],
            "wins":List['shipInfo']['wins'],
            "damage":List['shipInfo']['damage'],
            "xp":List['shipInfo']['xp'],
            "kda":List['shipInfo']['kd'],
            "hit":List['shipInfo']['hit'],
            "frags":f"{List['shipInfo']['frags']:.2f}",
            "solo_battles":List['shipSolo']['battles'],
            "solo_wins":List['shipSolo']['wins'],
            "solo_pr":List['shipSolo']['pr']['value'],
            "solo_xp":List['shipSolo']['xp'],
            "solo_damage":List['shipSolo']['damage'],
            "solo_kd":List['shipSolo']['kd'],
            "solo_hit":List['shipSolo']['hit'],
            "solo_frags":f"{List['shipSolo']['frags']:.2f}",
            "div2_battles":List['shipTwo']['battles'],
            "div2_wins":List['shipTwo']['wins'],
            "div2_pr":List['shipTwo']['pr']['value'],
            "div2_xp":List['shipTwo']['xp'],
            "div2_damage":List['shipTwo']['damage'],
            "div2_kd":List['shipTwo']['kd'],
            "div2_hit":List['shipTwo']['hit'],
            "div2_frags":f"{List['shipTwo']['frags']:.2f}",
            "div3_battles":List['shipThree']['battles'],
            "div3_wins":List['shipThree']['wins'],
            "div3_pr":List['shipThree']['pr']['value'],
            "div3_xp":List['shipThree']['xp'],
            "div3_damage":List['shipThree']['damage'],
            "div3_kd":List['shipThree']['kd'],
            "div3_hit":List['shipThree']['hit'],
            "div3_frags":f"{List['shipThree']['frags']:.2f}",
            "rank_battles":List['rankSolo']['battles'],
            "rank_wins":List['rankSolo']['wins'],
            "rank_pr":List['rankSolo']['pr']['value'],
            "rank_xp":List['rankSolo']['xp'],
            "rank_damage":List['rankSolo']['damage'],
            "rank_kd":List['rankSolo']['kd'],
            "rank_hit":List['rankSolo']['hit'],
            "rank_frags":f"{List['rankSolo']['frags']:.2f}",
            "maxDamage":List['shipInfo']['extensionDataInfo']['maxDamage'],
            "maxDamageScouting":List['shipInfo']['extensionDataInfo']['maxDamageScouting'],
            "maxTotalAgro":List['shipInfo']['extensionDataInfo']['maxTotalAgro'],
            "maxXp":List['shipInfo']['extensionDataInfo']['maxXp'],
            "maxFragsBattle":List['shipInfo']['extensionDataInfo']['maxFrags'],
            "maxPlanesKilled":List['shipInfo']['extensionDataInfo']['maxPlanesKilled'],
            "prColor":List['shipInfo']['pr']['color'],
            "solo_prColor":List['shipSolo']['pr']['color'],
            "div2_prColor":List['shipTwo']['pr']['color'],
            "div3_prColor":List['shipThree']['pr']['color'],
            "rank_prColor":List['rankSolo']['pr']['color'],
            "clanColor":List['clanInfo']['colorRgb'],
            "damageTopColor":damageTopColor,
            "winsTopColor":winsTopColor,
            "prTopColor":prTopColor,
            "winsColor":winsColor,
            "damageColor":damageColor,
            "solo_winsColor":solo_winsColor,
            "solo_damageColor":solo_damageColor,
            "div2_winsColor":div2_winsColor,
            "div2_damageColor":div2_damageColor,
            "div3_winsColor":div3_winsColor,
            "div3_damageColor":div3_damageColor,
            "rank_winsColor":rank_winsColor,
            "rank_damageColor":rank_damageColor
        }
        return result
    except Exception:
        traceback.print_exc()

async def set_shipRecentparams(List):
    try:   
        damageColor = await set_damageColor(List['shipData'][0]['shipInfo']['shipInfo']['shipType'],List['pvpInfo']['damage'])
        solo_winsColor = await set_winColor(List['pvpSoloInfo']['wins'])
        solo_damageColor = await set_damageColor(List['shipData'][0]['shipInfo']['shipInfo']['shipType'],List['pvpSoloInfo']['damage'])
        div2_winsColor = await set_winColor(List['pvpTwoInfo']['wins'])
        div2_damageColor = await set_damageColor(List['shipData'][0]['shipInfo']['shipInfo']['shipType'],List['pvpTwoInfo']['damage'])
        div3_winsColor = await set_winColor(List['pvpThreeInfo']['wins'])
        div3_damageColor = await set_damageColor(List['shipData'][0]['shipInfo']['shipInfo']['shipType'],List['pvpThreeInfo']['damage'])
        rank_winsColor = await set_winColor(List['rankInfo']['wins'])
        rank_damageColor = await set_damageColor(List['shipData'][0]['shipInfo']['shipInfo']['shipType'],List['rankInfo']['damage'])
        detail_data = await set_ShipRecent_Data(List['shipData'])
        if List['shipData'][0]['shipInfo']['shipInfo']['nameEnglish']:
            shipNameEn = List['shipData'][0]['shipInfo']['shipInfo']['nameEnglish']
            shipNameCn = List['shipData'][0]['shipInfo']['shipInfo']['nameCn']
        else:
            shipNameEn = List['shipData'][0]['rankSolo']['shipInfo']['nameEnglish']
            shipNameCn = List['shipData'][0]['rankSolo']['shipInfo']['nameCn']
        result = {
            "guild":List['clanInfo']['tag'],
            "userName":List['userName'],
            "serverName":List['serverName'],
            "shipNameEn":shipNameEn,
            "shipNameCn":shipNameCn,
            "prValue":f"{List['pvpInfo']['pr']['value']} {List['pvpInfo']['pr']['name']}",
            "recordTime":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(abs(List['shipData'][0]['recordDateTime']/1000)))),
            "battles":List['pvpInfo']['battles'],
            "wins":List['pvpInfo']['wins'],
            "damage":List['pvpInfo']['damage'],
            "xp":List['pvpInfo']['xp'],
            "kda":List['pvpInfo']['kd'],
            "hit":List['pvpInfo']['hit'],
            "frags":f"{List['pvpInfo']['frags']:.2f}",
            "solo_battles":List['pvpSoloInfo']['battles'],
            "solo_wins":List['pvpSoloInfo']['wins'],
            "solo_pr":List['pvpSoloInfo']['pr']['value'],
            "solo_xp":List['pvpSoloInfo']['xp'],
            "solo_damage":List['pvpSoloInfo']['damage'],
            "solo_kd":List['pvpSoloInfo']['kd'],
            "solo_hit":List['pvpSoloInfo']['hit'],
            "solo_frags":f"{List['pvpSoloInfo']['frags']:.2f}",
            "div2_battles":List['pvpTwoInfo']['battles'],
            "div2_wins":List['pvpTwoInfo']['wins'],
            "div2_pr":List['pvpTwoInfo']['pr']['value'],
            "div2_xp":List['pvpTwoInfo']['xp'],
            "div2_damage":List['pvpTwoInfo']['damage'],
            "div2_kd":List['pvpTwoInfo']['kd'],
            "div2_hit":List['pvpTwoInfo']['hit'],
            "div2_frags":f"{List['pvpTwoInfo']['frags']:.2f}",
            "div3_battles":List['pvpThreeInfo']['battles'],
            "div3_wins":List['pvpThreeInfo']['wins'],
            "div3_pr":List['pvpThreeInfo']['pr']['value'],
            "div3_xp":List['pvpThreeInfo']['xp'],
            "div3_damage":List['pvpThreeInfo']['damage'],
            "div3_kd":List['pvpThreeInfo']['kd'],
            "div3_hit":List['pvpThreeInfo']['hit'],
            "div3_frags":f"{List['pvpThreeInfo']['frags']:.2f}",
            "rank_battles":List['rankInfo']['battles'],
            "rank_wins":List['rankInfo']['wins'],
            "rank_pr":List['rankInfo']['pr']['value'],
            "rank_xp":List['rankInfo']['xp'],
            "rank_damage":List['rankInfo']['damage'],
            "rank_kd":List['rankInfo']['kd'],
            "rank_hit":List['rankInfo']['hit'],
            "rank_frags":f"{List['rankInfo']['frags']:.2f}",
            "detail_data":detail_data,
            "prColor":List['pvpInfo']['pr']['color'],
            "solo_prColor":List['pvpSoloInfo']['pr']['color'],
            "div2_prColor":List['pvpTwoInfo']['pr']['color'],
            "div3_prColor":List['pvpThreeInfo']['pr']['color'],
            "rank_prColor":List['rankInfo']['pr']['color'],
            "clanColor":List['clanInfo']['colorRgb'],
            "damageColor":damageColor,
            "solo_winsColor":solo_winsColor,
            "solo_damageColor":solo_damageColor,
            "div2_winsColor":div2_winsColor,
            "div2_damageColor":div2_damageColor,
            "div3_winsColor":div3_winsColor,
            "div3_damageColor":div3_damageColor,
            "rank_winsColor":rank_winsColor,
            "rank_damageColor":rank_damageColor
        }
        return result
    except Exception:
        traceback.print_exc()
        
async def set_ShipRecent_Data(List):
   Recent_Data = ''
   typeList = ['单野','自行车','三轮车','排位']
   for eachShipData in List:
       data = time.strftime('%Y-%m-%d',time.localtime(int(abs(eachShipData['recordDateTime']/1000))))
       if eachShipData['shipInfo']['battles'] or eachShipData['rankSolo']['battles']:
           Recent_Data += f'''<tr><td colspan="6" class="bold-data greyColor" style="text-align: center;">{data}</td></tr>'''
           for each in eachShipData:
               for index,value in enumerate(['shipSolo','shipTwo','shipThree','rankSolo']):
                   if str(each) == value and eachShipData[each]['battles']:
                       type = typeList[index]
                       Recent_Data += f'''
                       <tr>
                           <td class="bold-data greyColor">{type}</td>
                           <td class="blueColor">{eachShipData[each]['battles']}</td>
                           <td class="blueColor" style="color: {await set_winColor(eachShipData[each]['wins'])}">{eachShipData[each]['wins']}%</td>
                           <td class="blueColor" style="color: {eachShipData[each]['pr']['color']}">{eachShipData[each]['pr']['value']}</td>
                           <td class="blueColor" style="color: {await set_damageColor(eachShipData['shipInfo']['shipInfo']['shipType'],eachShipData[each]['damage'])}">{eachShipData[each]['damage']}</td>
                           <td class="blueColor">{eachShipData[each]['frags']:.2f}</td>
                       </tr>'''
                   else:
                       continue
   return Recent_Data


                 
async def select_prvalue_and_color(pr:int):
    for select in pr_select :
        if pr > select['value']:
            describe = select['name']
            color = select['color']
    return describe,color

async def set_InfoRecent_RandomData(List):
    Recent_RandomData = ''
    for ship in List['shipData']:
        if ship['shipInfo']['battles']:
            Recent_RandomData += r'<tr>'
            Recent_RandomData += r'<td colspan="8" class="blueColor">'+f"{ship['shipInfo']['shipInfo']['nameCn']}"+r'</td>'
            Recent_RandomData += r'<td colspan="3" class="blueColor">'+f"{ship['shipInfo']['shipInfo']['level']}"+r'</td>'
            Recent_RandomData += r'<td colspan="3" class="blueColor">'+f"{ship['shipInfo']['battles']}"+r'</td>'
            #Recent_RandomData += f'''<td colspan="7" class="blueColor" style="color: {ship['shipInfo']['pr']['color']}">{ship['shipInfo']['pr']['value']} {ship['shipInfo']['pr']['name']}</td>'''
            Recent_RandomData += f'''<td colspan="4" class="blueColor" style="color: {ship['shipInfo']['pr']['color']}">{ship['shipInfo']['pr']['value']}</td>'''
            Recent_RandomData += r'<td colspan="4" class="blueColor">'+f"{ship['shipInfo']['xp']}"+r'</td>'
            Recent_RandomData += f'''<td class="blueColor" colspan="5" style="color: {await set_winColor(ship['shipInfo']['wins'])}">{ship['shipInfo']['wins']}%</td>'''
            Recent_RandomData += f'''<td colspan="4" class="blueColor" style="color: {await set_damageColor(ship['shipInfo']['shipInfo']['shipType'],ship['shipInfo']['damage'])}">{ship['shipInfo']['damage']}</td>'''
            Recent_RandomData += r'<td colspan="4" class="blueColor">'+f"{ship['shipInfo']['frags']:.2f}"+r'</td>'
            Recent_RandomData += r'<td colspan="4" class="blueColor">'+f"{ship['shipInfo']['hit']:.2f}%"+r'</td>'
            Recent_RandomData += r'</tr>'
    return Recent_RandomData

async def set_InfoRecent_RankData(List):
    Recent_RankData = ''
    for ship in List['shipData']:
        if ship['rankSolo']['battles']:
            Recent_RankData += r'<tr>'
            Recent_RankData += r'<td colspan="8" class="blueColor">'+f"{ship['rankSolo']['shipInfo']['nameCn']}"+r'</td>'
            Recent_RankData += r'<td colspan="3" class="blueColor">'+f"{ship['rankSolo']['shipInfo']['level']}"+r'</td>'
            Recent_RankData += r'<td colspan="3" class="blueColor">'+f"{ship['rankSolo']['battles']}"+r'</td>'
            #Recent_RankData += f'''<td colspan="7" class="blueColor" style="color: {ship['rankSolo']['pr']['color']}">{ship['rankSolo']['pr']['value']} {ship['rankSolo']['pr']['name']}</td>'''
            Recent_RankData += f'''<td colspan="4" class="blueColor" style="color: {ship['rankSolo']['pr']['color']}">{ship['rankSolo']['pr']['value']}</td>'''
            Recent_RankData += r'<td colspan="4" class="blueColor">'+f"{ship['rankSolo']['xp']}"+r'</td>'
            Recent_RankData += f'''<td class="blueColor" colspan="5" style="color: {await set_winColor(ship['rankSolo']['wins'])}">{ship['rankSolo']['wins']}%</td>'''
            Recent_RankData += f'''<td colspan="4" class="blueColor" style="color: {await set_damageColor(ship['rankSolo']['shipInfo']['shipType'],ship['rankSolo']['damage'])}">{ship['rankSolo']['damage']}</td>'''
            Recent_RankData += r'<td colspan="4" class="blueColor">'+f"{ship['rankSolo']['frags']:.2f}"+r'</td>'
            Recent_RankData += r'<td colspan="4" class="blueColor">'+f"{ship['rankSolo']['hit']:.2f}%"+r'</td>'
            Recent_RankData += r'</tr>'
    return Recent_RankData

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