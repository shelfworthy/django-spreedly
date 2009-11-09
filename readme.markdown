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

Requirements
============

This code is currently only tested on django trunk, but should work without issue on 1.1

* python 2.5 
* [pyspreedly](http://github.com/chrisdrackett/python-spreedly) <- included as a submodule of this project
* LOGIN_URL variable in your settings file

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
	# this defaults to '/thanks/'
	SPREEDLY_RETURN_URL = '/welcome/'

	# the base subscription url (where users will be redirected when their subscriptions expire)
	# this defaults to '/subscriptions/' if you don't add a value to your settings.
	SPREEDLY_URL ='/register/'

	# If you want to use your own subscription list page template:
	# this defaults to 'subscriptions/templates/spreedly.html'
	SPREEDLY_LIST_TEMPLATE = 'path/to/your/template.html'

	# if you want to restrict access to your entire site based to only users with an active subscription
	# this defaults to False
	SPREEDLY_USERS_ONLY = True
	
	# URL paths that a user without a subscription can vist without being redirected to the subscription list:
	# these can be single pages ('/some/page/') of full directories ('/directory')
	SPREEDLY_ALLOWED_PATHS = ['/login', '/logout']

	# This template will be used when checking to make sure the user is using a valid email
	# this default to 'confirm_email.txt' Be sure to include {{ spreedly_url }} in your template
	SPREEDLY_CONFIRM_EMAIL = 'path/to/your/template.txt'

	# This subject will be used for confirmation emails
	# this defaults to "'complete your subscription to %s' % Site.object.get(id=settings.SITE_ID).name"
	SPREEDLY_CONFIRM_EMAIL_SUBJECT = 'This is a new subject'

	# Where a user is directed after signing up.
	# this defaults to 'email_sent.html'
	SPREEDLY_EMAIL_SENT_TEMPLATE = 'path/to/your/template.html'

	# this is the email that will be sent to the user recieving the gift subscription
	# this default to 'gift_email.txt' Be sure to include {{ spreedly_url }} in your template
	SPREEDLY_GIFT_EMAIL = 'path/to/your/template.txt'

	# the subject for the gift confirm email
	# this defaults to 'gift subscription to %s' % Site.objects.get(id=settings.SITE_ID).name
	SPREEDLY_GIFT_EMAIL_SUBJECT = 'This is a new subject'

	# the base url for your site to be used when returning users from spreedly.
	# this default to Site.objects.get(id=settings.SITE_ID) from the django Site app.
	SPREEDLY_SITE_URL = 'something.com'

4) Add the middleware to your `settings.py` MIDDLEWARE_CLASSES:

	'spreedly.middleware.SpreedlyMiddleware'

5) Add the following to urlpatterns in `urls.py`:

	import spreedly.settings as spreedly_settings
	(r'^%s' % spreedly_settings.SPREEDLY_URL[1:], include('spreedly.urls')),

6) Run syncdb

Use
===

After the app is installed, you can start creating subscriptions!

The app is designed to work with the following flow:

* new user enters user information and chooses a plan
* inactive user object is created and the user is sent an email with a link to spreedly to pay for plan
* after successful payment, user is directed back to your site
* the app will check with spreedly for users status
* if the user has an active subscription, the user object will be set to active and the user will be given a login url

If you want to make your site subscription only you can set the SPREEDLY_USERS_ONLY to True.
This will redirect any anonymous user (or user with an inactive subscription) who visits a page not in the SPREEDLY_ALLOWED_PATHS list to your SPREEDLY_URL

Some Important Notes
--------------------

Spreedly is sent a redirect url that will check and see if the user has signed up and activate their account. **A user may not click on this link** and in that case their account won't be active, unless:

Spreedly will ping a url with subscriptions change, and django-spreedly is setup to listen for this.

in your spreedly setting is the following: 'Subscribers Changed Notification URL'

if you are using the default settings for django-spreedly, the url you should put in this field is:

http://mysite.com/subscriptions/spreedly_listener/

if you changed SPREEDLY_URL, you'll need to substitute that for subscriptions.

If you want to add a fallback, you can also add the following to your login view after a user is logged in (but before you check if they are active):

	from spreedly.functions import get_subscription
	
	if not user.is_active:
		get_subscription(user)
