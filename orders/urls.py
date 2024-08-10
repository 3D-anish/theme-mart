from django.urls import path
from .views import create_order, checkout, order_success, cancel_order, my_orders,order_details, payment_callback

app_name = 'orders'

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('checkout/<uuid>/', checkout, name='checkout'),
    path('cancel-order/<uuid>/', cancel_order, name='cancel_order'),
    path('order-success/<uuid>/', order_success, name='order_success'),
    path('payment-callback/<uuid>/', payment_callback, name='payment_callback'),
    
    path('', my_orders, name='my_orders'),
    path('order-detials/<uuid>/', order_details, name='order_details'),
]
