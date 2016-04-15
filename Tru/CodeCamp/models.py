from __future__ import unicode_literals

from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(unique=True, default="DEFAULT", max_length=100)
    tuitionIS = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    tuitionOS = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    enrollGrad = models.IntegerField(null=True)
    enrollUnder = models.IntegerField(null=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    endowment = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    researchExp = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    datasource = models.CharField(default="Wikipedia", max_length=100, null=True)
    ranking = models.IntegerField()
