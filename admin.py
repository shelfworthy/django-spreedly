from django.contrib import admin

from spreedly.models import Gift, Subscription

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'lifetime', 'active_until', 'active')

admin.site.register(Gift)
admin.site.register(Subscription, SubscriptionAdmin)
