from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from common.decorators import ajax_request
from happyfridge.decorators import check_shopping_run_activated
from happyfridge.forms import get_item_checking_form, get_item_processing_form, \
    get_item_add_form
from happyfridge.shared_context import get_items_list_forms, get_spotted_items_form, get_add_item_form


@login_required
@ajax_request
@check_shopping_run_activated
def items_list(request):


    ItemProcessingForm = get_item_processing_form(request.user.roommate)
    shopping_run = request.user.roommate.inn.shoppingrun

    if request.method == "POST":
        itemid = request.POST['id']
        form = ItemProcessingForm(request.POST, instance=shopping_run.item_pool.get(pk=itemid))
        if form.is_valid():
            form.save()
        else:
            raise Exception('You have submitted an invalid form')


    items_form = get_items_list_forms(request.user.roommate)

    return render(request, 'happyfridge/ajax/items_list.html', {"items_form": items_form})

@login_required
@ajax_request
@check_shopping_run_activated
def check_item(request):

    roommate = request.user.roommate
    ItemCheckingForm = get_item_checking_form(roommate)

    template = "happyfridge/ajax/check_item.html"

    if request.method == "POST":
        itemid = request.POST['id']
        form = ItemCheckingForm(request.POST, instance=roommate.item_spotted.get(pk=itemid))
        if form.is_valid():
            form.save()

    formscheck = get_spotted_items_form(roommate, ItemCheckingForm)
    shopping_run = roommate.inn.shoppingrun

    return render(request, template, {"formscheck": formscheck,
                                      "shopping_run": shopping_run})


@login_required
@ajax_request
@check_shopping_run_activated
def quick_add_item(request):

    ItemAddForm = get_item_add_form(request.user.roommate)

    if request.POST:
        form_add_item = ItemAddForm(request.POST)
        if form_add_item.is_valid():
            form_add_item.save()
            form_add_item = get_add_item_form(request.user.roommate)
    else:
        form_add_item = get_add_item_form(request.user.roommate)

    return render(request, 'happyfridge/ajax/quick_add_item.html', {'form_add_item':form_add_item})