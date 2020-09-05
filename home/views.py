from django.shortcuts import render

# Create your views here.

def index(request):
    """ View will return index page """
    
    return render(request, 'home/index.html')
