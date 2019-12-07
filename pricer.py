import asyncio
from time import time
import multiprocessing as mp

from aiohttp import ClientOSError, ServerDisconnectedError, ClientSession
from googlesearch import search
from shop_page_parser.parser import parse_shop_pages


LINKS_PER_ITEM = 20
ITEMS = ['Йогуртин']


async def put_item_page_to_queue(client, link, queue, item):
    try:
        async with client.get(link) as resp:
            page = await resp.text()
            queue.put(tuple([link, page, item]))
            return
    except ClientOSError:
        print('fail to get', link)
    except ServerDisconnectedError:
        print('server disconnected', link)
    except UnicodeDecodeError:
        print('fail to decode unicode', link)


def get_item_links(items):
    links = []
    for item in items:
        for url in search(item, num=LINKS_PER_ITEM, stop=LINKS_PER_ITEM):
            links.append(dict({item: url}))
    print(links)
    return links


async def get_items(q, items):
    google_time_start = time()
    item_links = get_item_links(items)   # links_dbg   #get_shops_list(good)
    print('time for googling', time() - google_time_start)

    tasks = []
    async with ClientSession() as client:
        for item, link in item_links.items():
            task = asyncio.ensure_future(put_item_page_to_queue(client, link, q, item))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    items_list = ITEMS

    start_time = time()

    item_queue = mp.Queue()
    parser_process = mp.Process(target=parse_shop_pages, args=(item_queue,))
    parser_process.start()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_items(item_queue, items_list))
    loop.run_until_complete(future)

    item_queue.put('mission complete')
    parser_process.join()

    taken_time = time() - start_time
    print('TIME LEFT:', taken_time)


if __name__ == '__main__':
    main()
