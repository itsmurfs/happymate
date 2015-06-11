from happyfridge.forms import get_item_checking_form, get_item_add_form, \
    get_item_processing_form
from happyfridge.models import get_processing_items

def get_items_list_forms(roommate, ItemProcessingForm=None):
    """

    """
    shopping_run = roommate.inn.shoppingrun
    if not ItemProcessingForm:
        ItemProcessingForm = get_item_processing_form(roommate)

    items_form = []

    for item in shopping_run.item_pool.all():
        items_form += [ItemProcessingForm(instance=item)]

    return items_form


def get_spotted_items_form(roommate, ItemCheckingForm=None):

    if not ItemCheckingForm:
            ItemCheckingForm = get_item_checking_form(roommate)

    formscheck = []
    for item in get_processing_items(roommate):
        formscheck += [ItemCheckingForm(instance=item)]
    return formscheck


def get_add_item_form(roommate, ItemAddForm = None):

    if not ItemAddForm:
        ItemAddForm = get_item_add_form(roommate)

    return ItemAddForm()