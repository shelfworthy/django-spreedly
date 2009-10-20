from django.conf import settings

from subscriptions.models import Plan
from subscriptions.pyspreedly.api import Client

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