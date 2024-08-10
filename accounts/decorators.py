from django.contrib import messages
from django.http import HttpResponseRedirect
from functools import wraps

def deny_autheticated_user(func):
    @wraps(func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in.')
            return HttpResponseRedirect('/')
        return(func(request, *args, **kwargs))
    return wrapper_func
