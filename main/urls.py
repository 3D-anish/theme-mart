from django.urls import path
from .views import home, shop, cart, thememart_dashboard

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('shop/', shop, name='shop'),
    path('cart/', cart, name='cart'),
    path('admin/thememart-dashboard/', thememart_dashboard, name='thememart_dashboard'),
]
