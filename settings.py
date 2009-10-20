from django.conf import settings

SUBSCRIPTIONS_URL = getattr(settings, 'SUBSCRIPTION_URL', '/subscriptions')
SUBSCRIPTIONS_LIST_TEMPLATE = getattr(settings, 'SUBSCRIPTION_LIST_TEMPLATE', 'subscriptions.html')
SUBSCRIPTIONS_ALLOWED_PATHS = getattr(settings, 'SUBSCRIPTION_EXTRA_ALLOWED_PATHS', [])
SUBSCRIPTIONS_USERS_ONLY = getattr(settings, 'SUBSCRIPTION_USERS_ONLY', False)