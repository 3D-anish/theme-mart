from django.shortcuts import render
from assets.models import Asset
from .helper_func import get_paginated_objs
from orders.models import Order_Items
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Avg, Count
from django.core.cache import cache
from .models import HomeBanner
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Orders, Order_Items
from seller.models import Sell, Seller
from assets.models import Asset

def home(request):
    image_asset_objs = cache.get_or_set(
        'home_image_asset_objs',
        default=Asset.objects.select_related('user','category').prefetch_related('tags', 'asset_preview_images', 'licenses', 'feedbacks','licenses__license','licenses__license__asset_category').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).filter(status = 'published', category__slug = 'image').order_by('date_published')[:8],
        timeout= 120)
    
    web_tem_asset_objs = cache.get_or_set(
        'home_web_tem_asset_objs',
        default=Asset.objects.select_related('user','category').prefetch_related('tags', 'asset_preview_images', 'licenses', 'feedbacks','licenses__license','licenses__license__asset_category').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).filter(status = 'published', category__slug = 'website-template').order_by('date_published')[:8],
        timeout= 120)
    
    ppt_tem_asset_objs = cache.get_or_set(
        'home_ppt_tem_asset_objs',
        default=Asset.objects.select_related('user','category').prefetch_related('tags', 'asset_preview_images', 'licenses', 'feedbacks','licenses__license','licenses__license__asset_category').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).filter(status = 'published', category__slug = 'ppt-templates').order_by('date_published')[:8],
        timeout= 120)
    
    ebook_asset_objs = cache.get_or_set(
        'home_ebook_asset_objs',
        default=Asset.objects.select_related('user','category').prefetch_related('tags', 'asset_preview_images', 'licenses', 'feedbacks','licenses__license','licenses__license__asset_category').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).filter(status = 'published', category__slug = 'e-books').order_by('date_published')[:8],
        timeout= 120)
        
    trending_asset_objs = cache.get('home_trending_asset_objs')
    if not trending_asset_objs:
        trending_asset_objs = Asset.objects.select_related('user','category').prefetch_related('tags', 'asset_preview_images', 'licenses', 'feedbacks','licenses__license','licenses__license__asset_category').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).filter(status = 'published')[:8]
        trending_asset_objs = sorted(trending_asset_objs, key= lambda t: -Order_Items.objects.filter(asset = t, order__order_status = 'success', order__payment_on__gte = now() - timedelta(days=7)).count())
        cache.set('home_trending_asset_objs', trending_asset_objs, timeout=120)
    
    banners = cache.get_or_set(
        'home_banners',
        default=HomeBanner.objects.all(),
        timeout= 120)
    ctx = {
        'title' : 'ThemeMart',
        'image_asset_objs' : image_asset_objs,
        'web_tem_asset_objs' : web_tem_asset_objs,
        'ppt_tem_asset_objs' : ppt_tem_asset_objs,
        'ebook_asset_objs' : ebook_asset_objs,
        'trending_asset_objs' : trending_asset_objs,
        'banners' : banners,
    }
    return render(request, 'index.html', ctx)

def shop(request):
    q = request.GET.get('q')
    category = request.GET.get('category')
    if q and category:
        asset_objs = cache.get_or_set(
        f'shop_asset_objs_q_{q}_category_{category}',
        default=Asset.objects.select_related('user','category').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).prefetch_related('tags', 'asset_preview_images', 'licenses','feedbacks','licenses__license', 'licenses__license__asset_category').filter(status = 'published',title__icontains = q,category__slug = category),
        timeout= 120)
    elif q:
        asset_objs = cache.get_or_set(
        f'shop_asset_objs_q_{q}',
        default=Asset.objects.select_related('user','category').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).prefetch_related('tags', 'asset_preview_images', 'licenses','feedbacks','licenses__license', 'licenses__license__asset_category').filter(status = 'published',title__icontains = q),
        timeout= 120)
    elif category:
        asset_objs = cache.get_or_set(
        f'shop_asset_objs_category_{category}',
        default=Asset.objects.select_related('user','category').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).prefetch_related('tags', 'asset_preview_images', 'licenses','feedbacks','licenses__license', 'licenses__license__asset_category').filter(status = 'published',category__slug = category),
        timeout= 120)
    else:
        asset_objs = cache.get_or_set(
        'shop_asset_objs',
        default=Asset.objects.select_related('user','category').annotate(rating = Avg('feedbacks__rating'), total_rating = Count('feedbacks')).prefetch_related('tags', 'asset_preview_images', 'licenses','feedbacks','licenses__license', 'licenses__license__asset_category').filter(status = 'published'),
        timeout= 120)
    
    ctx = {
        'title' : 'Shop | ThemeMart',
        'asset_objs' : get_paginated_objs(asset_objs,request.GET.get("page", 1),12),
    }
    
    return render(request, 'main/shop.html', ctx)

def cart(request):
    ctx = {
        'title' : 'Cart | ThemeMart',
    }
    return render(request, 'main/cart.html', ctx)

@staff_member_required
def thememart_dashboard(request):
    total_assets = Asset.objects.filter(status = 'published').count()
    last_24_hours_new_assets = Asset.objects.filter(status = 'published',date_published__gte = now() - timedelta(hours=24)).count()
    last_7_days_new_assets = Asset.objects.filter(status = 'published',date_published__gte = now() - timedelta(days=7)).count()
    last_30_days_new_assets = Asset.objects.filter(status = 'published',date_published__gte = now() - timedelta(days=30)).count()
    
    total_orders = Orders.objects.filter(order_status = 'success').count()
    last_24_hours_orders = Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(hours=24)).count()
    last_7_days_orders = Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(days=7)).count()
    last_30_days_orders = Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(days=30)).count()
    
    total_orders_value = sum(order.total_price for order in Orders.objects.filter(order_status = 'success'))
    total_last_24_hours_orders_value = sum(order.total_price for order in Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(hours=24)))
    total_last_7_days_orders_value = sum(order.total_price for order in Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(days=30)))
    total_last_30_days_orders_value = sum(order.total_price for order in Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(days=7)))
    
    total_orders_subtotal = sum(order.sub_total for order in Orders.objects.filter(order_status = 'success'))
    total_last_24_hours_orders_subtotal = sum(order.sub_total for order in Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(hours=24)))
    total_last_7_days_orders_subtotal = sum(order.sub_total for order in Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(days=30)))
    total_last_30_days_orders_subtotal = sum(order.sub_total for order in Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(days=7)))
    
    total_gst_collected = sum(order.gst for order in Orders.objects.filter(order_status = 'success'))
    total_last_24_hours_gst_collected = sum(order.gst for order in Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(hours=24)))
    total_last_7_days_gst_collected = sum(order.gst for order in Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(days=7)))
    total_last_30_days_gst_collected = sum(order.gst for order in Orders.objects.filter(order_status = 'success',payment_on__gte = now() - timedelta(days=30)))
    
    total_seller = Seller.objects.all().count()
    
    total_razorpay_commission = sum(sell.razorpay_payment_commision for sell in Sell.objects.all())
    total_last_24_hours_razorpay_commission = sum(sell.razorpay_payment_commision for sell in Sell.objects.filter(date_created__gte = now() - timedelta(hours=24)))
    total_last_7_days_razorpay_commission = sum(sell.razorpay_payment_commision for sell in Sell.objects.filter(date_created__gte = now() - timedelta(days=7)))
    total_last_30_days_razorpay_commission = sum(sell.razorpay_payment_commision for sell in Sell.objects.filter(date_created__gte = now() - timedelta(days=30)))
    
    total_thememart_commission = sum(sell.thememart_commision for sell in Sell.objects.all())
    total_last_24_hours_thememart_commission = sum(sell.thememart_commision for sell in Sell.objects.filter(date_created__gte = now() - timedelta(hours=24)))
    total_last_7_days_thememart_commission = sum(sell.thememart_commision for sell in Sell.objects.filter(date_created__gte = now() - timedelta(days=7)))
    total_last_30_days_thememart_commission = sum(sell.thememart_commision for sell in Sell.objects.filter(date_created__gte = now() - timedelta(days=30)))
    
    total_seller_payment = sum(sell.final_sell for sell in Sell.objects.filter(paid = True))
    total_last_24_hours_seller_payment = sum(sell.final_sell for sell in Sell.objects.filter(paid = True,paid_on__gte = now() - timedelta(hours=24)))
    total_last_7_days_seller_payment = sum(sell.final_sell for sell in Sell.objects.filter(paid = True,paid_on__gte = now() - timedelta(days=7)))
    total_last_30_days_seller_payment = sum(sell.final_sell for sell in Sell.objects.filter(paid = True,paid_on__gte = now() - timedelta(days=30)))
    
    to_be_paid = sum(sell.final_sell for sell in Sell.objects.filter(paid = False))
    
    context = {
        "title" : 'ThemeMart Dashboard',
        'total_assets' :total_assets,
        'last_24_hours_new_assets' :last_24_hours_new_assets,
        'last_7_days_new_assets' :last_7_days_new_assets,
        'last_30_days_new_assets' :last_30_days_new_assets,
        
        'total_orders' :total_orders,
        'last_24_hours_orders' :last_24_hours_orders,
        'last_7_days_orders' :last_7_days_orders,
        'last_30_days_orders' :last_30_days_orders,
        
        'total_orders_value' :total_orders_value,
        'total_last_24_hours_orders_value' :total_last_24_hours_orders_value,
        'total_last_7_days_orders_value' :total_last_7_days_orders_value,
        'total_last_30_days_orders_value' :total_last_30_days_orders_value,
        
        'total_seller' : total_seller,
        
        "total_gst_collected" : total_gst_collected,
        "total_last_24_hours_gst_collected" : total_last_24_hours_gst_collected,
        "total_last_7_days_gst_collected" : total_last_7_days_gst_collected,
        "total_last_30_days_gst_collected" : total_last_30_days_gst_collected,
        
        "total_razorpay_commission" : total_razorpay_commission,
        "total_last_24_hours_razorpay_commission" : total_last_24_hours_razorpay_commission,
        "total_last_7_days_razorpay_commission" : total_last_7_days_razorpay_commission,
        "total_last_30_days_razorpay_commission" : total_last_30_days_razorpay_commission,
        
        "total_thememart_commission" : total_thememart_commission,
        "total_last_24_hours_thememart_commission" : total_last_24_hours_thememart_commission,
        "total_last_7_days_thememart_commission" : total_last_7_days_thememart_commission,
        "total_last_30_days_thememart_commission" : total_last_30_days_thememart_commission,
        
        "total_seller_payment" : total_seller_payment,
        "total_last_24_hours_seller_payment" : total_last_24_hours_seller_payment,
        "total_last_7_days_seller_payment" : total_last_7_days_seller_payment,
        "total_last_30_days_seller_payment" : total_last_30_days_seller_payment,
        
        "to_be_paid" : to_be_paid,
        
        "total_orders_subtotal" : total_orders_subtotal,
        "total_last_24_hours_orders_subtotal" : total_last_24_hours_orders_subtotal,
        "total_last_7_days_orders_subtotal" : total_last_7_days_orders_subtotal,
        "total_last_30_days_orders_subtotal" : total_last_30_days_orders_subtotal,
    }
    return render(request, 'admin/thememart_dashboard.html', context)