from django.http import Http404, HttpResponse
from django.views.generic import list_detail
from django.conf import settings

from subscriptions.pyspreedly.api import Client
from subscriptions.models import Plan, Subscription
import subscriptions.settings as subscription_settings

def plan_list(request):
    sub = None
    if request.user.is_authenticated():
        try:
            sub = Subscription.objects.get(user=request.user)
        except Subscription.DoesNotExist:
            pass
    
    return list_detail.object_list(
        request,
        queryset=Plan.objects.all(),
        template_name=subscription_settings.SUBSCRIPTIONS_LIST_TEMPLATE,
        extra_context={
            'current_user_subscription': sub,
            'site': settings.SPREEDLY_SITE_NAME
        }
    )

def spreedly_listener(request):
    if request.method == 'POST':
        # Try to extract customers' IDs
        if request.POST.has_key('subscriber_ids'):
            subscriber_ids = request.POST['subscriber_ids'].split(',')
            
            if len(subscriber_ids):
                client = Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
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