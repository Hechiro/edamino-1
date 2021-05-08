# betaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa, ok?
import asyncio
import base64
import logging
from time import time
from typing import BinaryIO

import aiohttp
import ujson

from ._exceptions import check_exception
from ._objects import Login, Event, GetFromCode, UserProfile, Thread
from ._utils import get_device, parse_headers, com


class Bot(object):
    """Library copied from Slima"""

    def __init__(self, com_id, email: str, password: str):
        self.__session = aiohttp.ClientSession()
        self.me = None
        self.socket = None
        self.com_id = com_id
        self.device_id = get_device()
        self.handlers = []

        self.ws_link = "wss://ws1.narvii.com"
        self.api = "https://service.narvii.com/api/v1"
        asyncio.ensure_future(self.login(email=email, password=password))

    async def start(self):
        headers = {
            "NDCDEVICEID": self.device_id,
            "NDCAUTH": f"sid={self.me.sid}"
        }
        while True:
            # what did you want to see the magic here?))) no, everything is done on the knee :)
            # himself shocked who it works
            # use google translate 2021
            async with self.__session.ws_connect(
                    url=f"{self.ws_link}/?signbody={self.device_id}%7{time() * 1000}",
                    headers=headers
            ) as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        if msg.data == 'close cmd':
                            await ws.close()
                            break
                        else:
                            await self.call(ujson.loads(msg.data))
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break

            logging.debug("reconnect web-socket")

    async def call(self, data):
        if data["t"] == 1000:
            await asyncio.gather(*[asyncio.create_task(handler(Event(
                message=data["o"]["chatMessage"],
                membershipStatus=data["o"]["membershipStatus"],
                ndcId=data["o"]["ndcId"],
                alertOption=data["o"]["alertOption"]
            ))) for handler in self.handlers])

    def event(self, handler):
        self.handlers.append(handler)

    async def close(self):
        await self.__session.close()
        logging.debug("session closed")

    async def login(self, email: str, password: str):
        """
        :param email: email
        :param password: password
        """
        data = ujson.dumps({
            "email": email,
            "v": 2,
            "secret": f"0 {password}",
            "deviceID": self.device_id,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(time() * 1000)
        })
        async with self.__session.post(url=f"{self.api}/g/s/auth/login", data=data, headers=parse_headers()) as resp:
            if resp.status == 200:
                logging.debug("login successful")
                response = await resp.json()
                self.me = Login(
                    profile=response["userProfile"],
                    account=response["account"],
                    api_duration=response['api:duration'],
                    api_message=response['api:message'],
                    api_status_code=response["api:statuscode"],
                    api_timestamp=response['api:timestamp'],
                    user_id=response["auid"],
                    secret=response['secret'],
                    sid=response['sid']
                )
                await self.get_community_info()
                asyncio.ensure_future(self.start())
                return self.me
            else:
                return check_exception(await resp.json())

    async def get_community_info(self):
        async with self.__session.get(
                url=f"{self.api}/g/s-x{self.com_id}/community/info?withInfluencerList=1&withTopicList=true",
                headers=parse_headers(sid=self.me.sid)) as resp:
            if resp.status == 200:
                return await resp.json()

            else:
                return await check_exception(await resp.json())

    async def send_message(
            self, chat_id: str, message: str = None, message_type: int = 0, ref_id: int = None,
            community: bool = True, reply: str = None, mentions: list = None
    ) -> int:
        if ref_id is None:
            ref_id = int(time() / 10 % 1000000000)

        if mentions:
            mentions = [{"uid": mention} for mention in mentions]

        data = {
            "type": message_type,
            "content": message.replace("<$", "‎‏").replace("$>", "‬‭"),
            "clientRefId": ref_id,
            "attachedObject": None,
            "timestamp": int(time() * 1000),
            "extensions": {"mentionedArray": mentions}
        }
        if reply:
            data["replyMessageId"] = reply

        data = ujson.dumps(data)
        async with self.__session.post(
                url=f"{self.api}//{com(self.com_id, community)}/s/chat/thread/{chat_id}/message",
                headers=parse_headers(data=data, sid=self.me.sid), data=data
        ) as resp:
            if resp.status != 200:
                return check_exception(await resp.json())
            else:
                return resp.status

    async def send_image(self, chat_id: str, image: BinaryIO, community: bool = True) -> int:
        data = ujson.dumps({
            "type": 0,
            "content": None,
            "clientRefId": int(time() / 10 % 1000000000),
            "attachedObject": None,
            "mediaType": 100,
            "mediaUploadValue": base64.b64encode(image.read()).decode(),
            "mediaUhqEnabled": False,
            "mediaUploadValueContentType": "image/jpg"
        })
        async with self.__session.post(
                url=f"{self.api}/{com(self.com_id, community)}/s/chat/thread/{chat_id}/message",
                headers=parse_headers(data=data, sid=self.me.sid), data=data
        ) as resp:
            if resp.status != 200:
                return check_exception(await resp.json())
            else:
                return resp.status

    async def join_chat(self, chat_id, community: bool = True):
        async with self.__session.post(
                url=f"{self.api}/{com(self.com_id, community)}/s/chat/thread/{chat_id}/member/{self.me.account.uid}",
                headers=parse_headers(uid=self.me.account.uid, sid=self.me.sid)) as resp:
            if resp.status != 200:
                return check_exception(await resp.json())
            else:
                return resp.status

    async def leave_chat(self, chat_id, community: bool = True):
        async with self.__session.delete(
                url=f"{self.api}/{com(self.com_id, community)}/s/chat/thread/{chat_id}/member/{self.me.account.uid}",
                headers=parse_headers(uid=self.me.account.uid, sid=self.me.sid)
        ) as resp:
            if resp.status != 200:
                return check_exception(await resp.json())
            else:
                return resp.status

    async def get_from_code(self, code: str):
        # made by Oksys Dola#5909
        async with self.__session.get(
                url=f"{self.api}/g/s/link-resolution?q={code}",
                headers=parse_headers(sid=self.me.sid)) as resp:
            if resp.status == 200:
                res = await resp.json()
                try:
                    res = res['linkInfoV2']["extensions"]["linkInfo"]
                except Exception as e:
                    logging.debug(e)
                    res = res['linkInfoV2']["extensions"]["community"]
                return GetFromCode.parse_raw(ujson.dumps(res))
            else:
                return check_exception(await resp.json())

    async def get_user_info(self, user_id, community: bool = True):
        async with self.__session.get(
                url=f"{self.api}/{com(self.com_id, community)}/s/user-profile/{user_id}",
                headers=parse_headers(sid=self.me.sid)
        ) as resp:
            if resp.status != 200:
                return check_exception(await resp.json())
            else:
                response = await resp.json()
                return UserProfile.parse_raw(ujson.dumps(response['userProfile']))

    async def get_from_id(self, object_id: str, object_type: int, com_id: str = None):
        # made by Oksys Dola#5909
        data = ujson.dumps({
            "objectId": object_id,
            "targetCode": 1,
            "objectType": object_type,
            "timestamp": int(time() * 1000)
        })

        if com_id:
            async with self.__session.post(
                    url=f"{self.api}/g/s-x{com_id}/link-resolution", headers=parse_headers(sid=self.me.sid, data=data),
                    data=data
            ) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    return GetFromCode.parse_raw(ujson.dumps(res['linkInfoV2']['extensions']['linkInfo']))
                else:
                    return check_exception(await resp.json())
        else:
            async with self.__session.post(
                    url=f"{self.api}/g/s/link-resolution", headers=parse_headers(data=data, sid=self.me.sid), data=data
            ) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    return GetFromCode.parse_raw(ujson.dumps(res['linkInfoV2']['extensions']['linkInfo']))
                else:
                    return check_exception(await resp.json())

    async def join_community(self, com_id):
        data = ujson.dumps({"timestamp": int(time() * 1000)})
        async with self.__session.post(
                url=f"{self.api}/x{com_id}/s/community/membership-request", data=data,
                headers=parse_headers(sid=self.me.sid, data=data)
        ) as resp:
            if resp.status != 200:
                return check_exception(await resp.json())
            else:
                return resp.status

    async def leave_community(self, com_id):
        async with self.__session.post(
                url=f"{self.api}/x{com_id}/s/community/leave", headers=parse_headers(sid=self.me.sid)
        ) as resp:
            if resp.status != 200:
                return check_exception(await resp.json())
            else:
                return resp.status

    async def get_chat_threads(self, start: int = 0, size: int = 25, community: bool = True):
        assert size < 100, "Max size 100"
        async with self.__session.get(
            url=f"{self.api}/{com(self.com_id, community)}/s/chat/thread?type=joined-me&start={start}&size={size}",
            headers=parse_headers(sid=self.me.sid)
        ) as resp:
            if resp.status != 200:
                return check_exception(await resp.json())
            else:
                res = await resp.json()

                return [Thread.parse_raw(ujson.dumps(thread)) for thread in res['threadList']]

    async def get_chat_info(self):
        pass
