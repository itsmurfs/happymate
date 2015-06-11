from django.contrib import admin

from happyfridge.models import Category, Item, ShoppingRun


# Register your models here.
from happyfridge.models_stats import ItemDeleted, ShoppingRunDeleted

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ShoppingRun)
admin.site.register(ItemDeleted)
admin.site.register(ShoppingRunDeleted)