from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Render the home page.
    """
    return render(request, 'homepage/home.html')

def contact(request):
    """
    Render the contact page.
    """
    return render(request, 'homepage/contact.html')

def projects(request):
    """
    Render the projects page.
    """
    return render(request, 'homepage/projects.html')