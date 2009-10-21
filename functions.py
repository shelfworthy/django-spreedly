from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from spreedly.models import Plan
from spreedly.pyspreedly.api import Client

def sync_plans():
    '''
    Sync subscription plans with Spreedly API
    '''
    client = Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
    
    for plan in client.get_plans():
        p, created = Plan.objects.get_or_create(speedly_id=plan['speedly_id'])
        
        changed = False
        for k, v in plan.items():
            if hasattr(p, k) and not getattr(p, k) == v:
                setattr(p, k, v)
                changed = True
        if changed:
            p.save()

def subscription_url(plan, user):
    return 'https://spreedly.com/%(site_name)s/subscribers/%(user_id)s/subscribe/%(plan_id)s/%(user_username)s?email=%(user_email)s&return_url=%(return_url)s' % {
        'site_name': settings.SPREEDLY_SITE_NAME,
        'plan_id': plan.pk,
        'user_id': user.id,
        'user_username': user.username,
        'user_email': user.email,
        'return_url': 'http://%s%s?user_id=%s' % (Site.objects.get(id=settings.SITE_ID), reverse('spreedly_return'), user.id)
    }