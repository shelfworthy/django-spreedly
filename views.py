from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.cache import cache
from django.conf import settings

from spreedly.pyspreedly.api import Client
from spreedly.functions import sync_plans, get_subscription, start_free_trial
from spreedly.models import Plan, Subscription
import spreedly.settings as spreedly_settings
from spreedly.forms import SubscribeForm

def plan_list(request, extra_context=None, **kwargs):
    sub = None
    if request.user.is_authenticated():
        try:
            sub = Subscription.objects.get(user=request.user)
        except Subscription.DoesNotExist:
            pass
    
    # cache the subscription list from spreedly for a day
    cache_key = 'spreedly_plans_list'
    plans = cache.get(cache_key)
    if not plans:
        sync_plans()
        plans = list(Plan.objects.enabled())
        cache.set(cache_key, plans, 60*60*24)
    
    # deal with the form
    form = SubscribeForm(request.POST or None)
    if form.is_valid():
        redirect_url = form.save()
        return HttpResponseRedirect(redirect_url)
    
    our_context={
        'current_user_subscription': sub,
        'site': settings.SPREEDLY_SITE_NAME,
        'login': settings.LOGIN_URL,
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
        spreedly_settings.SPREEDLY_LIST_TEMPLATE,
        kwargs,
        context_instance=context
    )

def gift_sign_up(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404
    
    return render_to_response(
        spreedly_settings.SPREEDLY_EMAIL_SENT_TEMPLATE, {
            'request': request,
            'user': user
        }
    )


def email_sent(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404
    
    return render_to_response(
        spreedly_settings.SPREEDLY_EMAIL_SENT_TEMPLATE, {
            'request': request,
            'user': user
        }
    )

def spreedly_return(request, user_id, plan_pk):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404
    
    if request.GET.has_key('trial'):
        plan = Plan.objects.get(pk=plan_pk)
        start_free_trial(plan, user)
    
    subscription = get_subscription(user)
    
    return render_to_response(
        spreedly_settings.SPREEDLY_RETURN_TEMPLATE, {
            'subscription': subscription,
            'request': request,
            'login_url': settings.LOGIN_URL
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