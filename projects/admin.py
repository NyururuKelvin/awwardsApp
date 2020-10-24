from django.contrib import admin
from .models import Profile,Votes,Project

admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Votes)
