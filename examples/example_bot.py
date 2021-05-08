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
