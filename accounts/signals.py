from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage

@receiver(pre_save, sender = get_user_model())
def delete_old_profile_image(sender, instance, **kwargs):
    """
    Signal to delete old profile image of the user when user changes it.
    """

    if not instance.pk:
        return False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except:
        return False

    if not old_instance.profile_image:
        return False

    if old_instance.profile_image != instance.profile_image:
        # Delete the old profile image file
        old_image_path = old_instance.profile_image.path
        if default_storage.exists(old_image_path):
            default_storage.delete(old_image_path)
            
@receiver(pre_delete, sender = get_user_model())
def delete_profile_image(sender,instance, **kwargs):
    """
    Signal to delete  profile image of the user when user account deletes.
    """
    if not instance.pk:
        return False
    
    if instance.profile_image:
        instance.profile_image.delete()

