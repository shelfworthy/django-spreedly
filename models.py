from django.db import models

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
    
    def __unicode__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey('auth.User')
    plan = models.ForeignKey(Plan)
    
    active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'Subscription for %s' % self.user
