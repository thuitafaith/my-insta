from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
class Image(models.Model):
    """
    Initializing image model

    """
    image_link = models.ImageField(upload_to ='pics/')
    name = models.CharField(max_length=100)
    caption = models.CharField(max_length=60,blank=True,null=True)
    likes = models. ManyToManyField(Like)
    image_comments = models.ManyToManyField(Comment)
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

    def __str__(self):


class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='pics/')
    avatar_thumbnail =ImageSpecField(source='profile_photo',
                                     processors=[ResizeToFill(100, 50)],
                                     format='JPEG',
                                     options={'quality': 60})
    Bio = models.TextField()
    user = models.ForeignKey(User)
    def save_profile(self):
        self.save()
    def delete_profile(self):
        self.delete()
