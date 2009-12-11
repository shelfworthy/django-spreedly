from django.dispatch import Signal

# This signal is sent when we get a sub
subscription_update = Signal(providing_args=["user"])
gift_accepted = Signal()