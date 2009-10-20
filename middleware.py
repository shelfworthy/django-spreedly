from django.conf import settings
from django.http import HttpResponseRedirect

from subscription.models import Subscription

class SubscriptionMiddleware(object):
    '''
    Checks if user is legible to use the website, i.e. has an active
    subscription.
    '''
    def process_request(self, request):
        if request.user.is_authenticated():
            user = request.user.get_profile()
            # If user has no active subsription - redirect
            # to subscription management page
            if not request.path in settings.SUBSCRIPTION_ALLOWED_PATHS \
                and not settings.SUBSCRIPTION_REDIRECT_URI in request.path \
                and not settings.MEDIA_URL in request.path \
                and not Subscription.objects.has_active(user):
                    return HttpResponseRedirect(SUBSCRIPTION_REDIRECT_URI)
        return