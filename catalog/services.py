
from config.settings import CACHE_ENABLED
from django.core.cache import cache
from catalog.models import Product

def get_cached_products():
    "Получает данные по продуктам из кэша, если кэш пуст, иначе получает данные из БД"
    if not CACHE_ENABLED:
        Product.objects.all()
    key = 'products_list'
    products = cache.get(key)

    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products, 150)
    return products
