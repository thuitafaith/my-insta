from django.db import models

# Create your models here.
class Image(models.Model):
    image_link = models.ImageField(upload_to ='pics/')
    name = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)
    comments = models.TextField()
class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='pics/')
    Bio = models.TextField()
