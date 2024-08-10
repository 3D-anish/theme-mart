from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Orders, Order_Items
from assets.models import Asset
from license.models import Asset_License
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from .helper_func import verify_signature
from .forms import EditOrderDetailForm
from main.helper_func import get_paginated_objs
from cryptography.fernet import Fernet

# Create your views here.

@login_required
def create_order(request):
    if not request.method == 'POST':
        messages.warning(request, 'Invalid request.')
        if request.headers.get('Referer'):
            return redirect(request.headers.get('Referer'))
        else:
            return redirect("main:home")
    
    data = dict(request.POST.copy())
    assets = data.get('assets')
    assets_list = []
    
    for i in assets:
        asset_pk, license_pk = tuple(str(i).split('_'))
        
        asset_obj = Asset.objects.filter(pk = asset_pk,status = 'published').first()
        if not asset_obj:
            messages.warning(request, 'Unable to found Asset')
            if request.headers.get('Referer'):
                return redirect(request.headers.get('Referer'))
            else:
                return redirect("main:home")
        
        asset_license_obj = Asset_License.objects.filter(pk = license_pk, asset = asset_obj).first()
        if not asset_license_obj:
            messages.warning(request, "Unable to found Asset License")
            if request.headers.get('Referer'):
                return redirect(request.headers.get('Referer'))
            else:
                return redirect("main:home")
        
        add = True
        for asset in assets_list:
            if asset_obj == asset.get('asset_obj'):
                add = False
                break
        
        if add:
            assets_list.append(
                {
                    'asset_obj' : asset_obj,
                    'asset_license_obj' : asset_license_obj,
                }
            )
    
    if assets_list:
        order_obj = Orders.objects.create(
            user = request.user,
        )
        order_obj.save()
        sub_total = 0
        
        for i in assets_list:
            order_item_obj = Order_Items.objects.create(
                order = order_obj,
                asset = i['asset_obj'],
                license = i['asset_license_obj'].license,
                price = i['asset_license_obj'].price,
            )
            order_item_obj.save()
            order_obj.order_items.add(order_item_obj)
            sub_total += order_item_obj.price
        
        order_obj.sub_total = sub_total
        order_obj.gst = 0.18 * float(sub_total)
        order_obj.total_price = float(sub_total) + float(order_obj.gst)
        order_obj.save()
    
        return redirect("orders:checkout", uuid = order_obj.uuid)
    else:
        messages.warning(request, 'No asset found')
        if request.headers.get('Referer'):
                return redirect(request.headers.get('Referer'))
        else:
            return redirect("main:home")

@login_required
def checkout(request, uuid):
    order_obj = get_object_or_404(Orders.objects.select_related('user'), uuid = uuid,user = request.user, order_status = 'pending')
    order_item_objs = Order_Items.objects.select_related('asset','license').filter(order = order_obj)
    
    if request.method == 'POST':
        form = EditOrderDetailForm(data = request.POST, instance = order_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Detail saved successfully')
            return redirect("orders:checkout",uuid = order_obj.uuid)
    else:
        form = EditOrderDetailForm(instance = order_obj)
    
    if not order_obj.razorpay_order_id:
        order_obj = order_obj.generate_razorpay_order_id()
    
    callback_url = "http://" + f"{settings.SITE_DOMAIN}" + str(reverse_lazy("orders:payment_callback", kwargs={'uuid' : order_obj.uuid}))
    
    ctx = {
        'title' : f"Checkout | {order_obj.uuid} | ThemeMart",
        "order_obj" : order_obj,
        "order_item_objs" : order_item_objs,
        "callback_url": callback_url,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "form" : form,
    }
    return render(request, 'orders/checkout.html', ctx)

@csrf_exempt
def payment_callback(request, uuid):
    keycipher_suite = Fernet.generate_key()
    cipher_suite = Fernet(keycipher_suite)
    
    razorpay_payment_id = str(request.POST.get("razorpay_payment_id", ""))
    razorpay_order_id = str(request.POST.get("razorpay_order_id", ""))
    razorpay_signature = str(request.POST.get("razorpay_signature", ""))
    
    encoded_razorpay_payment_id = cipher_suite.encrypt(razorpay_payment_id.encode('utf-8')).decode("utf-8")
    encoded_razorpay_order_id = cipher_suite.encrypt(razorpay_order_id.encode('utf-8')).decode("utf-8")
    encoded_razorpay_signature = cipher_suite.encrypt(razorpay_signature.encode('utf-8')).decode("utf-8")
    
    keycipher_suite = keycipher_suite.decode("utf-8")
    
    url = "http://" + f"{settings.SITE_DOMAIN}" + str(reverse_lazy("orders:order_success", kwargs={'uuid' : uuid})) + f'?encrkey={keycipher_suite}&payidraz={encoded_razorpay_payment_id}&payodidraz={encoded_razorpay_order_id}&paysigraz={encoded_razorpay_signature}'
    
    return redirect(url)

@login_required
def order_success(request, uuid):
    order_obj = get_object_or_404(Orders.objects.select_related('user'), uuid = uuid,user = request.user, order_status = 'pending')
    order_item_objs = Order_Items.objects.select_related('asset','license').filter(order = order_obj)
    
    cipher_suite = Fernet(request.GET.get("encrkey", "").encode('utf-8'))
    
    encoded_razorpay_payment_id = request.GET.get("payidraz", "").encode('utf-8')
    encoded_razorpay_order_id = request.GET.get("payodidraz", "").encode('utf-8')
    encoded_razorpay_signature = request.GET.get("paysigraz", "").encode('utf-8')
    
    razorpay_payment_id = cipher_suite.decrypt(encoded_razorpay_payment_id).decode("utf-8")
    razorpay_order_id = cipher_suite.decrypt(encoded_razorpay_order_id).decode("utf-8")
    razorpay_signature = cipher_suite.decrypt(encoded_razorpay_signature).decode("utf-8")
    
    if verify_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature) and order_obj.razorpay_order_id == razorpay_order_id:
        order_obj = order_obj.order_success(razorpay_payment_id= razorpay_payment_id, razorpay_signature= razorpay_signature)
        messages.success(request, 'Order placed successfully')
    else:
        order_obj.save()
        messages.warning(request, 'Order Failed')
        return redirect('orders:checkout', uuid = order_obj.uuid)
        
    ctx = {
        "title" : f'Order Success | {order_obj.uuid} | ThemeMart',
        "order_obj" : order_obj,
        "order_item_objs" : order_item_objs,
    }
    return render(request, 'orders/order_success.html', ctx)

def cancel_order(request, uuid):
    order_obj = get_object_or_404(Orders, uuid = uuid, user = request.user,order_status = 'pending')
    order_obj.order_status = 'canceled'
    order_obj.save()
    messages.warning(request, 'Order Cancelled')
    return redirect('main:home')
    
def my_orders(request):
    order_objs = Orders.objects.select_related('user').prefetch_related('order_items').filter(user = request.user)
    
    ctx = {
        'title' : 'My Orders | ThemeMart',
        'order_objs' : get_paginated_objs(order_objs,request.GET.get("page", 1),5),
    }
    return render(request, 'orders/my_orders.html', ctx)

def order_details(request, uuid):
    order_obj = get_object_or_404(Orders.objects.select_related('user'), uuid = uuid,user = request.user)
    order_item_objs = get_list_or_404(Order_Items.objects.select_related('asset', 'license', 'license__asset_category'), order = order_obj)
    ctx = {
        'title' : f'Order Details | {order_obj.uuid} | ThemeMart',
        'order_obj' : order_obj,
        'order_item_objs' : order_item_objs,
    }
    return render(request, 'orders/order_details.html', ctx)
    