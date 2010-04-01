from django.dispatch import Signal

# This signal is sent when we get a sub
subscription_update = Signal(providing_args=["user", "old_sub", "new_sub"])
gift_accepted = Signal()