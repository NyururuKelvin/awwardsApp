from django.shortcuts import render
from django.http  import HttpResponse

# Views
def index(request):
    # Default view
    return render(request,'index.html')
