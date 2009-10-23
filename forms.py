from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from spreedly.models import Plan
from spreedly.functions import subscription_url, check_trial_eligibility, return_url
import spreedly.settings as spreedly_settings

class SubscribeForm(forms.Form):
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
        username =  self.cleaned_data.get("username")
        email =     self.cleaned_data.get("email")
        pass1 =     self.cleaned_data.get("password1")
        pass2 =     self.cleaned_data.get("password2")
        plan =      self.cleaned_data.get("subscription")
        
        if username and email and pass1 and pass2:
            if pass1 != pass2:
                raise forms.ValidationError(_("You must type the same password each time."))
            
            if plan.is_free_trial_plan:
                existing_users = User.objects.filter(email=email).count()
                if existing_users:
                    raise forms.ValidationError(_("A user with this email has already had a free trial."))
            
            user, created = User.objects.get_or_create(username=username.lower(), defaults={
                'email': email,
                'is_active': False
            })
            
            if not created and user.is_active:
                raise forms.ValidationError(_("Sorry, This username is already taken."))
            elif not created:
                user.email = email
                user.save()
        return self.cleaned_data
    
    def save(self):
        user = User.objects.get(username=self.cleaned_data["username"].lower())
        user.set_password(self.cleaned_data["password2"])
        user.save()
        plan = self.cleaned_data["subscription"]
        
        trial = check_trial_eligibility(plan, user)
        if trial:
            url = return_url(plan, user, trial=True)
        else:
            url = subscription_url(plan, user)
        
        send_mail(
            spreedly_settings.SPREEDLY_CONFIRM_EMAIL_SUBJECT,
            render_to_string(spreedly_settings.SPREEDLY_CONFIRM_EMAIL, {
                'plan': plan,
                'user': user,
                'site': Site.objects.get(id=settings.SITE_ID),
                'spreedly_url': url
            }),
            settings.DEFAULT_FROM_EMAIL,
            [user.email,]
        )
        return reverse('spreedly_email_sent', args=[user.id])