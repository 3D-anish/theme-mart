"""
URL configuration for ThemeMart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import private_storage.urls
from django.views.generic.base import TemplateView
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from assets.sitemap import AssetSitemap
from main.sitemap import StaticSitemap

sitemaps = {
    'static': StaticSitemap,
    'assets' : AssetSitemap
}

urlpatterns = [
    path('favicon.ico', serve, {'document_root': settings.STATIC_DIR, 'path' : 'images/favicon_TM.png'}),
    path('robots.txt', TemplateView.as_view(template_name = 'robots.txt',content_type ="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'), 
    
    path('',include('main.urls')),
    
    path('admin/', admin.site.urls),
    
    path('accounts/',include('accounts.urls')),
    path('seller/',include('seller.urls')),
    path('license/',include('license.urls')),
    path('assets/',include('assets.urls')),
    path('orders/',include('orders.urls')),
    
    # Django Debug Toolbar
    path("__debug__/", include("debug_toolbar.urls")),
    # django-private-storage
    path('private-media/', include(private_storage.urls)),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)