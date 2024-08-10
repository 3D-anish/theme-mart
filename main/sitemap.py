from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy

class StaticSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9
    
    def items(self):
        return ['main:home', 'accounts:login', "accounts:register", "main:shop"]
    
    def location(self,item):
        return reverse_lazy(item)