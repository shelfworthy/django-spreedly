# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('subscription.views',
    (r'^$', 'plan_list'),
)