#Remember to use wraps before return a function.
#see http://stackoverflow.com/questions/308999/what-does-functools-wraps-do
from functools import wraps

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import available_attrs

from happyfridge.models import get_shopping_run


def check_shopping_run_activated(view_func):
    """
    Check if the ShoppingRun is activated.
    If yes prompts the items in pending state

    This decorator should decorates views that are already login required
    """

    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(*args, **kwargs):
        request = args[0]
        #check shopping run activation
        sr = get_shopping_run(request.user)

        if not sr or not sr.activated:
            if request.is_ajax():
                url = reverse("happyfridge:new_shopping_run")
                return HttpResponse(
                    """<script type="text/javascript">window.location.replace("{}");</script>""".format(url)
                )
            else:
                return HttpResponseRedirect(reverse('happyfridge:new_shopping_run'))
        else:
            #this is the normal behaviour
            return view_func(*args, **kwargs)
    return wrapped_view