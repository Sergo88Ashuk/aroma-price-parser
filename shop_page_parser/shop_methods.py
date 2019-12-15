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
    prices = []
    weights = []

    if len(tags) != 0:
        prod_tag = tags[0].parent.parent
        price_tag = prod_tag.find(name='h2')
        prices.append(str(price_tag.string).strip('\xa0 '))

    else:
        prices = []

    weights_opt_parent = soup.find(name='table', id='attributesFields')
    weights_opt = weights_opt_parent.find_all(name='option')
    weights_opt = list(weights_opt)

    for w in weights_opt:
        weights.append(re.findall(r'(\d{1,} (кг|г|мл))', str(w))[0][0])

    for p in weights_opt[1:]:
        prices.append(re.findall(r'(([\d]?[,]?\d{1,}.\d{1,}) (руб))', str(p))[0][0])

    options = tuple(zip(prices, weights))
    return 'co2-extract', item, options


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

    weight_tag_top = soup.find(name='span', itemprop='item')
    weight_tag = weight_tag_top.find(name='span', itemprop='name')
    weight_str = str(weight_tag.string).strip('\xa0')
    weight = re.findall(r'(\d{1,} (кг|г|мл))', weight_str)[0][0]

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
        try:
            weight = re.findall(r'(\d{1,} (кг|г|мл))', price_tag.contents[0])[0][0]
        except IndexError:
            print('fail to parse {} on magicsoup'.format(item))
            print('price tag:\n{}'.format(price_tag.contents[0]))
            weight = 0

    else:
        price = 0
        weight = 0

    return 'magicsoap', item, price, weight
