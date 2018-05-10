from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Image(models.Model):
    """
    Initializing image model
    
    """
    image_link = models.ImageField(upload_to ='pics/')
    name = models.CharField(max_length=100)
    caption = models.CharField(max_length=60,blank=True,null=True)
    likes = models.IntegerField()
    image_comments = models.ForeignKey('Comment',null=True)
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

class Like(models.Model):
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    created = models.DateTimeField(auto_now_add =True)

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
