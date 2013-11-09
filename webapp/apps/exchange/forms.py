from django import forms
from django.contrib.auth.models import User

from webapp.apps.exchange.models import Exchange, UserExchange


class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ('name',)

    def save(self, user, commit=True):
        exchange = super(ExchangeForm, self).save(commit=False)
        exchange.user = user
        if commit:
            exchange.save()
            user_exchange = UserExchange()
            user_exchange.user = user
            user_exchange.exchange = exchange
            user_exchange.save()

        return exchange


class UserExchangeForm(forms.Form):

    email = forms.CharField(max_length=100)

    def save(self, exchange, commit=True):

        user_exchange = UserExchange()
        email = self.cleaned_data['email']

        try:
            user = User.objects.get(email=email)
        except:
            user = User.objects.create(email=email)

        user_exchange.user = user
        user_exchange.exchange = exchange

        if commit:
            user_exchange.save()

        return user_exchange
