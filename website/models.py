from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Leads(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", models.SET_NULL, null=True)  # every lead have just 1 agent


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    '''lead = models.ForeignKey("Agent", models.SET_NULL, null=True) every agent has only one lead ->
    it's completely wrong'''
    def __str__(self):
        return self.user.email
