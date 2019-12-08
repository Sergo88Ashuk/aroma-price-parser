from bs4 import BeautifulSoup
import re

shop_methods = {}

# todo: add the weight to returning tuple


def search_method(shop_fun):
    shop_methods[shop_fun.__doc__] = shop_fun
    return shop_fun


@search_method
def co2_extract(page, item):
    """co2-extract"""

    soup = BeautifulSoup(page, features='html.parser')
    tags = soup.find_all(name='h1',
                         string=re.compile(item))

    if len(tags) != 0:
        prod_tag = tags[0].parent.parent
        price_tag = prod_tag.find(name='h2')
        price = str(price_tag.string).strip('\xa0 ')

    else:
        price = 0

    weight = 0
    return 'co2-extract', item, price, weight


@search_method
def my_formula(page, item):
    """my-formula"""

    soup = BeautifulSoup(page, features='html.parser')
    item_price_tag = soup.find(name='div',
                               class_='price')

    if len(item_price_tag) != 0:
        price_tag = item_price_tag.find(name='span', class_='price-new')
        price = str(price_tag.string).strip('\xa0 ')

    else:
        price = 0

    weight = 0
    return 'my-formula', item, price, weight


@search_method
def magicsoap(page, item):
    """magicsoap"""

    soup = BeautifulSoup(page, features='html.parser')
    tags = soup.find_all(name='h1',
                         string=re.compile(item))

    if len(tags) != 0:
        prod_tag = tags[0].parent
        price_tag = prod_tag.find(name='label')
        price = price_tag.contents[2].split('(')[1].split(')')[0]

    else:
        price = 0

    weight = 0
    return 'magicsoap', item, price, weight
