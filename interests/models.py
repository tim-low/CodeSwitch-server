from django.db import models

# Create your models here.

class Interest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)