from nonebot_plugin_htmlrender import html_to_pic

async def match_keywords(match_list,Lists):
    for List in Lists :                        
        for kw in List.keywords:
            for match_kw in match_list:
                if match_kw == kw or match_kw.upper() == kw.upper() or match_kw.lower() == kw.lower():
                    match_list.remove(match_kw)
                    return List.match_keywords,match_list
    return None,match_list

async def find_and_replace_keywords(match_list,Lists):
    for List in Lists :                        
        for kw in List.keywords:
            for i,match_kw in enumerate(match_list):
                if (match_kw.find(kw)+1):
                    match_list[i] = str(match_kw).replace(kw,"")
                    if match_list[i] == '':
                        match_list.remove('')
                    return List.match_keywords,match_list
    return None,match_list

