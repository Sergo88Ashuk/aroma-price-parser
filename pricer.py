import asyncio
import multiprocessing as mp
from time import time

from aiohttp import ClientOSError, ServerDisconnectedError, ClientSession
from googlesearch import search
from shop_page_parser.parser import parse_item_pages
from links_for_debug import recs_dbg


LINKS_PER_ITEM = 20
ITEMS = ['Йогуртин', 'НУФ']
SEARCH_FOR_ITEMS = True


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


def get_items_rec(items):
    search_prefix = 'руб | купить '
    recs = []
    for item in items:
        for url in search(search_prefix+item, num=LINKS_PER_ITEM, stop=LINKS_PER_ITEM):
            recs.append(tuple([item, url]))

    return recs


async def get_item_pages(q, items):
    if SEARCH_FOR_ITEMS:
        items_rec = get_items_rec(items)
    else:
        items_rec = recs_dbg

    tasks = []
    async with ClientSession() as client:
        for rec in items_rec:
            item, url = rec
            task = asyncio.ensure_future(put_item_page_to_queue(client, url, q, item))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    items_list = ITEMS

    start_time = time()

    item_queue = mp.Queue()
    result_queue = mp.Queue()
    parser_process = mp.Process(target=parse_item_pages, args=(item_queue, result_queue, ))
    parser_process.start()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_item_pages(item_queue, items_list))
    loop.run_until_complete(future)

    item_queue.put('mission complete')
    parser_process.join(timeout=10.0)

    prices = result_queue.get()

    taken_time = time() - start_time
    print('TIME LEFT:', taken_time)
    print(prices)


if __name__ == '__main__':
    main()
