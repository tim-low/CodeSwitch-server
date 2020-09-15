from django.db import models

class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=100)
    name = models.CharField(max_length=100, unique=True)