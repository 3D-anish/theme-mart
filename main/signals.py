from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.core.files.storage import default_storage
from .models import HomeBanner

@receiver(pre_save, sender = HomeBanner)
def delete_old_home_banner(sender, instance, **kwargs):

    if not instance.pk:
        return False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except:
        return False

    if not old_instance.banner:
        return False

    if old_instance.banner != instance.banner:
        # Delete the old profile image file
        old_image_path = old_instance.banner.path
        if default_storage.exists(old_image_path):
            default_storage.delete(old_image_path)
            
@receiver(pre_delete, sender = HomeBanner)
def delete_home_banner(sender,instance, **kwargs):
    if not instance.pk:
        return False
    
    if instance.banner:
        instance.banner.delete()