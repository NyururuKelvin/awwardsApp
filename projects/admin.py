from django.contrib import admin
from .models import Profile,Votes,Project

class VotesInLine(admin.TabularInline):
    model=Votes
    extra=3
    
class ProjectInLine(admin.ModelAdmin):
    fieldsets=[
        (None,{'fields':['user']}),
        (None,{'fields':['image']}),
        (None,{'fields':['title']}),
        (None,{'fields':['description']}),
        (None,{'fields':['link']}),
        (None,{'fields':['location']}),
    ]
    inlines=[VotesInLine]

admin.site.register(Project,ProjectInLine)
admin.site.register(Profile)
admin.site.register(Votes)

