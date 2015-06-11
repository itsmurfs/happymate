from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^check-item/$', 'happyfridge.views_ajax.views_ajax.check_item', name = 'check_item'),
    url(r'^items-list/$', 'happyfridge.views_ajax.views_ajax.items_list', name='items_list'),
    url(r'^quick-add-item$', 'happyfridge.views_ajax.views_ajax.quick_add_item', name = 'quick_add_item'),

)