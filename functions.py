from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from spreedly.models import Plan, Subscription
from spreedly.pyspreedly.api import Client
from spreedly import signals
import spreedly.settings as spreedly_settings

def sync_plans():
    '''
    Sync subscription plans with Spreedly API
    '''
    client = Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
    
    Plan.objects.all().delete()
    
    for plan in client.get_plans():
        p = Plan.objects.create(speedly_id=plan['speedly_id'])
        
        changed = False
        for k, v in plan.items():
            if hasattr(p, k) and not getattr(p, k) == v:
                setattr(p, k, v)
                changed = True
        if changed:
            p.save()

def get_subscription(user):
    import copy
    client = Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
    data = client.get_info(user.id)
    
    subscription, created = Subscription.objects.get_or_create(
        user=user
    )
    
    old_sub = copy.deepcopy(subscription)
    
    for k, v in data.items():
        if hasattr(subscription, k):
            setattr(subscription, k, v)
    subscription.save()
    
    signals.subscription_update.send(sender=subscription, user=user, old_sub=old_sub, new_sub=subscription)
    
    return subscription

def check_trial_eligibility(plan, user):
    if plan.plan_type != 'free':
        return False
    try:
        # make sure the user is trial eligable (they don't have a subscription yet, or they are trial_elegible)
        not_allowed = Subscription.objects.get(user=user, trial_elegible=False)
        return False
    except Subscription.DoesNotExist:
        return True

def start_free_trial(plan, user):
    if check_trial_eligibility(plan, user):
        client = Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
        client.get_or_create_subscriber(user.id, user.username)
        client.subscribe(user.id, plan.pk, trial=True)
        get_subscription(user)
        return True
    else:
        return False

def return_url(plan_pk, user, trial=False):
    url = 'http://%s%s' % (spreedly_settings.SPREEDLY_SITE_URL, reverse('spreedly_return', args=[user.id, plan_pk]))
    if trial:
        url = url + '?free=true'
    return url

def subscription_url(plan, user, giver_email=None, screen_name=None):
    url = 'https://spreedly.com/%(site_name)s/subscribers/%(user_id)s/subscribe/%(plan_id)s/%(screen_name)s?return_url=%(return_url)s' % {
        'site_name': settings.SPREEDLY_SITE_NAME,
        'plan_id': plan.pk,
        'user_id': user.id,
        'screen_name': screen_name or user.username,
        'user_email': user.email,
        'return_url': return_url(plan.pk, user)
    }
    
    if plan.is_gift_plan:
        email = giver_email
    else:
        email = user.email
    
    if email:
        url = url + '&email=%s' % email
    if not plan.is_gift_plan:
        if user.first_name:
            url = url + '&first_name=%s' % user.first_name
        if user.last_name:
            url = url + '&last_name=%s' % user.last_name
    
    return url
