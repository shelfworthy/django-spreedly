Info
====

This app can be used to add support for the [spreedly](https://spreedly.com/) subscription service to your django app.

**Note** this app is still in development, if you find issues or bugs, please submit them here:

[django-paid-subscriptions issue tracker](http://chrisdrackett.lighthouseapp.com/projects/39822-python-django-spreedly)

The app currently covers:

* syncing subscriptions with your spreedly account.
* listing available subscriptions on your site.
* letting a user choose and signup for a subscription from your site.
* letting spreedly checkin and relay currently user subscription info.
* disabling part of your site for non-subscribed users (optional)
* redirecting users to the subscription page when their subscription expires.

Installation
============

1. Checkout the project into a folder called `spreedly` on your python path:

	git clone git://github.com/chrisdrackett/django-spreedly.git spreedly

2. Update the submodules (this gets the python tender API wrapper)

	cd spreedly/
	git submodule update --init

2) Add `spreedly` to your installed apps, and add the following to `settings.py`:

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
	# this defaults to 'subscriptions/templates/spreedly.html'
	SUBSCRIPTIONS_LIST_TEMPLATE = 'path/to/your/template.html'

	# if you want to restrict access to your entire site based to only users with an active subscription
	# this defaults to False
	SUBSCRIPTIONS_USERS_ONLY = True
	
	# URL paths that a user without a subscription can vist without being redirected to the subscription list:
	# these can be single pages ('/some/page/') of full directories ('/directory')
	SUBSCRIPTIONS_ALLOWED_PATHS = ['/login', '/logout']

4) Add the middleware to your `settings.py` MIDDLEWARE_CLASSES:

	'spreedly.middleware.SpreedlyMiddleware'

5) Add the following to urlpatterns in `urls.py`:

	import spreedly.settings as spreedly_settings
	(r'^%s' % spreedly_settings.SUBSCRIPTIONS_URL[1:], include('spreedly.urls')),

6) Run syncdb

Use
===

After the app is installed, you can start creating subscriptions!

The app is designed to work with the following flow:

* new user enters user information and chooses a plan
* inactive user object is created and the user is sent to spreedly to pay for plan
* after successful payment, user is directed back to your site
* the app will check with spreedly for users status
* if the user has an active subscription, the user object will be set to active and the user will be given a login url

If you want to make your site subscription only you can set the SUBSCRIPTIONS_USERS_ONLY to True.
This will redirect any anonymous user (or user with an inactive subscription) who visits a page not in the SUBSCRIPTIONS_ALLOWED_PATHS list to your SUBSCRIPTIONS_URL
