from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User
from django import forms

# Serializers
class ProjectSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','title','description','link','image','posted']
        
class UserSerializer(serializers.ModelSerializer):
    email=forms.EmailField()
    is_staff=forms.BooleanField()
    class Meta:
        model=User
        fields=['id','is_staff','username','email']