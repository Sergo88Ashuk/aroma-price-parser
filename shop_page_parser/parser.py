from .shop_methods import shop_methods


def get_parse_method(link):
    # extract shop name from link
    # iterate shop_methods to look for shop name
    # if nothing found log out the request to implement the parsing method for shop
    # if method found return this method as a function
    pass


def parse_shop_pages(items_queue):
    while True:
        queue_element = items_queue.get()
        if len(queue_element) == 3:
            link, page, item = queue_element
            parse_result = get_parse_method(link)(page, item)
        elif queue_element == 'mission complete':
            break
