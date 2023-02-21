from django.shortcuts import render
from src import dbConnection

# Create your views

def index(request): 
    return render(request, 'index.html')

def createAccount(request): 
    return render(request, 'createAccount.html')

def home(request): 
    return render(request, 'home.html')

def calendar(request): 
    return render(request, 'calendar.html')

def login(request): 
    return render(request, 'login.html')

def settings(request): 
    return render(request, 'settings.html')

def groups(request): 
    return render(request, 'groups.html')

def notifications(request):
    return render(request, 'notifications.html')

def messages(request): 
    pass