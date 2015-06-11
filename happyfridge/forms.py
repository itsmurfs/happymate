from django import forms

from happyfridge.models import Item


def get_item_processing_form(roommate):
    class ItemProcessingForm(forms.ModelForm):
        """

        """

        id = forms.IntegerField(widget=forms.HiddenInput)
        status = forms.BooleanField(required=False)

        class Meta:
            model = Item
            fields = ['id']

        def __init__(self, *args, **kwargs):
            super(ItemProcessingForm, self).__init__(*args, **kwargs)
            self.fields['status'].initial = self.instance.status == Item.PROCESSING_CODE
            if self.instance.status != Item.UNCHECKED_CODE:
                self.fields['status'].widget.attrs = {'disabled': 'disabled'}

        def save(self, commit=True):

            item = super(ItemProcessingForm, self).save(commit=False)

            if self.cleaned_data['status']:
                item.process(roommate)


            item.save()
            return item

    return ItemProcessingForm


def get_item_checking_form(roommate):
    class ItemCheckingForm(forms.ModelForm):
        """

        """

        id = forms.IntegerField(widget=forms.HiddenInput)

        class Meta:
            model = Item
            fields = ['id']

        def save(self, commit=True):

            item = super(ItemCheckingForm, self).save(commit=False)

            if "action" in self.data:
                if self.data["action"] == "DELETE":
                    item.uncheck(roommate)
                elif self.data["action"] == "CHECK":
                    item.check(roommate)

            else:
                raise Exception("parameter state must be passed")

            item.save()
            return item

    return ItemCheckingForm

def get_item_add_form(roommate):

    class ItemAddForm(forms.ModelForm):
        """

        """
        quantity = forms.RegexField(Item.QUANTITY_REGEX)

        class Meta:
                model = Item
                fields = ['name', 'description', 'category', 'priority']


        def save(self, commit=True):
            item = super(ItemAddForm, self).save(commit=False)

            item.req_who = roommate
            item.status = Item.UNCHECKED_CODE
            item.shopping_run = roommate.inn.shoppingrun

            item.save()

            return item

    return ItemAddForm
