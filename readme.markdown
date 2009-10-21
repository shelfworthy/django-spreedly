Info
====

This app can be used to add support for [spreedly](https://spreedly.com/) to your django app.

The app currently covers:

* syncing subscriptions with your spreedly account.
* listing available subscriptions on your site.
* letting a user choose and signup for a subscription from your site.
* letting spreedly checkin and relay currently user subscription info.
* disabling part of your site for non-subscribed users (optional)
* redirecting users to the subscription page when their subscription expires.

Installation
============

1. Checkout the project into a folder called `subscriptions` on your python path:

	git clone git://github.com/chrisdrackett/django-paid-subscriptions.git subscriptions

2. Update the submodules (this gets the python tender API wrapper)

	cd subscriptions/
	git submodule update --init

2) Add `subscriptions` to your installed apps, and add the following to `settings.py`:

	SPREEDLY_AUTH_TOKEN = 'your auth token'
	SPREEDLY_SITE_NAME = 'your site name'
	SITE_URL = 'http://www.yoursitesurl.com'

3) The following can also be added, they are optional:

	# this string will be used as the url for returning users from spreedly.
	# this defaults to 'thanks'
	SPREEDLY_RETURN_URL = '/welcome/'

	# the base subscription url (where users will be redirected when their subscriptions expire)
	# this defaults to '/subscriptions' if you don't add a value to your settings.
	SUBSCRIPTIONS_URL ='/register/'

	# If you want to use your own subscription list page template:
	# this defaults to 'subscriptions/templates/subscriptions.html'
	SUBSCRIPTIONS_LIST_TEMPLATE = 'path/to/your/template.html'

	# if you want to restrict access to your entire site based to only users with an active subscription
	# this defaults to False
	SUBSCRIPTIONS_USERS_ONLY = True
	
	# URL paths that a user without a subscription can vist without being redirected to the subscription list:
	# these can be single pages ('/some/page/') of full directories ('/directory')
	SUBSCRIPTIONS_ALLOWED_PATHS = ['/login', '/logout']

3) Add the following to urlpatterns in `urls.py`:

	import subscriptions.settings as subscription_settings
	(r'^%s' % subscription_settings.SUBSCRIPTIONS_URL[1:], include('subscriptions.urls')),

4) Run syncdb

----

If you want to make your site subscription only:

use SubscriptionMiddleware and the following settings:


