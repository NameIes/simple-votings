from django.db import models

# Create your models here.


class modelTest(models.Model):
    question = models.CharField(max_length=50)
    click_count = models.IntegerField()

