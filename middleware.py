# -*- coding: utf-8 -*-
from django.conf import settings

SUBSCRIPTION_ALLOWED_PATH = getattr(settings, 'SUBSCRIPTION_ALLOWED_PATH', '/account/')
SUBSCRIPTION_REDIRECT_URI = getattr(settings, 'SUBSCRIPTION_REDIRECT_URI', '/account/subscription/')

class SubscriptionMiddleware(object):
    '''
    Checks if user is legible to use the website, i.e. has an active
    subscription.
    '''
    def process_request(self, request):
        from django.conf import settings
        from django.http import HttpResponseRedirect
        from apps.members.models import Member

        if request.user.is_authenticated():
            member = request.user.get_profile()

            # If user has no active subsription - redirect
            # to subscription management page
            if not SUBSCRIPTION_ALLOWED_PATH in request.path \
                and not request.user.username in request.path \
                and not settings.MEDIA_URL in request.path \
                and not member.has_active_subscription():
                    
                return HttpResponseRedirect(SUBSCRIPTION_REDIRECT_URI)

        return