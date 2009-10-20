To install:
-----------

SPREEDLY_AUTH_TOKEN = 
SPREEDLY_SITE_NAME = 

Add the following to your URLs

    # Subscription
    (r'^subscription/', include('subscription.urls')),


----

If you want to make your site subscription only:

use SubscriptionMiddleware and the following settings:

SUBSCRIPTION_ALLOWED_PATHS = ['/settings/', '']
SUBSCRIPTION_REDIRECT_URI ='/subscription/'