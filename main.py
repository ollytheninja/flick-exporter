import asyncio
import logging
import os
from pprint import pprint
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Starting up with username {USERNAME}")


async def get_flick_pricing():
    async with ClientSession() as session:
        auth = SimpleFlickAuth(USERNAME, PASSWORD, session)

        api = FlickAPI(auth)

        return await api.get_pricing()


def set_power_price():
    answer = asyncio.run(get_flick_pricing())
    price = answer.price / 100
    wait_time = answer.end_at - answer.now
    logger.info(f"Current price ${price}")
    logger.info(f"Waititing for {wait_time} ({wait_time.seconds}s) to fetch new price")

    SPOT_PRICE.set(price)
    return wait_time.seconds + 30  # give it a little extra time (Flick is a little slow)


def main():
    # Start up the server to expose the metrics.
    prometheus_client.start_http_server(8000)
    while True:
        wait_time = set_power_price()
        sleep(wait_time)


if __name__ == '__main__':
    main()
