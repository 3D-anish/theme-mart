from django.contrib import admin
from .models import License_Term, License, Asset_License

# Register your models here.
class License_TermInline(admin.TabularInline):
    model = License.license_terms.through
    extra = 1

class License_TermModelAdmin(admin.ModelAdmin):
    list_display = ["term_title", "term_detail"]
    search_fields = ['term_title']
    fieldsets = [
        (
            'Term Details',
            {
                "fields": ["term_title",'term_detail'],
            },
        ),
    ]

class LicenseModelAdmin (admin.ModelAdmin):
    list_display = ["name", "asset_category", "total_license_terms"]
    list_filter = ['name', 'asset_category']
    search_fields = ['name']
    fieldsets = [
        (
            'License Details',
            {
                "fields": ["name",'asset_category'],
            },
        ),
         (
            'License Terms',
            {
                "fields": ['license_terms'],
            },
        ),
    ]
    inlines = [
        License_TermInline,
    ]

class Asset_LicenseModelAdmin(admin.ModelAdmin):
    list_display = ["asset", "license", "price"]
    readonly_fields = ['date_created']
    list_filter = ['license', 'date_created']
    fieldsets = [
        (
            'Asset Details',
            {
                "fields": ["asset"],
            },
        ),
         (
            'License Details',
            {
                "fields": ['license', 'price'],
            },
        ),
        (
            'Important Dates',
            {
                "fields": ['date_created',],
            },
        ),
    ]


admin.site.register(License_Term, License_TermModelAdmin)
admin.site.register(License, LicenseModelAdmin)
admin.site.register(Asset_License, Asset_LicenseModelAdmin)