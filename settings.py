# -*- coding: utf-8 -*-
from django.conf import settings

SPREEDLY_AUTH_TOKEN = getattr(settings, 'SPREEDLY_AUTH_TOKEN', '')
SPREEDLY_SITE_NAME = getattr(settings, 'SPREEDLY_SITE_NAME', '')