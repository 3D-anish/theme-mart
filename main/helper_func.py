from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import os
from django.utils.crypto import get_random_string

def get_paginated_objs(objs,page_number,per_page):
    paginator = Paginator(objs, per_page=per_page, orphans=0)
    try:
        page_object = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_object = paginator.get_page(1)
    except EmptyPage:
        page_object = paginator.get_page(1)
        
    return page_object


def get_home_banner_path(instance, filename):
    file = filename.split(".")
    new_filename = f"home_banner_{get_random_string(length=5)}.{file[-1]}"
    return os.path.join('banners', new_filename)