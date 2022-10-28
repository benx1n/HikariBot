import time
import httpx
import traceback
import json
from pathlib import Path
from base64 import b64encode,b64decode
from nonebot import get_driver
from nonebot.log import logger
from ..utils import byte2md5

config =  get_driver().config
ocr_url = config.ocr_url
dir_path = Path(__file__).parent.parent
game_path = Path(__file__).parent
ocr_data_path = game_path/ 'ocr_data.json'
upload_url = "https://api.wows.shinoaki.com/api/wows/cache/image/ocr"
download_url = "https://api.wows.shinoaki.com/api/wows/cache/image/ocr"

headers = {
    'Authorization': config.api_token
}

try:
    with open(ocr_data_path, 'w', encoding='UTF-8') as f:
        resp = httpx.get(download_url,headers=headers)
        result = resp.json()
        json.dump(result['data'], f)
    global ocr_md5_data
    ocr_md5_data = result['data']
except:
    logger.error(traceback.format_exc())
    

async def pic2txt_byOCR(img_path):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(img_path)
            img_base64 = str(b64encode(resp.content),encoding='utf-8')
            img_md5 = await byte2md5(resp.content)
            global ocr_md5_data
            for key in ocr_md5_data:
                if img_md5 == key:
                    logger.success(f"md5匹配，跳过OCR:{img_md5}")
                    return b64decode(ocr_md5_data[key]).decode('utf-8'),img_md5
            start = time.time()
            params = {
                "image":img_base64
            }
            resp = await client.post(ocr_url, data=params, timeout=10,follow_redirects=True)
        end = time.time()
        logger.success(f"OCR结果：{resp.text},耗时{end-start:.4f}s\n图片url:{img_path}")
        return resp.text,img_md5
    except:
        logger.error(traceback.format_exc())
        return '',''
    
async def upload_OcrResult(result_text,img_md5):
    try:
        params = {
            "md5": img_md5,
            "text": b64encode(result_text.encode('utf-8')).decode('utf-8')
        }
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.post(upload_url,json=params)
            result= resp.json()
        if result['code'] == 200:
            await downlod_OcrResult()
    except:
        logger.error(traceback.format_exc())
        
async def downlod_OcrResult():
    try:
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(download_url)
            result = resp.json()
            with open(ocr_data_path, 'w', encoding='UTF-8') as f:
                json.dump(result['data'], f)
            global ocr_md5_data
            ocr_md5_data = result['data']
        return
    except:
        logger.error(traceback.format_exc())
    