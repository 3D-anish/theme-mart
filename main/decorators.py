from django.http import HttpResponse
from functools import wraps

def htmx_required(func):
    @wraps(func)
    def wrapper_func(request, *args, **kwargs):
        if not request.htmx:
            return HttpResponse('HTMX Required')
        return(func(request, *args, **kwargs))
    return wrapper_func
