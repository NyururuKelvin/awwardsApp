from django.test import TestCase
from .models import Project
from django.contrib.auth.models import User

# Create your tests here.
class TestProject(TestCase):
    def setUp(self):
        self.user=User(username='Nyururu')
        self.user.save()
        self.project=Project(user=self.user, title='test', description='this is a test project')
        self.project.save()
    
    #TEST METHOD    
    def test_save(self):
        self.project.save_project()
        project=Project.objects.all()
        self.assertTrue(len(project)==1)
     
    #TEST DELETE METHOD   
    def test_delete(self):
        Project.delete_project(self.project.pk)
        after_delete=Project.objects.all()
        self.assertTrue(len(after_delete)==0)
        
    #TEST GET ELEMENT BY D
    def test_get_by_id(self):
        project=Project.get_project(self.project.id)
        self.assertEqual(project.title,'test')
