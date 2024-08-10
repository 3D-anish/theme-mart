from assets.models import Asset_Category
from django.core.cache import cache

def get_asset_categories(request):
    asset_categories = cache.get_or_set(
        'get_asset_categories_asset_categories',
        default=Asset_Category.objects.all().order_by('name'),
        timeout= 120)
    return {'asset_categories' : asset_categories }