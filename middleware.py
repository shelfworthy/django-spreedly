# -*- coding: utf-8 -*-
from django.conf import settings

SUBSCRIPTION_ALLOWED_PATH = getattr(settings, 'SUBSCRIPTION_ALLOWED_PATH', '/settings/')
SUBSCRIPTION_REDIRECT_URI = getattr(settings, 'SUBSCRIPTION_REDIRECT_URI', '/subscription/')

class SubscriptionMiddleware(object):
    '''
    Checks if user is legible to use the website, i.e. has an active
    subscription.
    '''
    def process_request(self, request):
        from django.conf import settings
        from django.http import HttpResponseRedirect

        from subscription.models import Subscription

        if request.user.is_authenticated():
            user = request.user.get_profile()

            # If user has no active subsription - redirect
            # to subscription management page
            if not SUBSCRIPTION_ALLOWED_PATH in request.path \
                and not SUBSCRIPTION_REDIRECT_URI in request.path \
                and not request.user.username in request.path \
                and not settings.MEDIA_URL in request.path \
                and not Subscription.objects.has_active(user):

                    return HttpResponseRedirect(SUBSCRIPTION_REDIRECT_URI)

        return