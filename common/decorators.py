from functools import wraps

from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs


#Remember to use wraps before return a function.
#see http://stackoverflow.com/questions/308999/what-does-functools-wraps-do


def ajax_request(view_func):
    """
    Check if the request is ajax, if not raise PermissionDenied
    """

    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(*args, **kwargs):
        request = args[0]
        if not request.is_ajax():
            raise PermissionDenied
        else:
            return view_func(*args, **kwargs)
    return wrapped_view