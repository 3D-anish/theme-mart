from django.db import models
from assets.models import Asset
from license.models import License
from django.contrib.auth import get_user_model
import uuid
from django.utils.timezone import now
import razorpay
from django.conf import settings
from django.template.loader import get_template
from phonenumber_field.modelfields import PhoneNumberField
from orders.helper_func import html_to_pdf
import os

# Create your models here.

order_status = {
    'pending' : 'Pending',
    'success' : 'Success',
    'canceled' : 'Canceled',
    'failed' : 'Failed',
}

class Orders(models.Model):
    
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name= 'User',
    )
    
    user_email = models.EmailField(
        blank= True,
        default='',
        null= True,
        verbose_name= 'User Email',
    )
    
    user_phonenumber = PhoneNumberField(
        verbose_name = 'User Phone Number',
        blank= True,
        null= True,
    )
    
    user_full_name = models.CharField(
        max_length= 200,
        default='',
        blank= True,
        null= True,
        verbose_name= 'User Full Name',
    )
    
    uuid = models.UUIDField(
        default= uuid.uuid4,
        unique=True,
        verbose_name= 'UUID',
    )
    
    order_items = models.ManyToManyField(
        'Order_Items',
        verbose_name= 'Order Items',
    )
    
    order_status = models.CharField(
        max_length=100,
        choices= order_status,
        default= 'pending',
        verbose_name= 'Order Status',
    )
    
    sub_total = models.DecimalField(
        max_digits= 20,
        decimal_places= 2,
        default= 0,
        verbose_name= 'Sub Total',
    )
    
    gst = models.DecimalField(
        max_digits= 15,
        decimal_places= 2,
        default= 0,
        verbose_name= 'GST',
    )
    
    total_price = models.DecimalField(
        max_digits= 20,
        decimal_places= 2,
        default= 0,
        verbose_name= 'Total Price',
    )
    
    total_payment_recieved = models.DecimalField(
        max_digits= 20,
        decimal_places= 2,
        default= 0,
        verbose_name= 'Total Payment Recevied',
    )
    
    date_created = models.DateTimeField(
        auto_now_add= True,
        verbose_name= ' Date Created',
    )
    
    payment_on = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name= 'Payment Date',
    )
    
    razorpay_order_id = models.CharField(
        max_length= 400, 
        blank= True,
        null=True,
        verbose_name= 'Razorpay Order ID',
    )
    
    razorpay_payment_id = models.CharField(
        max_length= 400, 
        null=True,
        blank= True,
        verbose_name= 'Razorpay Payment ID',
    )
    
    razorpay_payment_signature = models.CharField(
        max_length= 400, 
        null=True,
        blank= True,
        verbose_name= 'Razorpay Payment Signature',
    )
    
    razorpay_payment_fee = models.DecimalField(
        max_digits= 10,
        decimal_places=2,
        default= 0,
        verbose_name= 'Razorpay Payment Fee',
    )
    
    razorpay_payment_tax = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        default= 0,
        verbose_name= 'Razorpay Payment Tax',
    )
    
    other_razorpay_payment_details = models.JSONField(
        blank=True,
        null=True,
        verbose_name= 'Other Razorpay Payment Details',
    )
    
    address_line_1 = models.CharField(
        max_length= 200,
        blank= True,
        null=True,
        default= '',
        verbose_name= 'Address Line 1',
    )
    
    address_line_2 = models.CharField(
        max_length= 200,
        blank= True,
        null= True,
        default= '',
        verbose_name= 'Address Line 2',
    )
    
    address_area = models.CharField(
        blank= True,
        null=True,
        max_length= 200,
        default= '',
        verbose_name= 'Address Area',
    )
    
    address_city = models.CharField(
        blank= True,
        null=True,
        max_length= 100,
        default= '',
        verbose_name= 'Address City',
    )
    
    address_state = models.CharField(
        blank= True,
        max_length= 100,
        default= '',
        null= True,
        verbose_name= 'Address State',
    )
    
    address_pincode = models.CharField(
        max_length= 6,
        default= '',
        null=True,
        blank=True,
        verbose_name= 'Address Pincode',
    )
    
    gst_number = models.CharField(
        max_length= 40,
        blank= True,
        null=True,
        verbose_name= 'GST Number'
    )
    
    def __str__(self):
        return str(self.user.username + ' - ' + str(self.uuid) + ' - ' + str(self.get_order_status_display()))
    
    def generate_razorpay_order_id(self):
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        razorpay_order = client.order.create(
            {"amount": float(self.total_price) * 100, "currency": "INR", "payment_capture": "1"}
        )
    
        self.razorpay_order_id = razorpay_order['id']
        self.save()
        return self
    
    def order_success(self,razorpay_payment_id,razorpay_signature):
        self.order_status = 'success'
        self.razorpay_payment_id = razorpay_payment_id
        self.razorpay_payment_signature = razorpay_signature
        
        try:
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            razorpay_order_data = client.payment.fetch(self.razorpay_payment_id)
            if razorpay_order_data:
                if razorpay_order_data.get('status') == 'captured':
                    self.total_payment_recieved = razorpay_order_data.get('amount') / 100
                    self.payment_on = now()
                    self.razorpay_payment_fee = razorpay_order_data.get('fee') / 100
                    self.razorpay_payment_tax = razorpay_order_data.get('tax') / 100
                    self.other_razorpay_payment_details = razorpay_order_data
                    order_items_objs = self.orders_items.all()
                    for order_item_obj in order_items_objs:
                        percentage = (float(order_item_obj.price) * 100) / float(self.sub_total)
                        order_item_obj.razorpay_payment_commision = (percentage * (float(self.razorpay_payment_fee) + float(self.razorpay_payment_tax))) / 100
                        order_item_obj.gst = (percentage * float(self.gst)) / 100
                        order_item_obj.save()
                        from seller.models import Sell
                        sell_obj = Sell.objects.create(
                            seller = order_item_obj.asset.user,
                            order_id = self,
                            order_item = order_item_obj,
                            asset = order_item_obj.asset,
                            asset_price = float(order_item_obj.price),
                            razorpay_payment_commision = float(order_item_obj.razorpay_payment_commision),
                        )
                        sell_obj.thememart_commision = float(float(sell_obj.asset_price)-float(sell_obj.razorpay_payment_commision)) * 0.15
                        sell_obj.final_sell = float(float(sell_obj.asset_price) - float(sell_obj.razorpay_payment_commision)) - float(sell_obj.thememart_commision)
                        sell_obj.save()
        except Exception as e:
            print(e)
        self.save()
        self.send_success_order_email()
        return self
    
    def send_success_order_email(self):
        from .tasks import send_success_order_email_task
        invoice_path = self.generate_invoice()
        licenses_paths = self.generate_licenses()
        # 5.64 <- 11.50
        send_success_order_email_task.delay(self.pk, invoice_path, licenses_paths)
            
    def generate_invoice(self):
        output_path = os.path.join(settings.MEDIA_DIR, 'orders', 'invoice', f'invoice_{self.pk}.pdf')
        if os.path.exists(output_path):
            return output_path 
        ctx = {
            'order_obj' : self,
            'order_item_objs' : self.orders_items.all(),
        }
        template = get_template('orders/invoice/invoice.html')
        html = template.render(ctx)
        html_to_pdf(html,output_path)
        return output_path
    
    def generate_licenses(self):
        order_item_objs = self.orders_items.all()
        licenses_paths = []
        for order_itme_obj in order_item_objs:
            ctx = {
                'order_obj' : self,
                'order_itme_obj' : order_itme_obj,
            }
            template = get_template('orders/license/license.html')
            html = template.render(ctx)
            output_path = os.path.join(settings.MEDIA_DIR, 'orders','licenses', f'license_{order_itme_obj.pk}.pdf')
            if os.path.exists(output_path):
                licenses_paths.append(output_path)
            else:
                html_to_pdf(html,output_path)
                licenses_paths.append(output_path)
        return licenses_paths
        
    def save(self, *args, **kwargs):
        if self.user_email == '' or self.user_email == None:
            self.user_email = self.user.email
        if self.user_full_name == '' and self.user.full_name:
            self.user_full_name = self.user.full_name
        if self.user_phonenumber == '' and self.user.phone_number:
            self.user_phonenumber = self.user.phone_number
        if self.address_line_1 == '' and self.user.address_line_1:
            self.address_line_1 = self.user.address_line_1
        if self.address_line_2 == '' and self.user.address_line_2:
            self.address_line_2 = self.user.address_line_2
        if self.address_area == '' and self.user.address_area:
            self.address_area = self.user.address_area
        if self.address_city == '' and self.user.address_city:
            self.address_city = self.user.address_city
        if self.address_state == '' and self.user.address_state:
            self.address_state = self.user.address_state
        if self.address_pincode == '' and self.user.address_pincode:
            self.address_pincode = self.user.address_pincode
        if self.gst_number == '' and self.user.gst_number:
            self.gst_number = self.user.gst_number
        
        super().save(*args, **kwargs)
    
    @property
    def is_eligibale_for_payment(self):
        if self.user and self.user_email and self.user_phonenumber and self.user_full_name and self.address_line_1 and self.address_line_2 and self.address_area and self.address_city and self.address_state and self.address_pincode:
            return True
        return False
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-date_created"]
    
class Order_Items(models.Model):
    
    order = models.ForeignKey(
        Orders,
        on_delete= models.CASCADE,
        related_name= 'orders_items',
        verbose_name= 'Order',
    )
    
    asset = models.ForeignKey(
        Asset,
        on_delete= models.CASCADE,
        verbose_name= 'Asset',
    )
    
    license = models.ForeignKey(
        License,
        on_delete= models.CASCADE,
        verbose_name= 'License',
    )
    
    price = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        default= 0,
        verbose_name= 'Price'
    )
    
    gst = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        default= 0,
        verbose_name= 'GST',
    )
    
    razorpay_payment_commision = models.DecimalField(
        max_digits= 10,
        decimal_places=2,
        default= 0,
        verbose_name= 'Razorpay Payment Commision',
    )
    
    date_created = models.DateTimeField(
        auto_now_add= True,
        verbose_name= 'Date Created'
    )
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["-date_created"]
    
    def __str__(self):
        return str(str(self.order.uuid)  + ' - ' + self.asset.title)
