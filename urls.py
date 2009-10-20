from django.conf.urls.defaults import *

urlpatterns = patterns('subscription.views',
    url(r'^$', 'plan_list', name='subscription_plans'),
    url(r'^spreedly_listener/$', 'spreedly_listener', name='spreedly_listener'),
)