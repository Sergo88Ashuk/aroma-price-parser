from bs4 import BeautifulSoup
import re

shop_methods = []


def search_method(shop_fun):
    shop_methods.append(shop_fun)
    return shop_fun


@search_method
def co2(page, item):
    def has_item(tag, good):
        if good in tag.contents:
            return True
        return False

    soup = BeautifulSoup(page, features='html.parser')
    tags = soup.find_all(name='h1',
                         string=re.compile(item))
    if len(tags) != 0:
        print('item found')
    else:
        print('not found item')


