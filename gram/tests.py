from django.test import TestCase
from .models import Image,Profile
# Create your tests here.
class ImageTestClass(TestCase):
    def setUp(self):
        self.new_image=Image(image_link='pics/img.jpg',name = 'dress',caption='staywoke',comments='lovely')
        self.new_image.save()
    def test_instance(self):
        self.assertTrue(isinstance(self.new_image,Image))
    #save method test
    def test_save_method(self):
        self.new_image.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images)>0)
    #test delete method
    def test_delete_method(self):
        self.new_image.save_image()
        images = Image.objects.all()
        self.new_image.delete_image()
        self.assertTrue(len(images)==0)
    #update caption test method
    def test_update_method(self):
        self.new_image.save_image()
        self.new_image.update_caption(self.new_image.id,'live life')
        image = Image.objects.filter(caption='live life').all()
        self.assertTrue(len(image)==1)
    #get image by id test method
    def test_get_image_by_id(self):
        find_img = self.new_image.get_image_by_id(self.new_image.id)
        img = Image.objects.filter(id = self.new_image.id)
        self.assertTrue(find_img,img)
    def tearDown(self):
        Image.objects.all().delete()

class ProfileTestClass(TestCase):
    def setUp(self):
        self.profile=Profile(profile_photo='pics/image.jpeg',Bio ='i am me')
        self.profile.save()
    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))
    def test_save_method(self):
        self.profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)
