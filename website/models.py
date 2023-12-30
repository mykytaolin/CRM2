from django.db import models


class Leads(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age_name = models.CharField(default=0)
