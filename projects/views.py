from django.shortcuts import render,get_object_or_404,redirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile,Project,Votes
from .forms import PostProject,UpdateUser,UpdateProfile,SignUpForm,Voting
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProjectSerailizer,UserSerializer
from rest_framework import status
from .permission import IsAdminOrReadOnly
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import numpy as np

# Views
# Index view
@login_required
def index(request):
    # Default view
    projects = Project.objects.order_by('-posted')
    profiles = Profile.objects.all()
    return render(request,'project/index.html', {'projects':projects, 'profiles':profiles})

# User profile view
@login_required
def profile(request):
    return render(request,'project/profile.html')

#specific project
@login_required
def project(request, id):
    form = Voting
    project= Project.objects.get(id=id)
    votes= Voting()
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
                return render(request, 'project/project.html',{'project':project,'votes':votes,'votes_list':votes_list,'mean':mean,'form':form})

    return render(request, 'project/project.html',{'project':project,'votes':votes,'votes_list':votes_list, 'form':form})

@login_required
def vote(request, id):
    project= Project.objects.get(id=id)
    votes=Voting()
    votes=Voting(request.POST)
    if votes.is_valid():
        vote=votes.save(commit=False)
        vote.user=request.user
        vote.project=project
        vote.save() 
        messages.success(request,'Votes Successfully submitted')
        return HttpResponseRedirect(reverse('project',  args=(id)))
    
    else:
        messages.warning(request,'ERROR! Voting Range is from 0-10')
        votes=Voting()     
    return render(request, 'project/project.html', locals())

@login_required
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

@login_required
def posted_by(request, user_id):
    user=get_object_or_404(User,pk=user_id)
    return render(request,'project/posted_by.html', {'user':user})

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

def search_project(request):
    """
    Function that searches for projects
    """
    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Project.objects.filter(title__icontains=search_term)
        message = f"{search_term}"
        projects = Project.objects.all()
        
        return render(request, 'project/search.html', {"message": message, "projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})

def update_profile(request):
    profile = Profile(user=request.user)

    update_user=UpdateUser(request.POST,instance=request.user)
    update_profile=UpdateProfile(request.POST,request.FILES,instance=profile)
    if update_user.is_valid() and update_profile.is_valid():
        update_user.save()
        update_profile.save()
        
        messages.success(request, 'Profile Updated Successfully')
        return redirect('profile')
    
    else:
        update_user=UpdateUser(instance=request.user)
        update_profile=UpdateProfile(instance=profile)
    return render(request, 'project/update_profile.html',{'update_user':update_user,'update_profile':update_profile})

# Api views
def api(request):
    return render(request,'project/api.html')

class ProjectList(APIView):
    def get(self,response,format=None):
        projects=Project.objects.all()
        serializer=ProjectSerailizer(projects,many=True)
        return Response(serializer.data)
    
    @login_required
    def post(self,request,format=None):
        permission_classes=(IsAdminOrReadOnly,)
        serializer=ProjectSerailizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        permission_classes=(IsAdminOrReadOnly,)

class UserList(APIView):
    def get(self,response,format=None):
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)
 
 # Gets project by id 
class ProjectDescription(APIView):
    permission_classes=(IsAdminOrReadOnly,)  
    def get_project(self,pk):
        return get_object_or_404(Project,pk=pk)
    # gets project by id
    def get(self, request, pk ,format=None):
        project= self.get_project(pk)
        serializer=ProjectSerailizer(project)
        return Response(serializer.data)
    # updates a specific project
    def put(self, request,pk, format=None):
        project=self.get_project(pk)
        serializer=ProjectSerailizer(project,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Deletes a pjoect 
    def delete(self,request,pk,format=None):
        project=self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
# Gets User by id     
class UserDescription(APIView):
    permission_classes=(IsAdminOrReadOnly,)  
    def get_user(self,pk):
        return get_object_or_404(User,pk=pk)
    # Gets user by id
    def get(self, request, pk ,format=None):
        user= self.get_user(pk)
        serializer=UserSerializer(user)
        return Response(serializer.data)
    # Updates a specific user
    def put(self, request,pk, format=None):
        user=self.get_user(pk)
        serializer=UserSerializer(user,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Deletes a user   
    def delete(self,request,pk,format=None):
        user=self.get_user(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)