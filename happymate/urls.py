from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from happymate.views import views


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', login_required(views.Home.as_view()), name="home"),


    url(r'account/login/$', 'happymate.views.account.login',{"template_name" : "happymate/account_login.html"}, name='login' ),
    url(r'^account/register/$','happymate.views.account.register', name="register"),
    url(r'^account/logout/$','django.contrib.auth.views.logout', {'next_page': '/'} ,name="logout"),
    url(r'^account/activate$', 'happymate.views.account.activate', name="activate"),
    url(r'^account/config-inn$', 'happymate.views.account.config_inn', name="config_inn"),
    url(r'^account/edit-profile', 'happymate.views.account.edit_profile', name="edit_profile"),
    url(r'^account/api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token', name="api_token_auth"),

    url(r'^happyfridge/', include('happyfridge.urls', namespace="happyfridge")),
    url(r'^happyfridge/ajax/', include('happyfridge.urls_ajax', namespace='happyfridge_ajax')),

    url(r'^admin/', include(admin.site.urls)),

)