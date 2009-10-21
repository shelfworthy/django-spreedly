from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from spreedly.models import Subscription
import spreedly.settings as spreedly_settings

class SpreedlyMiddleware(object):
    '''
    Checks if user is legible to use the website, i.e. has an active
    subscription.
    '''
    def process_request(self, request):
        allowed = False
        for path in spreedly_settings.SPREEDLY_ALLOWED_PATHS + [spreedly_settings.SPREEDLY_URL, settings.LOGIN_URL]:
            if request.path.startswith(path):
                allowed = True
        
        if not allowed:
            if not request.user.is_authenticated():
                if spreedly_settings.SPREEDLY_USERS_ONLY:
                    if spreedly_settings.SPREEDLY_ANONYMOUS_SHOULD_LOGIN:
                        return HttpResponseRedirect(settings.LOGIN_URL)
                    return HttpResponseRedirect(spreedly_settings.SPREEDLY_URL)
            elif request.user.is_authenticated() \
                and not Subscription.objects.has_active(request.user):
                    return HttpResponseRedirect(spreedly_settings.SPREEDLY_URL)
        return