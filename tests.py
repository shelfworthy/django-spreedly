from spreedly.pyspreedly.api import Client

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from models import Plan
from functions import sync_plans

class TestSubscription(TestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        self.sclient = Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
    
    def tearDown(self):
        # Remove all subscribers
        self.sclient.cleanup()
    
    def test_sync_plans(self):
        # Initial sync
        spreedly_count = len(self.sclient.get_plans())
        sync_plans()
        qs = Plan.objects.all()
        self.assertEquals(qs.count(), spreedly_count)