import tgbot_client
import asyncio


asyncio.run(tgbot_client.init())

tgbot_client.load("tgbot_client.startup")

if __name__ == "__main__":
    tgbot_client.run()
