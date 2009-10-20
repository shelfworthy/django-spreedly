from django.conf.urls.defaults import *

urlpatterns = patterns('subscriptions.views',
    url(r'^$', 'plan_list'),
    url(r'^spreedly_listener/$', 'spreedly_listener', name='spreedly_listener'),
)