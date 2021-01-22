from django.db import models


class Predictions(models.Model):
    username = models.CharField(max_length=30)
    is_real = models.BooleanField()

