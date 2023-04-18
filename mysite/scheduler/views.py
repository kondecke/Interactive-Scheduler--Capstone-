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
from django.db.models import Q
from src import hash
import json
import os
import random
import hashlib
# Create your views
    
@api_view(['GET', 'POST'])
def apiView(request): 
    if request.method == "GET": 
        params = (request.GET["id"])
        return Response("{'test':'test'}", status=status.HTTP_200_OK)

@api_view(['PUT', 'POST'])
def login(request): 
    
    if request.method == "POST":
        q = Q()
        json = request.body
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = serializers.loginSerializer(data=data)

        if serializer.is_valid(): 
            q &= Q(userName = serializer.data["userName"])
            login = models.Logins.objects.filter(q)
            key = login[0].pwd[-44:]
            salt = login[0].pwd[-44:-64]
            passHash = login[0].pwd[:64]
            print(key)
            print(request.headers)
            compHash = hash.decrypt("5a2f4199d67f20dc7789c98eb4a36f42df648f18be80f13e8c2d2271cbdd3f62","xBiyv8PmveSgICI03mYWjhqf9EJrFXKEV1I4i0MkBwQ=")
            print(compHash)
            if serializer.data["pwd"] == compHash:
                return Response(serializer.data, headers={'authenticated':'True'}, status=status.HTTP_200_OK)
            else:
                return Response("{'error':'Sorry that doesn't match.'}", status=status.HTTP_401_UNAUTHORIZED)

        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'PUT': 
        pass
            
@api_view(['GET', 'PUT'])
def events(request):
    #retrieve events list with filter options eventid, time, timegt (>), timelt(>), accesslevel, alert, and studentid
    if request.method == "GET": 
        # assemble query parameters into Q object and query db for params
        q = Q()

        if 'eventid' in request.GET:
            q &= Q(eventid=request.GET['eventid'])
        if 'time' in request.GET: 
            q &= Q(time=request.GET['time'])
        if 'timegt' in request.GET: 
            q &= Q(time__gt=request.GET['timegt'])
        if 'timelt' in request.GET: 
            q &= Q(time__lt=request.GET['timelt'])
        if 'accesslevel' in request.GET: 
            q &= Q(accesslevel=request.GET['accesslevel'])
        if 'alert' in request.GET: 
            q &= Q(alert=request.GET['alert'])

        events = models.Event.objects.filter(q)

        if 'studentid' in request.GET: 

            studentEvents = models.Studentevents.objects.filter(studentid=request.GET['studentid'])
            events = events.filter(studentevents__in=studentEvents)

        if 'groupid' in request.GET: 

            groupEvents = models.Studentevents.objects.filter(groupid=request.GET['groupid'])
            events = events.filter(studentevents__in=groupEvents)

        serializer = serializers.eventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT": 
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


@api_view(['GET', 'PUT'])
def groups(request):
    # get groups no params for *, filterable by: groupid, name, studentid
    if request.method == "GET": 
        q = Q()

        if 'groupid' in request.GET: 
            q &= Q(groupid=request.GET['groupid'])
        if 'name' in request.GET: 
            q &= Q(name__contains=request.GET['name'])
        if 'description' in request.GET: 
            q &= Q(description__contains=request.GET['description'])

        groups = models.Groups.objects.filter(q)
        if 'studentid' in request.GET: 

            studGroups = models.Studentsingroup.objects.filter(studentid=request.GET['studentid'])
            groups = groups.filter(studentsingroup__in=studGroups)
        
        serializer = serializers.groupSerializer(groups, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT': 
        json = request.body 
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = serializers.groupSerializer(data=data)
        if serializer.is_valid(): 
            newGroup = models.Groups(name=serializer.data['name'], description=serializer.data['description'])
            newGroup.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def followers(request): 
    if request.method == "GET": 
        q = Q()
        if 'userid' in request.GET: 
            q &= Q(userid=request.GET['userid'])
        if 'followingid' in request.GET:
            q &= Q(followingid=request.GET['followingid'])

        if q == Q(): 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        followers = models.Followers.objects.filter(q)
        serializer = serializers.followersSerializer(followers, many=True)

        
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT']) 
def messages(request): 
    if request.method == 'GET': 
        q = Q()
        if 'to' in request.GET: 
            q &= Q(touser=request.GET['to'])
        if 'from' in request.GET: 
            q &= Q(fromuser=request.GET['from'])
        if 'toGroup' in request.GET: 
            q &= Q(fromuser=request.GET['toGroup'])
        
        if q == Q(): 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        messages = models.Messages.objects.filter(q)
        serializer = serializers.messagesSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT'])
def posts(request): 
    if request.method == "GET": 
        q = Q() 
        if 'postid' in request.GET: 
            q &= Q(postid=request.id['postid'])
        if 'threadid' in request.GET: 
            q &= Q(threadid = request.GET['threadid'])
        if 'fromuser' in request.GET: 
            q &= Q(fromuser=request.GET['fromuser'])
        if 'threadtitle' in request.GET: 
            q &= Q(threadtitle=request.GET['threadtitle'])
        
        if q == Q(): 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        posts = models.Posts.filter(q)
        serializer = serializers.postsSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'PUT': 
        json = request.body 
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = serializers.postsSerializer(data=data)
        if serializer.is_valid(): 
            newPost = models.Posts(postid=serializer.data['postid'], threadid=serializer.data['threadid'], fromuser=serializer.data['fromuser'], threadtitle=serializer.data['threadtitle'], threaddescription=serializer.data['threaddescription'], postcontent=serializer.data['postcontent'])
            newPost.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
