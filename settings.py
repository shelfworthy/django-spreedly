from django.conf import settings

SPREEDLY_RETURN_URL = getattr(settings, 'SPREEDLY_RETURN_URL', '/thanks')
SUBSCRIPTIONS_URL = getattr(settings, 'SUBSCRIPTIONS_URL', '/subscriptions')
SUBSCRIPTIONS_LIST_TEMPLATE = getattr(settings, 'SUBSCRIPTIONS_LIST_TEMPLATE', 'subscriptions.html')
SUBSCRIPTIONS_RETURN_TEMPLATE = getattr(settings, 'SUBSCRIPTIONS_RETURN_TEMPLATE', 'thanks.html')
SUBSCRIPTIONS_ALLOWED_PATHS = getattr(settings, 'SUBSCRIPTIONS_ALLOWED_PATHS', [])
SUBSCRIPTIONS_USERS_ONLY = getattr(settings, 'SUBSCRIPTIONS_USERS_ONLY', False)