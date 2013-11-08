from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Exchange(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated = models.DateTimeField(auto_now=True, default=timezone.now())

    def __unicode__(self):
        return self.name


class UserExchange(models.Model):
    user = models.ForeignKey(User)
    exchange = models.ForeignKey(Exchange)
    created = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated = models.DateTimeField(auto_now=True, default=timezone.now())

    def __unicode__(self):
        return '%s -> %s' % (self.user.username, self.exchange.name)
