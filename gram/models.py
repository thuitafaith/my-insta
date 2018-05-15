from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Image(models.Model):
    """
    Initializing image model

    """
    image_link = models.ImageField(upload_to ='pics/',verbose_name ='Select Picture')
    name = models.CharField(max_length=100)
    caption = models.CharField(max_length=60,blank=True,null=True)
    owner_profile =models.ForeignKey('Profile',related_name ='owner')
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
    profile_photo = models.ImageField(upload_to='pics/',null=True,blank
                                      =True)
    avatar_thumbnail = ImageSpecField(source='profile_photo',processors=[ResizeToFill(100,50)],format='JPEG',options={'quality': 60})
    Bio = models.TextField(blank=True)
    owner_profile = models.OneToOneField(User)
    profile_follow = models.ManyToManyField('self',symmetrical=False, through='Follow',default=False, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def add_follow(self,profile, status):
        follow, created = Follow.objects.get_or_create(from_person=self,to_person=profile,status=status)
        return follow

    def remove_follow(self,profile,status):
        Follow.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        return
    def get_follows(self, status):
        return self.follows.filter(
        to_people__status=status,
        to_people__from_person=self)

    def get_related_to(self, status):
        return self.related_to.filter(
        from_people__status=status,
        from_people__to_person=self)

    def get_following(self):
        return self.get_follows(FOLLOW_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(FOLLOW_FOLLOWING)
    def save_profile(self):
        self.save()
    def delete_profile(self):
        self.delete()
FOLLOW_FOLLOWING = 1
FOLLOW_BLOCKED = 2
FOLLOW_STATUSES = (
    (FOLLOW_FOLLOWING, 'Following'),
    (FOLLOW_BLOCKED, 'Blocked')
)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner_profile=instance)
    instance.profile.save()

class Comment(models.Model):
    image = models.ForeignKey(Image)
    profile = models.ForeignKey(Profile)
    comment_post = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)
class Follow(models.Model):
    from_person = models.ForeignKey(Profile, related_name='from_people')
    to_person = models.ForeignKey(Profile, related_name='to_people')
    status = models.IntegerField(choices=FOLLOW_STATUSES)
