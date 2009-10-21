from django.conf import settings

# The URL that users get sent back to after visiting spreedly
SPREEDLY_RETURN_URL = getattr(settings, 'SPREEDLY_RETURN_URL', '/thanks/')

# The base URL for all spreedly related pages
SUBSCRIPTIONS_URL = getattr(settings, 'SUBSCRIPTIONS_URL', '/subscriptions/')

# The template that should be used for subscription listing and signup
SUBSCRIPTIONS_LIST_TEMPLATE = getattr(settings, 'SUBSCRIPTIONS_LIST_TEMPLATE', 'subscriptions.html')

# The template that should be used to show a user returning to your site from spreedly their new subscription status
SUBSCRIPTIONS_RETURN_TEMPLATE = getattr(settings, 'SUBSCRIPTIONS_RETURN_TEMPLATE', 'thanks.html')

# lock out your entire site (except for spreedly URLs and the paths below) to non-subscribed users?
SUBSCRIPTIONS_USERS_ONLY = getattr(settings, 'SUBSCRIPTIONS_USERS_ONLY', False)

# Paths that a user can visit without a subscription 
SUBSCRIPTIONS_ALLOWED_PATHS = getattr(settings, 'SUBSCRIPTIONS_ALLOWED_PATHS', [])

# Should anonymous users be sent to the login screen or the subscription screen?
SEND_ANONYMOUS_TO_LOGIN = getattr(settings, 'SEND_ANONYMOUS_TO_LOGIN', True)