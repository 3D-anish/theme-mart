from django.contrib import admin
from .models import Seller, Sell

# Register your models here.

class SellerModelAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "aadhar_card_number", 'date_created']
    readonly_fields = ['bank_account_number', 'bank_account_ifsc_code', 'date_created']
    # list_editable = ["is_verified",]
    list_filter = ['date_created']
    search_fields = ['phone_number','aadhar_card_number']
    fieldsets = [
         (
            'Account Details',
            {
                "fields": ["user", 'phone_number', 'aadhar_card_number', ],
            },
        ),
        (
            'Bank Account Details',
            {
                "fields": ["bank_account_number","bank_account_ifsc_code"],
            },
        ),
        (
            'Important Dates',
            {
                "fields": ["date_created"],
            },
        ),
    ]
    
class SellModelAdmin(admin.ModelAdmin):
    list_display = ["uuid", "asset_price", "thememart_commision", "final_sell", 'paid', 'paid_on']
    readonly_fields = ['date_created']
    # list_editable = ["is_verified",]
    list_filter = ['paid', 'paid_on', 'date_created']
    search_fields = ['uuid']
    fieldsets = [
         (
            None,
            {
                "fields": ["uuid"],
            },
        ),
         (
            'Seller',
            {
                "fields": ["seller"],
            },
        ),
        (
            'Order Details',
            {
                "fields": ["order_id","order_item", "asset"],
            },
        ),
        (
            'Prices & Commisions',
            {
                "fields": ["asset_price",'razorpay_payment_commision', 'thememart_commision', 'final_sell'],
            },
        ),
        (
            'Seller Payment Details',
            {
                "fields": ["paid",'paid_on'],
            },
        ),
        (
            'Important Dates',
            {
                "fields": ["date_created"],
            },
        ),
    ]

admin.site.register(Seller, SellerModelAdmin)
admin.site.register(Sell, SellModelAdmin)