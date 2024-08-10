from django.contrib import admin
from .models import Asset_Category, Asset, Asset_Preview_Images, AssetFeedback

# Register your models here.

class Asset_CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["name", "asset_category_image", "required_file_types", "min_asset_size", 'max_asset_size']
    list_editable = ["required_file_types", "min_asset_size", "max_asset_size"]
    search_fields = ['name','required_file_types']
    prepopulated_fields = {'slug' : ("name",)}
    readonly_fields = ['asset_category_image']
    fieldsets = [
        (
            'Asset Category Details',
            {
                "fields": ["name", 'slug', "asset_category_image", 'image'],
            },
        ),
         (
            'Required File Types',
            {
                "fields": ['required_file_types'],
            },
        ),
        (
            'Required Asset Size',
            {
                "fields": ["min_asset_size", "max_asset_size"],
            },
        ),
    ]

class Asset_Preview_ImagesInline(admin.TabularInline):
    model = Asset_Preview_Images
    fields = ['asset_preview_image_preview', 'image']
    readonly_fields = ['asset_preview_image_preview']
    extra = 1
    
class AssetAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "user", 'file_type', 'status', 'date_created',]
    readonly_fields = ['is_eligible_for_publish', 'date_created', 'date_updated']
    list_filter = ['status', 'date_created','date_published']
    search_fields = ['title', 'uuid','tags']
    fieldsets = [
        (
            'Unique ID',
            {
                "fields": ["uuid"],
            },
        ),
        (
            'Seller',
            {
                "fields": ['user'],
            },
        ),
        (
            'Asset Details',
            {
                "fields": ['title', 'category', 'meta_description', 'description', 'tags', 'size', 'file_type', 'is_eligible_for_publish', 'status'],
            },
        ),
        (
            'Asset',
            {
                "fields": ["asset"],
            },
        ),
        (
            'Important Dates',
            {
                "fields": [ 'date_created', 'date_updated', 'date_published'],
            },
        ),
    ]
    inlines = [
        Asset_Preview_ImagesInline,
    ]

class Asset_Preview_ImagesModelAdmin(admin.ModelAdmin):
    list_display = ["asset", "asset_preview_image_preview"]
    readonly_fields = ['asset_preview_image_preview', 'date_created']
    list_filter = ['date_created']
    fieldsets = [
        (
            'Asset',
            {
                "fields": ['asset'],
            },
        ),
        (
            'Asset Preview Image',
            {
                "fields": ["asset_preview_image_preview", 'image'],
            },
        ),
        (
            'Important Dates',
            {
                "fields": [ 'date_created'],
            },
        ),
    ]
    
class AssetFeedbackModelAdmin(admin.ModelAdmin):
    list_display = ["asset", "user", "rating", "date_created"]
    readonly_fields = ['date_created']
    list_filter = ['rating', 'date_created']
    fieldsets = [
        (
            'Order',
            {
                "fields": ['order'],
            },
        ),
        (
            'Asset',
            {
                "fields": ["asset"],
            },
        ),
        (
            'User',
            {
                "fields": [ 'user'],
            },
        ),
        (
            'Rating & Feedback',
            {
                "fields": [ 'rating', 'feedback'],
            },
        ),
        (
            'Important Dates',
            {
                "fields": [ 'date_created'],
            },
        ),
    ]

admin.site.register(Asset_Category, Asset_CategoryModelAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Asset_Preview_Images, Asset_Preview_ImagesModelAdmin)
admin.site.register(AssetFeedback, AssetFeedbackModelAdmin)