# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models

SPREEDLY_AUTH_TOKEN = getattr(settings, 'SPREEDLY_AUTH_TOKEN', '')
SPREEDLY_SITE_NAME = getattr(settings, 'SPREEDLY_SITE_NAME', '')

class PlanManager(models.Manager):
    def sync(self):
        '''
        Sync subscription plans with Spreedly API
        '''
        client = Client(
            SPREEDLY_AUTH_TOKEN, SPREEDLY_SITE_NAME
        )

        for plan in client.get_plans():
            created = False
            try:
                p = self.model.objects.get(speedly_id=plan['speedly_id'])
            except Plan.DoesNotExist:
                p = self.model()
                for k, v in plan.items():
                    if hasattr(p, k):
                        setattr(p, k, v)
                p.save()
                created = True

            # Let's compare existing records
            if not created:
                changed = False
                for k, v in plan.items():
                    if hasattr(p, k) and not getattr(p, k) == v:
                        setattr(p, k, v)
                        changed = True

                if changed:
                    p.save()


class Plan(models.Model):
    '''
    Subscription plan
    '''
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    terms = models.CharField(max_length=100, blank=True)

    plan_type = models.CharField(max_length=10, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default='0',
        help_text=u'USD')

    enabled = models.BooleanField(default=False)
    force_recurring = models.BooleanField(default=False)
    force_renew = models.BooleanField(default=False)

    duration = models.IntegerField(blank=True, default=0)
    duration_units = models.CharField(max_length=10, blank=True)

    feature_level = models.CharField(max_length=100)

    return_url = models.URLField(blank=True)

    date_created = models.DateTimeField(editable=False)
    date_changed = models.DateTimeField(editable=False)

    version = models.IntegerField(blank=True, default=1)

    speedly_id = models.IntegerField(db_index=True)
    speedly_site_id = models.IntegerField(db_index=True)

    objects = PlanManager()

    def __unicode__(self):
        return self.name

class SubscriptionManager(models.Manager):
    def create_subscription(self, data):
        client = Client(
            settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME
        )
        # We select a trial plan
        p = Plan.objects.get(plan_type='free_trial', enabled=True)

class Subscription(models.Model):
    '''
    Paid subscription
    '''
    user = models.ForeignKey('auth.User')
    plan = models.ForeignKey(Plan)

    active = models.BooleanField(default=False)
    lifetime = models.BooleanField(u'Lifetime subscription', default=False,
        help_text=u'It has no expiration date')

    date_created = models.DateTimeField(editable=False)
    date_changed = models.DateTimeField(editable=False)
    date_expiration = models.DateTimeField(blank=True, editable=False, null=True)

    token = models.CharField(max_length=100)
    trial_active = models.BooleanField(default=False)
    trial_elegible = models.BooleanField(default=False)
    recurring = models.BooleanField(default=False)

    speedly_customer_id = models.IntegerField(db_index=True)

    objects = SubscriptionManager()

    def __unicode__(self):
        return u'Subscription for %s' % self.member
