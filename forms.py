import uuid

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from spreedly.models import Plan, Gift
from spreedly.functions import subscription_url, check_trial_eligibility, return_url
import spreedly.settings as spreedly_settings

from spreedly.pyspreedly.api import Client

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
                existing_users = Subscription.objects.filter(user__email=email, trial_elegible=False).count()
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
            url = return_url(plan.pk, user, trial=True)
        else:
            url = subscription_url(plan, user)
        
        send_mail(
            spreedly_settings.SPREEDLY_CONFIRM_EMAIL_SUBJECT,
            render_to_string(spreedly_settings.SPREEDLY_CONFIRM_EMAIL, {
                'plan_name': plan.name,
                'user': user,
                'site': spreedly_settings.SPREEDLY_SITE_URL,
                'spreedly_url': url
            }),
            settings.DEFAULT_FROM_EMAIL,
            [user.email,]
        )
        return reverse('spreedly_email_sent', args=[user.id])

class GiftRegisterForm(forms.Form):
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
    gift_key = forms.CharField(max_length=32, required=True, widget=forms.HiddenInput)
    
    def clean(self):
        username =  self.cleaned_data.get("username")
        email =     self.cleaned_data.get("email")
        pass1 =     self.cleaned_data.get("password1")
        pass2 =     self.cleaned_data.get("password2")
        gift_key =  self.cleaned_data.get("gift_key")
        
        if username:
            try:
                User.objects.get(username=self.cleaned_data['username'], is_active=True)
                raise forms.ValidationError(_("Sorry, This username is already taken."))
            except User.DoesNotExist:
                pass
        if username and email and pass1 and pass2:
            if pass1 != pass2:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data
    
    def save(self):
        # remove any inactive users with this same username
        try:
            old_user = User.objects.get(username=self.cleaned_data['username'], is_active=False)
            old_user.delete()
        except User.DoesNotExist:
            pass
        gift = Gift.objects.get(uuid=self.cleaned_data["gift_key"])
        user = gift.to_user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.is_active=True
        user.save()
        #update spreedly info
        client = Client(settings.SPREEDLY_AUTH_TOKEN, settings.SPREEDLY_SITE_NAME)
        client.set_info(user.pk, email=user.email, screen_name=user.username)
        gift.delete()
        return user

class GiftForm(forms.Form):
    subscription = forms.ModelChoiceField(queryset=Plan.objects.filter(plan_type='gift'), empty_label=None)
    your_name = forms.CharField(
        label="Your Name",
        required=True
    )
    message = forms.CharField(
        label="Message",
        required=False,
        widget=forms.Textarea(attrs={'rows':3, 'cols':55})
    )
    email = forms.EmailField(
        label="Email",
        required=True
    )
    email_again = forms.EmailField(
        label="Email Again",
        required=True
    )
    
    def clean(self):
        email =     self.cleaned_data.get("email")
        email2 =    self.cleaned_data.get("email_again")
        
        if email and email2:
            if email != email2:
                raise forms.ValidationError(_("The two emails don't match. Please make sure both are correct."))
        return self.cleaned_data
    
    def save(self, request):
        gift_id = str(uuid.uuid4().hex)[:29]
        plan = self.cleaned_data["subscription"]
        
        user = User.objects.create(
            username=gift_id,
            email=self.cleaned_data["email"],
            is_active=False,
            password='GIFT'
        )
        
        Gift.objects.create(
            from_user=request.user,
            to_user=user,
            uuid = gift_id,
            plan_name=plan.name,
            message=self.cleaned_data["message"]
        )
        return (plan, user)

class PlanModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.enabled:
            return unicode(obj)
        else:
            return '*%s' % (obj)
        
class AdminGiftForm(forms.Form):
    plan_name = forms.CharField(
        label="Plan Name",
        required=True
    )
    feature_level = forms.ChoiceField(
        label="Feature Level",
        choices=[(x,x) for x in set(Plan.objects.values_list('feature_level', flat=True))]
    )
    time = forms.ChoiceField(
        label="Time",
        choices=[(i,i) for i in range(1,91)]
    )
    units = forms.ChoiceField(
        label="Time Units",
        choices=[
            ('days', 'Day(s)'),
            ('months', 'Month(s)')
        ]
    )

    your_name = forms.CharField(
        label="Your Name",
        required=True
    )
    message = forms.CharField(
        label="Message",
        required=False,
        widget=forms.Textarea(attrs={'rows':3, 'cols':55})
    )
    email = forms.EmailField(
        label="Email",
        required=True
    )

    def save(self, request):
        gift_id = str(uuid.uuid4().hex)[:29]
        
        user = User.objects.create(
            username=gift_id,
            email=self.cleaned_data["email"],
            is_active=False,
            password='GIFT'
        )
        
        Gift.objects.create(
            from_user=request.user,
            to_user=user,
            uuid = gift_id,
            message=self.cleaned_data["message"],
            plan_name=self.cleaned_data["plan_name"]
        )
        return user
