import random

from django import forms
from django.contrib.auth.models import User

from webapp.apps.exchange.models import Exchange, UserExchange, UserExchangeExclusion

import logging
logger = logging.getLogger(__name__)

class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ('name',)

    def save(self, user, commit=True):
        exchange = super(ExchangeForm, self).save(commit=False)
        exchange.user = user
        if commit:
            exchange.save()

            user_exchange = exchange.userexchange_set.filter(user=user)

            if not user_exchange:
                UserExchange.objects.create(user=user, exchange=exchange)

        return exchange


class UserExchangeForm(forms.Form):

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=100)

    def save(self, exchange, commit=True):

        user_exchange = UserExchange()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']

        try:
            user = User.objects.get(email=email)
            if not user.first_name and not user.last_name:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
        except:
            user = User.objects.create(username=self.generate_username(), email=email, first_name=first_name, last_name=last_name)

        user_exchange.user = user
        user_exchange.exchange = exchange

        if commit:
            user_exchange.save()

        return user_exchange

    def generate_username(self):
        username = str(random.randint(0,1000000))

        try:
            User.objects.get(username=username)
            return generate_username()
        except User.DoesNotExist:
            return username;


class UserExchangeExclusionForm(forms.Form):

    add_reverse = forms.BooleanField(required=False)

    def __init__(self, user_exchanges, *args, **kwargs):
        super(UserExchangeExclusionForm, self).__init__(*args, **kwargs)
        self.fields['user_exchange1'] = forms.ChoiceField(choices=self.get_choices(user_exchanges))
        self.fields['user_exchange2'] = forms.ChoiceField(choices=self.get_choices(user_exchanges))

    def get_choices(self, user_exchanges):
        result = []
        for user_exchange in user_exchanges:
            if user_exchange.user.first_name and user_exchange.user.last_name:
                result.append((user_exchange.id, "%s %s (%s)" % (user_exchange.user.first_name, user_exchange.user.last_name, user_exchange.user.email)))
            else:
                result.append((user_exchange.id, user_exchange.user.email))
        return result

    def save(self, exchange, commit=True):

        add_reverse = self.cleaned_data['add_reverse']
        user_exchange1 = self.cleaned_data['user_exchange1']
        user_exchange2 = self.cleaned_data['user_exchange2']

        user_exchange_exclusion = UserExchangeExclusion()
        user_exchange_exclusion.user_exchange1_id = user_exchange1
        user_exchange_exclusion.user_exchange2_id = user_exchange2
        user_exchange_exclusion.exchange = exchange

        if add_reverse:
            user_exchange_exclusion2 = UserExchangeExclusion()
            user_exchange_exclusion2.user_exchange1_id = user_exchange2
            user_exchange_exclusion2.user_exchange2_id = user_exchange1
            user_exchange_exclusion2.exchange = exchange

        if commit:
            user_exchange_exclusion.save()
            if add_reverse:
                user_exchange_exclusion2.save()

        return user_exchange_exclusion
