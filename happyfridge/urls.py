from django.conf.urls import patterns, url
from happyfridge.views.rest import GetItemPool, CheckItem

urlpatterns = patterns('',
    url(r'^$', 'happyfridge.views.views.home', name='home'),
    url(r'^new-shopping-run/$', 'happyfridge.views.views.new_shopping_run', name='new_shopping_run'),

#TODO new file urls for rest
    url(r'^rest/get-item-pool/$', GetItemPool.as_view(), name='get_item_pool'),
    url(r'^rest/check-item/$', CheckItem.as_view(), name='check_item')

)