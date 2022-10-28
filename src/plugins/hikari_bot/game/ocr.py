import time
import httpx
import traceback
from base64 import b64encode
from nonebot import get_driver
from nonebot.log import logger

ocr_url = get_driver().config.ocr_url

async def pic2txt_byOCR(img_path):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(img_path)
            img_base64 = str(b64encode(resp.content),encoding='utf-8')
            start = time.time()
            params = {
                "image":img_base64
            }
            resp = await client.post(ocr_url, data=params, timeout=5,follow_redirects=True)
        end = time.time()
        logger.success(f"OCR结果：{resp.text},耗时{end-start:.4f}s\n图片url:{img_path}")
        return resp.text
    except:
        logger.error(traceback.format_exc())
        return ''
    
async def upload_OcrResult(img_path):
    try:
        url = 
        async with httpx.AsyncClient() as client:
            resp = await client.get(img_path)
            img_base64 = str(b64encode(resp.content),encoding='utf-8')
            start = time.time()
            url = 'http://mc.youthnp.cn:23338/OCR/'
            params = {
                "image":img_base64
            }
            resp = await client.post(url, data=params, timeout=5,follow_redirects=True)
        end = time.time()
        logger.success(f"OCR结果：{resp.text},耗时{end-start:.4f}s\n图片url:{url}")
        return resp.text
    except:
        logger.error(traceback.format_exc())
        return ''