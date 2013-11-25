from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Exchange(models.Model):

    CREATED = 'CREATED'
    STARTED = 'STARTED'
    STATE = (
        (CREATED, 'CREATED'),
        (STARTED, 'STARTED'),
    )

    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=20, choices=STATE, default=CREATED)
    created = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated = models.DateTimeField(auto_now=True, default=timezone.now())

    def __unicode__(self):
        return self.name


class UserExchange(models.Model):
    user = models.ForeignKey(User)
    target = models.ForeignKey(User, blank=True, null=True, default=None, related_name="userexchange_set2")
    exchange = models.ForeignKey(Exchange)
    created = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated = models.DateTimeField(auto_now=True, default=timezone.now())

    def __unicode__(self):
        return '%s -> %s' % (self.user.email, self.exchange.name)


class UserExchangeExclusion(models.Model):
    exchange = models.ForeignKey(Exchange)
    user_exchange1 = models.ForeignKey(UserExchange, related_name="userexchangeexclusion_set1")
    user_exchange2 = models.ForeignKey(UserExchange, related_name="userexchangeexclusion_set2")

    created = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated = models.DateTimeField(auto_now=True, default=timezone.now())

    def __unicode__(self):
        return '%s <-> %s' % (self.user_exchange1.user.email, self.user_exchange2.user.email)
