import httpx
import traceback
from pathlib import Path
from nonebot.log import logger
from httpx import ConnectTimeout
from asyncio.exceptions import TimeoutError

dir_path = Path(__file__).parent

  
async def get_pupu_msg():
    try:
        url = 'https://v1.hitokoto.cn'
        params = {
    }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=5)
            result = resp.json()
        if resp.status_code == 200:
            return result['hitokoto']
        else:
            return '噗噗出问题了>_<'
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
    except Exception:
        logger.error(traceback.format_exc())
        return '噗噗出问题了>_<'
    