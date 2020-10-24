from django.shortcuts import render
from django.http  import HttpResponse

# Views
def index(request):
    # Default view
    return HttpResponse('Welcome to Projects Gallery')
