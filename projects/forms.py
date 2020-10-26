from django.contrib.auth.models import User
from django import forms
from .models import Profile,Project,Votes
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('email' ,'username','password1', 'password2', )

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