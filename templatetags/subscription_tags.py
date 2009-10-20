from django.conf import settings
from django import template

register = template.Library()

@register.simple_tag
def existing_plan_url(user):
    return 'https://spreedly.com/%(site_name)s/subscriber_accounts/%(user_token)s' % {
        'site_name': settings.SPREEDLY_SITE_NAME,
        'user_token': user.subscription.token
    }
