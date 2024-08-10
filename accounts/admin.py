from django.contrib import admin
from accounts.models import User

# Register your models here.

class UserModelAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "phone_number", 'profile_image_preview', 'is_verified', 'is_seller',]
    readonly_fields = ['email', 'password','profile_image_preview']
    list_editable = ["is_verified",]
    list_filter = ['is_staff', 'is_active', 'is_seller', 'is_superuser','is_verified','date_joined']
    search_fields = ['username','email', 'phone_number']
    fieldsets = [
        (
            'Account Details',
            {
                "fields": ["username",'full_name', "email", 'phone_number','profile_image_preview','profile_image'],
            },
        ),
         (
            'Credentials',
            {
                "fields": ['password', 'uuid', ],
            },
        ),
        (
            'Billing Address',
            {
                "fields": ["address_line_1","address_line_2", 'address_area', 'address_city', 'address_state', 'address_pincode', 'gst_number',],
            },
        ),
        (
            'Account Status',
            {
                "fields": ['is_active', 'is_staff', 'is_superuser', 'is_verified', 'is_seller' ],
            },
        ),
        (
            'Important Dates',
            {
                "fields": [ 'last_login', 'date_joined' ],
            },
        ),
        (
            'Groups & Permissions',
            {
                "fields": [ 'groups','user_permissions' ],
            },
        ),
    ]

admin.site.register(User, UserModelAdmin)