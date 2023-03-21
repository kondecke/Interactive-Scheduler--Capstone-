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
    
@api_view(['GET', 'POST'])
def apiView(request): 
    if request.method == "GET": 
        params = (request.GET["id"])
        return Response("{'test':'test'}", status=status.HTTP_200_OK)

@api_view(['Get', 'POST'])
def login(request): 
    if request.method == "GET":
        #retrieve login info for a given student need to join logins model with students table to return login 
        pass
    if request.method == "POST":
        #create login for a student linking it to the email provided in the student info table  
        data = request.POST
        serializer = serializers.loginSerializer(data=data)
        if serializer.is_valid(): 
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def events(request):
    #retrieve events list with various query params 
    if request.method == "GET": 
        data = request.GET
        if len(data) == 0: 
            #default case with no params
            events = models.Event.objects.all()
            serializer = serializers.eventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST": 
        # create a new event 
        json = request.body
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = serializers.eventSerializer(data=data)
        if serializer.is_valid(): 
            newEvent = models.Event(time=serializer.data['time'], description=serializer.data['description'], alert=serializer.data['alert'], accesslevel=serializer.data['accesslevel'])
            newEvent.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)   
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST'])
def notifications(request): 
    # Get notifications for a given student 
    if request.method == "GET": 
        data = request.GET
        serializer = serializers.notificationsSerializer(data=data)

    elif request.method == "POST": 
        # create a new notification 
        data = request.POST
        serializer = serializers.notificationSerializer(data=data)
        if serializer.is_valid(): 
            newNotification = models.Notifications(notificationID=serializer.data['notificationID'], userID=serializer.data['userID'], notificationMsg=serializer.data['notificationMsg'])
            newNotification.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def students(request): 
    pass


@api_view(['GET', 'POST'])
def groups(request):
    if request.method == "GET": 
        data = request.GET
        if len(data) == 0: 
            groups = models.Groups.objects.all()
            serializer = serializers.groupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

