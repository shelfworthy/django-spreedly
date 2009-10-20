from django.conf import settings

SUBSCRIPTIONS_URL = getattr(settings, 'SUBSCRIPTIONS_URL', '/subscriptions')
SUBSCRIPTIONS_LIST_TEMPLATE = getattr(settings, 'SUBSCRIPTIONS_LIST_TEMPLATE', 'subscriptions.html')
SUBSCRIPTIONS_ALLOWED_PATHS = getattr(settings, 'SUBSCRIPTIONS_ALLOWED_PATHS', [])
SUBSCRIPTIONS_USERS_ONLY = getattr(settings, 'SUBSCRIPTIONS_USERS_ONLY', False)