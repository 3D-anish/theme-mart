from django.contrib import admin
from .models import Orders, Order_Items

# Register your models here.

class Order_ItemsInline(admin.TabularInline):
    model = Order_Items
    fields = ['asset', 'license', 'price', 'gst', 'razorpay_payment_commision']
    readonly_fields = ['asset', 'license', 'price', 'gst', 'razorpay_payment_commision']
    extra = 0

class OrdersModelAdmin(admin.ModelAdmin):
    list_display = ["uuid", "user","total_price", 'order_status', 'payment_on']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_payment_signature', 'date_created']
    list_filter = ['order_status', 'payment_on', 'date_created']
    search_fields = ['uuid','user_email', 'user_phonenumber', 'user_full_name']
    fieldsets = [
        (
            'Order Unique ID',
            {
                "fields": ["uuid"],
            },
        ),
        (
            'Buyer Details',
            {
                "fields": ["user",'user_email', "user_phonenumber", 'user_full_name'],
            },
        ),
        (
            'Order Details',
            {
                "fields": ['order_items', 'order_status'],
            },
        ),
        (
            'Order Amount',
            {
                "fields": ['sub_total', 'gst', 'total_price', 'total_payment_recieved', 'razorpay_payment_fee', 'razorpay_payment_tax'],
            },
        ),
        (
            'Razorpay Details',
            {
                "fields": ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_payment_signature', 'other_razorpay_payment_details'],
            },
        ),
        (
            'Billing Address',
            {
                "fields": ["address_line_1","address_line_2", 'address_area', 'address_city', 'address_state', 'address_pincode', 'gst_number',],
            },
        ),
        (
            'Important Dates',
            {
                "fields": [ 'payment_on', 'date_created' ],
            },
        ),
    ]
    inlines = [
        Order_ItemsInline,
    ]

class Order_ItemsModelAdmin(admin.ModelAdmin):
    list_display = ["order", "asset","price", 'gst', 'razorpay_payment_commision']
    readonly_fields = ['date_created']
    list_filter = ['date_created']
    fieldsets = [
        (
            'Order',
            {
                "fields": ["order"],
            },
        ),
        (
            'Asset Details',
            {
                "fields": ["asset",'license'],
            },
        ),
        (
            'Order Amount',
            {
                "fields": ['price', 'gst', 'razorpay_payment_commision'],
            },
        ),
        (
            'Important Dates',
            {
                "fields": ['date_created'],
            },
        ),
    ]
admin.site.register(Orders, OrdersModelAdmin)
admin.site.register(Order_Items, Order_ItemsModelAdmin)