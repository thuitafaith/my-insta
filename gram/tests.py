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
