from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Exchange(models.Model):
    user = models.ForeignKey(User, related_name='exchanges')
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated = models.DateTimeField(auto_now=True, default=timezone.now())

    def __unicode__(self):
        return self.name
