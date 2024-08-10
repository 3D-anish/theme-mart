from django.urls import path
from .views import become_seller, dashboard, seller_store

app_name = 'seller'

urlpatterns = [
    path('@<username>/', seller_store, name='seller_store'),
    path('dashboard/', dashboard, name='dashboard'),
    path('become-seller/', become_seller, name='become_seller'),
]
