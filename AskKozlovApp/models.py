from django.db import models
from django.db.models import ObjectDoesNotExist
from django.db.models import Sum, Count
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    userPfp = models.CharField(max_length=255,
                                  default=None)

    def __str__(self):
        if self.user.username == '':
            return "ERROR-LOGIN IS NULL"
        return self.user.username

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    @property
    def userlink(self):
        return "/user/" + self.user.username
