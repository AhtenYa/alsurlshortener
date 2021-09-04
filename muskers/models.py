from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Culink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    longlink_text = models.URLField(max_length=255)
    shortlink_text = models.SlugField(max_length=32, unique=True)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    expiration_date = models.DateTimeField('expiration date', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('muskers:shorts')


class CulinkStat(models.Model):
    culink = models.ForeignKey(Culink, on_delete=models.CASCADE)
    creation_day = models.DateField('creation day', auto_now_add=True, unique=True)
    redirections = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f"{self.creation_day}-{self.redirections}"
