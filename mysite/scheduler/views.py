from django.shortcuts import render
from rest_framework import status 
from rest_framework.response import Response
from . import forms
from rest_framework.decorators import api_view
from . import serializers
from . import models
import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import json
# Create your views

def index(request): 
    return render(request, 'index.html')

def createAccount(request): 
    return render(request, 'createAccount.html')

def home(request): 
    return render(request, 'home.html')

def calendar(request): 
    return render(request, 'calendar.html')


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
    
@api_view(['GET', 'POST'])
def apiView(request): 
    if request.method == "GET": 
        params = (request.GET["id"])
        return Response("{'test':'test'}", status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request): 
    if request.method == "POST": 
        data = request.POST
        serializer = serializers.loginSerializer(data=data)
        if serializer.is_valid(): 
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def events(request):

    if request.method == "GET": 
        data = request.GET
        if len(data == 0): 
            #default case with no params
            events = models.Event.objects.all()
            serializer = serializers.eventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST": 
        data = request.POST
        serializer = serializers.eventSerializer(data=data)
        if serializer.is_valid(): 
            newEvent = models.Event(time=serializer.data['time'], description=serializer.data['description'], alert=serializer.data['alert'], accesslevel=serializer.data['accesslevel'])
            newEvent.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)   
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)