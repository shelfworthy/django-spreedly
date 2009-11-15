from django.conf.urls.defaults import *

import spreedly.settings as spreedly_settings

urlpatterns = patterns('spreedly.views',
    url(r'^$', 'plan_list'),
    url(r'^gift/(?P<gift_id>\w+)/$', 'gift_sign_up', name='gift_sign_up'),
    url(r'^admin_gift/$', 'admin_gift', name='admin_gift'),
    url(r'^email_sent/(?P<user_id>\d+)/$', 'email_sent', name='spreedly_email_sent'),
    url(r'^spreedly_listener/$', 'spreedly_listener', name='spreedly_listener'),
    url(r'^%s(?P<user_id>\d+)/(?P<plan_pk>\w+)/$' % spreedly_settings.SPREEDLY_RETURN_URL[1:], 'spreedly_return', name='spreedly_return'),
    url(r'^my_subscription/$', 'my_subscription', name='my_subscription'),
)