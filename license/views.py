from django.shortcuts import render, redirect, get_object_or_404
from .models import Asset_License, License
from assets.models import Asset, Asset_Category
from .forms import AddAssetLicenseForm, EditAssetLicenseForm
from django.contrib import messages
from main.decorators import htmx_required
from django.http import HttpResponse
from django.core.cache import cache

# Create your views here.

@htmx_required
def get_add_license_form(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">User Authentication is required</td></tr>")
    
    if not request.user.is_seller:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">Seller Account is required</td></tr>")
    
    asset_obj = Asset.objects.select_related('category').filter(pk = pk, user = request.user).values('category').first()
    
    if not asset_obj.get('category'):
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">No Asset found</td></tr>")
    
    form = AddAssetLicenseForm()
    form.fields['license'].queryset = License.objects.select_related('asset_category').filter(asset_category=asset_obj['category'])
    ctx = {
        "form" : form, 
        "pk" : pk,
    }
    return render(request, 'license/components/add_license_form.html', ctx)

@htmx_required
def add_license(request,pk):
    if request.method != 'POST':
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">Invalid Request</td></tr>")
    
    if not request.user.is_authenticated:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">User Authentication is required</td></tr>")
    
    if not request.user.is_seller:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">Seller Account is required</td></tr>")
    
    asset_obj = Asset.objects.select_related('category').filter(pk = pk, user = request.user).first()
    
    if not asset_obj:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">No Asset found</td></tr>")
    
    data = request.POST.copy()
    data['asset'] = asset_obj
    form = AddAssetLicenseForm(data=data)
    form.fields['license'].queryset = License.objects.select_related('asset_category').filter(asset_category=asset_obj.category)
    if form.is_valid():
        asset_license_obj = form.save()
        messages.success(request, 'Asset License added successfully.')
        ctx = {
            "asset_license_obj" : asset_license_obj,
            "asset_pk" : asset_obj.pk,
            "license_pk" : asset_license_obj.pk,
        }
        return render(request, 'license/components/license_row.html', ctx)
    else:
        ctx = {
            'form' : form,
            "pk" : asset_obj.pk,
        }
        return render(request, 'license/components/add_license_form.html', ctx)

@htmx_required
def get_edit_license_form(request, asset_pk, license_pk):
    if not request.user.is_authenticated:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">User Authentication is required</td></tr>")
    
    if not request.user.is_seller:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">Seller Account is required</td></tr>")
    
    asset_obj = Asset.objects.select_related('category','user').filter(pk = asset_pk, user = request.user).first()
    
    if not asset_obj:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">No Asset found</td></tr>")
    
    asset_license_obj = Asset_License.objects.select_related('asset', 'license').filter(pk = license_pk, asset = asset_obj).first()
    
    if not asset_license_obj:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">No Asset License found</td></tr>")
    
    form = EditAssetLicenseForm(instance=asset_license_obj)
    form.fields['license'].queryset = License.objects.select_related('asset_category').filter(asset_category=asset_obj.category)
    ctx = {
        "form" : form, 
        "asset_pk" : asset_pk,
        "license_pk" : license_pk,
    }
    return render(request, 'license/components/edit_license_form.html', ctx)

@htmx_required
def edit_license(request, asset_pk, license_pk):
    if request.method != 'POST':
       return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">Invalid Request</td></tr>")
    
    if not request.user.is_authenticated:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">User Authentication is required</td></tr>")
    
    if not request.user.is_seller:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">Seller Account is required</td></tr>")
    
    asset_obj = Asset.objects.select_related('category','user').filter(pk = asset_pk, user = request.user).first()
    
    if not asset_obj:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">No Asset found</td></tr>")
    
    asset_license_obj = Asset_License.objects.select_related('asset', 'license').filter(pk = license_pk, asset = asset_obj).first()
    
    if not asset_license_obj:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">No Asset License found</td></tr>")
    

    form = EditAssetLicenseForm(data = request.POST, instance=asset_license_obj)
    form.fields['license'].queryset = License.objects.select_related('asset_category').filter(asset_category=asset_obj.category)
    if form.is_valid():
        asset_license_obj = form.save()
        messages.success(request, 'Asset License saved successfully.')
        ctx = {
            'asset_license_obj' : asset_license_obj,
            'asset_pk' : asset_obj.pk,
            "license_pk" : asset_license_obj.pk,
        }
        return render(request, 'license/components/license_row.html', ctx)
    else:
        ctx = {
            "form" : form, 
            "asset_pk" : asset_pk,
            "license_pk" : license_pk,
        }
        return render(request, 'license/components/edit_license_form.html', ctx)

@htmx_required
def delete_license(request,asset_pk,license_pk):
    if request.method != 'GET':
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">Invalid Request</td></tr>")
    
    if not request.user.is_authenticated:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">User Authentication is required</td></tr>")
    
    if not request.user.is_seller:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">Seller Account is required</td></tr>")
    
    asset_obj = Asset.objects.select_related('category','user').filter(pk = asset_pk, user = request.user).first()
    
    if not asset_obj:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">No Asset found</td></tr>")
    
    asset_license_obj = Asset_License.objects.select_related('asset', 'license').filter(pk = license_pk, asset = asset_obj).first()
    
    if not asset_license_obj:
        return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">No Asset License found</td></tr>")
    
    if asset_obj.status == 'published' and asset_obj.licenses.all().count() <= 2:
        messages.warning(request, 'Cannot delete, Minimum 2 asset licenses are required')
        ctx = {
            'asset_license_obj' : asset_license_obj,
            'asset_pk' : asset_obj.pk,
            "license_pk" : asset_license_obj.pk,
        }
        return render(request, 'license/components/license_row.html', ctx)           

    asset_license_obj.delete()
    messages.warning(request, 'Asset License deleted successfully.')
    
    return HttpResponse("<tr><td colspan=\"5\" class=\"text-center\">Asset Deleted Succeessfully</td></tr>")

def licenses(request):
    ctx = {
        'title' : f'Licenses | ThemeMart',
    }
    return render(request, 'license/licenses.html', ctx)

def category_licenses(request,category_slug):
    asset_category_obj = get_object_or_404(Asset_Category, slug = category_slug)
    licenses_objs = cache.get_or_set(
        'category_licenses_licenses',
        default=License.objects.prefetch_related('license_terms').filter(asset_category = asset_category_obj),
        timeout= 120)

    ctx = {
        'title' : f'Licenses | {asset_category_obj.name} | ThemeMart',
        'asset_category_obj' : asset_category_obj,
        "licenses" : licenses_objs,
    }
    return render(request, 'license/category_licenses.html', ctx)