from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save
from .models import Asset_Preview_Images, Asset, Asset_Category
from django.core.files.storage import default_storage

@receiver(pre_save, sender = Asset_Category)
def delete_old_asset_category_image(sender, instance, **kwargs):

    if not instance.pk:
        return False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except:
        return False

    if not old_instance.image:
        return False

    if old_instance.image != instance.image:
        # Delete the old profile image file
        old_image_path = old_instance.image.path
        if default_storage.exists(old_image_path):
            default_storage.delete(old_image_path)
            
@receiver(pre_delete, sender = Asset_Category)
def delete_asset_category_image(sender,instance, **kwargs):
    if not instance.pk:
        return False
    
    if instance.image:
        instance.image.delete()

@receiver(pre_delete, sender = Asset_Preview_Images)
def delete_asset_preview_image(sender, instance, **kwargs):
    """
    Signal to delete asset preview image when user deletes it.
    """

    if not instance.pk:
        return False
    
    if instance.image:
        instance.image.delete()

@receiver(pre_delete, sender = Asset)
def delete_asset_file(sender, instance, **kwargs):
    """
    Signal to delete asset file when user deletes it.
    """

    if not instance.pk:
        return False
    
    if instance.asset:
        instance.asset.delete()
