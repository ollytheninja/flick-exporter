import asyncio
import os
from time import sleep

import prometheus_client
from aiohttp import ClientSession
from dotenv import load_dotenv
from prometheus_client import Gauge
from pyflick import FlickAPI
from pyflick.authentication import SimpleFlickAuth

SPOT_PRICE = Gauge('flick_power_spot_price', "Spot price in $/KWh")

load_dotenv()  # take environment variables from .env.

USERNAME = os.getenv("FLICK_USERNAME")
PASSWORD = os.getenv("FLICK_PASSWORD")


async def get_flick_pricing():
    async with ClientSession() as session:
        auth = SimpleFlickAuth(USERNAME, PASSWORD, session)

        api = FlickAPI(auth)

        return await api.get_pricing()


def set_power_price():
    answer = asyncio.run(get_flick_pricing())
    price = answer.price / 100
    wait_time = answer.end_at - answer.now
    print(f"Current price ${price}")
    print(f"Waititing for {wait_time} to fetch new price")

    SPOT_PRICE.set(price)
    return wait_time.seconds


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    prometheus_client.start_http_server(8000)
    while True:
        wait_time = set_power_price()
        sleep(wait_time)
