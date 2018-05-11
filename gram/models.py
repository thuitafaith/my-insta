from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
class Image(models.Model):
    """
    Initializing image model

    """
    image_link = models.ImageField(upload_to ='pics/',verbose_name ='Select Picture')
    name = models.CharField(max_length=100)
    caption = models.CharField(max_length=60,blank=True,null=True)
    created_by =models.ForeignKey('Profile',related_name ='owner')
    likes = models.ManyToManyField('Profile',default=False,blank=True,related_name='likes')
    comments = models.ManyToManyField('Profile',default=False,related_name='comments',through ='Comment',through_fields=('image','profile'))


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
        return self.name


class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='pics/')
    avatar_thumbnail = ImageSpecField(source='profile_photo',processors=[ResizeToFill(100,50)],format='JPEG',options={'quality': 60})
    Bio = models.TextField()
    owner_profile = models.ForeignKey(User)
    follow = models.ManyToManyField('self', symmetrical=False, default=False, blank=True)

    def save_profile(self):
        self.save()
    def delete_profile(self):
        self.delete()

class Comment(models.Model):
    image = models.ForeignKey(Image)
    profile = models.ForeignKey(Profile)
    comment_post = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)
