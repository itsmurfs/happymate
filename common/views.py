from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


def _check_ajax_request(request):
    if not request.is_ajax():
        raise PermissionDenied
    else:
        return True


#TODO find a place for this
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)