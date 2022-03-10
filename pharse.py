# import pprint
from epicstore_api.api import EpicGamesStoreAPI
from epicstore_api.models.categories import EGSCategory


Categories = {
    'CATEGORY_ACTION': EGSCategory.CATEGORY_ACTION,  # Боевой
    'CATEGORY_ADVENTURE': EGSCategory.CATEGORY_ADVENTURE,  # Приключения
    'CATEGORY_EDITOR': EGSCategory.CATEGORY_EDITOR,  # Создание
    'CATEGORY_MULTIPLAYER': EGSCategory.CATEGORY_MULTIPLAYER,  # Мультиплеер
    'CATEGORY_PUZZLE': EGSCategory.CATEGORY_PUZZLE,  # Головоломки
    'CATEGORY_RACING': EGSCategory.CATEGORY_RACING,  # Гонки
    'CATEGORY_RPG': EGSCategory.CATEGORY_RPG,  # РПГ
    'CATEGORY_SHOOTER': EGSCategory.CATEGORY_SHOOTER,  # Шутер
    'CATEGORY_SINGLE_PLAYER': EGSCategory.CATEGORY_SINGLE_PLAYER,  # Синглплеер
    'CATEGORY_STRATEGY': EGSCategory.CATEGORY_STRATEGY,  # Стратегия
    'CATEGORY_SURVIVAL': EGSCategory.CATEGORY_SURVIVAL,  # Выживание
    'CATEGORY_OSX': EGSCategory.CATEGORY_OSX,  # Mac OS
    'CATEGORY_WINDOWS': EGSCategory.CATEGORY_WINDOWS  # Windows
}

__request = EpicGamesStoreAPI(locale='ru-RU', country='RU', session=None)


def open_info(game):
    # pprint.pprint(game)
    price_info = game['price']['totalPrice']
    images_info = {img['type']: img['url'] for img in game['keyImages']}
    developer_info = ''
    for elem in game['linkedOffer']['customAttributes']:
        if 'developerName' in elem['key']:
            developer_info = elem['value']
    info = {
        'title': game['title'],
        'original_price': price_info['originalPrice'] / 100,
        'discount': price_info['discount'] / 100,
        'discount_price': price_info['discountPrice'] / 100,
        'developer_name': developer_info,
        'published_date': game['linkedOffer']['effectiveDate'].split('T')[0],
        'image_urls': {'Wide': images_info['DieselStoreFrontWide'],
                       'Tall': images_info['DieselStoreFrontTall']}}
    # pprint.pprint(info)
    return info


def game_find_similar(result_count=5, start=0, count=50, keywords='', categories=[]):
    data = __request.fetch_catalog(start=start, count=count, product_type='games',  # sort_by='effectiveDate',
                                   keywords=keywords, categories=categories)
    data = data['data']['Catalog']['catalogOffers']['elements']
    result = []
    for index, game in enumerate(data):
        if index == result_count:
            break
        result.append(open_info(game))
    return result


def value_to_str(value, is_total=False):
    if isinstance(value, int) or isinstance(value, float):
        if round(value, 2) or is_total:
            return f"{value:0.2f} ₽"
        else:
            return "Бесплатно"
    raise TypeError("Неправильный тип для валюты!")


# print(value_to_str(213.20))
# print(value_to_str(213.77))
# print(value_to_str(333))
# print(value_to_str(0))
# print(value_to_str(0.0))
# print(value_to_str(0.0, is_total=True))
# print(value_to_str(990, is_total=True))
# # print(value_to_str('2'))
# print(value_to_str(100))
