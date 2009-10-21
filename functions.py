from django.conf import settings
from django.contrib.sites.models import Site

from spreedly.models import Plan, Subscription
from spreedly.pyspreedly.api import Client
import spreedly.settings as spreedly_settings

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

def get_subscription(user):
    client = Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
    data = client.get_info(user.id)
    
    subscription, created = Subscription.objects.get_or_create(
        user=user
    )
    for k, v in data.items():
        if hasattr(subscription, k):
            setattr(subscription, k, v)
    subscription.save()
    if subscription.active:
        user.is_active=True
        user.save()
    return subscription

def free_trial(plan, user):
    if plan.plan_type == 'free_trial':
        try:
            # make sure the user is trial eligable (they don't have a subscription yet, or they are trial_elegible)
            not_allowed = Subscription.objects.get(user=user, trial_elegible=False)
            return False
        except Subscription.DoesNotExist:
            pass
        
        client = Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
        client.subscribe(user.id, plan.pk, trial=True)
        get_subscription(user)
        return True
    else:
        return False

def return_url(user):
    return 'http://%s%s?user_id=%s' % (Site.objects.get(id=settings.SITE_ID), spreedly_settings.SPREEDLY_RETURN_URL, user.id)

def subscription_url(plan, user):
    return 'https://spreedly.com/%(site_name)s/subscribers/%(user_id)s/subscribe/%(plan_id)s/%(user_username)s?email=%(user_email)s&return_url=%(return_url)s' % {
        'site_name': settings.SPREEDLY_SITE_NAME,
        'plan_id': plan.pk,
        'user_id': user.id,
        'user_username': user.username,
        'user_email': user.email,
        'return_url': return_url(user)
    }