from bs4 import BeautifulSoup
import re

shop_methods = {}


def search_method(shop_fun):
    shop_methods[shop_fun.__doc__] = shop_fun
    return shop_fun


@search_method
def co2_extract(page, item):
    """co2-extract"""
    def has_item(tag, item):
        if item in tag.contents:
            return True
        return False

    soup = BeautifulSoup(page, features='html.parser')
    tags = soup.find_all(name='h1',
                         string=re.compile(item))
    if len(tags) != 0:
        print('item found')
    else:
        print('not found item')
    price = None
    return 'co2-extract', item, price


@search_method
def my_formula(page, item):
    """my-formula"""
    price = None
    return 'my-formula', item, price


@search_method
def magicsoup(page, item):
    """magicsoup"""
    price = None
    return 'magicsoap', item, price