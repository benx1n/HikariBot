import time
import traceback
from base64 import b64decode, b64encode
from pathlib import Path

import orjson
from nonebot.log import logger

from ..data_source import config
from ..HttpClient_pool import client_default, client_yuyuko

ocr_url = config.ocr_url
dir_path = Path(__file__).parent.parent
game_path = Path(__file__).parent
ocr_data_path = game_path / "ocr_data.json"
upload_url = "https://api.wows.shinoaki.com/api/wows/cache/image/ocr"
download_url = "https://api.wows.shinoaki.com/api/wows/cache/image/ocr"

async def pic2txt_byOCR(img_path, filename):
    try:
        global ocr_filename_data
        if filename in ocr_filename_data:
            logger.success(f"filename匹配，跳过OCR:{filename}")
            return b64decode(ocr_filename_data[filename]).decode("utf-8")
        if config.ocr_offline:
            return ""
        start = time.time()
        params = {"url": img_path}
        resp = await client_default.post(
            f"{ocr_url}/OCR/", data=params, timeout=5, follow_redirects=True
        )
        end = time.time()
        result = orjson.loads(resp.content)
        if result['code'] == 200:
            logger.success(f"OCR结果：{result['data']['msg']},耗时{end-start:.4f}s\n图片url:{img_path}")
            return result['data']['msg']
    except:
        logger.error(traceback.format_exc())
        return ""


async def upload_OcrResult(result_text, filename):
    try:
        params = {
            "md5": filename,
            "text": b64encode(result_text.encode("utf-8")).decode("utf-8"),
        }
        resp = await client_yuyuko.post(upload_url, json=params)
        result = orjson.loads(resp.content)
        if result["code"] == 200:
            await downlod_OcrResult()
    except:
        logger.error(traceback.format_exc())


async def downlod_OcrResult():
    try:
        global ocr_filename_data
        resp = await client_yuyuko.get(download_url)
        result = orjson.loads(resp.content)
        with open(ocr_data_path, "w", encoding="UTF-8") as f:
            if result["code"] == 200 and result["data"]:
                f.write(orjson.dumps(result['data']).decode())
                ocr_filename_data = result["data"]
            else:
                with open(ocr_data_path, "rb") as f:    
                    ocr_filename_data = orjson.loads(f.read())
        return
    except:
        logger.error("请检查token是否配置正确，如无问题请尝试重启，可能是网络波动或服务器原因")
        logger.error(traceback.format_exc())
        try:
            with open(ocr_data_path, "rb") as f:    
                ocr_filename_data = orjson.loads(f.read())
        except:
            ocr_filename_data = None


async def get_Random_Ocr_Pic(server_type, info, bot, ev):
    try:
        resp = await client_default.post(f"{ocr_url}/ImageRandom/")
        img = b64decode(resp.text)
        return img
    except:
        logger.error(traceback.format_exc())  
        return 'OCR服务器出了点问题，请稍后再试哦' 
        