from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateAssetForm, EditAssetForm, AddPreviewImageForm, FeedbackForm
from .models import Asset, Asset_Preview_Images, AssetFeedback
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from seller.decorators import seller_required
from license.models import Asset_License
from main.decorators import htmx_required
from django.http import HttpResponse, FileResponse, Http404
from orders.models import Orders, Order_Items
from django.utils.timezone import now
from datetime import timedelta
from main.helper_func import get_paginated_objs
from django.template.defaultfilters import slugify
from django.db.models import Avg, Count
from django.core.cache import cache

# Create your views here.

@login_required
@seller_required
def create_asset(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['user'] = request.user
        form = CreateAssetForm(data= data, files= request.FILES)
        if form.is_valid():
            asset_pk = form.save()
            messages.success(request, "Asset created successfully.")
            return redirect('assets:edit_asset',pk = asset_pk)
        
    else:
        form = CreateAssetForm()
    
    ctx = {
        'title' : 'Create Asset | ThemeMart',
        'form' : form,
    }
    return render(request, 'assets/create_asset.html', ctx)

@login_required
@seller_required
def edit_asset(request,pk):
    asset_obj = get_object_or_404(Asset.objects.select_related('user', 'category').prefetch_related('tags', 'licenses', 'asset_preview_images','licenses__license','licenses__license__license_terms'),pk = pk, user = request.user)
    if request.method == 'POST':
        form = EditAssetForm(data = request.POST, instance= asset_obj)
        if form.is_valid():
            form.save()
            messages.success(request,"Asset saved successfully")
            return redirect('assets:edit_asset',pk = pk)
    else:
        form = EditAssetForm(instance=asset_obj)
    
    ctx = {
        'title' : f'Edit | {asset_obj.title} | ThemeMart',
        'form' : form,
        'asset_obj' : asset_obj,
    }
    return render(request, 'assets/edit_asset.html', ctx)

@login_required
def publish_asset(request, pk):
    asset_obj = get_object_or_404(Asset,pk = pk, user = request.user, status = 'draft')
    asset_obj.status = 'published'
    asset_obj.date_published = now()
    asset_obj.save()
    messages.success(request, 'Asset Published successfully')
    return redirect('assets:edit_asset',pk = pk)
    
@htmx_required
def get_add_asset_preview_image_form(request, pk):
    form = AddPreviewImageForm()
    ctx = {
        "form" : form, 
        "pk" : pk,
    }
    return render(request, 'assets/components/add_preview_image_form.html', ctx)

@htmx_required
def add_asset_preview_image(request,pk):
    if request.method != 'POST':
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">Invalid Request</td></tr>")
    if not request.FILES:
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">No File Found</td></tr>")
    
    if not request.user.is_authenticated:
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">User Authentication is required</td></tr>")
    
    if not request.user.is_seller:
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">Seller Account is required</td></tr>")
    
    asset_obj = Asset.objects.filter(pk = pk, user = request.user).first()
    
    if not asset_obj:
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">No Asset found</td></tr>")
    
    data = request.POST.copy()
    data['asset'] = asset_obj
    form = AddPreviewImageForm(data=data, files=request.FILES)
    if form.is_valid():
        asset_preview_image_obj = form.save()
        messages.success(request, 'Preview image added successfully.')
        ctx = {
            'form' : form,
            'asset_preview_image_obj' : asset_preview_image_obj,
            'asset_pk' : asset_obj.pk,
        }
        return render(request, 'assets/components/asset_preview_image_row.html', ctx)
    else:
        ctx = {
            'form' : form,
            'pk' : asset_obj.pk,
        }
        return render(request, 'assets/components/add_preview_image_form.html', ctx)
    
@htmx_required
def delete_asset_preview_image(request,asset_pk,asset_preview_image_pk):
    if request.method != 'GET':
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">Invalid Request</td></tr>")
    
    if not request.user.is_authenticated:
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">User Authentication is required</td></tr>")
    
    if not request.user.is_seller:
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">Seller Account is required</td></tr>")
    
    asset_obj = Asset.objects.filter(pk = asset_pk, user = request.user).first()
    
    if not asset_obj:
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">No Asset found</td></tr>")
    
    asset_preview_images_obj = Asset_Preview_Images.objects.filter(pk = asset_preview_image_pk, asset = asset_obj).first()
    
    if not asset_preview_images_obj:
        return HttpResponse("<tr><td colspan=\"3\" class=\"text-center\">No preview Images Found</td></tr>")
    
    if asset_obj.status == 'published' and asset_obj.asset_preview_images.all().count() <= 3:
        messages.warning(request, 'Cannot delete, Minimum 3 images required')
        ctx = {
            'asset_preview_image_obj' : asset_preview_images_obj,
            'asset_pk' : asset_obj.pk,
        }
        return render(request, 'assets/components/asset_preview_image_row.html', ctx)                

    asset_preview_images_obj.delete()
    messages.warning(request, 'Preview image deleted successfully.')
        
    return HttpResponse("")

@login_required
@seller_required
def my_assets(request):
    assets_objs = Asset.objects.select_related('user','category').prefetch_related('asset_preview_images').filter(user = request.user)
    
    ctx = {
        "title" : 'My Assets | ThemeMart',
        "assets_objs" : get_paginated_objs(assets_objs,request.GET.get("page", 1),5),
    }
    return render(request, 'assets/my_assets.html', ctx)

def asset_detail(request, uuid):
    license_name = request.GET.get("license", None)
    asset_obj = cache.get(f'asset_detail_asset_obj_{uuid}')
    if not asset_obj:
        asset_obj = get_object_or_404(
            Asset.objects.select_related('user','category').prefetch_related('tags','asset_preview_images','licenses','feedbacks', 'feedbacks__user',).annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')),
            uuid = uuid,
        )
        cache.set(f'asset_detail_asset_obj_{uuid}', asset_obj, timeout=120)
    
    if not request.user == asset_obj.user:
        if not asset_obj.status == 'published':
            raise Http404('No asset found')
    
    all_licenses = cache.get_or_set(
        f'asset_detail_all_licenses_{uuid}',
        default=Asset_License.objects.select_related("license").filter(asset = asset_obj),
        timeout= 120)
    
    other_licenses = None
    license = None
    if all_licenses:
        if license_name:
            license = all_licenses.prefetch_related('license__license_terms').filter(license__name = license_name).first()
        else:
            license = all_licenses.first()
    if license:
        other_licenses = all_licenses.exclude(pk = license.pk)
    else:
        other_licenses = all_licenses

    total_orders = cache.get_or_set(
        f'asset_detail_total_orders_{uuid}',
        default=Orders.objects.filter(order_status = 'success', order_items__asset =asset_obj,payment_on__gte = now() - timedelta(hours=24) ).count(),
        timeout= 120)
    # total_orders = Orders.objects.filter(order_status = 'success', order_items__asset =asset_obj,payment_on__gte = now() - timedelta(hours=24) ).count()
    
    # related_products = Asset.objects.select_related('user','category').prefetch_related('tags','asset_preview_images','licenses','feedbacks','licenses__license').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).filter(status = 'published', category = asset_obj.category).exclude(pk = asset_obj.pk)[:6]
    related_products = cache.get_or_set(
        f'asset_detail_related_products_{asset_obj.category}_{asset_obj.pk}',
        default=Asset.objects.select_related('user','category').prefetch_related('tags','asset_preview_images','licenses','feedbacks','licenses__license').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).filter(status = 'published', category = asset_obj.category).exclude(pk = asset_obj.pk)[:6],
        timeout= 120)
    
    feedback_form = None
    if request.user.is_authenticated:
        order_item_obj = asset_obj.did_user_purchase(request.user)
        if order_item_obj:
            if request.method == 'POST':
                feedback_form = FeedbackForm(data = request.POST,initial={'user' : request.user, 'order' : order_item_obj.order,'asset' : asset_obj})
                if feedback_form.is_valid():
                    feedback_form.save()
                    messages.success(request, 'Feedback added successfully')
                    return redirect('assets:asset_detail', uuid = asset_obj.uuid)
                else:
                    messages.warning(request, 'Provide valid feedback')
            else:
                feedback_form = FeedbackForm(initial={'user' : request.user, 'order' : order_item_obj.order,'asset' : asset_obj})
            
    
    ctx = {
        "title" : f'{asset_obj.title} | ThemeMart',
        "asset_obj" : asset_obj,
        'total_orders' : total_orders,
        "related_products" : related_products,
    }
    
    if other_licenses:
        ctx['other_licenses'] = other_licenses
    if license:
        ctx['license'] = license
    if feedback_form:
        ctx['feedback_form'] = feedback_form
        
    return render(request, 'assets/asset_detail.html', ctx)

@login_required
def download_asset(request,order_uuid,pk):
    order_obj = get_object_or_404(Orders, uuid = order_uuid, user = request.user, order_status = 'success')
    order_item_obj = get_object_or_404(Order_Items,pk = pk, order = order_obj )
    
    asset_file_path = order_item_obj.asset.asset.path
    filename = str(slugify(order_item_obj.asset.title)) + '.'+ str(order_item_obj.asset.asset.name.split('.')[-1])
    response = FileResponse(open(asset_file_path, 'rb'), as_attachment=True, filename = filename)
    return response

@login_required
@seller_required
def delete_asset(request,pk):
    asset_obj = get_object_or_404(Asset, pk = pk, user = request.user)
    if asset_obj.status == 'published':
        messages.warning(request, 'Published Asset can\'t be deleted')
    else:
        asset_obj.delete()
        messages.success(request, 'Asset deleted successfully')
    return redirect('assets:my_assets')

@login_required
def delete_feedback(request,pk):
    assetfeedback_obj = get_object_or_404(AssetFeedback, pk = pk, user = request.user)
    assetfeedback_obj.delete()
    messages.warning(request, 'Feedback deleted successfully')
    return redirect('assets:asset_detail', uuid = assetfeedback_obj.asset.uuid)