# -*- coding: utf-8 -*-
from django.test import TestCase

class TestSubscription(TestCase):
    def setUp(self):
        user = User.objects.create(username='test')

    def tearDown(self):
        # Remove all subscribers
        self.sclient.cleanup()

    def test_sync_plans(self):
        # Initial sync
        Plan.objects.sync()
        qs = Plan.objects.all()
        self.assertEquals(qs.count(), 4)

        # Lets simulate a situation when some plan was changed.
        # We change it locally to cheat the system.
        p = qs[0]
        p.name = 'New Subscription'
        p.save()
        Plan.objects.sync()
        qs = Plan.objects.all()
        self.assertEquals(qs.count(), 4)
        p = qs[0]
        self.assertEquals(p.name, 'Subscription') # It should be 'Subscription' again