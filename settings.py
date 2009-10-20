from django.conf import settings

SUBSCRIPTION_URL = getattr(settings, 'SUBSCRIPTION_URL', 'subscriptions')
SUBSCRIPTION_LIST_TEMPLATE = getattr(settings, 'SUBSCRIPTION_LIST_TEMPLATE', 'subscriptions.html')
SUBSCRIPTION_EXTRA_ALLOWED_PATHS = getattr(settings, 'SUBSCRIPTION_EXTRA_ALLOWED_PATHS', [])
SUBSCRIPTION_USERS_ONLY = getattr(settings, 'SUBSCRIPTION_USERS_ONLY', False)