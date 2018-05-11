from django.test import TestCase
from .models import Image,Profile
from django.contrib.auth.models import User
# Create your tests here.
class ImageTestClass(TestCase):
    def setUp(self):
        self.user =User.objects.create_user('mememe','trytrytry@me')
        self.user.save()
        self.new_profile = Profile.objects.create(profile_photo='pics/img2.jpg',Bio='live life',owner_profile=self.user)
        self.image = Image.objects.create(image_link='pics/img1.jpg',name ='me',caption='staywoke',owner_profile=self.new_profile)

    def test_instance(self):
        self.user.save()
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
#     def test_save_method(self):
#         self.new_image.save_image()
#         images = Image.objects.all()
#         self.assertTrue(len(images)>0)
#     #test delete method
#     def test_delete_method(self):
#         self.new_image.save_image()
#         images = Image.objects.all()
#         self.new_image.delete_image()
#         self.assertTrue(len(images)==0)
#     #update caption test method
#     def test_update_method(self):
#         self.new_image.save_image()
#         self.new_image.update_caption(self.new_image.id,'live life')
#         image = Image.objects.filter(caption='live life').all()
#         self.assertTrue(len(image)==1)
#     #get image by id test method
#     def test_get_image_by_id(self):
#         find_img = self.new_image.get_image_by_id(self.new_image.id)
#         img = Image.objects.filter(id = self.new_image.id)
#         self.assertTrue(find_img,img)
#     def tearDown(self):
#         Image.objects.all().delete()
#
# class ProfileTestClass(TestCase):
#     def setUp(self):
#         self.profile=Profile(profile_photo='pics/image.jpeg',Bio ='i am me')
#         self.profile.save()
#     def test_instance(self):
#         self.assertTrue(isinstance(self.profile,Profile))
#     def test_save_method(self):
#         self.profile.save_profile()
#         profile = Profile.objects.all()
#         self.assertTrue(len(profile)>0)
#     def test_delete_method(self):
#         self.profile.save_profile()
#         profile = Profile.objects.all()
#         self.profile.delete_profile()
#         self.assertTrue(len(profile)==0)
#     def test_update_method(self):
#         new_profile = 'pics/img3.png','i can'
#         self.profile.update_profile(self.profile.id,new_profile)
#         new_profile = Profile.objects.filter(profile_photo='pics/img3.png',Bio='i can')
#         self.assertTrue(len(new_profile)==1)
