from django.conf.urls.defaults import *

import spreedly.settings as spreedly_settings

urlpatterns = patterns('spreedly.views',
    url(r'^$', 'plan_list'),
    url(r'^spreedly_listener/$', 'spreedly_listener', name='spreedly_listener'),
    url(r'^%s$' % spreedly_settings.SPREEDLY_RETURN_URL[1:], 'spreedly_return', name='spreedly_return'),
)