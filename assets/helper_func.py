import os
from django.utils.crypto import get_random_string

def get_asset_category_image_path(instance, filename):
    file = filename.split(".")
    new_filename = f"asset_category_{instance.slug}.{file[-1]}"
    return os.path.join('assets','asset_category', new_filename)

def get_asset_preview_image_path(instance, filename):
    file = filename.split(".")
    new_filename = f"preview_image_{get_random_string(length = 5)}.{file[-1]}"
    # return os.path.join('users', f'{instance.asset.user.pk}', 'assets', f'{instance.asset.uuid}', 'asset_preview_images', new_filename)
    return os.path.join('assets','asset_preview_images', new_filename)

def get_asset_path(instance, filename):
    file = filename.split(".")
    new_filename = f"asset_file_{get_random_string(length = 32)}.{file[-1]}"
    # return os.path.join('users', f'{instance.user.pk}', 'assets', f'{instance.pk}', f'{get_random_string(20)}', new_filename)
    return os.path.join('assets', 'asset_files', new_filename)