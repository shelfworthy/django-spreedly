from django.conf import settings
from django.contrib.sites.models import Site

# The URL that users get sent back to after visiting spreedly
SPREEDLY_RETURN_URL = getattr(settings, 'SPREEDLY_RETURN_URL', '/thanks/')

# The base URL for all spreedly related pages
SPREEDLY_URL = getattr(settings, 'SPREEDLY_URL', '/subscriptions/')

# The template that should be used for subscription listing and signup
SPREEDLY_LIST_TEMPLATE = getattr(settings, 'SPREEDLY_LIST_TEMPLATE', 'subscriptions.html')

# The template that should be used to show a user returning to your site from spreedly their new subscription status
SPREEDLY_RETURN_TEMPLATE = getattr(settings, 'SPREEDLY_RETURN_TEMPLATE', 'thanks.html')

# lock out your entire site (except for spreedly URLs and the paths below) to non-subscribed users?
SPREEDLY_USERS_ONLY = getattr(settings, 'SPREEDLY_USERS_ONLY', False)

# Paths that a user can visit without a subscription 
SPREEDLY_ALLOWED_PATHS = getattr(settings, 'SPREEDLY_ALLOWED_PATHS', [])

# Should anonymous users be sent to the login screen or the subscription screen?
SPREEDLY_ANONYMOUS_SHOULD_LOGIN = getattr(settings, 'SPREEDLY_ANONYMOUS_SHOULD_LOGIN', True)

# the template to use for the confirmation email
SPREEDLY_CONFIRM_EMAIL = getattr(settings, 'SPREEDLY_CONFIRM_EMAIL', 'confirm_email.txt')

# the subject for the confirmation email
SPREEDLY_CONFIRM_EMAIL_SUBJECT = getattr(settings, 'SPREEDLY_CONFIRM_EMAIL_SUBJECT', 'complete your subscription to %s' % Site.objects.get(id=settings.SITE_ID).name)

# the template to use for the confirmation email
SPREEDLY_GIFT_EMAIL = getattr(settings, 'SPREEDLY_GIFT_EMAIL', 'gift_email.txt')

# the subject for the confirmation email
SPREEDLY_GIFT_EMAIL_SUBJECT = getattr(settings, 'SPREEDLY_GIFT_EMAIL_SUBJECT', 'gift subscription to %s' % Site.objects.get(id=settings.SITE_ID).name)

# This template will be used after a user has signed up on your site and a confirm email has been sent to them
SPREEDLY_EMAIL_SENT_TEMPLATE = getattr(settings, 'SPREEDLY_EMAIL_SENT_TEMPLATE', 'email_sent.html')

# the url that will be used to return users from spreedly to your site.
SPREEDLY_SITE_URL = getattr(settings, 'SPREEDLY_SITE_URL', Site.objects.get(id=settings.SITE_ID))

SPREEDLY_GIFT_REGISTER_TEMPLATE = getattr(settings, 'SPREEDLY_GIFT_REGISTER_TEMPLATE', 'log_in.html')
SPREEDLY_ADMIN_GIFT_TEMPLATE = getattr(settings, 'SPREEDLY_ADMIN_GIFT_TEMPLATE', 'admin_gift.html')