from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.cache import cache
from django.conf import settings

from subscriptions.pyspreedly.api import Client
from subscriptions.functions import sync_plans
from subscriptions.models import Plan, Subscription
import subscriptions.settings as subscription_settings
from subscriptions.forms import subscribeForm

def plan_list(request, extra_context=None, **kwargs):
    sub = None
    if request.user.is_authenticated():
        try:
            sub = Subscription.objects.get(user=request.user)
        except Subscription.DoesNotExist:
            pass
    
    # cache the subscription list from spreedly for a day
    cache_key = 'subscriptions_plans_list'
    plans = cache.get(cache_key)
    if not plans:
        sync_plans()
        plans = list(Plan.objects.filter(enabled=True))
        cache.set(cache_key, plans, 60*60*24)
    
    # deal with the form
    form = subscribeForm(request.POST or None)
    if form.is_valid():
        redirect_url = form.save()
        return HttpResponseRedirect(redirect_url)
    
    our_context={
        'current_user_subscription': sub,
        'site': settings.SPREEDLY_SITE_NAME,
        'plans': plans,
        'request': request,
        'form': form
    }
    if extra_context:
        our_context.update(extra_context)
    context = RequestContext(request)
    for key, value in our_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(
        subscription_settings.SUBSCRIPTIONS_LIST_TEMPLATE,
        kwargs,
        context_instance=context
    )

def spreedly_return(request):
    if request.GET.has_key('user_id'):
        user_id = request.GET['user_id']
        user = User.objects.get(id=user_id)
        
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
        
        context = {
            'subscription': subscription,
            'request': request,
        }
        return render_to_response(
            subscription_settings.SUBSCRIPTIONS_RETURN_TEMPLATE,
            context_instance=context
        )
    raise Http404

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