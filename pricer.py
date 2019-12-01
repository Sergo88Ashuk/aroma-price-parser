import asyncio
from time import time
import re
import requests
from requests import ConnectionError

from aiohttp import ClientOSError
import aiohttp
from bs4 import BeautifulSoup
from googlesearch import search


item = 'Йогуртин'


async def get_shop_content(client, link):
    async with client.get(link) as resp:
        # assert resp.status == 200
        page = await resp.text()
        return page


def get_shops_list(item):
    links = []
    for url in search(item, stop=10):
        links.append(url)
    return links


shops = {}


def sync_get_page(link):
    data = requests.request(method='GET', url=link)
    return data.text


async def main():
    google_time_start = time()
    shop_links = get_shops_list(item)
    print('time for googling', time() - google_time_start)

    # for shop in shop_links:
    #     try:
    #         shops[shop] = sync_get_page(shop)
    #     except ConnectionError:
    #         print('fail to get ', shop)

    # async with aiohttp.ClientSession() as client:
    #     for shop in shop_links:
    #         try:
    #             shops[shop] = await get_shop_content(client, shop)
    #         except ClientOSError:
    #             print('fail to get', shop)


def has_item(tag):
    if item in tag.contents:
        return True
    return False


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_time = time()
    loop.run_until_complete(main())

    # for link, html in shops.items():
    #     if 'co2' in link:
    #         soup = BeautifulSoup(html, features='html.parser')
    #         print(link)
    #         tags = soup.find_all(name='h1',
    #                              string=re.compile(item))
    #         if len(tags) != 0:
    #             parent = tags[0].parent.parent
    #             print(parent)
    #         else:
    #             print('not found item')

    taken_time = time() - start_time
    print('TIME LEFT:', taken_time)
