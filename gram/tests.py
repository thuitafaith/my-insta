from django.test import TestCase
from .models import Image,Profile
from django.contrib.auth.models import User
# Create your tests here.
class ImageTestClass(TestCase):
    def setUp(self):
        self.user =User.objects.create_user('mememe','trytrytry@me')
        self.user.save()
        self.new_profile = Profile.objects.create(profile_photo='pics/img2.jpg',Bio='live life',owner_profile=self.user)
        self.new_profile.save()
        self.image = Image.objects.create(image_link='pics/img1.jpg',name ='me',caption='staywoke',owner_profile=self.new_profile)
        self.image.save()

    def test_instance(self):

        self.assertTrue(isinstance(self.image,Image))
    """
    Tests that we can save an Image
    """
    def test_save_method(self):
        self.image.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images)>0)
    """
    Tests to delete an image
    """
    def test_delete_method(self):
        self.image.save_image()
        images = Image.objects.all()
        self.image.delete_image()
        self.assertTrue(len(images)==0)

    def test_update_method(self):
        self.image.save_image()
        self.image.update_caption(self.image.id,'live life')
        image = Image.objects.filter(caption='live life').all()
        self.assertTrue(len(image)==1)
     #get image by id test method
    def test_get_image_by_id(self):
        find_img = self.image.get_image_by_id(self.image.id)
        img = Image.objects.filter(id = self.image.id)
        self.assertTrue(find_img,img)
    def tearDown(self):
        Image.objects.all().delete()

class ProfileTestClass(TestCase):
    def setUp(self):
        self.user =User.objects.create_user('mememe','trytrytry@me')
        self.user.save()
        self.new_profile=Profile(profile_photo='pics/image.jpeg',Bio ='i am me',owner_profile=self.user)
        # self.new_profile.save()
    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))
    def test_save_method(self):
        self.new_profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)
    def test_delete_method(self):
        self.new_profile.save_profile()
        profile = Profile.objects.all()
        self.new_profile.delete_profile()
        self.assertTrue(len(profile)==0)
    #def test_update_method(self):
        #self.new_profile.save_profile()
        #self.new_profile.update_profile(self.new_profile.id,'pics/img3.png','i can')
        #change_profile = Profile.objects.filter(profile_photo='pics/img3.png',Bio='i can').all()
        #self.assertTrue(len(change_profile)==1)
#class CommentTestClass(TestCase):
