from django.conf import settings
from django.db import models

class PlanManager(models.Manager):
    def sync(self):
        '''
        Sync subscription plans with Spreedly API
        '''
        from pyspreedly.api import Client

        client = Client(SPREEDLY_AUTH_TOKEN, SPREEDLY_SITE_NAME)

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
    def get_for_user(self, user):
        qs = self.model.objects.filter(user=user)
        if qs.count() > 0:
            return qs.latest()
    
    def has_active(self, user):
        '''
        Determine if given user has active subscription
        '''
        return self.model.objects.filter(user=user, active=True).count()

class Subscription(models.Model):
    user = models.ForeignKey('auth.User')
    plan = models.ForeignKey(Plan)
    
    active = models.BooleanField(default=False)
    
    objects = SubscriptionManager()
    
    def __unicode__(self):
        return u'Subscription for %s' % self.user
