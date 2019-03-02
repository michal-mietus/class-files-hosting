from functools import wraps
from django.shortcuts import redirect


def prevent_logged(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('class_files:home')
        return function(request, *args, **kwargs)
    return wrapper