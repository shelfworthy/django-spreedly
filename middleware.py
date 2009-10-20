from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from subscriptions.models import Subscription
import subscriptions.settings as subscription_settings

class SubscriptionMiddleware(object):
    '''
    Checks if user is legible to use the website, i.e. has an active
    subscription.
    '''
    def process_request(self, request):
        allowed = False
        for path in subscription_settings.SUBSCRIPTIONS_ALLOWED_PATHS + [subscription_settings.SUBSCRIPTIONS_URL]:
            if request.path.startswith(path):
                allowed = True
        
        if not allowed:
            if not request.user.is_authenticated() \
                and  subscription_settings.SUBSCRIPTIONS_USERS_ONLY:
                    return HttpResponseRedirect(subscription_settings.SUBSCRIPTIONS_URL)
            elif request.user.is_authenticated() \
                and not Subscription.objects.has_active(request.user):
                    return HttpResponseRedirect(subscription_settings.SUBSCRIPTIONS_URL)
        return