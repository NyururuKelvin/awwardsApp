from django.shortcuts import render,get_object_or_404,redirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile,Project,Votes
from .forms import PostProject,UpdateUser,UpdateProfile,Votes
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProjectSerailizer,UserSerializer
from rest_framework import status
from .permission import IsAdminOrReadOnly
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Views
# Index view
def index(request):
    # Default view
    projects = Project.objects.all()
    return render(request,'project/index.html', {'projects':projects})

# User profile view
def profile(request):
    return render(request,'project/profile.html')

#specific project
def project(request, project_id):
    project=get_object_or_404(Project,pk=project_id)
    votes=Votes()
    votes_list=project.votes_set.all()
    for vote in votes_list:
        vote_mean=[]
        usability=vote.usability
        vote_mean.append(usability)
        content=vote.content
        vote_mean.append(content)
        design=vote.design
        vote_mean.append(design)
        mean=np.mean(vote_mean)
        mean=round(mean,2)
        if mean:
            return render(request, 'project/project.html',{'project':project,'votes':votes,'votes_list':votes_list,'mean':mean})

def new_project(request):
    current_user=request.user
    if request.method=='POST':
        form=PostProject(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.user=current_user
            project.save()
        return redirect('home')
    
    else:
        form=PostProject()
        
    return render(request,'project/new_project.html',{'form':form})

def posted_by(request, user_id):
    user=get_object_or_404(User,pk=user_id)
    return render(request,'project/posted_by.html', {'user':user})

def update_settings(request):
    update_user=UpdateUser(request.POST,instance=request.user)
    update_profile=UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
    if update_user.is_valid() and update_profile.is_valid():
        update_user.save()
        update_profile.save()
        
        messages.success(request, 'Profile Updated Successfully')
        return redirect('profile')
    
    else:
        update_user=UpdateUser(instance=request.user)
        update_profile=UpdateProfile(instance=request.user.profile)
    return render(request, 'project/update_profile.html',{'update_user':update_user,'update_profile':update_profile})

def vote(request, project_id):
    project=get_object_or_404(Project, pk=project_id)
    votes=Votes()
    votes=Votes(request.POST)
    if votes.is_valid():
        vote=votes.save(commit=False)
        vote.user=request.user
        vote.project=project
        vote.save() 
        messages.success(request,'Votes Successfully submitted')
        return HttpResponseRedirect(reverse('project:project',  args=(project.id,)))
    
    else:
        messages.warning(request,'ERROR! Voting Range is from 0-10')
        votes=Votes()     
    return render(request, 'project/project.html',{'project':project,'votes':votes})

def signup(request):
    name = "Sign Up"
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('username')
            send_mail(
            'Welcome to Awwards Gallery App.',
            f'Hello {name},\n '
            'Welcome to Instagram App and have fun.',
            'nyururukelvin99@gmail.com@gmail.com',
            [email],
            fail_silently=False,
            )
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form, 'name':name})
