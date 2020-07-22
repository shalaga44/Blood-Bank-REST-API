from django.db import models
from BloodBankWebApp.StringUtils import bloodGroups


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    bloodGroupsChoices = ((i, i) for i in bloodGroups)
    bloodGroup = models.CharField(max_length=4, choices=bloodGroupsChoices)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
