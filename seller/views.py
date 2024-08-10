from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateSellerForm, EditSellerForm
from django.contrib import messages
from main.tasks import send_email
from .decorators import seller_required
from orders.models import Orders, Order_Items
from assets.models import Asset
from .models import Sell, Seller
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model
from main.helper_func import get_paginated_objs
from django.db.models import Avg, Count


# Create your views here.

@login_required
def become_seller(request):
    if request.user.is_seller:
        messages.warning(request, 'You are seller already')
        if request.headers.get('Referer'):
            return redirect(request.headers.get('Referer'))
        else:
            return redirect("main:home")
    
    if request.method == 'POST':
        data = request.POST.copy()
        data['user'] = request.user
        form = CreateSellerForm(data= data)
        if form.is_valid():
            form.save()
            send_email.delay(
                'Successfully registered for seller account on ThemeMart',
                {'username' : request.user.username},
                'seller/emails/register_successful.html',
                [request.user.email,]
            )
            messages.success(request,'Seller account successfully created.')
            return redirect('main:home')
        else:
            messages.warning(request, 'Provide Valid Details')
    else:
        form = CreateSellerForm()
    
    ctx = {
        'title' : 'Become Seller | ThemeMart',
        'form' : form,
    }
    return render(request, 'seller/become_seller.html', ctx)

@seller_required
def dashboard(request):
    if request.method == 'POST':
        form = EditSellerForm(data= request.POST, instance= request.user.seller)
        if form.is_valid():
            form.save()
            messages.success(request, 'Details Saved Successfully')
            return redirect('seller:dashboard')
        else:
            messages.warning(request, 'Provide Details')
    else:
        form = EditSellerForm(instance=request.user.seller)
    
    asset_objs = Asset.objects.filter(user = request.user,status = 'published')
    sell_objs = Sell.objects.filter(seller = request.user)
    # total_earning = sum(sell.final_sell for sell in sell_objs)
    last_24_hours_earning = sum(sell.final_sell for sell in sell_objs.filter(date_created__gte = now() - timedelta(hours=24)))
    last_7_days_earning = sum(sell.final_sell for sell in sell_objs.filter(date_created__gte = now() - timedelta(days=7)))
    last_30_days_earning = sum(sell.final_sell for sell in sell_objs.filter(date_created__gte = now() - timedelta(days=30)))
    to_be_paid = sum(sell.final_sell for sell in sell_objs.filter(paid = False))
    last_7_paid = sum(sell.final_sell for sell in sell_objs.filter(paid = True,paid_on__gte = now() - timedelta(days=7)))
    last_30_paid = sum(sell.final_sell for sell in sell_objs.filter(paid = True,paid_on__gte = now() - timedelta(days=30)))
    
    ctx = {
        'title' : 'Seller DashBoard | ThemeMart',
        'asset_objs' : asset_objs,
        'sell_objs' : sell_objs,
        'last_24_hours_earning' : last_24_hours_earning,
        'last_7_days_earning' : last_7_days_earning,
        'last_30_days_earning' : last_30_days_earning,
        'to_be_paid' : to_be_paid,
        'last_7_paid' : last_7_paid,
        'last_30_paid' : last_30_paid,
        'form' : form,
    }
    return render(request, 'seller/dashboard.html', ctx)

def seller_store(request, username):
    user_obj = get_object_or_404(get_user_model(), username = username, is_seller = True)
    asset_objs = Asset.objects.select_related('user','category').prefetch_related('tags', 'asset_preview_images', 'licenses').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).filter(user = user_obj)
    if user_obj != request.user:
        asset_objs = asset_objs.filter(status = 'published')
    if request.GET.get('category'):
        asset_objs = asset_objs.filter(category__slug = request.GET.get('category'))
    ctx = {
        'title' : f'Seller | @{user_obj.username} | ThemeMart',
        'user_obj' : user_obj,
        'asset_objs' : get_paginated_objs(asset_objs,request.GET.get("page", 1),12),
    }
    return render(request, 'seller/seller.html', ctx)