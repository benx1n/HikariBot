from dataclasses import dataclass
from typing import Protocol, Tuple

from .game.ban_search import get_BanInfo
from .game.box_check import check_christmas_box
from .game.ocr import get_Random_Ocr_Pic
from .game.roll import roll_ship
from .game.sx import get_sx_info
from .moudle.publicAPI import get_ship_name
from .moudle.wws_bind import (
    change_BindInfo,
    delete_BindInfo,
    get_BindInfo,
    set_BindInfo,
    set_special_BindInfo,
)
from .moudle.wws_clan import get_ClanInfo
from .moudle.wws_info import get_AccountInfo
from .moudle.wws_recent import get_RecentInfo
from .moudle.wws_record import get_record
from .moudle.wws_ship import get_ShipInfo, get_ShipInfoRecent
from .moudle.wws_shiprank import get_ShipRank


class Func(Protocol):
    async def __call__(self, **kwargs):
        ...


@dataclass
class command:
    keywords: Tuple[str, ...]
    func: Func
    default_func: Func = None


first_command_list = [  # 同指令中越长的匹配词越靠前
    command(("切换绑定", "更换绑定", "更改绑定"), change_BindInfo),
    command(("查询绑定", "绑定查询", "绑定列表", "查绑定"), get_BindInfo),
    command(("删除绑定",), delete_BindInfo),
    command(("特殊绑定",), set_special_BindInfo),
    command(("ship.rank", "rank"), get_ShipRank),
    command(("bind", "绑定", "set"), set_BindInfo),
    command(("recent","近期",),None,get_RecentInfo,),
    command(("ship","单船",),None,get_ShipInfo,),
    command(("record", "历史记录"), None, get_record),
    command(("clan", "军团", "公会", "工会"), None, get_ClanInfo),
    command(("随机表情包",), get_Random_Ocr_Pic),
    command(("roll", "随机"), roll_ship),
    command(("sx", "扫雪"), get_sx_info),
    command(("ban","封号记录"),get_BanInfo),
    command(("box", "sd", "圣诞船池"), check_christmas_box),
    command(("搜船名", "查船名", "船名"), get_ship_name),
]

second_command_list = [
    command(("recent","近期",),get_ShipInfoRecent,),
    command(("ship","单船",),get_ShipInfoRecent,),
    command(("clan", "军团", "公会", "工会"), get_record),
    command(("record", "历史记录"), get_record),
]


async def findFunction_and_replaceKeywords(match_list, command_List, default_func):
    for com in command_List:
        for kw in com.keywords:
            for i, match_kw in enumerate(match_list):
                if match_kw.find(kw) + 1:
                    match_list[i] = str(match_kw).replace(kw, "")
                    if match_list[i] == "":  # 为空时才删除，防止未加空格没有被split切割
                        match_list.remove("")
                    return com, match_list
    return command(None, default_func, None), match_list


async def select_command(search_list):
    command, search_list = await findFunction_and_replaceKeywords(
        search_list, first_command_list, get_AccountInfo
    )
    if command.func == None:
        command, search_list = await findFunction_and_replaceKeywords(
            search_list, second_command_list, command.default_func
        )
    return command.func, search_list
