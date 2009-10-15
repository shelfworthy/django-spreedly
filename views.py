# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic import list_detail

from subscription.models import Plan, Subscription

@login_required
def plan_list(request):
    from subscription.models import Plan, Subscription, SPREEDLY_SITE_NAME

    return list_detail.object_list(
        request,
        queryset=Plan.objects.all(),
        template_name='plan_list.html',
        extra_context={
            'subscription': Subscription.objects.get_for_user(request.user),
            'site': SPREEDLY_SITE_NAME
        }
    )

def changes(request):
    from django.conf import settings
    from django.http import Http404, HttpResponse
    from pyspreedly.api import Client
    
    if request.method == 'POST':
        SPREEDLY_AUTH_TOKEN = getattr(settings, 'SPREEDLY_AUTH_TOKEN', '')
        SPREEDLY_SITE_NAME = getattr(settings, 'SPREEDLY_SITE_NAME', '')

        # Try to extract customers' IDs
        if request.POST.has_key('subscriber_ids'):
            subscriber_ids = request.POST['subscriber_ids'].split(',')

            if len(subscriber_ids):
                client = Client(SPREEDLY_AUTH_TOKEN, SPREEDLY_SITE_NAME)
                for id in subscriber_ids:
                    # Now let's query Spreedly API for the actual changes
                    data = client.get_info(int(id))

                    subscription, created = Subscription.objects.get_or_create(
                        user__pk=id
                        )

                    for k, v in data.items():
                        if hasattr(subscription, k):
                            setattr(subscription, k, v)

                    subscription.save()

    raise Http404
        