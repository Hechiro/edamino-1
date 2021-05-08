import json
import logging
from functools import wraps

import ujson


def get_device():
    try:
        with open("device.json", 'r', encoding="utf-8") as file:
            return ujson.load(file)["device_id"]
    except (FileNotFoundError, Exception):
        data = {"device_id": "011C08D4DE2ED187F76C2943EFFC1BAF9C84141246A86E31C62CFE19BC3B33CFF12EC21FE6B79318FE"}
        with open("device.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return data["device_id"]


DEVICE_ID = get_device()


def parse_headers(data: str = None, sid: str = None, uid: str = None, content_type=None):
    headers = {
        "NDCDEVICEID": DEVICE_ID,
        "NDC-MSG-SIG": "Aa0ZDPOEgjt1EhyVYyZ5FgSZSqJt",
        "Accept-Language": "en-US",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; "
                      "SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)",
        "Host": "service.narvii.com",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }
    if sid:
        headers["NDCAUTH"] = f"sid={sid}"
    if data:
        headers["Content-Length"] = str(len(data))
    if uid:
        headers["AUID"] = uid
    if content_type:
        headers["Content-Type"] = content_type
    return headers


# not working
def auto_closing(session):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logging.error(e)
                await session.close()

        return wrapped

    return wrapper


def com(com_id: str, check: bool) -> str:
    if check:
        return f"x{com_id}"
    else:
        return "g"
