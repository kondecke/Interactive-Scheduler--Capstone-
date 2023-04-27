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
from cryptography.fernet import Fernet
# Create your views
    
@api_view(['GET', 'POST'])
def apiView(request): 
    # test view deleteable later 
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
            passHash = login[0].pwd[:64]
            pwd = data.get("pwd")
            pwd = hash.hash_password(pwd, n=100000)
            if pwd == passHash:
                return Response(serializer.data, headers={'authenticated':'True'}, status=status.HTTP_200_OK)
            else:
                return Response("{'error':'Sorry that doesn't match.'}", status=status.HTTP_401_UNAUTHORIZED)

        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'PUT': 
        json = request.body
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        email = data.get('email')
        pwd = data.get('password')
        firstName = data.get('firstname')
        lastName = data.get('lastname')
        address = data.get('address')
        phoneNumber = data.get('phonenumber')
        userName = data.get('userName')
        userData = dict()
        userData['email'] = email
        userData['firstname'] = firstName
        userData['lastname'] = lastName
        userData['address'] = address
        userData['phonenumber'] = phoneNumber
        print(userData)
        loginData = dict()
        pwd = hash.hash_password(pwd, n=100000) + hash.to_string(Fernet.generate_key())
        loginData['pwd'] = pwd
        loginData['userName'] = userName
        print(loginData)
        userSerializer = serializers.userSerializer(data=userData)
        loginSerializer = serializers.loginSerializer(data=loginData)
        if userSerializer.is_valid() and loginSerializer.is_valid(): 
            newUser = models.User(email=userSerializer.data['email'], address=userSerializer.data['address'], phonenumber=userSerializer.data['phonenumber'], firstname=userSerializer.data['firstname'], lastname=userSerializer.data['lastname'])
            newLogin = models.Logins(userName=loginSerializer.data['userName'], pwd=loginSerializer.data['pwd'])
            newUser.save()
            newLogin.save()
            return Response([userSerializer.data, loginSerializer.data], status=status.HTTP_200_OK)
        else: 
            print(userSerializer.errors)
            print(loginSerializer.errors)
            return Response([userSerializer.errors, loginSerializer.errors], status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['GET', 'PUT'])
def events(request):
    #retrieve events list with filter options eventid, time, timegt (>), timelt(>), accesslevel, alert, and studentid
    if request.method == "GET": 
        # assemble query parameters into Q object and query db for params
        q = Q()

        if 'eventid' in request.GET:
            q &= Q(eventid=request.GET['eventid'])
        if 'starttime' in request.GET: 
            q &= Q(start=request.GET['starttime'])
        if 'starttimegt' in request.GET: 
            q &= Q(start__gt=request.GET['starttimegt'])
        if 'starttimelt' in request.GET: 
            q &= Q(start__lt=request.GET['starttimelt'])
        if 'endtime' in request.GET: 
            q &= Q(end=request.GET['endtime'])
        if 'endtimegt' in request.GET: 
            q &= Q(end__gt=request.GET['endtimegt'])
        if 'endtimelt' in request.GET: 
            q &= Q(end__lt=request.GET['endtimelt'])
        if 'accesslevel' in request.GET: 
            q &= Q(accesslevel=request.GET['accesslevel'])
        if 'alert' in request.GET: 
            q &= Q(alert=request.GET['alert'])

        events = models.Event.objects.filter(q)

        if 'studentid' in request.GET: 
            # inner join student Events to make queryable by student
            studentEvents = models.Studentevents.objects.filter(studentid=request.GET['studentid'])
            events = events.filter(studentevents__in=studentEvents)

        if 'groupid' in request.GET: 
            # inner join group events to make queryable by groups 
            groupEvents = models.Studentevents.objects.filter(groupid=request.GET['groupid'])
            events = events.filter(studentevents__in=groupEvents)

        serializer = serializers.eventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT": 
        # create a new event 
        json = request.body
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        q = Q()
        joinData = {}
        if 'groupid' in data: 
            q &= Q(groupid=data['groupid'])
            data.pop('groupid')
            group = models.Groups.objects.filter(q).first()
            if group is not None: 
                joinData['groupid'] = group.groupid
        if 'studentid' in data: 
            q = Q(studentid=data['studentid'])
            data.pop('studentid')
            student = models.User.objects.filter(q).first()
            if student is not None: 
                joinData['studentid'] = student.studentid
        
        eventserializer = serializers.eventSerializer(data=data)

        if eventserializer.is_valid(): 
            # sanitize data and save if all nonnull fields provided 
            newEvent = models.Event(start=eventserializer.data['start'], end=eventserializer.data['end'], title=eventserializer.data['title'], alert=eventserializer.data['alert'], accesslevel=eventserializer.data['accesslevel'])
            newEvent.save()
            last = models.Event.objects.order_by('-eventid').first()
            id = last.eventid
            joinData['eventid'] = id
            print(id)
            joinSerializer = serializers.studentEventsSerializer(data=joinData)
            print(joinData)
            if joinSerializer.is_valid(): 
                joinSerializer.save()
                return Response(joinSerializer.data, status=status.HTTP_201_CREATED)  
            return Response(joinSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
        # create a new group 
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
    # get followers for a user 
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
        # get messages filterable by parameters 
        q = Q()
        if 'touser' in request.GET: 
            q &= Q(touser=request.GET['touser'])
        if 'fromuser' in request.GET: 
            q &= Q(fromuser=request.GET['fromuser'])
        if 'toGroup' in request.GET: 
            q &= Q(togroup=request.GET['toGroup'])
        if q == Q(): 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        messages = models.Messages.objects.filter(q)
        serializer = serializers.messagesSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        # create a new message to student given username
        json = request.body
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        q = Q()

        if 'email' in data:
            q &= Q(email=data['email'])
            data.pop('email')
            student = models.User.objects.filter(q).first()
            if student is not None:
                data['touser'] = student.studentid
            else:
                return Response("Student with the provided email not found", status=status.HTTP_404_NOT_FOUND)

        elif 'firstname' in data and 'lastname' in data:
            q &= Q(firstname=data['firstname'])
            data.pop('firstname')
            q &= Q(lastname=data['lastname'])
            data.pop('lastname')
            student = models.User.objects.filter(q).first()
            if student is not None:
                data['touser'] = student.studentid
            else:
                return Response("Student with the provided first and last names not found", status=status.HTTP_404_NOT_FOUND)

        elif 'username' in data:
            q &= Q(username=data['username'])
            login = models.Logins.objects.filter(q).first()
            if login is not None:
                data['touser'] = login.studentid
            else:
                return Response("Student with the provided username not found", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.messagesSerializer(data=data)
        if serializer.is_valid():
            newMsg = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





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
