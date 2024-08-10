from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Seller

@receiver(post_save, sender = Seller)
def make_user_seller(created,sender, instance, **kwargs):
    if created:
        instance.user.is_seller = True
        instance.user.save()    

