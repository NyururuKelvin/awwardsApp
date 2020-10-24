from django.contrib.auth.models import User
from django import forms
from .models import Profile,Project,Votes

class UpdateUser(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username', 'email']
        
class UpdateProfile(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['contact','location','bio','image']
        
        
        
class PostProject(forms.ModelForm):
    class Meta:
        model=Project
        fields=['image','title','description','link','location']
        
class Votes(forms.ModelForm):
    class Meta:
        model=Votes
        fields=['usability','design','content']