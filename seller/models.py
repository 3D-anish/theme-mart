from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from .validators import account_number_validator, account_ifsc_code_validator, aadhar_card_number_validator
from orders.models import Orders, Order_Items
from assets.models import Asset
import uuid

# Create your models here.

class Seller(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        on_delete = models.CASCADE,
    )
    
    phone_number = PhoneNumberField(
        verbose_name = 'Phone Number',
    )
    
    bank_account_number = models.CharField(
        max_length= 100,
        verbose_name= 'Bank Account Number',
        validators= [account_number_validator,]
    )
    
    bank_account_ifsc_code = models.CharField(
        max_length= 100,
        verbose_name= 'Bank Account IFSC Code',
        validators= [account_ifsc_code_validator,]
    )
    
    aadhar_card_number = models.CharField(
        max_length= 50,
        verbose_name= 'Aadhar Card Number',
        validators=[aadhar_card_number_validator,]
    )
    
    date_created = models.DateTimeField(
        auto_now_add= True,
        verbose_name= ' Date Created'
    )
    
    class Meta:
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
        ordering = ["-date_created"]
    
    def __str__(self):
        return f'{self.user.username} - {self.phone_number}'
    
class Sell(models.Model):
    seller = models.ForeignKey(
        get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= 'Seller',
    )
    
    order_id = models.ForeignKey(
        Orders,
        on_delete= models.CASCADE,
        verbose_name= 'Order',
    )
    
    order_item = models.ForeignKey(
        Order_Items,
        on_delete= models.CASCADE,
        verbose_name= ' Order Item',
    )
    
    asset = models.ForeignKey(
        Asset,
        on_delete= models.CASCADE,
        verbose_name= 'Asset',
        related_name= 'sells'
    )
    
    uuid = models.UUIDField(
        unique= True,
        default= uuid.uuid4,
        verbose_name= 'UUID',
    )
    
    asset_price = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        verbose_name= 'Asset Price',
    )
    
    razorpay_payment_commision = models.DecimalField(
        max_digits= 10,
        decimal_places=2,
        default= 0,
        verbose_name= 'Razorpay Payment Commision',
    )
    
    thememart_commision = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        default= 0,
        verbose_name= 'ThemeMart Commision',
    )
    
    final_sell = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        default= 0,
        verbose_name= 'Final Sale Amount',
    )
    
    paid = models.BooleanField(
        default=False,
        verbose_name= 'Is Paid?',
    )
    
    paid_on = models.DateTimeField(
        blank= True,
        null= True,
        verbose_name= 'Paid On',
    )
    
    date_created = models.DateTimeField(
        auto_now_add= True,
        verbose_name= 'Date Created',
    )
    
    class Meta:
        verbose_name = "Sell"
        verbose_name_plural = "Sells"
        ordering = ["-date_created"]
        
    def __str__(self):
        return f'{self.uuid} - {self.final_sell}'