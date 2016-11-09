from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=45)
    gender = models.CharField(max_length=45,null=True)
    birthdate = models.DateField(null=True)
    source = models.CharField(max_length=45)

class Post(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=1000)
    time = models.TimeField()
    verbs = models.IntegerField(default=0)
    adjectives = models.IntegerField(default=0)

