from django.contrib import admin
from .models import HomeBanner

# Register your models here.

class HomeBannerModelAdmin(admin.ModelAdmin):
    list_display = ["link", "h1_title", "banner_preview", 'date_created']
    readonly_fields = ['date_created', 'banner_preview']
    list_filter = ['date_created']
    search_fields = ['h1_title', 'h4_title','link']
    fieldsets = [
        (
            'Titles',
            {
                "fields": ["h1_title", "h4_title"],
            },
        ),
        (
            'Banner',
            {
                "fields": ['banner_preview','banner'],
            },
        ),
        (
            'Link',
            {
                "fields": ['link','link_text'],
            },
        ),
        (
            'Important Dates',
            {
                "fields": ['date_created'],
            },
        ),
    ]

admin.site.register(HomeBanner, HomeBannerModelAdmin)
