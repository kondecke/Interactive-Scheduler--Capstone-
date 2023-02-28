from django.shortcuts import render
from src import dbConnection
from . import forms

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
    if request.method == "GET": 
        context = {'form': forms.LoginForm}
        return render(request, 'login.html', context)
    if request.method == "POST": 
        # validate login and redirect to new page 
        context = {'form':forms.LoginForm}
        return render(request, 'login.html', context)

def settings(request): 
    return render(request, 'settings.html')

def groups(request): 
    return render(request, 'groups.html')

def notifications(request):
    return render(request, 'notifications.html')

def messages(request): 
    return render(request, 'messages.html')

def faq(request): 
    return render(request, 'faq.html')

def createGroup(request):
    if request.method == "GET":
        context = {'form': forms.createGroup}
        return render(request, 'createGroup.html', context)
    if request.method == "POST":
        context = {'form':forms.createGroup}
        return render(request, 'createGroup.html', context)