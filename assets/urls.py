from django.urls import path
from .views import (
    create_asset, edit_asset, add_asset_preview_image, 
    delete_asset_preview_image, my_assets, asset_detail,
    get_add_asset_preview_image_form, download_asset,
    publish_asset, delete_feedback, delete_asset

)

app_name = 'assets'

urlpatterns = [
    
    path('', my_assets, name='my_assets'),
    path('create/', create_asset, name='create_asset'),
    path('edit/<pk>/', edit_asset, name='edit_asset'),
    path('delete/<pk>/', delete_asset, name='delete_asset'),
    path('publish-asset/<pk>/', publish_asset, name='publish_asset'),
    
    path('get-add-asset-preview-image-form/<pk>/', get_add_asset_preview_image_form, name='get_add_asset_preview_image_form'),
    path('add-asset-preview-image/<pk>/', add_asset_preview_image, name='add_asset_preview_image'),
    path('delete-asset-preview-image/<asset_pk>/<asset_preview_image_pk>/', delete_asset_preview_image, name='delete_asset_preview_image'),
    
    path('<uuid>/', asset_detail, name='asset_detail'),
    
    path('download-asset/<order_uuid>/<pk>/', download_asset, name='download_asset'),
    path('delete-feedback/<pk>/', delete_feedback, name='delete_feedback'),
]
