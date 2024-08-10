from celery import Celery
from .models import Sell, Seller
from django.utils.timezone import now
from main.tasks import send_email
from celery import shared_task
from datetime import timedelta


app = Celery()

@shared_task(name='seller_payment')
def seller_payment():
    seller_objs = Seller.objects.all()
    for seller_obj in seller_objs:
        sell_objs = Sell.objects.filter(paid = False, seller = seller_obj.user, date_created__gte = now() - timedelta(minutes=7))
        if sell_objs:
            total_earning = 0
            commission = 0
            net_amount = 0
            bank_account_last4 = (str(seller_obj.bank_account_number))[-4:]
            for sell_obj in sell_objs:
                total_earning += float(sell_obj.asset_price)
                commission += (float(sell_obj.razorpay_payment_commision) + float(sell_obj.thememart_commision))
                net_amount += float(sell_obj.final_sell)
                sell_obj.paid = True
                sell_obj.paid_on = now()
                sell_obj.save()
            send_email(
                'ThemeMart Payment',
                {
                    'username' : seller_obj.user.username,
                    'total_earnings' : round(total_earning,2),
                    'commission' : round(commission,2),
                    'net_amount' : round(net_amount,2),
                    'bank_account_last4' : bank_account_last4,
                },
                'seller/emails/seller_payment.html',
                [seller_obj.user.email,],
            )