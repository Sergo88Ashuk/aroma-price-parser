import asyncio
from time import time
import re
import requests
from requests import ConnectionError

from aiohttp import ClientOSError, ServerDisconnectedError
import aiohttp
from bs4 import BeautifulSoup
from googlesearch import search
from links_for_debug import links_dbg

ASYNC = True

item = 'Йогуртин'
shops = {}


async def get_shop_content(client, link):
    try:
        async with client.get(link) as resp:
            page = await resp.text()
            shops[link] = page
            return
    except ClientOSError:
        print('fail to get', link)
    except ServerDisconnectedError:
        print('server disconnected', link)
    except UnicodeDecodeError:
        print('fail to decode unicode', link)
    except BaseException:
        print('got unknown exception from', link)


def get_shops_list(item):
    links = []
    for url in search(item, num=100, stop=200):
        links.append(url)
    print(links)
    return links


def sync_get_page(link):
    data = requests.request(method='GET', url=link)
    return data.text


async def main():
    google_time_start = time()
    shop_links = links_dbg   #links_dbg   #get_shops_list(item)
    print('time for googling', time() - google_time_start)

    if not ASYNC:
        print('SYNC')
        for shop in shop_links:
            try:
                shops[shop] = sync_get_page(shop)
            except ConnectionError:
                print('fail to get ', shop)
            except UnicodeDecodeError:
                print('fail to decode unicode', shop)
    else:
        print('ASYNC')
        tasks = []
        async with aiohttp.ClientSession() as client:
            for shop in shop_links:
                task = asyncio.ensure_future(get_shop_content(client, shop))
                tasks.append(task)
            await asyncio.gather(*tasks)


def has_item(tag):
    if item in tag.contents:
        return True
    return False


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_time = time()
    future = asyncio.ensure_future(main())
    loop.run_until_complete(future)

    for link, html in shops.items():
        soup = BeautifulSoup(html, features='html.parser')

        tags = soup.find_all(name='h1',
                             string=re.compile(item))
        if len(tags) != 0:
            print('item found', link)
            # parent = tags[0].parent.parent
            # print(parent)
        else:
            print('not found item')

    taken_time = time() - start_time
    print('TIME LEFT:', taken_time)
