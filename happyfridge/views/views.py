from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from happyfridge.decorators import check_shopping_run_activated
from happyfridge.models import Item, get_shopping_run, ShoppingRun
from happyfridge.models_stats import create_item_deleted
from happyfridge.shared_context import get_spotted_items_form, get_add_item_form, get_items_list_forms


@login_required
def new_shopping_run(request):
    #TODO class based view

    sr = get_shopping_run(request.user)
    inn = request.user.roommate.inn

    #Double check if the user goes to this view manually
    if sr and sr.activated:
        return HttpResponseRedirect(reverse("happyfridge:home"))

    if request.POST:

        if not sr:
            #ShoppingRun not created yet
            raise PermissionDenied

        item_pending = sr.item_pool.all()

        if request.POST["choice"] == "yes":

            for item in item_pending:
                item.status = Item.UNCHECKED_CODE
                item.save()

        elif request.POST["choice"] == "no":

            for item in item_pending.all():
                create_item_deleted(item, inn)
                item.delete()

        #Let's active the new shopping run
        sr.activated = True
        sr.activation_date = datetime.now()
        sr.save()

        return HttpResponseRedirect(reverse("happyfridge:home"))
    else:

        if not sr:
            #first access to happyfridge.
            sr= ShoppingRun()
            sr.activated = False
            sr.days = 7 #TODO change models for days: null=True
            sr.run_number = 1
            sr.inn = inn
            sr.save()

            item_pending=None
        else:
            item_pending = sr.item_pool.all()

        return render(request, 'happyfridge/new_shopping_run.html', {"item_pending":item_pending})


@login_required
@check_shopping_run_activated
def home(request):


    items_form = get_items_list_forms(request.user.roommate)
    formscheck = get_spotted_items_form(request.user.roommate)
    form_add_item = get_add_item_form(request.user.roommate)
    shopping_run = request.user.roommate.inn.shoppingrun
    return render(request, 'happyfridge/home.html', {"items_form": items_form,
                                                            "formscheck": formscheck,
                                                            "form_add_item": form_add_item,
                                                            "shopping_run": shopping_run})