# edamino


# Installation
To run the program, you need to install Python 3+ and all the requirements for the project are written in `requirements.txt` using the command `pip install -r requirements.txt` or in other ways

# Установка
Для запуска программы необходимо установить Python 3+ и все требования к проекту записанные в `requirements.txt` с помощью команды `pip install -r requirements.txt` или другими способами


#Example client
```py
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
```
#Example bot (Please do not use)
```py
import asyncio
import logging
import edamino
# не юзайте этот код, ок?
# нет, я серьёзно без понятия как закрыть эту сессию при ошибке
# лучше юзайте обычный Client тем более зачем вам бот
logging.basicConfig(level=logging.DEBUG)

bot = edamino.Bot(com_id="", email="", password="")


@bot.event
async def on_message(data):
    if data.message.content == "!ping":
        await bot.send_message(chat_id=data.message.threadId, message="Pong")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_forever()

```
