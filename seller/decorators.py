from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from functools import wraps

def seller_required(func):
    @wraps(func)
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_seller:
            messages.warning(request, 'Make your seller account first')
            if settings.BECOME_SELLER_URL:
                return HttpResponseRedirect(settings.BECOME_SELLER_URL)
            else:
                return HttpResponseRedirect('/')
        return(func(request, *args, **kwargs))
            
    return wrapper_func