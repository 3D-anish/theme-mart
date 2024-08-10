from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from accounts.validators import username_validator
from accounts.helper_func import get_profile_image_path
from django_resized import ResizedImageField
import uuid
from main.tasks import send_email
from django.utils.html import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from django.templatetags.static import static

# Create your models here.

class User(AbstractUser):
    
    username = models.CharField(
        max_length=30,
        unique=True,
        error_messages= {
            "unique":"Username is not available.",
            "max_length":"Username is too long, Max - 30."
            },
        help_text = "a-z, 0-9 and underscore,dash & dot",
        validators = [username_validator,],
        verbose_name="Username",
    )
    
    first_name = None
    last_name = None
    
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator,],
        error_messages= {
            "unique":"Email ID is already register, try login",
            },
        help_text = "Only for security reasons",
        verbose_name="Email Id",
    )
    
    phone_number = PhoneNumberField(
        verbose_name = 'Phone Number',
        blank= True,
        null= True,
    )
    
    full_name = models.CharField(
        max_length =50,
        blank=True,
        null = True,
        error_messages ={
            "max_length" : "Name is too long, max - 50.",
        },
        verbose_name = "Full Name",
    )
    
    profile_image = ResizedImageField(
        size=[600, 600],
        crop=['middle', 'center'],
        quality=95,
        upload_to=get_profile_image_path,
        blank=True,
        null=True,
        verbose_name="Profile Image",
    )
    
    uuid = models.UUIDField(
        unique = True,
        verbose_name = "UUID",
        blank = True,
        null = True,
    )
    
    is_verified = models.BooleanField(
        default = False,
        verbose_name = 'Is Verified'
    )
    
    is_seller = models.BooleanField(
        default = False,
        verbose_name = 'Is Seller'
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
    
    
    def send_verification_link(self):
        if not self.uuid:
            self.uuid = uuid.uuid4()
            self.save()
        send_email.delay(
            subject="To verify your account at ThemeMart",
            ctx={"uuid" : self.uuid, "username" : self.username},
            template_path="accounts/emails/account_verification_link.html",
            recipient_list=[self.email,]
        )
    
    @property
    def profile_image_preview(self):
        if self.profile_image:
            return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.profile_image))
        else:
            return mark_safe('<img src="%s" width="150" height="150" />' % (static('images/profile.png')))
    
    def activate_account(self):
        self.is_active = True
        self.is_verified = True
        self.uuid = None
        self.save()
    
    def send_reset_password_link(self):
        self.uuid = uuid.uuid4()
        self.save()
        send_email.delay(
            subject="Someone requested for forgot password of the account with this email id",
            ctx = {'uuid' : self.uuid,},
            template_path= 'accounts/emails/reset_password_link.html',
            recipient_list=[self.email,]
        )
    
    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.username.replace("_"," ").replace("."," ").replace("-"," ").title()
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

