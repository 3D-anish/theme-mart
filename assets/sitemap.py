from django.contrib.sitemaps import Sitemap 
from .models import Asset 
  
class AssetSitemap(Sitemap):
    changefreq = "always"
    priority = 0.8
    def items(self): 
        return Asset.objects.filter(status = 'published') 
        
    def lastmod(self, obj): 
        return obj.date_updated