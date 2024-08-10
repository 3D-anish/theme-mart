from django.urls import path
from .views import (
    get_add_license_form, add_license, 
    get_edit_license_form, edit_license, 
    delete_license, category_licenses,
    licenses
)

app_name = 'license'

urlpatterns = [
    path('get-add-license-form/<pk>/', get_add_license_form, name='get_add_license_form'),
    path('add-license/<pk>/', add_license, name='add_license'),
    
    path('get-edit-license-form/<asset_pk>/<license_pk>/', get_edit_license_form, name='get_edit_license_form'),
    path('edit-license/<asset_pk>/<license_pk>/', edit_license, name='edit_license'),
    
    path('delete-license/<asset_pk>/<license_pk>/', delete_license, name='delete_license'),
    
    path('', licenses, name='licenses'),
    path('<category_slug>/', category_licenses, name='category'),
]
