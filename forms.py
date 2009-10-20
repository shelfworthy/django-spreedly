from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from subscriptions.models import Plan

class subscribeForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True
    )
    email = forms.EmailField(
        required=True
    )
    password1 = forms.CharField(
                                label="Password",
                                required=True,
                                widget=forms.PasswordInput(),
                            )
    password2 = forms.CharField(
                                label="Password again",
                                required=True,
                                widget=forms.PasswordInput(),
                            )
    subscription = forms.ModelChoiceField(queryset=Plan.objects.filter(enabled=True), empty_label=None)
    
    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        
        if username and email and pass1 and pass2:
            if pass1 != pass2:
                raise forms.ValidationError(_("You must type the same password each time."))
            
            user, created = User.objects.get_or_create(username=username, defaults={
                'email': email,
                'is_active': False
            })
            
            if not created:
                if user.is_active:
                    raise forms.ValidationError(_("Sorry, This username is already taken."))
                elif user.email != email:
                    raise forms.ValidationError(_("Sorry, This username is already linked to a different email address. If you started signing up with this username in the past, please use the same e-mail you used last time."))
        return self.cleaned_data
    
    def save(self):
        user = User.objects.get(username=self.cleaned_data["username"])
        user.set_password(self.cleaned_data["password2"])
        
        url = 'https://spreedly.com/%(site_name)s/subscribers/%(user_id)s/subscribe/%(plan_id)s/%(user_username)s?email=%(user_email)s' % {
            'site_name': settings.SPREEDLY_SITE_NAME,
            'plan_id': self.cleaned_data["subscription"].pk,
            'user_id': user.id,
            'user_username': user.username,
            'user_email': user.email
        }
        print url
        return url