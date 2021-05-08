import asyncio
import logging
import edamino

logging.basicConfig(level=logging.DEBUG)


async def main():
    async with edamino.Client(com_id="com_id") as client:
        await client.login(email="email", password="password")
        await client.send_message(chat_id="chat_id", message="message")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
