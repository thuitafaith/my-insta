from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Image(models.Model):
    image_link = models.ImageField(upload_to ='pics/')
    name = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)
    comments = models.TextField()
    profile = models.ForeignKey('Profile',null=True)

    def save_image(self):
        self.save()
    def delete_image(self):
        self.delete()
    @classmethod
    def update_caption(cls,id,caption):
        cls.objects.filter(id = id).update(caption=caption)
    @classmethod
    def get_image_by_id(cls,id):
        imge = cls.objects.filter(id=id).all()
        return imge

class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='pics/')
    Bio = models.TextField()
    user = models.ForeignKey(User)
    def save_profile(self):
        self.save()
    def delete_profile(self):
        self.delete()
