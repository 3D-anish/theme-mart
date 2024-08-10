from celery import shared_task
from main.tasks import send_email
import os
from orders.models import Orders

@shared_task
def send_success_order_email_task(order_pk,invoice_path, licenses_paths):

    order_obj = Orders.objects.get(pk = order_pk)

    with open(invoice_path, 'rb') as f:
        invoice_content = f.read()
    
    attchament_list = [['invoice.pdf',invoice_content,'application/pdf']]
    for license_path in licenses_paths:
        with open(license_path, 'rb') as f:
            license_content = f.read()
        attchament_list.append(['license.pdf', license_content,'application/pdf'])

    send_email(
        subject= 'Order Success | ThemeMart',
        ctx = {
            'order_obj' : order_obj,
            'order_item_objs' : order_obj.orders_items.all(),
        },
        template_path= 'orders/emails/order_success.html',
        recipient_list= [order_obj.user.email],
        attchament_list= attchament_list,
    )
    if os.path.exists(invoice_path):
        os.remove(invoice_path)
    for license_path in licenses_paths:
        if os.path.exists(license_path):
            os.remove(license_path)