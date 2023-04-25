from rest_framework import serializers
from . import models
# necessary serializer classes from django REST framework to serialize and deserialize data in json format for api
class eventSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = models.Event 
        fields = ['eventid', 'startTime', 'endTime', 'description', 'alert', 'accesslevel']

class loginSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = models.Logins
        fields = ['userName', 'pwd']

class notificationsSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = models.Notifications
        fields = ['notificationID', 'userID', 'notificationMsg']

class groupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Groups
        fields = ['groupid', 'name', 'description']

class followersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Followers
        fields = ['userid', 'followingid']

class messagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Messages
        fields = ['msgid', 'msgcontent', 'touser', 'fromuser', 'togroup']

class notificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notifications
        fields = ['notificationid', 'userid', 'notificationmsg']

class postsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Posts
        fields = ['postid', 'threadid', 'fromuser','threadtitle', 'threaddescription', 'postcontent']

class professorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Professor
        fields = ['profid', 'email', 'firstname', 'lastname']

class rolesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Roles
        fields = ['roleid', 'title', 'level', 'cancreateevent', 'candeleteevent', 'canviewevents']

class studentEventsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Studentevents
        fields = ['studentid', 'eventid', 'groupid']

class studentsinGroupSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Studentsingroup
        fields = ['studentid', 'groupid', 'role']

class userSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.User
        fields = ['studentid', 'email', 'address', 'phonenumber', 'firstname', 'lastname', 'standing']



