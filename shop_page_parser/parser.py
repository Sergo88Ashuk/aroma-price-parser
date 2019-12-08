from .shop_methods import shop_methods


def get_shop_name(link):
    shop_name_tmp = link.split('/')[2]
    shop_addr = shop_name_tmp.split('.')
    if 'www' in shop_addr:
        shop_name = shop_addr[shop_addr.index('www') + 1]
    else:
        shop_name = shop_addr[0]
    return shop_name


def get_parse_method(link):
    shop_name = get_shop_name(link)
    parse_method = shop_methods.get(shop_name, None)

    if not parse_method:
        #   todo: add ckecking if the link is actually a shop
        # print('implement search method for {} {}'.format(link, shop_name))
        return None

    return parse_method


def parse_item_pages(items_queue, result_queue):
    results = []
    while True:
        queue_element = items_queue.get()
        if len(queue_element) == 3:
            link, page, item = queue_element
            parse_method = get_parse_method(link)
            if parse_method:
                parse_result = parse_method(page, item)
                results.append(parse_result)

        elif queue_element == 'mission complete':
            result_queue.put(results)
            break
