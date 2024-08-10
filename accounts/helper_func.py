import os
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model

def get_profile_image_path(instance, filename):
    file = filename.split(".")
    new_filename = f"profile_image_{instance.pk}.{file[-1]}"
    return os.path.join('users', 'profile_images', new_filename)

def get_user_object_from_username_or_email(username_or_email):
    email_validator = EmailValidator()
    try:
        email_validator(username_or_email)
        user_obj = get_user_model().objects.filter(email = username_or_email).first()
    except:
        user_obj = get_user_model().objects.filter(username = username_or_email).first()
    return user_obj