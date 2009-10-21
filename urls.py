from django.conf.urls.defaults import *

import subscriptions.settings as subscription_settings

urlpatterns = patterns('subscriptions.views',
    url(r'^$', 'plan_list'),
    url(r'^spreedly_listener/$', 'spreedly_listener', name='spreedly_listener'),
    url(r'^%s/$' % subscription_settings.SPREEDLY_RETURN_URL[1:], 'spreedly_return', name='spreedly_return'),
)