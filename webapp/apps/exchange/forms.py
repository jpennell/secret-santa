from django.forms import ModelForm
from webapp.apps.exchange.models import Exchange


class ExchangeForm(ModelForm):
    class Meta:
        model = Exchange
        fields = ('name',)

    def save(self, user, commit=True):
        exchange = super(ExchangeForm, self).save(commit=False)
        exchange.user = user
        if commit:
            exchange.save()
        return exchange

