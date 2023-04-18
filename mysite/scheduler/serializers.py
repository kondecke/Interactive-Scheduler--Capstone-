from rest_framework import serializers
from . import models
class eventSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = models.Event 
        fields = ['eventid', 'time', 'description', 'alert', 'accesslevel']

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
    class meta:
        model = models.Followers
        fields = ['userid', 'followingid']

class messagesSerializer(serializers.ModelSerializer):
    class meta:
        model = models.Messages
        fields = ['msgid', 'msgcontent', 'touser', 'fromuser', 'togroup']

class notificationsSerializer(serializers.ModelSerializer):
    class meta:
        model = models.Notifications
        fields = ['notificationid', 'userid', 'notificationmsg']

class postsSerializer(serializers.ModelSerializer):
    class meta:
        model = models.Posts
        fields = ['postid', 'threadid', 'fromuser','threadtitle', 'threaddescription', 'postcontent']

class professorSerializer(serializers.ModelSerializer):
    class meta:
        model = models.Professor
        fields = ['profid', 'email', 'firstname', 'lastname']

class rolesSerializer(serializers.ModelSerializer):
    class meta: 
        model = models.Roles
        fields = ['roleid', 'title', 'level', 'cancreateevent', 'candeleteevent', 'canviewevents']

class studentEventsSerializer(serializers.ModelSerializer):
    class meta: 
        model = models.Studentevents
        fields = ['studentid', 'eventid', 'groupid']

class studentsinGroupSerializer(serializers.ModelSerializer):
    class meta: 
        model = models.Studentsingroup
        fields = ['studentid', 'groupid', 'role']

class userSerializer(serializers.ModelSerializer):
    class meta: 
        model = models.User
        fields = ['studentid', 'email', 'address', 'phonenumber', 'firstname', 'lastname', 'standing']

class userLoginSerializer(serializers.ModelSerializer):
    user = userSerializer()
    password = serializers.CharField(source='loginSerializer.pwd')
    class Meta:
        model = models.User
        fields = ['user', 'password']


