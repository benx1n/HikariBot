import json
import time
import traceback
from base64 import b64decode, b64encode
from pathlib import Path

import httpx
from nonebot import get_driver
from nonebot.log import logger

config = get_driver().config
ocr_url = config.ocr_url
dir_path = Path(__file__).parent.parent
game_path = Path(__file__).parent
ocr_data_path = game_path / "ocr_data.json"
upload_url = "https://api.wows.shinoaki.com/api/wows/cache/image/ocr"
download_url = "https://api.wows.shinoaki.com/api/wows/cache/image/ocr"

headers = {"Authorization": config.api_token}


async def pic2txt_byOCR(img_path, filename):
    try:
        global ocr_filename_data
        if filename in ocr_filename_data:
            logger.success(f"filename匹配，跳过OCR:{filename}")
            return b64decode(ocr_filename_data[filename]).decode("utf-8")
        if config.ocr_offline:
            return ""
        async with httpx.AsyncClient() as client:
            # logger.success(f"图片地址{img_path}")
            # resp = await client.get(img_path)
            # img_base64 = str(b64encode(resp.content),encoding='utf-8')
            start = time.time()
            # params = {
            #    "image":img_base64
            # }
            params = {"url": img_path}
            resp = await client.post(
                ocr_url, data=params, timeout=5, follow_redirects=True
            )
        end = time.time()
        logger.success(f"OCR结果：{resp.text},耗时{end-start:.4f}s\n图片url:{img_path}")
        return resp.text
    except:
        logger.error(traceback.format_exc())
        return ""


async def upload_OcrResult(result_text, filename):
    try:
        params = {
            "md5": filename,
            "text": b64encode(result_text.encode("utf-8")).decode("utf-8"),
        }
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.post(upload_url, json=params)
            result = resp.json()
        if result["code"] == 200:
            await downlod_OcrResult()
    except:
        logger.error(traceback.format_exc())


async def downlod_OcrResult():
    try:
        global ocr_filename_data
        async with httpx.AsyncClient(headers=headers, timeout=None) as client:
            resp = await client.get(download_url)
            result = resp.json()
            with open(ocr_data_path, "w", encoding="UTF-8") as f:
                if result["code"] == 200 and result["data"]:
                    json.dump(result["data"], f)
                    ocr_filename_data = result["data"]
                else:
                    ocr_filename_data = json.load(
                        open(ocr_data_path, "r", encoding="utf8")
                    )
        return
    except:
        logger.error("请检查token是否配置正确，如无问题请尝试重启，可能是网络波动或服务器原因")
        logger.error(traceback.format_exc())
        try:
            ocr_filename_data = json.load(open(ocr_data_path, "r", encoding="utf8"))
        except:
            ocr_filename_data = None


async def get_Random_Ocr_Pic(server_type, info, bot, ev):
    try:
        async with httpx.AsyncClient(headers=headers, timeout=None) as client:
            resp = await client.post('http://mc.youthnp.cn:23338/ImageRandom/')
            img = b64decode(resp.text)
        return img
    except:
        logger.error(traceback.format_exc())  
        return 'OCR服务器出了点问题，请稍后再试哦' 
        